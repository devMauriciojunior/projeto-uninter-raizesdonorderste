# uvicorn main:app --reload
# pip freeze > requirements.txt

from fastapi import FastAPI
from infrastructure.database import engine, Base
from api import rotas_pedidos, rotas_usuarios

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Raízes do Nordeste",
    version="1.0.0",
    description="Esta é uma api do projeto backend da faculdade Uninter - criada por: Mauricio Jr - RU:4918358"
)

app.include_router(rotas_usuarios.router)
app.include_router(rotas_pedidos.router)

