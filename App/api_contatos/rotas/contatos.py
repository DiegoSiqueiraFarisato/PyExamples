"""Rotas de /contatos (exercícios 5, 6, 7 e 10).

As rotas são FINAS: recebem, chamam o repositório e devolvem. A regra
de como guardar os dados fica no armazenamento.py.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from api_contatos.dependencias import Repositorio, obter_contato_ou_404, paginacao
from api_contatos.modelos import Contato, ContatoAtualizar, ContatoCriar

# Exercício 10: um APIRouter é um "mini app". O main.py o inclui no app.
router = APIRouter(prefix="/contatos", tags=["contatos"])

ContatoExistente = Annotated[Contato, Depends(obter_contato_ou_404)]


# ---- Exercício 5 -----------------------------------------------------
@router.post("", response_model=Contato, status_code=status.HTTP_201_CREATED)
def criar_contato(dados: ContatoCriar, repositorio: Repositorio) -> Contato:
    return repositorio.criar(dados)


# ---- Exercícios 5 e 7 (busca e paginação) -----------------------------
@router.get("", response_model=list[Contato])
def listar_contatos(
    repositorio: Repositorio,
    pagina: Annotated[dict, Depends(paginacao)],
    busca: Annotated[str | None, Query(min_length=1)] = None,
) -> list[Contato]:
    contatos = repositorio.listar()
    if busca is not None:
        termo = busca.lower()
        contatos = [c for c in contatos if termo in c.nome.lower()]
    inicio = pagina["pular"]
    return contatos[inicio : inicio + pagina["limite"]]


# ---- Exercícios 5 e 6 (dependência obter_contato_ou_404) --------------
@router.get("/{contato_id}", response_model=Contato)
def buscar_contato(contato: ContatoExistente) -> Contato:
    return contato


# ---- Exercício 6 -----------------------------------------------------
@router.patch("/{contato_id}", response_model=Contato)
def atualizar_contato(
    alteracoes: ContatoAtualizar,
    contato: ContatoExistente,
    repositorio: Repositorio,
) -> Contato:
    mudancas = alteracoes.model_dump(exclude_unset=True)
    return repositorio.atualizar(contato.id, mudancas)


@router.delete("/{contato_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_contato(contato: ContatoExistente, repositorio: Repositorio) -> None:
    repositorio.remover(contato.id)
