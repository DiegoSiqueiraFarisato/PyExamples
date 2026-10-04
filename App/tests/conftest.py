"""conftest.py: fixtures COMPARTILHADAS por todos os arquivos de teste.

O pytest carrega este arquivo automaticamente. Não precisa importar!
Qualquer teste em tests/ pode pedir estas fixtures pelo nome do
parâmetro.
"""

import pytest

from loja.carrinho import Carrinho


@pytest.fixture
def carrinho_vazio() -> Carrinho:
    return Carrinho()


@pytest.fixture
def carrinho_com_itens() -> Carrinho:
    # Cada teste que pedir esta fixture recebe um carrinho NOVO.
    # Um teste nunca "suja" o carrinho do outro.
    carrinho = Carrinho()
    carrinho.adicionar("caderno", 25.00, quantidade=2)
    carrinho.adicionar("caneta", 3.50, quantidade=4)
    return carrinho
