"""Pacote de exemplo do material 11_modulos.py.

Uma PASTA com um arquivo __init__.py é um PACOTE: um conjunto de
módulos. Este __init__.py roda automaticamente na primeira vez que
alguém faz "import meus_modulos" (ou importa algo de dentro dele).

Ele pode ficar vazio. Aqui usamos para "expor" as funções mais usadas
direto no pacote, permitindo:
    from meus_modulos import somar
em vez de:
    from meus_modulos.calculos import somar
"""

# Import RELATIVO: o "." significa "deste mesmo pacote"
from .calculos import calcular_media, somar
from .textos import eh_palindromo

VERSAO = "1.0.0"
