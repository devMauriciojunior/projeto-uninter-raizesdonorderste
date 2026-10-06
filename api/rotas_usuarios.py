from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from domain.schemas import UsuarioCreate, UsuarioResponse
from infrastructure.database import get_db
from infrastructure.security import criar_token_acesso, verificar_senha
from infrastructure.repositories import UsuarioRepository
from application.services import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuários e Autenticação"])

@router.post("/cadastrar", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(
        usuario: UsuarioCreate,
        db: Session = Depends(get_db)
):
    service = UsuarioService(db)
    return service.cadastrar_usuario(usuario)

@router.post("/login")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    repo = UsuarioRepository(db)
    usuario = repo.buscar_por_email(form_data.username)

    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    perfil_str = usuario.perfil.value if hasattr(usuario.perfil, 'value') else usuario.perfil

    dados_token = {"sub": usuario.email, "perfil": perfil_str}
    token = criar_token_acesso(dados=dados_token)

    return {"access_token": token, "token_type": "bearer"}