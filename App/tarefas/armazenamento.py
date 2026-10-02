"""Leitura e gravação das tarefas em JSON.

Este módulo não sabe nada sobre "concluir" ou "listar" tarefas. Ele só
sabe salvar e carregar uma lista. Se um dia você trocar o JSON por um
banco de dados, só este arquivo muda.
"""

import json
from pathlib import Path

CAMINHO_PADRAO = Path(__file__).resolve().parent / "tarefas.json"


def carregar(caminho: Path = CAMINHO_PADRAO) -> list[dict]:
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar(tarefas: list[dict], caminho: Path = CAMINHO_PADRAO) -> None:
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, indent=2, ensure_ascii=False)
