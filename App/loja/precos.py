"""Regras de preço da loja: desconto, frete e formatação.

Testado por tests/test_precos.py.
"""

FRETE_PADRAO = 19.90
VALOR_FRETE_GRATIS = 200.00
MAXIMO_PARCELAS = 12


def aplicar_desconto(preco: float, percentual: float) -> float:
    """Aplica um desconto percentual (0 a 100) e arredonda em 2 casas."""
    if preco < 0:
        raise ValueError(f"preço não pode ser negativo: {preco}")
    if not 0 <= percentual <= 100:
        raise ValueError(f"percentual deve estar entre 0 e 100: {percentual}")
    return round(preco * (1 - percentual / 100), 2)


def calcular_frete(valor_compra: float) -> float:
    """Frete grátis a partir de VALOR_FRETE_GRATIS, senão FRETE_PADRAO."""
    if valor_compra >= VALOR_FRETE_GRATIS:
        return 0.0
    return FRETE_PADRAO


def calcular_parcelas(valor: float, vezes: int) -> float:
    """Valor de cada parcela, arredondado em 2 casas (1 a 12 vezes).

    Criada com TDD no exercício 8 do material 15_testes.py: os testes
    (tests/test_respostas_exercicios.py) foram escritos ANTES.
    """
    if not 1 <= vezes <= MAXIMO_PARCELAS:
        raise ValueError(f"parcelas devem ser de 1 a {MAXIMO_PARCELAS}: {vezes}")
    return round(valor / vezes, 2)


def formatar_preco(valor: float) -> str:
    """Formata no padrão brasileiro: 1234.5 -> 'R$ 1.234,50'."""
    # Formata no padrão americano (1,234.50) e troca os separadores.
    # O "X" é um marcador temporário para a troca não se embolar.
    americano = f"{valor:,.2f}"
    brasileiro = americano.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {brasileiro}"
