"""Classe Carrinho de compras.

Testado por tests/test_carrinho.py.
"""

import json
from pathlib import Path

from loja.precos import calcular_frete


class Carrinho:
    def __init__(self):
        self._itens: dict[str, dict] = {}     # {nome: {"preco": x, "quantidade": y}}

    def adicionar(self, nome: str, preco: float, quantidade: int = 1) -> None:
        if quantidade <= 0:
            raise ValueError("a quantidade deve ser positiva")
        if preco < 0:
            raise ValueError("o preço não pode ser negativo")
        if nome in self._itens:
            self._itens[nome]["quantidade"] += quantidade
        else:
            self._itens[nome] = {"preco": preco, "quantidade": quantidade}

    def remover(self, nome: str) -> None:
        if nome not in self._itens:
            raise KeyError(f"'{nome}' não está no carrinho")
        del self._itens[nome]

    def subtotal(self) -> float:
        return round(sum(item["preco"] * item["quantidade"] for item in self._itens.values()), 2)

    def total(self) -> float:
        """Subtotal + frete (o frete só é cobrado se houver itens)."""
        if self.esta_vazio():
            return 0.0
        return round(self.subtotal() + calcular_frete(self.subtotal()), 2)

    def quantidade_itens(self) -> int:
        return sum(item["quantidade"] for item in self._itens.values())

    def esta_vazio(self) -> bool:
        return not self._itens

    def salvar(self, caminho: Path) -> None:
        caminho.write_text(json.dumps(self._itens, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def carregar(cls, caminho: Path) -> "Carrinho":
        carrinho = cls()
        carrinho._itens = json.loads(caminho.read_text(encoding="utf-8"))
        return carrinho
