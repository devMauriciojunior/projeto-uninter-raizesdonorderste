# api/rotas_pedidos.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from domain.schemas import PedidoCreate, PedidoResponse
from domain.enums import PerfilUsuario, CanalPedido
from infrastructure.database import get_db
from infrastructure.security import requer_perfil
from application.services import PedidoService

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(
        pedido: PedidoCreate,
        db: Session = Depends(get_db),
        usuario_atual: dict = Depends(requer_perfil([PerfilUsuario.CLIENTE, PerfilUsuario.ATENDENTE]))
):
    service = PedidoService(db)
    pedido_criado = service.criar_novo_pedido(pedido, usuario_email=usuario_atual["email"])

    return PedidoResponse(
        id=pedido_criado.id,
        status=pedido_criado.status,
        valorTotal=pedido_criado.valor_total,
        mensagem=f"Pedido criado por: {usuario_atual['email']}"
    )

@router.post("/pagar", status_code=status.HTTP_200_OK)
def realizar_pagamento_mock(
        pedido_id: int,
        db: Session = Depends(get_db)
):
    service = PedidoService(db)
    return service.processar_pagamento(pedido_id)

@router.get("/", response_model=List[PedidoResponse])
def listar_pedidos(
        canalPedido: Optional[CanalPedido] = None,
        db: Session = Depends(get_db),
        usuario_atual: dict = Depends(requer_perfil([PerfilUsuario.ADMIN, PerfilUsuario.ATENDENTE, PerfilUsuario.CLIENTE]))
):
    service = PedidoService(db)
    pedidos_banco = service.listar_pedidos(canal_filtro=canalPedido)

    lista_resposta = []
    for p in pedidos_banco:
        lista_resposta.append(
            PedidoResponse(
                id=p.id,
                status=p.status,
                valorTotal=p.valor_total,
                mensagem=f"Canal de origem: {p.canal_pedido.value}"
            )
        )

    return lista_resposta