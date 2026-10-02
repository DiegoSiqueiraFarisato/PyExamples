"""Módulo de exemplo com funções de texto.

Usado pelo material 11_modulos.py.
"""


def inverter(texto: str) -> str:
    return texto[::-1]


def eh_palindromo(texto: str) -> bool:
    normalizado = texto.lower().replace(" ", "")
    return normalizado == inverter(normalizado)


def contar_vogais(texto: str) -> int:
    return sum(1 for letra in texto.lower() if letra in "aeiouáéíóúâêôãõà")


def titulo(texto: str, largura: int = 40, caractere: str = "=") -> str:
    """Retorna o texto centralizado entre duas linhas de caracteres."""
    linha = caractere * largura
    return f"{linha}\n{texto.center(largura)}\n{linha}"
