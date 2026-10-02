"""Regras da lista de tarefas: adicionar, concluir, remover e listar.

As funções recebem e devolvem DADOS (não usam input nem print). Assim
dá para usá-las num menu de terminal, numa interface gráfica ou num
site, sem mudar nada aqui.
"""

from pathlib import Path

from tarefas import armazenamento


def adicionar(titulo: str, caminho: Path = armazenamento.CAMINHO_PADRAO) -> None:
    titulo = titulo.strip()
    if not titulo:
        raise ValueError("o título da tarefa não pode ser vazio")
    tarefas = armazenamento.carregar(caminho)
    tarefas.append({"titulo": titulo, "feita": False})
    armazenamento.salvar(tarefas, caminho)


def concluir(numero: int, caminho: Path = armazenamento.CAMINHO_PADRAO) -> bool:
    """Marca como feita a tarefa de número `numero` (começando em 1)."""
    tarefas = armazenamento.carregar(caminho)
    if not 1 <= numero <= len(tarefas):
        return False
    tarefas[numero - 1]["feita"] = True
    armazenamento.salvar(tarefas, caminho)
    return True


def remover(numero: int, caminho: Path = armazenamento.CAMINHO_PADRAO) -> bool:
    tarefas = armazenamento.carregar(caminho)
    if not 1 <= numero <= len(tarefas):
        return False
    tarefas.pop(numero - 1)
    armazenamento.salvar(tarefas, caminho)
    return True


def listar(caminho: Path = armazenamento.CAMINHO_PADRAO) -> list[str]:
    """Devolve as linhas já formatadas, ex: '1. [x] Estudar'."""
    linhas = []
    for numero, tarefa in enumerate(armazenamento.carregar(caminho), start=1):
        marcador = "x" if tarefa["feita"] else " "
        linhas.append(f"{numero}. [{marcador}] {tarefa['titulo']}")
    return linhas
