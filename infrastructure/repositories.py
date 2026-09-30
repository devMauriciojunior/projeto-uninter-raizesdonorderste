from sqlalchemy.orm import Session
from infrastructure.models import PedidoModel, UsuarioModel, ProdutoModel, EstoqueModel

class PedidoRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, pedido: PedidoModel):
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def buscar_por_id(self, pedido_id: int):
        return self.db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()

    def atualizar_status(self, pedido: PedidoModel, novo_status):
        pedido.status = novo_status
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def listar_pedidos(self, canal_filtro=None):
        query = self.db.query(PedidoModel)

        if canal_filtro:
            query = query.filter(PedidoModel.canal_pedido == canal_filtro)

        return query.all()

class ProdutoRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_id(self, produto_id: int):
        return self.db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()

class EstoqueRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_unidade_e_produto(self, unidade_id: int, produto_id: int):
        return self.db.query(EstoqueModel).filter(
            EstoqueModel.unidade_id == unidade_id,
            EstoqueModel.produto_id == produto_id
        ).first()

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_email(self, email: str):
        return self.db.query(UsuarioModel).filter(UsuarioModel.email == email).first()

    def salvar(self, usuario: UsuarioModel):
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def buscar_por_id(self, usuario_id: int):
        return self.db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()

    def atualizar(self, usuario: UsuarioModel):
        self.db.commit()
        self.db.refresh(usuario)
        return usuario