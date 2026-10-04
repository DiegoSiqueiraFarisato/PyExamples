"""Testes da API do material 17_fastapi.py.

Rode a partir da pasta App:
    python -m pytest tests/test_fastapi.py -v

Conceitos usados (material 15 e 17):
  - TestClient: faz requisições para a API sem subir servidor
  - fixtures: cada teste recebe um cliente com o "banco" vazio
  - monkeypatch: troca o banco em memória por um novo, e desfaz depois
  - parametrize: vários corpos inválidos que devem dar 422
"""

import importlib
from itertools import count

import pytest

pytest.importorskip("fastapi", reason="instale com: python -m pip install \"fastapi[standard]\"")

from fastapi.testclient import TestClient  # noqa: E402  (só depois do importorskip)

# "import 17_fastapi" é erro de sintaxe (nome começa com número), mas o
# importlib aceita o nome como texto. É assim que o uvicorn também faz.
api = importlib.import_module("17_fastapi")

TOKEN_ADMIN = api.TOKEN_ADMIN


# =====================================================================
# FIXTURES
# =====================================================================
@pytest.fixture
def cliente(monkeypatch) -> TestClient:
    """Cliente da API com o banco em memória VAZIO.

    Sem isto, as tarefas criadas num teste "vazariam" para o próximo, e
    os testes passariam ou falhariam dependendo da ORDEM em que rodam.
    """
    monkeypatch.setattr(api, "tarefas_db", {})
    monkeypatch.setattr(api, "gerador_de_ids", count(start=1))
    return TestClient(api.app)


@pytest.fixture
def tarefas_exemplo(cliente) -> list[dict]:
    """Cria 3 tarefas e devolve o JSON de cada uma."""
    corpos = [
        {"titulo": "Estudar FastAPI", "prioridade": "alta"},
        {"titulo": "Fazer os exercícios"},
        {"titulo": "Ler o código do Server", "descricao": "app/main.py primeiro"},
    ]
    return [cliente.post("/tarefas", json=corpo).json() for corpo in corpos]


@pytest.fixture
def headers_admin() -> dict:
    return {"X-Token": TOKEN_ADMIN}


# =====================================================================
# ROTAS SIMPLES E PARÂMETROS (seções 4 a 6)
# =====================================================================
def test_raiz(cliente):
    resposta = cliente.get("/")
    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Olá, FastAPI!"


def test_saudacao_usa_o_parametro_do_caminho(cliente):
    assert cliente.get("/saudacao/Diego").json() == {"mensagem": "Olá, Diego!"}


def test_quadrado_converte_o_texto_da_url_para_int(cliente):
    assert cliente.get("/quadrado/7").json() == {"numero": 7, "quadrado": 49}


def test_quadrado_com_texto_devolve_422(cliente):
    resposta = cliente.get("/quadrado/abc")
    assert resposta.status_code == 422
    # O "loc" diz ONDE está o erro: no caminho (path), parâmetro numero
    assert resposta.json()["detail"][0]["loc"] == ["path", "numero"]


@pytest.mark.parametrize(
    ("url", "resultado"),
    [
        ("/calculadora/somar?a=10&b=5", 15),
        ("/calculadora/somar?a=10", 10),          # b é opcional (padrão 0)
        ("/calculadora/somar?a=1.5&b=2.25", 3.75),
    ],
)
def test_somar(cliente, url, resultado):
    assert cliente.get(url).json()["resultado"] == pytest.approx(resultado)


def test_somar_sem_o_parametro_obrigatorio_devolve_422(cliente):
    resposta = cliente.get("/calculadora/somar?b=5")
    assert resposta.status_code == 422
    assert resposta.json()["detail"][0]["loc"] == ["query", "a"]


# =====================================================================
# CRIAR (POST) — seção 7 e 10
# =====================================================================
def test_criar_tarefa_devolve_201_e_a_tarefa_completa(cliente):
    resposta = cliente.post("/tarefas", json={"titulo": "Estudar", "prioridade": "alta"})

    assert resposta.status_code == 201
    tarefa = resposta.json()
    assert tarefa["id"] == 1
    assert tarefa["titulo"] == "Estudar"
    assert tarefa["prioridade"] == "alta"
    assert tarefa["feita"] is False
    assert tarefa["descricao"] is None
    assert "criada_em" in tarefa


def test_criar_tarefa_usa_prioridade_media_como_padrao(cliente):
    resposta = cliente.post("/tarefas", json={"titulo": "Sem prioridade"})
    assert resposta.json()["prioridade"] == "media"


def test_ids_sao_sequenciais(cliente):
    ids = [cliente.post("/tarefas", json={"titulo": f"T{n}"}).json()["id"] for n in range(3)]
    assert ids == [1, 2, 3]


def test_cliente_nao_consegue_escolher_id_nem_feita(cliente):
    # Campos que não estão em TarefaCriar são ignorados pelo Pydantic
    resposta = cliente.post("/tarefas", json={"titulo": "Espertinho", "id": 999, "feita": True})
    assert resposta.json()["id"] == 1
    assert resposta.json()["feita"] is False


@pytest.mark.parametrize(
    ("corpo", "campo_com_erro"),
    [
        ({}, "titulo"),                                       # sem título
        ({"titulo": ""}, "titulo"),                           # título vazio
        ({"titulo": "x" * 101}, "titulo"),                    # título longo demais
        ({"titulo": "X", "prioridade": "urgente"}, "prioridade"),  # fora do Literal
        ({"titulo": 123}, "titulo"),                          # tipo errado
    ],
    ids=["sem-titulo", "titulo-vazio", "titulo-longo", "prioridade-invalida", "titulo-numero"],
)
def test_criar_tarefa_com_dados_invalidos_devolve_422(cliente, corpo, campo_com_erro):
    resposta = cliente.post("/tarefas", json=corpo)

    assert resposta.status_code == 422
    assert resposta.json()["detail"][0]["loc"] == ["body", campo_com_erro]


def test_tarefa_invalida_nao_e_salva(cliente):
    cliente.post("/tarefas", json={"titulo": ""})
    assert cliente.get("/tarefas").json() == []


# =====================================================================
# LISTAR, FILTRAR E PAGINAR (GET /tarefas)
# =====================================================================
def test_listar_sem_tarefas_devolve_lista_vazia(cliente):
    resposta = cliente.get("/tarefas")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_listar_devolve_todas_as_tarefas(cliente, tarefas_exemplo):
    assert len(cliente.get("/tarefas").json()) == 3


def test_filtrar_por_prioridade(cliente, tarefas_exemplo):
    titulos = [t["titulo"] for t in cliente.get("/tarefas?prioridade=alta").json()]
    assert titulos == ["Estudar FastAPI"]


def test_busca_ignora_maiusculas(cliente, tarefas_exemplo):
    titulos = [t["titulo"] for t in cliente.get("/tarefas?busca=SERVER").json()]
    assert titulos == ["Ler o código do Server"]


def test_busca_com_um_caractere_devolve_422(cliente):
    assert cliente.get("/tarefas?busca=a").status_code == 422


def test_filtrar_por_feita(cliente, tarefas_exemplo):
    cliente.patch("/tarefas/2", json={"feita": True})

    feitas = cliente.get("/tarefas?feita=true").json()
    pendentes = cliente.get("/tarefas?feita=false").json()

    assert [t["id"] for t in feitas] == [2]
    assert [t["id"] for t in pendentes] == [1, 3]


@pytest.mark.parametrize(
    ("query", "ids_esperados"),
    [
        ("limite=2", [1, 2]),
        ("pular=1", [2, 3]),
        ("pular=1&limite=1", [2]),
        ("pular=10", []),                 # pular além do fim: lista vazia
    ],
)
def test_paginacao(cliente, tarefas_exemplo, query, ids_esperados):
    ids = [t["id"] for t in cliente.get(f"/tarefas?{query}").json()]
    assert ids == ids_esperados


@pytest.mark.parametrize("query", ["limite=0", "limite=101", "pular=-1"])
def test_paginacao_fora_dos_limites_devolve_422(cliente, query):
    assert cliente.get(f"/tarefas?{query}").status_code == 422


# =====================================================================
# BUSCAR UMA (GET /tarefas/{id}) — Depends + 404
# =====================================================================
def test_buscar_tarefa_existente(cliente, tarefas_exemplo):
    resposta = cliente.get("/tarefas/1")
    assert resposta.status_code == 200
    assert resposta.json() == tarefas_exemplo[0]


def test_buscar_tarefa_inexistente_devolve_404_com_mensagem(cliente):
    resposta = cliente.get("/tarefas/999")
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "Tarefa 999 não encontrada"}


# =====================================================================
# ATUALIZAR (PATCH)
# =====================================================================
def test_patch_altera_so_os_campos_enviados(cliente, tarefas_exemplo):
    original = tarefas_exemplo[0]

    resposta = cliente.patch("/tarefas/1", json={"feita": True})

    assert resposta.status_code == 200
    atualizada = resposta.json()
    assert atualizada["feita"] is True
    # O exclude_unset=True garante que o resto NÃO virou None
    assert atualizada["titulo"] == original["titulo"]
    assert atualizada["prioridade"] == original["prioridade"]
    assert atualizada["criada_em"] == original["criada_em"]


def test_patch_fica_salvo(cliente, tarefas_exemplo):
    cliente.patch("/tarefas/1", json={"titulo": "Título novo"})
    assert cliente.get("/tarefas/1").json()["titulo"] == "Título novo"


def test_patch_com_dados_invalidos_devolve_422_e_nao_altera(cliente, tarefas_exemplo):
    resposta = cliente.patch("/tarefas/1", json={"prioridade": "urgente"})

    assert resposta.status_code == 422
    assert cliente.get("/tarefas/1").json()["prioridade"] == "alta"


def test_patch_em_tarefa_inexistente_devolve_404(cliente):
    assert cliente.patch("/tarefas/999", json={"feita": True}).status_code == 404


# =====================================================================
# APAGAR (DELETE) — header X-Token
# =====================================================================
@pytest.mark.parametrize(
    "headers",
    [{}, {"X-Token": "chute"}],
    ids=["sem-token", "token-errado"],
)
def test_apagar_sem_token_valido_devolve_401_e_nao_apaga(cliente, tarefas_exemplo, headers):
    resposta = cliente.delete("/tarefas/1", headers=headers)

    assert resposta.status_code == 401
    assert cliente.get("/tarefas/1").status_code == 200   # continua lá


def test_apagar_com_token_devolve_204_sem_corpo(cliente, tarefas_exemplo, headers_admin):
    resposta = cliente.delete("/tarefas/1", headers=headers_admin)

    assert resposta.status_code == 204
    assert resposta.content == b""
    assert cliente.get("/tarefas/1").status_code == 404


def test_apagar_tarefa_inexistente_devolve_404(cliente, headers_admin):
    assert cliente.delete("/tarefas/999", headers=headers_admin).status_code == 404


def test_header_do_token_nao_diferencia_maiusculas(cliente, tarefas_exemplo):
    # Nomes de headers HTTP não diferenciam maiúsculas de minúsculas
    resposta = cliente.delete("/tarefas/1", headers={"x-token": TOKEN_ADMIN})
    assert resposta.status_code == 204


# =====================================================================
# STATUS, DOCUMENTAÇÃO E ISOLAMENTO
# =====================================================================
def test_status_conta_as_tarefas(cliente, tarefas_exemplo):
    assert cliente.get("/status").json() == {"status": "ok", "total_tarefas": 3}


def test_documentacao_esta_disponivel(cliente):
    assert cliente.get("/docs").status_code == 200


def test_openapi_lista_todas_as_rotas(cliente):
    rotas = set(cliente.get("/openapi.json").json()["paths"])
    assert {"/", "/tarefas", "/tarefas/{tarefa_id}", "/status"} <= rotas


def test_cada_teste_comeca_com_o_banco_vazio(cliente):
    # Se a fixture "cliente" não limpasse o banco, as tarefas dos testes
    # anteriores apareceriam aqui. Este teste protege o próprio isolamento.
    assert cliente.get("/status").json()["total_tarefas"] == 0
