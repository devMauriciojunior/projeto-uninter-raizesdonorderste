from sqlalchemy import String, Column, Integer, Float, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.database import Base
from domain.enums import CanalPedido, StatusPedido, PerfilUsuario

class PedidoModel(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=True)
    canal_pedido = Column(SQLEnum(CanalPedido), nullable=False)
    status = Column(SQLEnum(StatusPedido), nullable=False, default=StatusPedido.AGUARDANDO_PAGAMENTO)
    valor_total = Column(Float, nullable=False, default=0.0)
    criado_em = Column(DateTime, default=datetime.utcnow)
    itens = relationship("ItemPedidoModel", backref="pedido")

class ItemPedidoModel(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=True) # Adicionado para bater com o DER
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    perfil = Column(SQLEnum(PerfilUsuario), nullable=False, default=PerfilUsuario.CLIENTE)
    pontos_fidelidade = Column(Integer, default=0) # Novo campo para o programa de pontos

class UnidadeModel(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    endereco = Column(String, nullable=False)

class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    ativo = Column(Boolean, default=True)

class EstoqueModel(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True, index=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=0)