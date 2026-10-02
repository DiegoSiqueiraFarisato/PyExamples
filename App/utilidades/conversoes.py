"""Funções de conversão de unidades e moedas.

Resposta dos exercícios 5 e 6 do material 11_modulos.py.

Teste rodando diretamente:
    python utilidades/conversoes.py
"""

KM_POR_MILHA = 1.609344


def celsius_para_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32


def km_para_milhas(km: float) -> float:
    return km / KM_POR_MILHA


def reais_para_dolar(valor: float, cotacao: float) -> float:
    """Converte reais para dólares. cotacao = quantos reais vale 1 dólar."""
    if cotacao <= 0:
        raise ValueError(f"cotação deve ser positiva, recebi {cotacao}")
    return round(valor / cotacao, 2)


# EXERCÍCIO 6: testes com assert que SÓ rodam quando o arquivo é
# executado diretamente, e não quando é importado.
if __name__ == "__main__":
    assert celsius_para_fahrenheit(0) == 32
    assert celsius_para_fahrenheit(100) == 212
    assert round(km_para_milhas(1.609344), 6) == 1
    assert reais_para_dolar(550, 5.5) == 100
    try:
        reais_para_dolar(100, 0)
        assert False, "deveria ter dado ValueError"
    except ValueError:
        pass
    print("conversoes.py: todos os testes passaram!")
