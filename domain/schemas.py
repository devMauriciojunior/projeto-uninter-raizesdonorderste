from pydantic import BaseModel, Field
from typing import List, Optional
from domain.enums import CanalPedido, StatusPedido, PerfilUsuario

class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0, description="A quantidade deve ser maior que zero")

class PedidoCreate(BaseModel):
    canalPedido: CanalPedido
    itens: List[ItemPedidoCreate]
    unidade_id: int

class PedidoResponse(BaseModel):
    id: int
    status: StatusPedido
    valorTotal: float
    mensagem: Optional[str] = None

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    preco: float
    ativo: bool

class EstoqueResponse(BaseModel):
    produto_id: int
    quantidade: int

class UsuarioCreate(BaseModel):
    email: str
    senha: str
    perfil: PerfilUsuario

class UsuarioResponse(BaseModel):
    id: int
    email: str
    perfil: PerfilUsuario
