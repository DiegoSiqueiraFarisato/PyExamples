"""
=====================================================================
  RESPOSTAS DOS EXERCÍCIOS — 17_fastapi.py
=====================================================================

COMO USAR ESTE ARQUIVO:
  Tente resolver SOZINHO antes de olhar! Depois compare com a resposta.

ONDE ESTÁ CADA RESPOSTA:
  Exercícios 1 a 4   -> neste arquivo (rotas simples)
  Exercícios 5 a 10  -> no pacote api_contatos/ (o exercício 10 pede
                        para reorganizar a API de contatos num pacote,
                        então a resposta final dos exercícios 5 a 9 já
                        está nessa forma). Cada arquivo diz qual
                        exercício responde.
  Exercício 8        -> tests/test_api_contatos.py
  Exercício 11       -> no final deste arquivo (o fluxo do Server/)

ESTE ARQUIVO TEM DOIS MODOS (como o material):
  python 18_respostas_fastapi.py                       -> demonstração
  python -m uvicorn 18_respostas_fastapi:app --reload  -> servidor
  E a API de contatos:
  python -m uvicorn api_contatos.main:app --reload
"""

from typing import Annotated

try:
    from fastapi import FastAPI, Query
except ImportError:
    print("O FastAPI não está instalado neste Python. Instale com:")
    print('  python -m pip install "fastapi[standard]"')
    raise SystemExit(1)

from utilidades import celsius_para_fahrenheit

app = FastAPI(title="Respostas dos exercícios 1 a 4")


# =====================================================================
# EXERCÍCIO 1 — GET /ola
# =====================================================================
@app.get("/ola")
def ola() -> dict:
    return {"mensagem": "Olá, mundo!"}


# =====================================================================
# EXERCÍCIO 2 — GET /par-ou-impar/{numero}
# =====================================================================
# Repare na URL em kebab-case (par-ou-impar) e na função em snake_case.
@app.get("/par-ou-impar/{numero}")
def par_ou_impar(numero: int) -> dict:
    return {"numero": numero, "resultado": "par" if numero % 2 == 0 else "ímpar"}

# E /par-ou-impar/x? Como "numero: int", o FastAPI tenta converter "x"
# para int, não consegue e responde 422 SOZINHO, sem chamar a função.


# =====================================================================
# EXERCÍCIO 3 — GET /conversor/temperatura?celsius=25
# =====================================================================
ZERO_ABSOLUTO = -273.15


@app.get("/conversor/temperatura")
def converter_temperatura(
    celsius: Annotated[float, Query(ge=ZERO_ABSOLUTO, description="Temperatura em °C")],
) -> dict:
    return {
        "celsius": celsius,
        "fahrenheit": round(celsius_para_fahrenheit(celsius), 2),  # pacote utilidades!
        "kelvin": round(celsius - ZERO_ABSOLUTO, 2),
    }

# Bônus: Query(ge=-273.15) recusa temperaturas abaixo do zero absoluto.
# O enunciado não pedia, mas é o tipo de validação que vale a pena ter.


# =====================================================================
# EXERCÍCIO 4 — GET /imc?peso=70&altura=1.75
# =====================================================================
def classificar_imc(imc: float) -> str:
    # Função PURA, separada da rota: dá para testar sem HTTP (material 15)
    if imc < 18.5:
        return "Abaixo do peso"
    if imc < 25:
        return "Peso normal"
    if imc < 30:
        return "Sobrepeso"
    return "Obesidade"


@app.get("/imc")
def calcular_imc(
    peso: Annotated[float, Query(gt=0, description="Peso em kg")],
    altura: Annotated[float, Query(gt=0, description="Altura em metros")],
) -> dict:
    imc = round(peso / altura ** 2, 2)
    return {"imc": imc, "classificacao": classificar_imc(imc)}

# gt = "greater than" (maior que). Peso 0 ou negativo -> 422 automático.
# Sem o gt=0, altura=0 daria ZeroDivisionError -> erro 500 (bug!).


# =====================================================================
# EXERCÍCIOS 5 a 10 — pacote api_contatos/
# =====================================================================
# Leia na ordem:
#   api_contatos/modelos.py        ex. 5 e 6: ContatoCriar, ContatoAtualizar,
#                                  Contato. Valida o e-mail reaproveitando
#                                  utilidades.eh_email_valido (material 11)
#   api_contatos/armazenamento.py  ex. 9: classe RepositorioContatos, que
#                                  salva em JSON. Guarda "proximo_id" para
#                                  ids nunca serem reaproveitados
#   api_contatos/dependencias.py   ex. 6 e 7: obter_repositorio,
#                                  obter_contato_ou_404 e paginacao
#   api_contatos/rotas/contatos.py ex. 5, 6, 7 e 10: as rotas num APIRouter
#   api_contatos/main.py           ex. 10: cria o app e inclui o router
#   tests/test_api_contatos.py     ex. 8: 28 testes
#
# DESTAQUES:
#   - Exercício 8: a fixture usa app.dependency_overrides para trocar o
#     repositório por um que grava em tmp_path. O banco começa vazio a
#     cada teste, e o seu contatos.json de verdade nunca é tocado.
#   - Exercício 6: o PATCH recusa {"nome": null}. "Opcional no PATCH"
#     quer dizer "pode não ser enviado", e não "pode virar null". (Este
#     cuidado também foi adicionado ao material 17, no TarefaAtualizar.)
#   - Exercício 9: o arquivo corrompido não derruba a API: ela começa
#     vazia (try/except do material 07).


# =====================================================================
# EXERCÍCIO 11 (Desafio) — o caminho de um POST /orders no Server/
# =====================================================================
# Arquivos envolvidos (em Server/app/):
#   main.py                      -> monta tudo no "lifespan"
#   services/orders_service.py   -> rotas /orders e reação ao envio
#   services/shipping_service.py -> "despacha" pedidos
#   broker/memory.py (ou redis_broker.py) -> entrega as mensagens
#
# ANTES DE TUDO: quando o servidor sobe (lifespan, em main.py)
#   1. create_broker() cria o broker (memória ou Redis, conforme o
#      config.env) e o guarda em app.state.broker.
#   2. Para cada arquivo *_service.py em app/services/, o main.py:
#      - inclui o "router" dele no app (como o nosso include_router!)
#      - chama register(broker), se existir. É aí que cada serviço diz
#        quais mensagens quer receber:
#          shipping assina "order.created"
#          orders   assina "order.shipped"
#   3. broker.start() liga os "workers": tarefas assíncronas que ficam
#      esperando mensagens, uma por assinatura.
#
# O PEDIDO: POST /orders {"item": "livro", "quantity": 2}
#   1. O FastAPI valida o corpo com o modelo OrderIn (quantity > 0, senão
#      422). Igual ao nosso TarefaCriar!
#   2. Depends(get_broker) (core/deps.py) entrega o broker à rota, lendo
#      request.app.state.broker. Igual ao nosso obter_repositorio.
#   3. create_order salva o pedido num dict em memória com status
#      "created", PUBLICA a mensagem "order.created" no broker e
#      responde 201 NA HORA, sem esperar o envio.
#   4. O broker coloca a mensagem na fila de quem assinou
#      "order.created": o shipping_service.
#   5. O worker do shipping chama _on_order_created: registra o id em
#      _shipped e PUBLICA "order.shipped".
#   6. O worker do orders recebe "order.shipped" e _on_shipped muda o
#      status do pedido para "shipped".
#   7. Um GET /orders/1 logo depois mostra "shipped".
#
# COM MINHAS PALAVRAS: a rota não chama o serviço de envio diretamente.
# Ela só AVISA ("um pedido foi criado") e segue a vida. Quem se
# interessa pelo aviso reage no seu tempo. Isso é arquitetura ORIENTADA
# A EVENTOS: os serviços não se conhecem, só conhecem as mensagens. Dá
# para adicionar um serviço de e-mail que também escuta "order.created"
# sem mexer no orders_service.
#
# Detalhes que o broker cuida por você (broker/base.py, _deliver):
#   - se um handler falhar, tenta de novo (até BROKER_MAX_RETRIES vezes,
#     esperando um pouco mais a cada tentativa)
#   - se falhar sempre, a mensagem vai para a "dead letter" (uma lista
#     de mensagens que não puderam ser processadas, para análise)
#   - com Redis, as mensagens sobrevivem a reinícios e vários servidores
#     dividem o trabalho
#
# Por isso os testes do Server usam wait_until(...) (tests/conftest.py):
# a mudança para "shipped" acontece DEPOIS da resposta, em segundo plano.
#
# Para rodar os testes do Server (veja Server/CLAUDE.md), da pasta Server:
#   .\.venv\Scripts\python.exe -m pytest -q


# =====================================================================
# DEMONSTRAÇÃO (só no modo: python 18_respostas_fastapi.py)
# =====================================================================
def demonstrar() -> None:
    import tempfile
    import warnings
    from pathlib import Path

    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    def chamar(cliente: TestClient, metodo: str, url: str, **opcoes):
        resposta = cliente.request(metodo, url, **opcoes)
        extra = f"  corpo={opcoes['json']}" if "json" in opcoes else ""
        if not resposta.content:
            corpo = "(sem corpo)"
        elif resposta.status_code == 422:
            corpo = [f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in resposta.json()["detail"]]
        else:
            corpo = resposta.json()
        print(f"→ {metodo} {url}{extra}")
        print(f"← {resposta.status_code} {corpo}\n")

    def secao(titulo: str) -> None:
        print("=" * 60)
        print(titulo)
        print("=" * 60)

    cliente = TestClient(app)
    secao("EXERCÍCIOS 1 a 4")
    chamar(cliente, "GET", "/ola")
    chamar(cliente, "GET", "/par-ou-impar/7")
    chamar(cliente, "GET", "/par-ou-impar/10")
    chamar(cliente, "GET", "/par-ou-impar/x")
    chamar(cliente, "GET", "/conversor/temperatura?celsius=25")
    chamar(cliente, "GET", "/conversor/temperatura?celsius=-300")
    chamar(cliente, "GET", "/imc?peso=70&altura=1.75")
    chamar(cliente, "GET", "/imc?peso=70&altura=0")

    # A API de contatos, gravando num arquivo TEMPORÁRIO (mesma técnica
    # dos testes) para a demonstração não criar contatos de verdade.
    from api_contatos.armazenamento import RepositorioContatos
    from api_contatos.dependencias import obter_repositorio
    from api_contatos.main import app as app_contatos

    with tempfile.TemporaryDirectory() as pasta:
        arquivo = Path(pasta) / "contatos.json"
        app_contatos.dependency_overrides[obter_repositorio] = lambda: RepositorioContatos(arquivo)
        cliente = TestClient(app_contatos)

        secao("EXERCÍCIOS 5 a 7 e 9 — API de contatos (api_contatos/)")
        chamar(cliente, "POST", "/contatos", json={"nome": "Ana Souza", "telefone": "11 91111-1111", "email": "ana@email.com"})
        chamar(cliente, "POST", "/contatos", json={"nome": "Mariana Costa", "telefone": "31 93333-3333"})
        chamar(cliente, "POST", "/contatos", json={"nome": "Bruno", "telefone": "21 92222-2222", "email": "bruno@"})
        chamar(cliente, "GET", "/contatos?busca=ana")
        chamar(cliente, "PATCH", "/contatos/2", json={"email": "mari@email.com"})
        chamar(cliente, "PATCH", "/contatos/2", json={"nome": None})
        chamar(cliente, "DELETE", "/contatos/1")
        chamar(cliente, "GET", "/contatos/1")

        print("Conteúdo do JSON salvo (exercício 9):")
        print(arquivo.read_text(encoding="utf-8"))

        app_contatos.dependency_overrides.clear()

    print()
    print("=" * 60)
    print("FIM DAS RESPOSTAS! Rode também os testes do exercício 8:")
    print("  python -m pytest tests/test_api_contatos.py -v")
    print("=" * 60)


if __name__ == "__main__":
    demonstrar()
