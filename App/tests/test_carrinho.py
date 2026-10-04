"""Testes de loja/carrinho.py (classe com estado).

As fixtures carrinho_vazio e carrinho_com_itens vêm do conftest.py.
"""

import pytest

from loja.carrinho import Carrinho
from loja.precos import FRETE_PADRAO


def test_carrinho_novo_esta_vazio(carrinho_vazio):
    assert carrinho_vazio.esta_vazio()
    assert carrinho_vazio.quantidade_itens() == 0
    assert carrinho_vazio.total() == 0.0


def test_adicionar_item(carrinho_vazio):
    carrinho_vazio.adicionar("livro", 40.0)
    assert not carrinho_vazio.esta_vazio()
    assert carrinho_vazio.quantidade_itens() == 1


def test_adicionar_mesmo_item_soma_quantidade(carrinho_vazio):
    carrinho_vazio.adicionar("livro", 40.0, quantidade=1)
    carrinho_vazio.adicionar("livro", 40.0, quantidade=2)
    assert carrinho_vazio.quantidade_itens() == 3
    assert carrinho_vazio.subtotal() == 120.0


@pytest.mark.parametrize("quantidade", [0, -1])
def test_adicionar_quantidade_invalida_da_erro(carrinho_vazio, quantidade):
    with pytest.raises(ValueError, match="quantidade"):
        carrinho_vazio.adicionar("livro", 40.0, quantidade=quantidade)


def test_remover_item(carrinho_com_itens):
    carrinho_com_itens.remover("caneta")
    assert carrinho_com_itens.quantidade_itens() == 2


def test_remover_item_inexistente_da_erro(carrinho_com_itens):
    with pytest.raises(KeyError):
        carrinho_com_itens.remover("borracha")


# Agrupando testes relacionados numa classe (opcional). O nome precisa
# começar com "Test" e a classe NÃO tem __init__.
class TestTotal:
    def test_subtotal(self, carrinho_com_itens):
        # 2 x 25.00 + 4 x 3.50 = 64.00
        assert carrinho_com_itens.subtotal() == 64.0

    def test_total_abaixo_do_limite_cobra_frete(self, carrinho_com_itens):
        assert carrinho_com_itens.total() == pytest.approx(64.0 + FRETE_PADRAO)

    def test_total_acima_do_limite_tem_frete_gratis(self, carrinho_vazio):
        carrinho_vazio.adicionar("monitor", 900.0)
        assert carrinho_vazio.total() == 900.0


# tmp_path: fixture PRONTA do pytest. Cria uma pasta temporária única
# para o teste e apaga depois. Perfeita para testar arquivos sem sujar
# o seu disco.
def test_salvar_e_carregar_mantem_os_itens(carrinho_com_itens, tmp_path):
    caminho = tmp_path / "carrinho.json"

    carrinho_com_itens.salvar(caminho)
    carregado = Carrinho.carregar(caminho)

    assert caminho.exists()
    assert carregado.subtotal() == carrinho_com_itens.subtotal()
    assert carregado.quantidade_itens() == carrinho_com_itens.quantidade_itens()
