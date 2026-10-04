"""Testes de loja/precos.py (funções puras).

Rode a partir da pasta App:
    python -m pytest -v
"""

import pytest

from loja.precos import (
    FRETE_PADRAO,
    VALOR_FRETE_GRATIS,
    aplicar_desconto,
    calcular_frete,
    formatar_preco,
)


# ---------------------------------------------------------------------
# Testes simples: uma função, um cenário, um assert
# ---------------------------------------------------------------------
def test_aplicar_desconto_de_10_por_cento():
    # Arrange (preparar)
    preco = 100.0
    # Act (agir)
    resultado = aplicar_desconto(preco, 10)
    # Assert (verificar)
    assert resultado == 90.0


def test_aplicar_desconto_zero_mantem_preco():
    assert aplicar_desconto(59.90, 0) == 59.90


def test_aplicar_desconto_de_100_por_cento_zera_preco():
    assert aplicar_desconto(59.90, 100) == 0.0


# ---------------------------------------------------------------------
# Testando ERROS: pytest.raises
# ---------------------------------------------------------------------
def test_aplicar_desconto_com_preco_negativo_da_erro():
    with pytest.raises(ValueError):
        aplicar_desconto(-10, 5)


def test_aplicar_desconto_acima_de_100_da_erro_com_mensagem_clara():
    # match= confere se a MENSAGEM do erro contém o texto
    with pytest.raises(ValueError, match="entre 0 e 100"):
        aplicar_desconto(100, 150)


# ---------------------------------------------------------------------
# Floats: pytest.approx
# ---------------------------------------------------------------------
def test_soma_de_floats_com_approx():
    # 0.1 + 0.2 == 0.3 é False no computador! approx tolera a diferença.
    assert 0.1 + 0.2 == pytest.approx(0.3)


# ---------------------------------------------------------------------
# PARAMETRIZE: o mesmo teste com vários casos
# ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("valor_compra", "frete_esperado"),
    [
        (0, FRETE_PADRAO),
        (199.99, FRETE_PADRAO),                 # logo ANTES do limite
        (VALOR_FRETE_GRATIS, 0.0),              # EXATAMENTE no limite
        (1000, 0.0),
    ],
)
def test_calcular_frete(valor_compra, frete_esperado):
    assert calcular_frete(valor_compra) == frete_esperado


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (0, "R$ 0,00"),
        (9.9, "R$ 9,90"),
        (1234.5, "R$ 1.234,50"),
        (1234567.891, "R$ 1.234.567,89"),
    ],
    ids=["zero", "centavos", "milhar", "milhao"],   # nomes legíveis no -v
)
def test_formatar_preco(valor, esperado):
    assert formatar_preco(valor) == esperado
