# Python Studies

Material de estudo de Python **do zero**, em português, escrito como arquivos `.py` executáveis. Cada arquivo explica os conceitos em comentários, mostra exemplos que rodam e termina com exercícios. Logo depois de cada material vem um arquivo com as respostas comentadas.

## Requisitos

- **Python 3.10 ou mais novo.** Os materiais usam type hints como `str | None` e `list[str]`. Foram testados no Python 3.13 e no 3.14.
- Os materiais 1 a 7 não usam nenhuma biblioteca externa. Só o exercício 10 de módulos usa `requests`, e ele é opcional.
- O material 8 (testes) usa o `pytest`: `python -m pip install pytest`.
- O material 9 (FastAPI) usa o FastAPI: `python -m pip install "fastapi[standard]"`.

## Como estudar

1. Siga os arquivos **na ordem numérica**.
2. Leia os comentários de cima para baixo e rode o arquivo:
   ```bash
   python 01_fundamentos_python.py
   ```
3. Compare o que aparece no terminal com o código. Mude valores, quebre o código e conserte.
4. Faça os exercícios do final de cada material **sem olhar as respostas**. Só depois compare com o arquivo de respostas.

> **Acentos estranhos no terminal do Windows?** No PowerShell, rode antes:
> `$env:PYTHONIOENCODING='utf-8'`

## Trilha de estudo

| # | Material | Respostas | Assuntos |
|---|----------|-----------|----------|
| 1 | [`01_fundamentos_python.py`](01_fundamentos_python.py) | [`02_respostas_exercicios.py`](02_respostas_exercicios.py) | `print`, variáveis, tipos, operadores, strings, f-strings, `input`, `if/elif/else`, listas, `for`, `while`, `break/continue`, naming conventions (PEP 8) |
| 2 | [`03_funcoes.py`](03_funcoes.py) | [`04_respostas_funcoes.py`](04_respostas_funcoes.py) | `def`, parâmetros, `return`, valores padrão, argumentos nomeados, `*args/**kwargs`, escopo, docstrings, type hints, `lambda`, recursão, `if __name__ == "__main__"` |
| 3 | [`05_dicionarios.py`](05_dicionarios.py) | [`06_respostas_dicionarios.py`](06_respostas_dicionarios.py) | criar, acessar (`[]` vs `get`), alterar, remover, percorrer, mesclar, aninhados, lista de dicts, dict comprehension, contar/agrupar, `Counter`, `defaultdict`, cópia vs referência, ordenação, JSON |
| 4 | [`07_tratamento_erros.py`](07_tratamento_erros.py) | [`08_respostas_erros.py`](08_respostas_erros.py) | traceback, exceções comuns, `try/except/else/finally`, `raise`, exceções próprias, validação de entrada, EAFP vs LBYL, hierarquia de exceções, más práticas |
| 5 | [`09_arquivos.py`](09_arquivos.py) | [`10_respostas_arquivos.py`](10_respostas_arquivos.py) | caminhos, `pathlib`, modos de `open`, `with`, ler/escrever/acrescentar, encoding, pastas, CSV, JSON, mini projeto de tarefas |
| 6 | [`11_modulos.py`](11_modulos.py) | [`12_respostas_modulos.py`](12_respostas_modulos.py) | formas de `import`, biblioteca padrão, módulos próprios, `__name__`, pacotes e `__init__.py`, `sys.path`, `pip`, `venv`, `requirements.txt` |
| 7 | [`13_classes.py`](13_classes.py) | [`14_respostas_classes.py`](14_respostas_classes.py) | classes e objetos, `__init__` e `self`, métodos, `__str__/__repr__`, atributos de classe, `@property`, `@classmethod/@staticmethod`, herança, polimorfismo, composição, métodos especiais, `@dataclass` |
| 8 | [`15_testes.py`](15_testes.py) | [`16_respostas_testes.py`](16_respostas_testes.py) e [`tests/test_respostas_exercicios.py`](tests/test_respostas_exercicios.py) | `assert`, `pytest`, como ler falhas, padrão AAA, `pytest.raises`, `pytest.approx`, `parametrize`, fixtures, `conftest.py`, `tmp_path`, código testável, o que testar, cobertura, TDD |
| 9 | [`17_fastapi.py`](17_fastapi.py) | [`18_respostas_fastapi.py`](18_respostas_fastapi.py), pacote [`api_contatos/`](api_contatos/) e [`tests/test_api_contatos.py`](tests/test_api_contatos.py) | APIs e HTTP, métodos e status codes, rotas, parâmetros de caminho e de query, Pydantic, `HTTPException`, CRUD, `Depends`, headers, `async`, documentação `/docs`, `TestClient`, `APIRouter`, organização de projetos |

## Pacotes de exemplo

Os materiais de módulos e de testes usam pastas que funcionam como pacotes de verdade:

```
meus_modulos/     exemplo usado em 11_modulos.py
  __init__.py
  calculos.py     teste com: python meus_modulos/calculos.py
  textos.py

utilidades/       respostas dos exercícios 5, 6 e 7 de módulos
  __init__.py
  conversoes.py   teste com: python utilidades/conversoes.py
  validacoes.py
  entrada.py      pedir_inteiro (exercício 10 de testes)

tarefas/          resposta do exercício 11 de módulos (lista de tarefas em JSON)
  __init__.py
  armazenamento.py
  operacoes.py
  main.py         rode com: python -m tarefas.main

loja/             código testado no material 15_testes.py
  __init__.py
  precos.py
  carrinho.py

api_contatos/     respostas dos exercícios 5 a 10 de FastAPI (API de contatos)
  main.py         rode com: python -m uvicorn api_contatos.main:app --reload
  modelos.py
  armazenamento.py
  dependencias.py
  rotas/
    contatos.py

tests/            testes (pytest)
  conftest.py
  test_precos.py
  test_carrinho.py
  test_respostas_exercicios.py   respostas dos exercícios de testes
  test_fastapi.py                testes da API do 17_fastapi.py
  test_api_contatos.py           testes da API de contatos (exercício 8 de FastAPI)
```

## Rodando os testes

Na pasta `App`, rode:

```bash
python -m pytest -v
```

O `pytest.ini` limita a busca à pasta `tests/`, para o `pytest` não misturar estes testes com os do `Server/`, que têm configuração própria.

## Arquivos gerados ao rodar

Alguns scripts criam arquivos de exemplo. Esses arquivos estão no `.gitignore` e podem ser apagados quando você quiser:

- `saida_09_arquivos/`: criada por `09_arquivos.py`, que apaga e recria a pasta a cada execução
- `saida_10_respostas/`: criada por `10_respostas_arquivos.py`. Ela é mantida entre execuções para mostrar o log crescendo e a agenda salva
- `tarefas/tarefas.json`: criado pelo menu `python -m tarefas.main`
- `api_contatos/contatos.json`: criado pela API de contatos quando ela roda com o `uvicorn`. Para gravar em outro lugar, use a variável de ambiente `CONTATOS_ARQUIVO`

## Rodando a API do material de FastAPI

O `17_fastapi.py` funciona de dois jeitos:

```bash
python 17_fastapi.py                       # mostra requisições e respostas no terminal
python -m uvicorn 17_fastapi:app --reload  # sobe o servidor de verdade
```

Com o servidor rodando, abra http://127.0.0.1:8000/docs para testar a API pelo navegador.

## Próximos passos

Assuntos sugeridos para continuar:

- Banco de dados com `sqlite3` (e trocar o JSON da API de contatos por um banco)
- Programação assíncrona (`async`/`await`), base para entender o broker do `Server/`
- Expressões regulares (`re`)
- Consumir APIs com `requests`
