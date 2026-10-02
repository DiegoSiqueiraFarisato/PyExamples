"""Funções de validação de textos.

Resposta do exercício 5 do material 11_modulos.py.
"""


def eh_email_valido(texto: str) -> bool:
    """Validação SIMPLES: exatamente um "@", algo antes dele e um "."
    depois dele (com algo antes e depois do ponto).

    Validar e-mail de verdade é bem mais complexo. Na prática, a única
    validação 100% confiável é enviar um e-mail de confirmação.
    """
    if texto.count("@") != 1 or " " in texto:
        return False
    usuario, dominio = texto.split("@")
    if not usuario:
        return False
    if "." not in dominio:
        return False
    # o domínio não pode começar nem terminar com "." (ex: "a@.com", "a@b.")
    return not dominio.startswith(".") and not dominio.endswith(".")


def eh_cpf_formatado(texto: str) -> bool:
    """Verifica só o FORMATO 000.000.000-00 (não valida os dígitos)."""
    if len(texto) != 14:
        return False
    for posicao, caractere in enumerate(texto):
        if posicao in (3, 7):
            if caractere != ".":
                return False
        elif posicao == 11:
            if caractere != "-":
                return False
        elif not caractere.isdigit():
            return False
    return True

# Mais pra frente, você vai aprender expressões regulares (módulo re),
# que resolvem isso em uma linha:
#   import re
#   re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", texto) is not None
