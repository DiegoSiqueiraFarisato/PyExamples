"""Ponto de entrada da API de contatos (exercício 10).

Rode a partir da pasta App:
    python -m uvicorn api_contatos.main:app --reload
ou:
    python -m api_contatos.main
"""

from fastapi import FastAPI

from api_contatos.rotas import contatos

app = FastAPI(
    title="API de Contatos",
    description="Respostas dos exercícios 5 a 10 do material 17_fastapi.py",
    version="1.0.0",
)

app.include_router(contatos.router)


@app.get("/", tags=["sistema"])
def raiz() -> dict:
    return {"mensagem": "API de Contatos", "documentacao": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api_contatos.main:app", reload=True)
