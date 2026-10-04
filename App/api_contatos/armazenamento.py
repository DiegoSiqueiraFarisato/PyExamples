"""Leitura e gravação dos contatos em JSON (exercício 9).

Formato do arquivo:
    {
      "proximo_id": 3,
      "contatos": [{"id": 1, "nome": "...", ...}, ...]
    }

Por que guardar "proximo_id" em vez de calcular "maior id + 1"?
Porque, se o último contato for apagado, "maior id + 1" REUTILIZARIA o
id dele. Um cliente que guardou o id antigo passaria a acessar OUTRO
contato. Ids não devem ser reaproveitados.
"""

import json
import os
from pathlib import Path

from api_contatos.modelos import Contato, ContatoCriar

# O caminho pode ser trocado pela variável de ambiente CONTATOS_ARQUIVO
# (material 11: configurações fora do código).
CAMINHO_PADRAO = Path(
    os.environ.get("CONTATOS_ARQUIVO", Path(__file__).resolve().parent / "contatos.json")
)


class RepositorioContatos:
    """Guarda os contatos num arquivo JSON.

    "Repositório" é o nome comum para a classe que esconde COMO os dados
    são guardados. As rotas só chamam listar/obter/criar..., e não sabem
    que existe um JSON. Trocar por um banco de dados mudaria só esta
    classe.
    """

    def __init__(self, caminho: Path = CAMINHO_PADRAO):
        self.caminho = Path(caminho)

    # ---- leitura e gravação do arquivo (uso interno) --------------------
    def _carregar(self) -> dict:
        try:
            return json.loads(self.caminho.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return {"proximo_id": 1, "contatos": []}

    def _salvar(self, dados: dict) -> None:
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self.caminho.write_text(json.dumps(dados, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---- operações usadas pelas rotas ------------------------------------
    def listar(self) -> list[Contato]:
        return [Contato(**item) for item in self._carregar()["contatos"]]

    def obter(self, contato_id: int) -> Contato | None:
        for contato in self.listar():
            if contato.id == contato_id:
                return contato
        return None

    def criar(self, dados: ContatoCriar) -> Contato:
        banco = self._carregar()
        contato = Contato(id=banco["proximo_id"], **dados.model_dump())
        banco["contatos"].append(contato.model_dump())
        banco["proximo_id"] += 1
        self._salvar(banco)
        return contato

    def atualizar(self, contato_id: int, mudancas: dict) -> Contato | None:
        banco = self._carregar()
        for posicao, item in enumerate(banco["contatos"]):
            if item["id"] == contato_id:
                atualizado = Contato(**{**item, **mudancas})
                banco["contatos"][posicao] = atualizado.model_dump()
                self._salvar(banco)
                return atualizado
        return None

    def remover(self, contato_id: int) -> bool:
        banco = self._carregar()
        restantes = [item for item in banco["contatos"] if item["id"] != contato_id]
        if len(restantes) == len(banco["contatos"]):
            return False
        banco["contatos"] = restantes
        self._salvar(banco)
        return True
