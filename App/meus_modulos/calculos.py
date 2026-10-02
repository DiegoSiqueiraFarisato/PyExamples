"""Módulo de exemplo com funções de cálculo.

Usado pelo material 11_modulos.py. Este arquivo é um MÓDULO: qualquer
arquivo .py pode ser importado por outro arquivo .py.

Experimente rodar este arquivo diretamente:
    python meus_modulos/calculos.py
e compare com o que acontece quando ele é importado pelo 11_modulos.py.
"""

# Constante do módulo: quem importar pode usar calculos.TAXA_PADRAO
TAXA_PADRAO = 0.1


def somar(a: float, b: float) -> float:
    return a + b


def calcular_media(numeros: list[float]) -> float:
    if not numeros:
        raise ValueError("a lista de números está vazia")
    return sum(numeros) / len(numeros)


def aplicar_taxa(valor: float, taxa: float = TAXA_PADRAO) -> float:
    return round(valor * (1 + taxa), 2)


def _arredondar_interno(valor: float) -> float:
    """O "_" no início avisa: uso INTERNO do módulo, não importe de fora."""
    return round(valor, 2)


# Este bloco SÓ roda quando o arquivo é executado diretamente
# (python meus_modulos/calculos.py), e NÃO quando é importado.
# É o lugar ideal para testes rápidos do próprio módulo.
if __name__ == "__main__":
    print("calculos.py rodando DIRETAMENTE. __name__ =", repr(__name__))
    print("somar(2, 3) =", somar(2, 3))
    print("calcular_media([7, 8, 9]) =", calcular_media([7, 8, 9]))
    print("aplicar_taxa(100) =", aplicar_taxa(100))
