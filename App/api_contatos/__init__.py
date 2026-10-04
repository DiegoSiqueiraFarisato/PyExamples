"""API de Contatos: respostas dos exercícios 5 a 10 do material 17_fastapi.py.

    api_contatos/
        main.py            <- cria o app e inclui o router       (ex. 10)
        modelos.py         <- modelos Pydantic                   (ex. 5 e 6)
        armazenamento.py   <- leitura/gravação em JSON           (ex. 9)
        dependencias.py    <- repositório, 404 e paginação       (ex. 6 e 7)
        rotas/
            contatos.py    <- as rotas, com APIRouter            (ex. 5 a 7 e 10)

Os testes (exercício 8) estão em tests/test_api_contatos.py.

Para rodar o servidor, a partir da pasta App:
    python -m uvicorn api_contatos.main:app --reload
"""
