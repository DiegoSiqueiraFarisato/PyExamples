"""Testes da API de contatos (exercício 8 do material 17_fastapi.py).

Rode a partir da pasta App:
    python -m pytest tests/test_api_contatos.py -v

A ideia principal: dependency_overrides.
A API grava os contatos num JSON. Nos testes, trocamos a dependência
obter_repositorio por uma que grava num arquivo dentro de tmp_path. Cada
teste começa com um "banco" vazio, e os seus contatos de verdade nunca
são tocados.
"""

import pytest

pytest.importorskip("fastapi", reason="instale com: python -m pip install \"fastapi[standard]\"")

from fastapi.testclient import TestClient  # noqa: E402

from api_contatos.armazenamento import RepositorioContatos  # noqa: E402
from api_contatos.dependencias import obter_repositorio  # noqa: E402
from api_contatos.main import app  # noqa: E402


# =====================================================================
# FIXTURES
# =====================================================================
@pytest.fixture
def arquivo_contatos(tmp_path):
    return tmp_path / "contatos.json"


@pytest.fixture
def cliente(arquivo_contatos):
    # Toda rota que pedir obter_repositorio vai receber ESTE repositório
    app.dependency_overrides[obter_repositorio] = lambda: RepositorioContatos(arquivo_contatos)
    yield TestClient(app)
    # Depois do "yield": limpeza, roda quando o teste termina (mesmo se falhar)
    app.dependency_overrides.clear()


@pytest.fixture
def contatos_exemplo(cliente) -> list[dict]:
    corpos = [
        {"nome": "Ana Souza", "telefone": "11 91111-1111", "email": "ana@email.com"},
        {"nome": "Bruno Lima", "telefone": "21 92222-2222"},
        {"nome": "Mariana Costa", "telefone": "31 93333-3333"},
    ]
    return [cliente.post("/contatos", json=corpo).json() for corpo in corpos]


# =====================================================================
# CRIAR (201 e 422)
# =====================================================================
def test_criar_contato_devolve_201_com_id(cliente):
    resposta = cliente.post("/contatos", json={"nome": "Ana", "telefone": "11 91234-5678"})

    assert resposta.status_code == 201
    assert resposta.json() == {"id": 1, "nome": "Ana", "telefone": "11 91234-5678", "email": None}


@pytest.mark.parametrize(
    ("corpo", "campo"),
    [
        ({"telefone": "11 91234-5678"}, "nome"),                       # sem nome
        ({"nome": "A", "telefone": "11 91234-5678"}, "nome"),          # nome curto
        ({"nome": "A" * 51, "telefone": "11 91234-5678"}, "nome"),     # nome longo
        ({"nome": "Ana"}, "telefone"),                                 # sem telefone
        ({"nome": "Ana", "telefone": "123"}, "telefone"),              # telefone curto
        ({"nome": "Ana", "telefone": "11 91234-5678", "email": "ana@"}, "email"),
    ],
    ids=["sem-nome", "nome-curto", "nome-longo", "sem-telefone", "telefone-curto", "email-invalido"],
)
def test_criar_contato_invalido_devolve_422(cliente, corpo, campo):
    resposta = cliente.post("/contatos", json=corpo)

    assert resposta.status_code == 422
    assert resposta.json()["detail"][0]["loc"] == ["body", campo]


# =====================================================================
# BUSCAR (200 e 404)
# =====================================================================
def test_buscar_contato_existente(cliente, contatos_exemplo):
    resposta = cliente.get("/contatos/2")
    assert resposta.status_code == 200
    assert resposta.json() == contatos_exemplo[1]


def test_buscar_contato_inexistente_devolve_404(cliente):
    resposta = cliente.get("/contatos/999")
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "Contato 999 não encontrado"}


# =====================================================================
# LISTAR, BUSCA E PAGINAÇÃO (exercício 7)
# =====================================================================
def test_listar_sem_contatos(cliente):
    assert cliente.get("/contatos").json() == []


@pytest.mark.parametrize(
    ("busca", "nomes"),
    [
        ("ana", ["Ana Souza", "Mariana Costa"]),   # "mariANA" também contém "ana"
        ("BRUNO", ["Bruno Lima"]),                 # sem diferenciar maiúsculas
        ("zé", []),
    ],
)
def test_busca_por_parte_do_nome(cliente, contatos_exemplo, busca, nomes):
    resposta = cliente.get("/contatos", params={"busca": busca})
    assert [c["nome"] for c in resposta.json()] == nomes


@pytest.mark.parametrize(
    ("params", "ids"),
    [
        ({"limite": 2}, [1, 2]),
        ({"pular": 2}, [3]),
        ({"pular": 1, "limite": 1}, [2]),
    ],
)
def test_paginacao(cliente, contatos_exemplo, params, ids):
    assert [c["id"] for c in cliente.get("/contatos", params=params).json()] == ids


# =====================================================================
# ATUALIZAR (PATCH)
# =====================================================================
def test_patch_altera_so_o_que_foi_enviado(cliente, contatos_exemplo):
    resposta = cliente.patch("/contatos/1", json={"telefone": "11 90000-0000"})

    assert resposta.status_code == 200
    assert resposta.json() == {**contatos_exemplo[0], "telefone": "11 90000-0000"}


def test_patch_com_email_null_apaga_o_email(cliente, contatos_exemplo):
    resposta = cliente.patch("/contatos/1", json={"email": None})
    assert resposta.json()["email"] is None


@pytest.mark.parametrize("corpo", [{"nome": None}, {"telefone": None}, {"email": "invalido"}])
def test_patch_invalido_devolve_422_e_nao_altera(cliente, contatos_exemplo, corpo):
    assert cliente.patch("/contatos/1", json=corpo).status_code == 422
    assert cliente.get("/contatos/1").json() == contatos_exemplo[0]


def test_patch_em_contato_inexistente_devolve_404(cliente):
    assert cliente.patch("/contatos/999", json={"nome": "Zé"}).status_code == 404


# =====================================================================
# REMOVER (204 e depois 404)
# =====================================================================
def test_remover_contato(cliente, contatos_exemplo):
    resposta = cliente.delete("/contatos/1")

    assert resposta.status_code == 204
    assert cliente.get("/contatos/1").status_code == 404
    assert len(cliente.get("/contatos").json()) == 2


def test_remover_contato_inexistente_devolve_404(cliente):
    assert cliente.delete("/contatos/999").status_code == 404


# =====================================================================
# PERSISTÊNCIA EM JSON (exercício 9)
# =====================================================================
def test_contatos_ficam_salvos_no_arquivo(cliente, contatos_exemplo, arquivo_contatos):
    assert arquivo_contatos.exists()
    # Um repositório NOVO lendo o mesmo arquivo = "o servidor reiniciou"
    nomes = [c.nome for c in RepositorioContatos(arquivo_contatos).listar()]
    assert nomes == ["Ana Souza", "Bruno Lima", "Mariana Costa"]


def test_ids_nao_sao_reaproveitados_apos_remocao(cliente, contatos_exemplo):
    cliente.delete("/contatos/3")              # apaga o ÚLTIMO
    novo = cliente.post("/contatos", json={"nome": "Novo", "telefone": "11 94444-4444"})
    assert novo.json()["id"] == 4              # e não 3


def test_arquivo_corrompido_comeca_vazio(cliente, arquivo_contatos):
    arquivo_contatos.write_text("{isto não é json", encoding="utf-8")
    assert cliente.get("/contatos").json() == []


def test_dependency_override_e_desfeito_depois_do_teste():
    # Se a fixture não limpasse os overrides, eles vazariam para outros testes
    assert obter_repositorio not in app.dependency_overrides
