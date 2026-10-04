"""Respostas dos exercícios 1 a 10 do material 15_testes.py.

Rode a partir da pasta App:
    python -m pytest tests/test_respostas_exercicios.py -v

Ou rode o 16_respostas_testes.py, que executa estes testes e explica
o exercício 11 (cobertura).
"""

import pytest

from loja.carrinho import Carrinho
from loja.precos import VALOR_FRETE_GRATIS, calcular_parcelas
from meus_modulos.calculos import calcular_media
from meus_modulos.textos import eh_palindromo
from tarefas import operacoes
from utilidades import celsius_para_fahrenheit, eh_email_valido, reais_para_dolar
from utilidades.entrada import pedir_inteiro


# =====================================================================
# EXERCÍCIO 1 — eh_palindromo: 3 testes simples
# =====================================================================
def test_eh_palindromo_com_palavra_palindromo():
    assert eh_palindromo("arara")


def test_eh_palindromo_com_palavra_que_nao_e():
    assert not eh_palindromo("python")


def test_eh_palindromo_ignora_espacos_e_maiusculas():
    assert eh_palindromo("Ame o Poema")

# Repare: "assert eh_palindromo(...)" já basta. Não precisa escrever
# "== True" (a PEP 8 até recomenda NÃO escrever).


# =====================================================================
# EXERCÍCIO 2 — celsius_para_fahrenheit com parametrize
# =====================================================================
@pytest.mark.parametrize(
    ("celsius", "fahrenheit"),
    [
        (0, 32),           # congelamento da água
        (100, 212),        # ebulição da água
        (37, 98.6),        # corpo humano
        (-40, -40),        # o ponto em que as duas escalas se encontram!
    ],
)
def test_celsius_para_fahrenheit(celsius, fahrenheit):
    # approx porque 37 * 9 / 5 + 32 dá 98.60000000000001
    assert celsius_para_fahrenheit(celsius) == pytest.approx(fahrenheit)


# =====================================================================
# EXERCÍCIO 3 — eh_email_valido: válidos e inválidos
# =====================================================================
@pytest.mark.parametrize(
    ("email", "esperado"),
    [
        # válidos
        ("ana@email.com", True),
        ("joao.silva@empresa.com.br", True),
        ("a@b.co", True),
        ("dev+teste@gmail.com", True),
        # inválidos
        ("anaemail.com", False),          # sem @
        ("ana@email", False),             # sem ponto no domínio
        ("@email.com", False),            # nada antes do @
        ("ana@@email.com", False),        # dois @
        ("ana silva@email.com", False),   # espaço
        ("ana@.com", False),              # domínio começa com ponto
    ],
)
def test_eh_email_valido(email, esperado):
    assert eh_email_valido(email) is esperado


# Alternativa: separar em dois testes, um só de válidos e outro só de
# inválidos, cada um com uma lista de e-mails. Fica com um parâmetro a
# menos, e o nome do teste já diz o que se espera.


# =====================================================================
# EXERCÍCIO 4 — reais_para_dolar: ValueError com match=
# =====================================================================
@pytest.mark.parametrize("cotacao_invalida", [0, -5.5])
def test_reais_para_dolar_com_cotacao_invalida_da_erro(cotacao_invalida):
    with pytest.raises(ValueError, match="cotação deve ser positiva"):
        reais_para_dolar(100, cotacao_invalida)


def test_reais_para_dolar_caso_normal():
    assert reais_para_dolar(550, 5.5) == 100


# =====================================================================
# EXERCÍCIO 5 — calcular_media: normal, um número e lista vazia
# =====================================================================
def test_calcular_media_caso_normal():
    assert calcular_media([6, 7, 8]) == 7


def test_calcular_media_com_um_numero():
    assert calcular_media([9.5]) == 9.5


def test_calcular_media_com_lista_vazia_da_erro():
    with pytest.raises(ValueError, match="vazia"):
        calcular_media([])


# =====================================================================
# EXERCÍCIO 6 — pacote tarefas com fixture + tmp_path
# =====================================================================
@pytest.fixture
def lista_tarefas_temporaria(tmp_path):
    """Caminho de um JSON numa pasta temporária, com 2 tarefas."""
    caminho = tmp_path / "tarefas.json"
    operacoes.adicionar("Estudar testes", caminho)
    operacoes.adicionar("Fazer exercícios", caminho)
    return caminho

# Uma fixture pode usar OUTRA fixture (aqui, a tmp_path do pytest)
# simplesmente pedindo ela como parâmetro.


def test_adicionar_tarefa(lista_tarefas_temporaria):
    operacoes.adicionar("Revisar", lista_tarefas_temporaria)
    assert operacoes.listar(lista_tarefas_temporaria)[-1] == "3. [ ] Revisar"


def test_concluir_tarefa(lista_tarefas_temporaria):
    assert operacoes.concluir(1, lista_tarefas_temporaria) is True
    assert operacoes.listar(lista_tarefas_temporaria)[0] == "1. [x] Estudar testes"


def test_concluir_tarefa_inexistente_retorna_false(lista_tarefas_temporaria):
    assert operacoes.concluir(99, lista_tarefas_temporaria) is False


def test_remover_tarefa(lista_tarefas_temporaria):
    operacoes.remover(1, lista_tarefas_temporaria)
    assert operacoes.listar(lista_tarefas_temporaria) == ["1. [ ] Fazer exercícios"]


def test_adicionar_titulo_vazio_da_erro(lista_tarefas_temporaria):
    with pytest.raises(ValueError, match="vazio"):
        operacoes.adicionar("   ", lista_tarefas_temporaria)


def test_arquivo_inexistente_lista_vazia(tmp_path):
    # Teste extra: o caso "primeira execução", sem arquivo nenhum
    assert operacoes.listar(tmp_path / "nao_existe.json") == []


# =====================================================================
# EXERCÍCIO 7 — Carrinho: preço negativo e limite exato do frete
# =====================================================================
# carrinho_vazio vem do tests/conftest.py (sem import!)
def test_adicionar_preco_negativo_da_erro(carrinho_vazio):
    with pytest.raises(ValueError, match="preço"):
        carrinho_vazio.adicionar("produto bugado", -10.0)


def test_total_exatamente_no_limite_tem_frete_gratis(carrinho_vazio):
    carrinho_vazio.adicionar("fone", VALOR_FRETE_GRATIS)
    # No limite EXATO, o frete é grátis (>=). Se alguém trocar >= por >
    # em calcular_frete, este teste pega o bug.
    assert carrinho_vazio.total() == VALOR_FRETE_GRATIS


def test_total_um_centavo_abaixo_do_limite_cobra_frete(carrinho_vazio):
    carrinho_vazio.adicionar("fone", VALOR_FRETE_GRATIS - 0.01)
    assert carrinho_vazio.total() > VALOR_FRETE_GRATIS


# =====================================================================
# EXERCÍCIO 8 — TDD: calcular_parcelas
# =====================================================================
# COMO FOI FEITO (o ciclo do TDD):
#   1. VERMELHO: estes testes foram escritos PRIMEIRO. Rodando, todos
#      falharam com ImportError (calcular_parcelas não existia).
#   2. VERDE: a função foi criada em loja/precos.py, com o mínimo para
#      os testes passarem.
#   3. REFATORE: o número 12 virou a constante MAXIMO_PARCELAS, e os
#      testes garantiram que nada quebrou.
@pytest.mark.parametrize(
    ("valor", "vezes", "parcela"),
    [
        (100, 1, 100.0),       # à vista
        (100, 4, 25.0),
        (100, 3, 33.33),       # arredondamento
        (1200, 12, 100.0),     # máximo de parcelas
    ],
)
def test_calcular_parcelas(valor, vezes, parcela):
    assert calcular_parcelas(valor, vezes) == parcela


@pytest.mark.parametrize("vezes_invalidas", [0, 13, -1])
def test_calcular_parcelas_fora_do_intervalo_da_erro(vezes_invalidas):
    with pytest.raises(ValueError, match="de 1 a 12"):
        calcular_parcelas(100, vezes_invalidas)

# Reflexão do passo "refatore": 3 x 33.33 = 99.99, e some 1 centavo!
# Em sistemas reais, a diferença vai para a 1ª parcela (33.34). Seria um
# ótimo próximo ciclo de TDD: escreva o teste para isso primeiro.


# =====================================================================
# EXERCÍCIO 9 — capsys: testando o que foi impresso
# =====================================================================
def saudar(nome: str) -> None:
    # Função do enunciado. Definida aqui só para o exercício. Num
    # projeto real, ela estaria num módulo e seria importada.
    print(f"Olá, {nome}!")


def test_saudacao(capsys):
    saudar("Ana")
    assert capsys.readouterr().out == "Olá, Ana!\n"


# readouterr() devolve o que foi impresso DESDE a última leitura, então
# dá para conferir em etapas:
def test_saudacao_duas_vezes(capsys):
    saudar("Ana")
    assert capsys.readouterr().out == "Olá, Ana!\n"
    saudar("Bruno")
    assert capsys.readouterr().out == "Olá, Bruno!\n"


# =====================================================================
# EXERCÍCIO 10 (Desafio) — monkeypatch: simulando o input()
# =====================================================================
def test_pedir_inteiro_com_entrada_valida(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _mensagem: "42")
    assert pedir_inteiro("Número: ") == 42


def test_pedir_inteiro_tenta_de_novo_apos_entrada_invalida(monkeypatch, capsys):
    # iter() cria um "fornecedor" de respostas: cada next() pega a próxima
    respostas = iter(["abc", "", "7"])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(respostas))

    resultado = pedir_inteiro("Número: ")

    assert resultado == 7
    # As 2 entradas inválidas geraram 2 avisos
    assert capsys.readouterr().out.count("Valor inválido") == 2

# O monkeypatch desfaz a troca sozinho no fim do teste: o input() de
# verdade volta a funcionar nos outros testes.
