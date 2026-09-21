from fastapi import FastAPI

app = FastAPI(
    title="Teste de API FastAPI",
    description="Descrição aaaaaaaaaaaaaaaa",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"mensagem": "API com FastAPI!"}

