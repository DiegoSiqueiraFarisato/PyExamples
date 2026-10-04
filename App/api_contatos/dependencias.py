"""Dependências usadas com Depends nas rotas (exercícios 6, 7 e 9)."""

from typing import Annotated

from fastapi import Depends, HTTPException, Query, status

from api_contatos.armazenamento import RepositorioContatos
from api_contatos.modelos import Contato


def obter_repositorio() -> RepositorioContatos:
    """Entrega o repositório às rotas.

    Por ser uma DEPENDÊNCIA, os testes podem trocá-la por um repositório
    que grava num arquivo temporário (app.dependency_overrides), sem
    mexer nos seus contatos de verdade. Veja tests/test_api_contatos.py.
    """
    return RepositorioContatos()


# Atalho para não repetir Annotated[..., Depends(...)] em toda rota
Repositorio = Annotated[RepositorioContatos, Depends(obter_repositorio)]


def obter_contato_ou_404(contato_id: int, repositorio: Repositorio) -> Contato:
    """Exercício 6: usada nas três rotas que recebem o id.

    Repare: uma dependência pode depender de OUTRA (do repositório).
    """
    contato = repositorio.obter(contato_id)
    if contato is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contato {contato_id} não encontrado",
        )
    return contato


def paginacao(
    pular: Annotated[int, Query(ge=0)] = 0,
    limite: Annotated[int, Query(ge=1, le=100)] = 10,
) -> dict:
    """Exercício 7."""
    return {"pular": pular, "limite": limite}
