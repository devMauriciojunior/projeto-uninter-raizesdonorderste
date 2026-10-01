from datetime import timedelta
from infrastructure.database import SessionLocal
from infrastructure.models import PedidoModel, UsuarioModel, UnidadeModel, ProdutoModel, EstoqueModel

AZUL = "\033[1;34m"
RESET = "\033[0m"

def visualizar_dados():
    db = SessionLocal()
    try:
        # --- CONSULTA DE UNIDADES ---
        unidades = db.query(UnidadeModel).all()
        print(f"\n{AZUL}=============================== ENCONTRADAS {len(unidades)} UNIDADES NO BANCO ===================================={RESET}")
        for und in unidades:
            print(f"ID: {und.id} | Nome: {und.nome} | Endereço: {und.endereco}")
        print(f"{AZUL}===================================================================================================={RESET}\n")

        # --- CONSULTA DE PRODUTOS ---
        produtos = db.query(ProdutoModel).all()
        print(f"{AZUL}=============================== ENCONTRADOS {len(produtos)} PRODUTOS NO BANCO ===================================={RESET}")
        for prod in produtos:
            status = "Ativo" if prod.ativo else "Inativo"
            print(f"ID: {prod.id} | Nome: {prod.nome} | Preço: R$ {prod.preco:.2f} | Status: {status}")
        print(f"{AZUL}===================================================================================================={RESET}\n")

        # --- CONSULTA DE ESTOQUE ---
        estoques = db.query(EstoqueModel).all()
        print(f"{AZUL}================================== REGISTROS DE ESTOQUE: {len(estoques)} ========================================={RESET}")
        for est in estoques:
            print(
                f"ID: {est.id} | Unidade ID: {est.unidade_id} | Produto ID: {est.produto_id} | Qtd Disponível: {est.quantidade}")
        print(f"{AZUL}===================================================================================================={RESET}\n")

        # --- CONSULTA DE USUÁRIOS ---
        usuarios = db.query(UsuarioModel).all()
        print(f"{AZUL}=============================== ENCONTRADOS {len(usuarios)} USUÁRIOS NO BANCO ===================================={RESET}")
        for usuario in usuarios:
            senha_curta = usuario.senha_hash[:15] + "..." if usuario.senha_hash else "N/A"
            perfil_limpo = usuario.perfil.value if hasattr(usuario.perfil, 'value') else usuario.perfil

            print(
                f"ID: {usuario.id} | E-mail: {usuario.email} | "
                f"Perfil: {perfil_limpo} | Pontos: {usuario.pontos_fidelidade} | Hash: {senha_curta}"
            )
        print(f"{AZUL}===================================================================================================={RESET}\n")

        # --- CONSULTA DE PEDIDOS ---
        pedidos = db.query(PedidoModel).all()
        print(f"{AZUL}=============================== ENCONTRADOS {len(pedidos)} PEDIDOS NO BANCO ====================================={RESET}")
        for pedido in pedidos:
            canal_limpo = pedido.canal_pedido.value if hasattr(pedido.canal_pedido, 'value') else pedido.canal_pedido
            status_limpo = pedido.status.value if hasattr(pedido.status, 'value') else pedido.status

            criado_br = pedido.criado_em - timedelta(hours=3) if pedido.criado_em else None
            data_formatada = criado_br.strftime("%d/%m/%Y %H:%M:%S") if criado_br else "N/A"

            print(
                f"ID: {pedido.id} | Unidade: {pedido.unidade_id} | Canal: {canal_limpo} | "
                f"Status: {status_limpo} | Valor: R$ {pedido.valor_total:.2f} | ClienteID: {pedido.cliente_id} | Criado: {data_formatada}"
            )
        print(f"{AZUL}===================================================================================================={RESET}\n")
    finally:
        db.close()

visualizar_dados()