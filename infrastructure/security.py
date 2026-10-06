import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "chave_secreta_padrao")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

def verificar_senha(senha_pura, senha_hash):
    return pwd_context.verify(senha_pura, senha_hash)

def obter_hash_senha(senha):
    return pwd_context.hash(senha)

def criar_token_acesso(dados: dict):
    dados_para_codificar = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_para_codificar.update({"exp": expiracao})

    token_jwt = jwt.encode(dados_para_codificar, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def obter_usuario_atual(token: str = Depends(oauth2_scheme)):
    erro_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        perfil: str = payload.get("perfil")

        if email is None or perfil is None:
            raise erro_credenciais

        return {"email": email, "perfil": perfil}
    except JWTError:
        raise erro_credenciais

def requer_perfil(perfis_permitidos: list):
    def verificador_perfil(usuario: dict = Depends(obter_usuario_atual)):
        perfis_str = [p.value if hasattr(p, 'value') else p for p in perfis_permitidos]
        if usuario.get("perfil") not in perfis_str:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operação não permitida para o seu perfil"
            )
        return usuario
    return verificador_perfil