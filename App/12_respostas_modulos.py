"""
=====================================================================
  RESPOSTAS DOS EXERCÍCIOS — 11_modulos.py
=====================================================================

COMO USAR ESTE ARQUIVO:
  Tente resolver SOZINHO antes de olhar! Depois compare com a resposta.

  Rode:   python 12_respostas_modulos.py

  Os exercícios 5, 6, 7 e 11 pedem para CRIAR pacotes. Eles estão em
  pastas próprias, ao lado deste arquivo:

    utilidades/              <- exercícios 5, 6 e 7
        __init__.py
        conversoes.py
        validacoes.py
    tarefas/                 <- exercício 11
        __init__.py
        armazenamento.py
        operacoes.py
        main.py

  Abra e leia esses arquivos também! Comandos para testar:
    python utilidades/conversoes.py     (exercício 6: roda os testes)
    python -m tarefas.main              (exercício 11: menu interativo)
"""

# Imports organizados em grupos, como manda a PEP 8 (seção 11):
# 1. biblioteca padrão
import math
import random
import secrets
import string
import subprocess
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path

# 3. módulos do próprio projeto
# (o grupo 2, de terceiros, ficaria aqui no meio. O requests é importado
# lá embaixo, dentro de um try, porque talvez não esteja instalado.)
from tarefas import operacoes
from utilidades import (
    celsius_para_fahrenheit,
    eh_cpf_formatado,
    eh_email_valido,
    km_para_milhas,
    reais_para_dolar,
)


def imprimir_cabecalho(titulo: str) -> None:
    """Função auxiliar só para separar as respostas na saída."""
    print()
    print("=" * 60)
    print(titulo)
    print("=" * 60)


# =====================================================================
# EXERCÍCIO 1
# area_circulo(raio) e perimetro_circulo(raio) usando math.pi.
# =====================================================================
def area_circulo(raio: float) -> float:
    return math.pi * raio ** 2


def perimetro_circulo(raio: float) -> float:
    return 2 * math.pi * raio


imprimir_cabecalho("EXERCÍCIO 1 — math")
for raio in [1, 2.5, 10]:
    print(f"raio {raio:>4}: área {area_circulo(raio):8.2f} | perímetro {perimetro_circulo(raio):6.2f}")


# =====================================================================
# EXERCÍCIO 2
# sortear_senha(tamanho) com letras e números (random), depois com
# secrets. Por quê?
# =====================================================================
CARACTERES_SENHA = string.ascii_letters + string.digits
# string.ascii_letters = "abc...zABC...Z" | string.digits = "0123456789"


def sortear_senha(tamanho: int = 12) -> str:
    """Versão com random: NÃO use para senhas reais (veja abaixo)."""
    return "".join(random.choice(CARACTERES_SENHA) for _ in range(tamanho))


def gerar_senha_segura(tamanho: int = 12) -> str:
    """Versão com secrets: a correta para senhas e tokens."""
    return "".join(secrets.choice(CARACTERES_SENHA) for _ in range(tamanho))


imprimir_cabecalho("EXERCÍCIO 2 — random vs secrets")
print("random: ", sortear_senha())
print("secrets:", gerar_senha_segura())
print("secrets.token_urlsafe(16):", secrets.token_urlsafe(16))

# POR QUÊ?
# O random é PSEUDOaleatório e PREVISÍVEL: ele é feito para simulações e
# jogos. Com o mesmo seed, gera sempre a mesma sequência (lembra do
# random.seed(42) no material?), e quem observar alguns valores consegue
# prever os próximos. O secrets usa a fonte de aleatoriedade segura do
# sistema operacional e foi feito para senhas, tokens e chaves.
random.seed(1)
a = sortear_senha(8)
random.seed(1)
b = sortear_senha(8)
print(f"com o mesmo seed, random repete a 'senha': {a} == {b} -> {a == b}")


# =====================================================================
# EXERCÍCIO 3
# calcular_idade("dd/mm/aaaa") retorna a idade em anos completos.
# =====================================================================
def calcular_idade(data_nascimento: str, hoje: date | None = None) -> int:
    nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y").date()
    hoje = hoje or date.today()
    idade = hoje.year - nascimento.year
    # Se o aniversário deste ano ainda não chegou, tira 1.
    # Comparar tuplas (mês, dia) compara primeiro o mês e, se empatar,
    # o dia. É um truque muito prático!
    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
        idade -= 1
    return idade


imprimir_cabecalho("EXERCÍCIO 3 — calcular_idade")
print("nascido em 15/03/1995:", calcular_idade("15/03/1995"), "anos")
print("nascido em 25/12/1995:", calcular_idade("25/12/1995"), "anos (aniversário ainda não chegou)")

# O parâmetro "hoje" é opcional e serve para TESTAR com uma data fixa.
# Sem ele, o teste mudaria de resultado conforme o dia em que roda.
dia_fixo = date(2026, 10, 2)
assert calcular_idade("02/10/2000", dia_fixo) == 26   # aniversário é hoje
assert calcular_idade("03/10/2000", dia_fixo) == 25   # é amanhã
print("testes com data fixa passaram!")

try:
    calcular_idade("31/02/2000")
except ValueError as e:
    print("data inválida ->", e)


# =====================================================================
# EXERCÍCIO 4
# dias_ate(data_texto) retorna quantos dias faltam até uma data.
# =====================================================================
def dias_ate(data_texto: str) -> int:
    alvo = datetime.strptime(data_texto, "%d/%m/%Y").date()
    return (alvo - date.today()).days       # negativo se já passou


def dias_ate_proximo_aniversario(dia: int, mes: int) -> int:
    hoje = date.today()
    aniversario = date(hoje.year, mes, dia)
    if aniversario < hoje:                  # já passou este ano
        aniversario = date(hoje.year + 1, mes, dia)
    return (aniversario - hoje).days


imprimir_cabecalho("EXERCÍCIO 4 — dias_ate")
ano_que_vem = date.today().year + 1
print(f"dias até 01/01/{ano_que_vem}:", dias_ate(f"01/01/{ano_que_vem}"))
print("dias até 01/01/2000:", dias_ate("01/01/2000"), "(negativo: já passou)")
print("próximo aniversário em 15/03:", dias_ate_proximo_aniversario(15, 3), "dias")
# Atenção: quem faz aniversário em 29/02 precisa de tratamento especial,
# porque date(ano, 2, 29) dá erro em ano não bissexto!


# =====================================================================
# EXERCÍCIOS 5, 6 e 7 — pacote utilidades
# =====================================================================
# Leia: utilidades/__init__.py, utilidades/conversoes.py e
# utilidades/validacoes.py
imprimir_cabecalho("EXERCÍCIOS 5, 6 e 7 — pacote utilidades")

print("25 °C =", celsius_para_fahrenheit(25), "°F")
print("42.195 km (maratona) =", round(km_para_milhas(42.195), 2), "milhas")
print("R$ 1000 com dólar a R$ 5.40 =", reais_para_dolar(1000, 5.40), "dólares")

for email in ["ana@email.com", "ana@email", "@email.com", "ana@@x.com", "ana@.com"]:
    print(f"  e-mail {email!r:<16} válido? {eh_email_valido(email)}")

for cpf in ["123.456.789-00", "12345678900", "123.456.789.00", "abc.def.ghi-jk"]:
    print(f"  cpf {cpf!r:<18} formatado? {eh_cpf_formatado(cpf)}")

# Exercício 6: rodando conversoes.py DIRETAMENTE (como se você digitasse
# "python utilidades/conversoes.py" no terminal). subprocess executa um
# comando e captura o que ele imprimiu.
resultado = subprocess.run(
    [sys.executable, "utilidades/conversoes.py"],
    capture_output=True, text=True, encoding="utf-8",
    cwd=Path(__file__).resolve().parent,
)
print("rodando direto  ->", resultado.stdout.strip())
print("importando aqui -> (nada foi impresso: o bloco __main__ não rodou)")


# =====================================================================
# EXERCÍCIO 8
# Um random.py "falso" ao lado de um teste.py com import random.
# =====================================================================
# Em vez de você criar e apagar os arquivos na mão, este código cria
# tudo numa pasta temporária, roda e mostra o erro.
imprimir_cabecalho("EXERCÍCIO 8 — o random.py falso")

with tempfile.TemporaryDirectory() as pasta_teste:     # apagada no final
    pasta = Path(pasta_teste)
    (pasta / "random.py").write_text('print("sou o falso!")\n', encoding="utf-8")
    (pasta / "teste.py").write_text(
        "import random\nprint(random.randint(1, 6))\n", encoding="utf-8"
    )
    resultado = subprocess.run(
        [sys.executable, "teste.py"],
        capture_output=True, text=True, encoding="utf-8", cwd=pasta,
    )

print("saída:", resultado.stdout.strip())
print("erro: ", resultado.stderr.strip().splitlines()[-1])
# O "import random" encontrou o random.py da pasta (1º lugar do sys.path)
# em vez do verdadeiro. Ele rodou o print e não tem randint.


# =====================================================================
# EXERCÍCIO 9
# Criar um venv, instalar requests e gerar o requirements.txt.
# =====================================================================
# Este exercício é feito no TERMINAL (PowerShell), não em código:
#
#   mkdir teste_venv
#   cd teste_venv
#   python -m venv .venv
#   .venv\Scripts\Activate.ps1
#   python -m pip install requests
#   python -m pip freeze > requirements.txt
#   type requirements.txt          (no Linux/Mac: cat requirements.txt)
#
# O requirements.txt terá algo como:
#   certifi==2026.x.x
#   charset-normalizer==3.x.x
#   idna==3.x
#   requests==2.x.x
#   urllib3==2.x.x
# Repare: você instalou SÓ o requests, mas vieram outros 4. São as
# DEPENDÊNCIAS dele (pacotes que o requests usa por dentro).
#
# Se o Activate.ps1 der erro de "execução de scripts desabilitada", rode
# uma vez:  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
imprimir_cabecalho("EXERCÍCIO 9 — venv (feito no terminal)")
print("Veja os comandos nos comentários deste exercício.")
print("Neste momento, rodando dentro de um venv?", sys.prefix != sys.base_prefix)


# =====================================================================
# EXERCÍCIO 10 (Desafio)
# Buscar um usuário na API do GitHub com requests.
# =====================================================================
def buscar_usuario_github(usuario: str) -> dict | None:
    import requests      # import aqui dentro: só é exigido se a função rodar

    url = f"https://api.github.com/users/{usuario}"
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()      # transforma 404, 500... em exceção
    except requests.HTTPError:
        print(f"  Usuário '{usuario}' não encontrado (HTTP {resposta.status_code}).")
        return None
    except requests.RequestException as e:   # sem internet, timeout etc.
        print(f"  Erro de conexão: {e}")
        return None

    dados = resposta.json()              # JSON -> dict
    criada_em = datetime.strptime(dados["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    return {
        "nome": dados.get("name") or usuario,
        "repositorios_publicos": dados["public_repos"],
        "conta_criada_em": criada_em.strftime("%d/%m/%Y"),
    }


imprimir_cabecalho("EXERCÍCIO 10 — API do GitHub com requests")
try:
    import requests  # noqa: F401
except ImportError:
    print("O pacote requests não está instalado neste Python.")
    print("Faça o exercício 9 e rode este arquivo com o venv ativado.")
else:
    # "else" do try: só roda se o import deu certo (material 07!)
    usuario_github = "octocat"            # troque pelo seu usuário
    perfil = buscar_usuario_github(usuario_github)
    if perfil:
        for chave, valor in perfil.items():
            print(f"  {chave}: {valor}")


# =====================================================================
# EXERCÍCIO 11 (Desafio) — pacote tarefas
# =====================================================================
# Leia: tarefas/__init__.py, armazenamento.py, operacoes.py e main.py.
#
# A divisão segue "uma responsabilidade por módulo":
#   armazenamento -> só lê/grava JSON
#   operacoes     -> só regras (sem input/print)
#   main          -> só interação com o usuário
#
# Aqui testamos as operações num arquivo TEMPORÁRIO, para não mexer nas
# suas tarefas reais (tarefas/tarefas.json, usado pelo menu).
imprimir_cabecalho("EXERCÍCIO 11 — pacote tarefas")

with tempfile.TemporaryDirectory() as pasta_teste:
    arquivo_teste = Path(pasta_teste) / "tarefas_teste.json"
    operacoes.adicionar("Estudar classes", arquivo_teste)
    operacoes.adicionar("Fazer exercícios", arquivo_teste)
    operacoes.adicionar("Tarefa errada", arquivo_teste)
    operacoes.concluir(1, arquivo_teste)
    operacoes.remover(3, arquivo_teste)
    print("concluir tarefa 99?", operacoes.concluir(99, arquivo_teste))
    for linha in operacoes.listar(arquivo_teste):
        print(" ", linha)
    try:
        operacoes.adicionar("   ", arquivo_teste)
    except ValueError as e:
        print("  título vazio ->", e)

print("Para usar o menu de verdade:  python -m tarefas.main")

print()
print("=" * 60)
print("FIM DAS RESPOSTAS!")
print("=" * 60)
