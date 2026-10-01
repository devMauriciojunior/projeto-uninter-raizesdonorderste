from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from domain.schemas import PedidoCreate, UsuarioCreate
from domain.enums import StatusPedido
from infrastructure.models import PedidoModel, UsuarioModel, ItemPedidoModel
from infrastructure.repositories import PedidoRepository, UsuarioRepository, ProdutoRepository, EstoqueRepository
from infrastructure.security import obter_hash_senha
from infrastructure.gateway_pagamento import PagamentoMockAdapter

class PedidoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PedidoRepository(db)
        self.usuario_repo = UsuarioRepository(db)
        self.produto_repo = ProdutoRepository(db)
        self.estoque_repo = EstoqueRepository(db)

    def criar_novo_pedido(self, pedido_in: PedidoCreate, usuario_email: str):

        usuario = self.usuario_repo.buscar_por_email(usuario_email)
        if not usuario:
            raise HTTPException(status_code=401,
                                detail="Usuário não encontrado no banco de dados. Faça login novamente.")

        valor_total = 0.0
        itens_model = []

        for item in pedido_in.itens:
            produto = self.produto_repo.buscar_por_id(item.produto_id)
            if not produto or not produto.ativo:
                raise HTTPException(status_code=404, detail=f"Produto ID {item.produto_id} não encontrado ou inativo.")

            estoque = self.estoque_repo.buscar_por_unidade_e_produto(pedido_in.unidade_id, item.produto_id)

            if not estoque or estoque.quantidade < item.quantidade:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Estoque insuficiente para '{produto.nome}'. Solicitado: {item.quantidade}, "
                           f"Disponível: {estoque.quantidade if estoque else 0}."
                )

            estoque.quantidade -= item.quantidade
            valor_total += (produto.preco * item.quantidade)

            itens_model.append(
                ItemPedidoModel(
                    produto_id=produto.id,
                    quantidade=item.quantidade,
                    preco_unitario=produto.preco
                )
            )

        novo_pedido = PedidoModel(
            cliente_id=usuario.id,
            unidade_id=pedido_in.unidade_id,
            canal_pedido=pedido_in.canalPedido,
            status=StatusPedido.AGUARDANDO_PAGAMENTO,
            valor_total=valor_total,
            itens=itens_model
        )

        pedido_salvo = self.repo.salvar(novo_pedido)
        return pedido_salvo

    def processar_pagamento(self, pedido_id: int):
        # 1. Busca o pedido no banco
        pedido = self.repo.buscar_por_id(pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")

        # 2. Regra de Negócio: Só paga se estiver aguardando
        if pedido.status != StatusPedido.AGUARDANDO_PAGAMENTO:
            raise HTTPException(status_code=400, detail="Este pedido não está aguardando pagamento.")

        # 3. Chama o Gateway de Pagamento (Mock)
        gateway = PagamentoMockAdapter()
        resposta_pagamento = gateway.processar_pagamento(pedido_id=pedido.id)

        # 4. Atualiza o status e PROCESSA FIDELIDADE
        if resposta_pagamento["sucesso"]:
            self.repo.atualizar_status(pedido, StatusPedido.COZINHA)

            # --- LÓGICA DE FIDELIDADE (1 ponto por cada Real gasto) ---
            if pedido.cliente_id:
                usuario = self.usuario_repo.buscar_por_id(pedido.cliente_id)
                if usuario:
                    pontos_ganhos = int(pedido.valor_total)
                    usuario.pontos_fidelidade += pontos_ganhos
                    self.usuario_repo.atualizar(usuario)
                    resposta_pagamento["fidelidade"] = f"Você ganhou {pontos_ganhos} pontos!"
            # -----------------------------------------------------------
        else:
            self.repo.atualizar_status(pedido, StatusPedido.CANCELADO)

        # 5. Retorna um resumo para a API
        return {
            "pedido_id": pedido.id,
            "status_atual": pedido.status,
            "detalhes_pagamento": resposta_pagamento
        }

    def listar_pedidos(self, canal_filtro=None):
        return self.repo.listar_pedidos(canal_filtro=canal_filtro)

class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def cadastrar_usuario(self, user_in: UsuarioCreate):
        # 1. Verifica se o e-mail já existe (Regra de negócio)
        if self.repo.buscar_por_email(user_in.email):
            raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

        # 2. Criptografa a senha (Requisito de LGPD/Segurança)
        senha_criptografada = obter_hash_senha(user_in.senha)

        # 3. Salva no banco
        novo_usuario = UsuarioModel(
            email=user_in.email,
            senha_hash=senha_criptografada,
            perfil=user_in.perfil
        )
        return self.repo.salvar(novo_usuario)