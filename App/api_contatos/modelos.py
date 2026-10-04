"""Modelos Pydantic da API de contatos (exercícios 5 e 6)."""

from pydantic import BaseModel, Field, field_validator

from utilidades import eh_email_valido


def _validar_email(email: str | None) -> str | None:
    # Reaproveita a validação do pacote utilidades (material 11)!
    if email is not None and not eh_email_valido(email):
        raise ValueError("e-mail inválido")
    return email


class ContatoCriar(BaseModel):
    """O que o cliente ENVIA para criar um contato."""

    nome: str = Field(min_length=2, max_length=50, examples=["Ana Souza"])
    telefone: str = Field(min_length=8, max_length=20, examples=["11 91234-5678"])
    email: str | None = Field(default=None, examples=["ana@email.com"])

    # @field_validator: uma validação PRÓPRIA, além das do Field. Se
    # levantar ValueError, o FastAPI responde 422 com a mensagem.
    @field_validator("email")
    @classmethod
    def email_valido(cls, email: str | None) -> str | None:
        return _validar_email(email)


class ContatoAtualizar(BaseModel):
    """Para o PATCH (exercício 6): tudo opcional."""

    nome: str | None = Field(default=None, min_length=2, max_length=50)
    telefone: str | None = Field(default=None, min_length=8, max_length=20)
    email: str | None = None      # null aqui = apagar o e-mail (é opcional)

    @field_validator("email")
    @classmethod
    def email_valido(cls, email: str | None) -> str | None:
        return _validar_email(email)

    # "Opcional no PATCH" = pode não ser enviado, e NÃO "pode virar null".
    # Nome e telefone são obrigatórios no contato, então null é recusado.
    @field_validator("nome", "telefone")
    @classmethod
    def nao_aceitar_null(cls, valor: str | None) -> str:
        if valor is None:
            raise ValueError("não pode ser null (para não alterar, não envie o campo)")
        return valor


class Contato(ContatoCriar):
    """O que a API DEVOLVE: os dados + o id."""

    id: int
