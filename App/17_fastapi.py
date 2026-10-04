"""
=====================================================================
  MATERIAL DE ESTUDO PYTHON — APIs COM FastAPI
  O que é uma API -> HTTP e JSON -> Primeira rota -> Rodando o
  servidor -> Parâmetros de caminho e de query -> Pydantic (corpo da
  requisição) -> Status codes -> HTTPException -> CRUD completo ->
  Depends -> Headers -> async -> Documentação automática -> Testes ->
  Organização de projetos -> Boas práticas
=====================================================================

PRÉ-REQUISITOS: 01 a 15 (principalmente funções, dicionários, erros,
classes, type hints e testes).

INSTALAÇÃO (se ainda não tiver):
  python -m pip install "fastapi[standard]"
  (instala o FastAPI, o servidor uvicorn e o httpx usado nos testes)

ESTE ARQUIVO TEM DOIS MODOS:

  1. Como MATERIAL (rode direto):
       python 17_fastapi.py
     Ele faz requisições de exemplo para a API e mostra cada pedido e
     cada resposta no terminal, sem precisar subir servidor.

  2. Como SERVIDOR de verdade (da pasta App):
       python -m uvicorn 17_fastapi:app --reload
     Depois abra no navegador:
       http://127.0.0.1:8000/docs     <- documentação interativa!
     Para parar o servidor: Ctrl + C

  Faça os dois! Leia os comentários, rode o modo 1 e depois brinque com
  a API no /docs (modo 2).
"""

from datetime import datetime
from itertools import count
from typing import Annotated, Literal

try:
    from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
    from pydantic import BaseModel, Field, field_validator
except ImportError:
    print("O FastAPI não está instalado neste Python. Instale com:")
    print('  python -m pip install "fastapi[standard]"')
    raise SystemExit(1)


# =====================================================================
# 1. O QUE É UMA API?
# =====================================================================
# API (Application Programming Interface) = uma "porta de entrada" para
# que OUTROS PROGRAMAS conversem com o seu.
#
# Exemplo do dia a dia: o app do banco no seu celular não acessa o banco
# de dados direto. Ele faz PEDIDOS para a API do banco ("qual o saldo?",
# "faça este pix") e a API RESPONDE.
#
#   [ cliente ]  --- pedido (requisição) --->  [ servidor / API ]
#   app, site,   <--- resposta -------------   seu código Python
#   outro sistema
#
# Uma API web (ou "API REST") conversa usando o protocolo HTTP, o mesmo
# que o navegador usa para abrir sites. A diferença: em vez de devolver
# uma página HTML, ela devolve DADOS, quase sempre em JSON (lembra do
# material de dicionários?).


# =====================================================================
# 2. HTTP EM 5 MINUTOS
# =====================================================================
# Toda requisição HTTP tem:
#   - MÉTODO: o que você quer fazer
#   - URL (caminho): em qual recurso
#   - (opcional) HEADERS: informações extras (ex: token de acesso)
#   - (opcional) CORPO: os dados enviados (em JSON)
#
# Os métodos mais usados (o famoso "CRUD"):
# ---------------------------------------------------------------------
#  MÉTODO  | CRUD     | EXEMPLO                 | SIGNIFICADO
# ---------------------------------------------------------------------
#  GET     | Read     | GET /tarefas            | listar tarefas
#  GET     | Read     | GET /tarefas/5          | buscar a tarefa 5
#  POST    | Create   | POST /tarefas           | criar uma tarefa
#  PUT     | Update   | PUT /tarefas/5          | substituir a tarefa 5 inteira
#  PATCH   | Update   | PATCH /tarefas/5        | alterar PARTE da tarefa 5
#  DELETE  | Delete   | DELETE /tarefas/5       | apagar a tarefa 5
# ---------------------------------------------------------------------
#
# Toda resposta tem um STATUS CODE (código de situação):
#   2xx = sucesso         200 OK | 201 Created | 204 No Content
#   4xx = erro do CLIENTE  400 Bad Request | 401 Unauthorized |
#                          403 Forbidden | 404 Not Found |
#                          422 Unprocessable Entity (dados inválidos)
#   5xx = erro do SERVIDOR 500 Internal Server Error (bug no seu código!)
#
# Regra de bolso: 4xx = "você pediu errado"; 5xx = "eu (servidor) errei".


# =====================================================================
# 3. POR QUE FastAPI?
# =====================================================================
# Existem vários frameworks web em Python (Flask, Django...). O FastAPI
# ficou muito popular porque:
#   - Usa os TYPE HINTS que você já conhece para VALIDAR os dados
#     automaticamente. Declarou "idade: int"? Se chegar "abc", ele
#     responde 422 sozinho, sem você escrever um if.
#   - Gera DOCUMENTAÇÃO INTERATIVA automática (/docs)
#   - É rápido e moderno (suporta async)
#   - Pouco código: uma rota é só uma FUNÇÃO com um decorador


# =====================================================================
# 4. A PRIMEIRA API
# =====================================================================
# app = FastAPI() cria a aplicação. Cada ROTA (endpoint) é uma função
# com um DECORADOR que diz o MÉTODO e o CAMINHO:
#
#   @app.get("/")          <- "quando chegar um GET em /, chame raiz()"
#   def raiz():
#       return {...}        <- o dict é convertido para JSON sozinho
#
# Decorador (@algo em cima de uma função) é um recurso do Python que
# "registra" ou "embrulha" a função. Você já viu @property, @classmethod
# e @dataclass. Aqui, @app.get registra a função como rota da API.

app = FastAPI(
    title="API de Tarefas",
    description="API de exemplo do material 17_fastapi.py",
    version="1.0.0",
)


@app.get("/")
def raiz() -> dict:
    return {"mensagem": "Olá, FastAPI!", "documentacao": "/docs"}


# =====================================================================
# 5. PARÂMETROS DE CAMINHO (path parameters)
# =====================================================================
# Partes da URL entre { } viram parâmetros da função:
#   GET /saudacao/Ana  ->  saudar(nome="Ana")
#
# O TYPE HINT é a mágica: em /quadrado/{numero} com "numero: int", o
# FastAPI CONVERTE "7" (texto da URL) para 7 (int). E se chegar
# /quadrado/abc, ele responde 422 explicando o erro, sem a sua função
# nem ser chamada.


@app.get("/saudacao/{nome}")
def saudar(nome: str) -> dict:
    return {"mensagem": f"Olá, {nome}!"}


@app.get("/quadrado/{numero}")
def calcular_quadrado(numero: int) -> dict:
    return {"numero": numero, "quadrado": numero ** 2}


# =====================================================================
# 6. PARÂMETROS DE QUERY (query parameters)
# =====================================================================
# Query = o que vem depois do "?" na URL, no formato chave=valor,
# separados por "&":
#   GET /calculadora/somar?a=10&b=5
#
# No FastAPI: todo parâmetro da função que NÃO está no caminho vira
# parâmetro de query.
#   - Sem valor padrão  -> OBRIGATÓRIO (se faltar: 422)
#   - Com valor padrão  -> opcional


@app.get("/calculadora/somar")
def somar(a: float, b: float = 0) -> dict:
    return {"a": a, "b": b, "resultado": a + b}

# CAMINHO ou QUERY? Regra geral:
#   caminho -> IDENTIFICA um recurso:        /tarefas/5
#   query   -> FILTRA, ORDENA ou PAGINA:     /tarefas?feita=true&limite=10


# =====================================================================
# 7. PYDANTIC: VALIDANDO O CORPO DA REQUISIÇÃO
# =====================================================================
# Para CRIAR uma tarefa, o cliente envia os dados no CORPO, em JSON:
#   POST /tarefas
#   {"titulo": "Estudar FastAPI", "prioridade": "alta"}
#
# Você descreve o formato esperado com uma classe que herda de BaseModel
# (biblioteca Pydantic, que vem junto com o FastAPI). Parece muito um
# @dataclass, mas VALIDA e CONVERTE os dados:
#   - campo obrigatório faltando        -> 422
#   - tipo errado ("prioridade": 123)   -> 422
#   - regra violada (título vazio)      -> 422
#
# Field(...) adiciona regras: min_length, max_length, ge (>=), le (<=)...
# Literal["baixa", "media", "alta"] aceita SÓ esses valores.
#
# É comum ter MAIS DE UM modelo para o mesmo recurso:
#   TarefaCriar     -> o que o cliente ENVIA para criar (sem id!)
#   TarefaAtualizar -> o que pode ser alterado (tudo opcional)
#   Tarefa          -> o que a API DEVOLVE (com id, data etc.)

Prioridade = Literal["baixa", "media", "alta"]


class TarefaCriar(BaseModel):
    titulo: str = Field(min_length=1, max_length=100, examples=["Estudar FastAPI"])
    descricao: str | None = None
    prioridade: Prioridade = "media"


class TarefaAtualizar(BaseModel):
    # Para o PATCH: todos os campos opcionais. Só muda o que for enviado.
    titulo: str | None = Field(default=None, min_length=1, max_length=100)
    descricao: str | None = None
    prioridade: Prioridade | None = None
    feita: bool | None = None

    # PEGADINHA: "opcional" (pode NÃO ser enviado) é diferente de "pode
    # ser null". Sem esta validação, {"titulo": null} seria aceito e a
    # tarefa ficaria SEM título. @field_validator cria uma regra própria:
    # se levantar ValueError, o FastAPI responde 422. Ela só roda para
    # campos ENVIADOS, então não enviar o campo continua permitido.
    # (descricao fica de fora de propósito: null ali = apagar a descrição)
    @field_validator("titulo", "prioridade", "feita")
    @classmethod
    def nao_aceitar_null(cls, valor):
        if valor is None:
            raise ValueError("não pode ser null (para não alterar, não envie o campo)")
        return valor


class Tarefa(TarefaCriar):
    # Herda titulo, descricao e prioridade de TarefaCriar (material 13!)
    id: int
    feita: bool = False
    criada_em: datetime


# =====================================================================
# 8. O "BANCO DE DADOS" (em memória)
# =====================================================================
# Para focar no FastAPI, as tarefas ficam num dict, na memória. Ao
# reiniciar o servidor, tudo se perde. Num projeto real, aqui entraria
# um banco de dados (SQLite, PostgreSQL...) ou, no mínimo, um arquivo
# JSON como no material 09.

tarefas_db: dict[int, Tarefa] = {}       # {id: Tarefa}
gerador_de_ids = count(start=1)          # next(gerador_de_ids) -> 1, 2, 3...


# =====================================================================
# 9. DEPENDÊNCIAS: Depends
# =====================================================================
# Uma DEPENDÊNCIA é uma função que o FastAPI executa ANTES da rota, e
# cujo resultado é entregue à rota. Serve para REAPROVEITAR lógica que
# várias rotas precisam:
#   - buscar um item ou devolver 404
#   - ler parâmetros de paginação
#   - conferir se o usuário está autenticado
#
# Annotated[tipo, Depends(funcao)] diz: "para obter este parâmetro,
# chame funcao()". (Annotated só "anota" informação extra num type hint.)
#
# E a dependência pode ter seus PRÓPRIOS parâmetros (de caminho, query,
# header...), que o FastAPI preenche do mesmo jeito que numa rota.


def obter_tarefa_ou_404(tarefa_id: int) -> Tarefa:
    """Busca a tarefa pelo id do caminho, ou responde 404."""
    tarefa = tarefas_db.get(tarefa_id)
    if tarefa is None:
        # HTTPException interrompe a requisição e devolve o erro ao
        # cliente com o status e a mensagem escolhidos.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa {tarefa_id} não encontrada",
        )
    return tarefa


def paginacao(
    pular: Annotated[int, Query(ge=0, description="Quantos itens pular")] = 0,
    limite: Annotated[int, Query(ge=1, le=100, description="Máximo de itens")] = 10,
) -> dict:
    return {"pular": pular, "limite": limite}


# HEADERS: "x_token: Header()" lê o header HTTP "X-Token" (o FastAPI
# troca _ por - e ignora maiúsculas).
#
# ATENÇÃO: isto é só uma DEMONSTRAÇÃO de dependência com header. Num
# sistema real:
#   - o segredo NUNCA fica escrito no código (use variável de ambiente
#     ou arquivo de configuração fora do git, como o config.env do Server)
#   - a autenticação usa padrões como OAuth2 + JWT (o FastAPI tem
#     suporte pronto em fastapi.security)
TOKEN_ADMIN = "segredo-de-estudo"


def exigir_token_admin(x_token: Annotated[str | None, Header()] = None) -> None:
    if x_token != TOKEN_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou ausente (envie o header X-Token)",
        )


# =====================================================================
# 10. CRUD COMPLETO DE TAREFAS
# =====================================================================
# Repare em cada decorador:
#   response_model -> o formato da RESPOSTA. O FastAPI valida e filtra a
#                     saída por ele, e usa na documentação.
#   status_code    -> o status de SUCESSO da rota (padrão: 200)
#   tags           -> agrupa as rotas na documentação /docs


@app.post(
    "/tarefas",
    response_model=Tarefa,
    status_code=status.HTTP_201_CREATED,     # 201 = "criado"
    tags=["tarefas"],
)
def criar_tarefa(dados: TarefaCriar) -> Tarefa:
    # "dados: TarefaCriar" -> o FastAPI lê o JSON do corpo, valida pelo
    # modelo e entrega um objeto TarefaCriar pronto. Se for inválido, a
    # função nem é chamada (422).
    tarefa = Tarefa(
        id=next(gerador_de_ids),
        criada_em=datetime.now(),
        **dados.model_dump(),     # model_dump() = o modelo como dict
    )
    tarefas_db[tarefa.id] = tarefa
    return tarefa


@app.get("/tarefas", response_model=list[Tarefa], tags=["tarefas"])
def listar_tarefas(
    pagina: Annotated[dict, Depends(paginacao)],
    feita: bool | None = None,
    prioridade: Prioridade | None = None,
    busca: Annotated[str | None, Query(min_length=2)] = None,
) -> list[Tarefa]:
    resultado = list(tarefas_db.values())

    # Filtros opcionais: só aplica o que o cliente pediu
    if feita is not None:
        resultado = [t for t in resultado if t.feita == feita]
    if prioridade is not None:
        resultado = [t for t in resultado if t.prioridade == prioridade]
    if busca is not None:
        resultado = [t for t in resultado if busca.lower() in t.titulo.lower()]

    inicio = pagina["pular"]
    return resultado[inicio : inicio + pagina["limite"]]


@app.get("/tarefas/{tarefa_id}", response_model=Tarefa, tags=["tarefas"])
def buscar_tarefa(tarefa: Annotated[Tarefa, Depends(obter_tarefa_ou_404)]) -> Tarefa:
    # O tarefa_id do caminho vai para a DEPENDÊNCIA obter_tarefa_ou_404,
    # que devolve a tarefa (ou já respondeu 404). Aqui só resta retornar.
    return tarefa


@app.patch("/tarefas/{tarefa_id}", response_model=Tarefa, tags=["tarefas"])
def atualizar_tarefa(
    alteracoes: TarefaAtualizar,
    tarefa: Annotated[Tarefa, Depends(obter_tarefa_ou_404)],
) -> Tarefa:
    # exclude_unset=True -> só os campos que o cliente ENVIOU.
    # Sem isso, os campos não enviados viriam como None e apagariam os
    # valores atuais!
    mudancas = alteracoes.model_dump(exclude_unset=True)
    atualizada = tarefa.model_copy(update=mudancas)
    tarefas_db[tarefa.id] = atualizada
    return atualizada


@app.delete(
    "/tarefas/{tarefa_id}",
    status_code=status.HTTP_204_NO_CONTENT,  # 204 = sucesso, sem corpo
    dependencies=[Depends(exigir_token_admin)],
    tags=["tarefas"],
)
def apagar_tarefa(tarefa: Annotated[Tarefa, Depends(obter_tarefa_ou_404)]) -> None:
    # dependencies=[...] no decorador: roda a dependência (conferir o
    # token) sem precisar do resultado dela dentro da função.
    del tarefas_db[tarefa.id]


# =====================================================================
# 11. async def
# =====================================================================
# Você vai ver MUITO "async def" em código FastAPI:
#
#   @app.get("/status")
#   async def status_api(): ...
#
# async/await é programação ASSÍNCRONA: enquanto uma requisição ESPERA
# algo lento (banco de dados, outra API, arquivo), o servidor atende
# outras requisições em vez de ficar parado.
#
# Para começar, a regra prática:
#   - Use "async def" se dentro da função você usar "await" (bibliotecas
#     assíncronas, como httpx.AsyncClient, ou o broker do seu Server)
#   - Use "def" normal em todo o resto. O FastAPI roda as funções "def"
#     numa thread separada, então elas também não travam o servidor.
#   - NUNCA chame algo lento e NÃO assíncrono (time.sleep, requests.get)
#     dentro de "async def": isso trava o servidor inteiro.
#
# async é um assunto próprio. Por isso este material usa "def".


@app.get("/status", tags=["sistema"])
async def status_api() -> dict:
    return {"status": "ok", "total_tarefas": len(tarefas_db)}


# =====================================================================
# 12. DOCUMENTAÇÃO AUTOMÁTICA
# =====================================================================
# Com o servidor rodando (modo 2, no topo do arquivo), abra:
#   http://127.0.0.1:8000/docs   -> Swagger UI: dá para TESTAR cada rota
#                                   clicando em "Try it out"
#   http://127.0.0.1:8000/redoc  -> ReDoc: documentação para leitura
#   http://127.0.0.1:8000/openapi.json -> a especificação OpenAPI pura
#
# Tudo isso foi gerado a partir dos type hints, dos modelos Pydantic,
# das docstrings e dos parâmetros (title, tags, description...). Você
# não escreveu uma linha de documentação à parte!
#
# Ferramentas como o Postman (usado no seu Server/) também importam o
# openapi.json.


# =====================================================================
# 13. TESTANDO A API (pytest + TestClient)
# =====================================================================
# O TestClient faz requisições para a sua API SEM subir servidor. É o
# que o modo 1 deste arquivo usa. Num arquivo de testes, fica assim:
#
#   from fastapi.testclient import TestClient
#   from api_tarefas.main import app
#
#   cliente = TestClient(app)
#
#   def test_criar_tarefa_devolve_201():
#       resposta = cliente.post("/tarefas", json={"titulo": "Estudar"})
#       assert resposta.status_code == 201
#       assert resposta.json()["titulo"] == "Estudar"
#
#   def test_buscar_tarefa_inexistente_devolve_404():
#       assert cliente.get("/tarefas/999").status_code == 404
#
# Tudo que você aprendeu no material de testes vale aqui: fixtures (um
# cliente novo com o banco limpo para cada teste), parametrize (vários
# corpos inválidos que devem dar 422) etc.
# Os testes DESTA API estão em tests/test_fastapi.py (46 testes, com
# fixture que limpa o banco, parametrize de 422, token etc.). Rode com:
#   python -m pytest tests/test_fastapi.py -v
# O seu Server/tests/test_api.py usa as mesmas ideias. Leia os dois!


# =====================================================================
# 14. ORGANIZANDO UMA API DE VERDADE
# =====================================================================
# Este material usa UM arquivo para facilitar o estudo. Um projeto real
# divide em módulos (material 11!), por exemplo:
#
#   api_tarefas/
#       __init__.py
#       main.py          <- cria o app = FastAPI() e inclui os routers
#       modelos.py       <- modelos Pydantic (TarefaCriar, Tarefa...)
#       dependencias.py  <- funções usadas com Depends
#       config.py        <- configurações (lidas de variáveis de ambiente)
#       rotas/
#           __init__.py
#           tarefas.py   <- router = APIRouter(prefix="/tarefas")
#           usuarios.py
#   tests/
#       test_tarefas.py
#
# APIRouter é um "mini app": cada arquivo de rotas cria o seu, e o
# main.py junta todos:
#
#   # rotas/tarefas.py
#   from fastapi import APIRouter
#   router = APIRouter(prefix="/tarefas", tags=["tarefas"])
#
#   @router.get("")          # vira GET /tarefas
#   def listar(): ...
#
#   # main.py
#   from api_tarefas.rotas import tarefas
#   app = FastAPI()
#   app.include_router(tarefas.router)
#
# SEU Server/ USA ESSAS IDEIAS (e vai além). Abra os arquivos e procure:
#   - app/services/*_service.py -> cada um tem um "router" (APIRouter)
#   - app/main.py -> inclui os routers automaticamente, e usa um
#     "lifespan" para iniciar/parar o broker junto com o servidor
#   - app/core/deps.py -> dependências usadas com Depends
#   - app/core/config.py -> configuração lida do config.env
#   - tests/conftest.py -> fixture "client" com TestClient
# Agora você tem a base para ler aquele código!


# =====================================================================
# 15. ERROS COMUNS
# =====================================================================
# ERRO 1: "Error loading ASGI app. Could not import module".
#         Rode o uvicorn da pasta certa e confira o nome:
#         python -m uvicorn modulo:variavel_do_app
# ERRO 2: 422 inesperado. Leia o "detail" da resposta: ele diz QUAL
#         campo ("loc") e POR QUÊ ("msg"). Muitas vezes é o tipo errado
#         ou o JSON enviado sem o header Content-Type: application/json.
# ERRO 3: enviar dados de criação pela URL em vez do corpo. Use
#         json=... no cliente e um modelo Pydantic na rota.
# ERRO 4: retornar 200 para tudo. Use 201 ao criar, 204 ao apagar,
#         404 quando não existe, 401/403 para acesso negado.
# ERRO 5: devolver dados sensíveis (senha, token) na resposta. Use um
#         response_model SEM esses campos.
# ERRO 6: PATCH sem exclude_unset=True, apagando campos não enviados.
#         E o irmão dele: aceitar {"titulo": null} no PATCH só porque o
#         campo é opcional. Veja o @field_validator em TarefaAtualizar.
# ERRO 7: duas rotas conflitando: /tarefas/{tarefa_id} declarada ANTES
#         de /tarefas/pendentes faz "pendentes" ser lido como id (e dar
#         422). Rotas fixas vêm ANTES das rotas com parâmetro.
# ERRO 8: segredo (senha, token, chave de API) escrito no código e
#         commitado no git.


# =====================================================================
# 16. NAMING CONVENTIONS E BOAS PRÁTICAS
# =====================================================================
# URLS (as "rotas"):
#   - SUBSTANTIVOS no PLURAL, nunca verbos: o MÉTODO HTTP já é o verbo
#       ✅ POST /tarefas            ❌ POST /criarTarefa
#       ✅ DELETE /tarefas/5        ❌ GET /apagar_tarefa?id=5
#   - Minúsculas e, se precisar de duas palavras, hífen (kebab-case):
#       /itens-pedido, /dead-letters
#   - Hierarquia para recursos relacionados: /usuarios/7/tarefas
#   - Campos do JSON: snake_case, consistente em toda a API
#
# CÓDIGO:
#   - Modelos Pydantic: PascalCase, com sufixo que diz o PAPEL:
#       TarefaCriar, TarefaAtualizar, Tarefa (ou TarefaResposta)
#   - Funções das rotas: snake_case com verbo: criar_tarefa, listar_tarefas
#   - Dependências: o que entregam -> obter_tarefa_ou_404, paginacao
#
# BOAS PRÁTICAS:
#   1. Deixe os type hints e o Pydantic validarem. Evite ifs de validação
#      manual quando um Field resolve.
#   2. Modelos separados para entrada e saída.
#   3. Status codes corretos e mensagens de erro claras no "detail".
#   4. Reaproveite lógica com Depends (buscar-ou-404, autenticação).
#   5. Rotas finas: a regra de negócio vai para funções/módulos próprios
#      (testáveis sem HTTP!). A rota só recebe, chama e devolve.
#   6. Configurações e segredos em variáveis de ambiente.
#   7. Teste com TestClient: caminho feliz, 404, 422 e acesso negado.
#   8. Use APIRouter e divida em módulos quando a API crescer.


# =====================================================================
# 17. DEMONSTRAÇÃO (só roda no modo 1: python 17_fastapi.py)
# =====================================================================
# Quando o uvicorn IMPORTA este arquivo (modo 2), o bloco abaixo NÃO
# roda, graças ao if __name__ == "__main__" (material 11).

def demonstrar() -> None:
    import warnings

    # Algumas versões do TestClient mostram um aviso de depreciação que
    # vem de DENTRO das bibliotecas (não do seu código). Escondemos só
    # esse aviso para não poluir a saída do material.
    warnings.filterwarnings("ignore", message=".*httpx.*")

    from fastapi.testclient import TestClient

    cliente = TestClient(app)

    def chamar(metodo: str, url: str, **opcoes):
        resposta = cliente.request(metodo, url, **opcoes)
        extra = ""
        if "json" in opcoes:
            extra += f"  corpo={opcoes['json']}"
        if "headers" in opcoes:
            extra += f"  headers={opcoes['headers']}"
        print(f"→ {metodo} {url}{extra}")

        if not resposta.content:
            corpo = "(sem corpo)"
        elif resposta.status_code == 422:
            # Mostra só o essencial de cada erro de validação
            corpo = [f"{'.'.join(map(str, erro['loc']))}: {erro['msg']}" for erro in resposta.json()["detail"]]
        else:
            corpo = resposta.json()
        print(f"← {resposta.status_code} {corpo}\n")
        return resposta

    def secao(titulo: str) -> None:
        print("=" * 60)
        print(titulo)
        print("=" * 60)

    secao("4 a 6. ROTAS SIMPLES E PARÂMETROS")
    chamar("GET", "/")
    chamar("GET", "/saudacao/Diego")
    chamar("GET", "/quadrado/7")
    chamar("GET", "/quadrado/abc")                 # 422: não é int
    chamar("GET", "/calculadora/somar?a=10&b=5")
    chamar("GET", "/calculadora/somar?a=10")       # b é opcional
    chamar("GET", "/calculadora/somar?b=5")        # 422: falta o a

    secao("7 e 10. CRIANDO TAREFAS (POST + Pydantic)")
    chamar("POST", "/tarefas", json={"titulo": "Estudar FastAPI", "prioridade": "alta"})
    chamar("POST", "/tarefas", json={"titulo": "Fazer os exercícios"})
    chamar("POST", "/tarefas", json={"titulo": "Ler o código do Server", "descricao": "app/main.py primeiro"})
    print("Agora, dados INVÁLIDOS (o FastAPI responde 422 sozinho):\n")
    chamar("POST", "/tarefas", json={"titulo": ""})
    chamar("POST", "/tarefas", json={"titulo": "X", "prioridade": "urgentíssima"})
    chamar("POST", "/tarefas", json={"descricao": "sem título"})

    secao("10. LISTANDO, FILTRANDO E PAGINANDO (GET + query)")
    chamar("GET", "/tarefas?limite=2")
    chamar("GET", "/tarefas?prioridade=alta")
    chamar("GET", "/tarefas?busca=server")
    chamar("GET", "/tarefas?limite=500")           # 422: limite máximo é 100

    secao("9 e 10. BUSCANDO UMA TAREFA (Depends + 404)")
    chamar("GET", "/tarefas/1")
    chamar("GET", "/tarefas/999")

    secao("10. ATUALIZANDO PARTE DE UMA TAREFA (PATCH)")
    chamar("PATCH", "/tarefas/2", json={"feita": True})
    print("Repare: título e prioridade da tarefa 2 continuaram iguais.\n")
    chamar("GET", "/tarefas?feita=true")

    secao("9 e 10. APAGANDO (DELETE + header de token)")
    chamar("DELETE", "/tarefas/3")                                   # 401
    chamar("DELETE", "/tarefas/3", headers={"X-Token": "chute"})     # 401
    chamar("DELETE", "/tarefas/3", headers={"X-Token": TOKEN_ADMIN}) # 204
    chamar("GET", "/tarefas/3")                                      # 404

    secao("11. ROTA async")
    chamar("GET", "/status")

    print("=" * 60)
    print("FIM! Agora suba o servidor e explore o /docs:")
    print("  python -m uvicorn 17_fastapi:app --reload")
    print("  http://127.0.0.1:8000/docs")
    print("Depois vá para os exercícios no final deste arquivo.")
    print("=" * 60)


if __name__ == "__main__":
    demonstrar()


# =====================================================================
# 18. EXERCÍCIOS PARA PRATICAR
# =====================================================================
# Crie um arquivo novo (ex: exercicios_fastapi.py) e rode com o uvicorn.
# Teste cada rota pelo /docs e, quando fizer sentido, com TestClient.
#
#  1. Crie uma rota GET /ola que devolve {"mensagem": "Olá, mundo!"}.
#     Suba o servidor e abra a rota no navegador e no /docs.
#  2. Crie GET /par-ou-impar/{numero} que devolve
#     {"numero": 7, "resultado": "ímpar"}. O que acontece com /par-ou-impar/x?
#  3. Crie GET /conversor/temperatura?celsius=25 que devolve celsius,
#     fahrenheit e kelvin. Reaproveite o pacote utilidades (material 11).
#  4. Crie GET /imc?peso=70&altura=1.75 que devolve o IMC e a
#     classificação. Use Query(gt=0) para recusar peso e altura <= 0.
#  5. Crie uma API de CONTATOS com um modelo Pydantic Contato (nome
#     obrigatório de 2 a 50 caracteres, telefone obrigatório e email
#     opcional) e as rotas: POST /contatos (201), GET /contatos e
#     GET /contatos/{contato_id} (404 se não existir).
#  6. Na API de contatos, adicione PATCH /contatos/{contato_id} e
#     DELETE /contatos/{contato_id} (204). Use uma dependência
#     obter_contato_ou_404 nas três rotas que recebem o id.
#  7. Adicione em GET /contatos um filtro ?busca= (parte do nome, sem
#     diferenciar maiúsculas) e paginação com ?pular= e ?limite=.
#  8. Escreva testes com pytest + TestClient para a API de contatos:
#     criação (201), busca (200 e 404), dados inválidos (422, com
#     parametrize) e remoção (204 e depois 404). Use uma fixture que
#     limpa o "banco" antes de cada teste.
#  9. (Desafio) Faça a API de contatos SALVAR em JSON (material 09), para
#     os dados sobreviverem quando o servidor reinicia. Dica: separe a
#     leitura e a gravação num módulo próprio, como no pacote tarefas/.
# 10. (Desafio) Reorganize a API de contatos num pacote (api_contatos/)
#     com main.py, modelos.py, dependencias.py e rotas/contatos.py usando
#     APIRouter. Os testes do exercício 8 devem continuar passando.
# 11. (Desafio) Leia o seu Server/: siga o caminho de um POST /orders
#     desde a rota em app/services/orders_service.py até o broker, e
#     explique com suas palavras o que acontece. Depois rode os testes
#     dele (veja o Server/CLAUDE.md).
