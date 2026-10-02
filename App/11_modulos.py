"""
=====================================================================
  MATERIAL DE ESTUDO PYTHON — MÓDULOS, PACOTES E import
  O que são -> Formas de import -> Biblioteca padrão -> Criando seus
  módulos -> __name__ -> Pacotes e __init__.py -> Como o Python acha
  os módulos -> pip e ambientes virtuais -> Erros comuns -> Boas
  práticas
=====================================================================

PRÉ-REQUISITOS: 01 a 09 (principalmente funções).

ARQUIVOS DESTE MATERIAL:
  11_modulos.py               <- você está aqui
  meus_modulos/               <- um PACOTE de exemplo
      __init__.py
      calculos.py
      textos.py
  Abra os arquivos da pasta meus_modulos também! Eles fazem parte da
  explicação.

COMO USAR ESTE ARQUIVO:
  1. Leia os comentários de cima para baixo.
  2. Rode no terminal:   python 11_modulos.py
  3. Rode também:        python meus_modulos/calculos.py
     e compare (seção 6).
"""


# =====================================================================
# 1. O QUE É UM MÓDULO
# =====================================================================
# MÓDULO = qualquer arquivo .py. Só isso.
# Tudo que está dentro dele (funções, variáveis, classes) pode ser
# usado em OUTRO arquivo através do "import".
#
# PACOTE = uma PASTA com vários módulos (e um arquivo __init__.py).
#
# BIBLIOTECA = um conjunto de módulos/pacotes para um propósito.
#   - Biblioteca PADRÃO: já vem com o Python (math, random, json,
#     csv, datetime, pathlib...). Você já usou várias!
#   - Bibliotecas de TERCEIROS: instaladas com pip (requests, pandas,
#     flask, django...).
#
# Por que dividir o código em módulos?
#   - Organização: um arquivo de 5000 linhas é impossível de manter
#   - Reaproveitamento: escreveu uma vez, importa em vários projetos
#   - Não reinventar a roda: milhares de módulos prontos e testados


# =====================================================================
# 2. AS FORMAS DE IMPORTAR
# =====================================================================
# Por convenção (PEP 8), os imports ficam no TOPO do arquivo. Aqui eles
# estão espalhados só porque é um material de estudo.

print("=" * 60)
print("2. FORMAS DE IMPORTAR")
print("=" * 60)

# 2.1 import modulo -> usa com o prefixo "modulo."
import math

print("math.sqrt(16) =", math.sqrt(16))
print("math.pi =", math.pi)
# O prefixo deixa CLARO de onde vem cada coisa. É a forma mais segura.

# 2.2 from modulo import nome -> traz o nome direto, sem prefixo
from math import ceil, floor

print("ceil(4.2) =", ceil(4.2), "| floor(4.8) =", floor(4.8))
# Mais curto, mas ao ler "ceil" no meio do código, de onde veio?

# 2.3 import modulo as apelido -> renomeia o módulo
import statistics as stats

print("stats.mean([1, 2, 3, 4]) =", stats.mean([1, 2, 3, 4]))
# Muito usado com nomes longos e em convenções da comunidade:
#   import numpy as np
#   import pandas as pd
#   import matplotlib.pyplot as plt

# 2.4 from modulo import nome as apelido
from datetime import datetime as dt

print("ano atual:", dt.now().year)

# 2.5 from modulo import *  -> importa TUDO. EVITE!
#   from math import *
#   Problemas: você não sabe o que entrou no seu arquivo, e pode
#   sobrescrever suas próprias variáveis sem perceber. Exemplo: se
#   você tem uma variável "e" e faz "from math import *", ela vira
#   2.718... (a constante e do math).

# Explorando um módulo:
#   dir(math)   -> lista tudo que existe dentro dele
#   help(math.sqrt) -> mostra a documentação (no terminal interativo)
funcoes_math = [nome for nome in dir(math) if not nome.startswith("_")]
print(f"o módulo math tem {len(funcoes_math)} nomes públicos, ex: {funcoes_math[:6]}")
print()


# =====================================================================
# 3. UM PASSEIO PELA BIBLIOTECA PADRÃO
# =====================================================================
# "Batteries included": o Python vem com muita coisa pronta. Antes de
# escrever algo do zero, pergunte: "será que já existe um módulo?"

print("=" * 60)
print("3. BIBLIOTECA PADRÃO")
print("=" * 60)

# --- math: matemática ---
print("[math]")
print("  potência 2^10:", math.pow(2, 10), "| fatorial(5):", math.factorial(5))
print("  arredondar p/ cima 7/2:", math.ceil(7 / 2))
print("  hipotenusa 3,4:", math.hypot(3, 4))

# --- random: números aleatórios ---
import random

print("[random]")
random.seed(42)   # "semente": fixa a sequência para o resultado ser repetível
print("  randint(1, 6):", random.randint(1, 6))
print("  choice:", random.choice(["pedra", "papel", "tesoura"]))
cartas = ["A", "K", "Q", "J"]
random.shuffle(cartas)    # embaralha a lista ORIGINAL (não retorna nada)
print("  shuffle:", cartas)
print("  sample (3 sem repetir de 1-60):", sorted(random.sample(range(1, 61), 3)))
# Sem o seed, cada execução dá um resultado diferente. O seed é útil em
# testes. Para senhas/tokens, use o módulo "secrets", não o random.

# --- datetime: datas e horas ---
from datetime import date, timedelta

print("[datetime]")
hoje = date.today()
print("  hoje:", hoje, "| formatado BR:", hoje.strftime("%d/%m/%Y"))
daqui_30 = hoje + timedelta(days=30)
print("  daqui 30 dias:", daqui_30.strftime("%d/%m/%Y"))
natal = date(hoje.year, 12, 25)
print("  dias até o Natal:", (natal - hoje).days)
data_convertida = dt.strptime("15/03/2026", "%d/%m/%Y")   # texto -> data
print("  texto convertido:", data_convertida.date(), "| dia da semana (0=seg):", data_convertida.weekday())

# --- statistics: estatística básica ---
notas = [7, 8, 8, 9, 10, 6]
print("[statistics]")
print(f"  média {stats.mean(notas):.2f} | mediana {stats.median(notas)} | moda {stats.mode(notas)}")

# --- collections: estruturas extras (visto em dicionários) ---
from collections import Counter

print("[collections]")
print("  Counter:", Counter("mississippi").most_common(2))

# --- sys e os: informações do sistema ---
import os
import sys

print("[sys / os]")
print("  versão do Python:", sys.version.split()[0])
print("  sistema:", sys.platform, "| pasta atual:", os.getcwd())
print("  variável de ambiente USERNAME/USER:", os.environ.get("USERNAME") or os.environ.get("USER"))

# --- time: pausas e medição de tempo ---
import time

print("[time]")
inicio = time.perf_counter()
soma = sum(range(1_000_000))      # _ nos números: só para facilitar a leitura
duracao = time.perf_counter() - inicio
print(f"  somar 1 milhão de números levou {duracao * 1000:.1f} ms")
# time.sleep(2) pausaria o programa por 2 segundos

# Outros que valem conhecer (pesquise quando precisar):
#   json, csv, pathlib, shutil  -> vistos no material de arquivos
#   re          -> expressões regulares (buscar padrões em textos)
#   itertools   -> ferramentas para loops e combinações
#   secrets     -> geração segura de senhas/tokens
#   urllib      -> acessar URLs (na prática, usa-se "requests")
#   sqlite3     -> banco de dados SQL num arquivo
#   unittest    -> testes automatizados
#   logging     -> logs profissionais (melhor que print)
print()


# =====================================================================
# 4. CRIANDO SEU PRÓPRIO MÓDULO
# =====================================================================
# Abra o arquivo meus_modulos/calculos.py: é um .py normal, com
# funções. Para usar essas funções aqui, basta importar.
#
# REGRA IMPORTANTE: o nome do módulo é o nome do arquivo SEM o .py, e
# ele precisa ser um nome válido de variável. Por isso:
#   calculos.py       -> import calculos            OK
#   meu-modulo.py     -> import meu-modulo          ERRO (hífen)
#   11_modulos.py     -> import 11_modulos          ERRO (começa com número)
# Os arquivos DESTE curso começam com número para ficarem em ordem na
# pasta. Isso é ótimo para scripts de estudo, mas eles NÃO podem ser
# importados com import. Para módulos reutilizáveis: snake_case, sem
# número no início.

print("=" * 60)
print("4. USANDO SEUS PRÓPRIOS MÓDULOS")
print("=" * 60)

from meus_modulos import calculos

print("calculos.somar(10, 5) =", calculos.somar(10, 5))
print("calculos.calcular_media([6, 7, 8]) =", calculos.calcular_media([6, 7, 8]))
print("calculos.TAXA_PADRAO =", calculos.TAXA_PADRAO)
print("calculos.aplicar_taxa(200) =", calculos.aplicar_taxa(200))

from meus_modulos.textos import eh_palindromo, titulo

print("eh_palindromo('Socorram me subi no onibus em Marrocos')?",
      eh_palindromo("Socorram me subi no onibus em Marrocos"))
print(titulo("Título feito pelo módulo textos", largura=44, caractere="~"))

# A docstring do módulo (o texto entre """ no topo) fica disponível:
print("doc de calculos:", calculos.__doc__.splitlines()[0])
print()


# =====================================================================
# 5. O CÓDIGO DO MÓDULO RODA UMA VEZ SÓ
# =====================================================================
# Na PRIMEIRA vez que um módulo é importado, o Python EXECUTA o arquivo
# inteiro, de cima a baixo. Os próximos imports reaproveitam o mesmo
# módulo, que fica guardado em sys.modules.
#
# Consequência: tudo que está "solto" no nível do arquivo (fora de
# funções) roda no import. Se calculos.py tivesse um print() solto, ele
# apareceria aqui só por importar! Por isso módulos devem ter apenas
# DEFINIÇÕES (funções, constantes, classes) no nível do arquivo, e o
# código "de teste" fica dentro do if __name__ == "__main__".

print("=" * 60)
print("5. MÓDULOS SÃO CARREGADOS UMA VEZ")
print("=" * 60)

from meus_modulos import calculos as calculos_de_novo

print("é o MESMO objeto?", calculos is calculos_de_novo)
print("'meus_modulos.calculos' está em sys.modules?", "meus_modulos.calculos" in sys.modules)
print()


# =====================================================================
# 6. if __name__ == "__main__" (agora fazendo sentido)
# =====================================================================
# Todo módulo tem uma variável automática chamada __name__:
#   - Se o arquivo foi EXECUTADO diretamente: __name__ == "__main__"
#   - Se o arquivo foi IMPORTADO: __name__ == "nome.do.modulo"
#
# Então:
#   if __name__ == "__main__":
#       ...
# significa "rode isto só se eu sou o programa principal".
#
# TESTE AGORA no terminal:
#   python meus_modulos/calculos.py   -> o bloco do final do arquivo RODA
#   python 11_modulos.py              -> o bloco NÃO roda (foi importado)

print("=" * 60)
print("6. __name__")
print("=" * 60)

print("__name__ DESTE arquivo:", repr(__name__))
print("__name__ do módulo calculos:", repr(calculos.__name__))
print("(o bloco de teste de calculos.py NÃO rodou, repare que nada dele apareceu)")
print()


# =====================================================================
# 7. PACOTES E __init__.py
# =====================================================================
# Abra meus_modulos/__init__.py. Uma pasta com __init__.py é um PACOTE.
#
#   meus_modulos/
#       __init__.py     <- roda ao importar o pacote
#       calculos.py     <- módulo meus_modulos.calculos
#       textos.py       <- módulo meus_modulos.textos
#
# Formas de importar de um pacote:
#   import meus_modulos.calculos              -> meus_modulos.calculos.somar()
#   from meus_modulos import calculos         -> calculos.somar()
#   from meus_modulos.calculos import somar   -> somar()
#   from meus_modulos import somar            -> somar()  (só funciona porque
#                                                o __init__.py "expôs" somar)
#
# Pacotes podem ter subpacotes (pastas dentro de pastas), cada um com
# seu __init__.py: from loja.pagamentos.pix import gerar_qrcode

print("=" * 60)
print("7. PACOTES")
print("=" * 60)

import meus_modulos

print("meus_modulos.VERSAO =", meus_modulos.VERSAO)
print("meus_modulos.somar(1, 1) =", meus_modulos.somar(1, 1))   # exposto no __init__

from meus_modulos import calcular_media

print("calcular_media direto do pacote:", calcular_media([10, 5]))

# IMPORT ABSOLUTO vs RELATIVO
#   Absoluto: from meus_modulos.calculos import somar
#     -> caminho completo a partir da raiz do projeto. Use por padrão.
#   Relativo: from .calculos import somar
#     -> "." = este pacote, ".." = o pacote de cima.
#     -> SÓ funciona DENTRO de um pacote (como no __init__.py). Não
#        funciona num script executado diretamente.
print()


# =====================================================================
# 8. COMO O PYTHON ENCONTRA OS MÓDULOS (sys.path)
# =====================================================================
# Ao fazer "import algo", o Python procura, em ordem, nas pastas da
# lista sys.path:
#   1. A pasta do script que você executou (por isso meus_modulos foi
#      encontrado: está ao lado deste arquivo)
#   2. As pastas da biblioteca padrão
#   3. A pasta site-packages (onde o pip instala os pacotes)
#
# Ele usa o PRIMEIRO que encontrar. Isso causa uma pegadinha clássica
# (ver seção 10, erro 2).

print("=" * 60)
print("8. sys.path")
print("=" * 60)

for posicao, pasta in enumerate(sys.path[:4]):
    print(f"  {posicao}: {pasta}")
print("  ...")
print("math vem de:", getattr(math, "__file__", "(embutido no próprio Python)"))
print("random vem de:", random.__file__)
print("calculos vem de:", calculos.__file__)
print()


# =====================================================================
# 9. BIBLIOTECAS DE TERCEIROS: pip E AMBIENTES VIRTUAIS
# =====================================================================
# O PyPI (pypi.org) tem centenas de milhares de pacotes feitos pela
# comunidade. Você instala com o pip, pelo TERMINAL (não no código!):
#
#   pip install requests          -> instala
#   pip install requests==2.32.3  -> instala uma versão específica
#   pip list                      -> lista o que está instalado
#   pip uninstall requests        -> remove
#
# Depois de instalado, é só importar normalmente:
#   import requests
#   resposta = requests.get("https://api.github.com")
#
# ---------------------------------------------------------------------
# AMBIENTE VIRTUAL (venv): MUITO IMPORTANTE
# ---------------------------------------------------------------------
# Sem venv, tudo é instalado no Python "global" do computador. Com o
# tempo, projetos diferentes precisam de versões diferentes do mesmo
# pacote e tudo entra em conflito.
#
# O venv cria uma pasta com um Python ISOLADO para cada projeto:
#
#   python -m venv .venv               -> cria o ambiente (uma vez)
#
#   Ativar (toda vez que abrir o terminal):
#     Windows PowerShell:  .venv\Scripts\Activate.ps1
#     Windows cmd:         .venv\Scripts\activate.bat
#     Linux/Mac:           source .venv/bin/activate
#   (o nome (.venv) aparece no início da linha do terminal)
#
#   pip install requests               -> instala SÓ neste projeto
#   deactivate                         -> sai do ambiente
#
# REQUIREMENTS.TXT: a "lista de compras" do projeto
#   pip freeze > requirements.txt      -> salva os pacotes e versões
#   pip install -r requirements.txt    -> instala tudo da lista
#                                         (num PC novo, por exemplo)
#
# Regra prática para TODO projeto novo:
#   1. Criar pasta  2. python -m venv .venv  3. ativar  4. pip install
#   5. Não colocar a pasta .venv no git (só o requirements.txt)
#
# Ferramentas modernas como "uv" e "poetry" fazem tudo isso de forma
# mais automática. Vale conhecer quando estiver confortável com o básico.

print("=" * 60)
print("9. PACOTES DE TERCEIROS")
print("=" * 60)

print("Rodando dentro de um venv?", sys.prefix != sys.base_prefix)

try:
    import requests  # noqa: F401  (pode não estar instalado)
    print("requests está instalado, versão:", requests.__version__)
except ImportError:
    print("requests NÃO está instalado. Para instalar: pip install requests")
# Repare: try/except ImportError é o jeito de lidar com pacotes
# opcionais. É o tratamento de erros do material 07 em ação!
print()


# =====================================================================
# 10. ERROS COMUNS
# =====================================================================

print("=" * 60)
print("10. ERROS COMUNS")
print("=" * 60)

# ERRO 1: ModuleNotFoundError: No module named 'xyz'
#   - Nome digitado errado?
#   - Pacote de terceiros não instalado? -> pip install xyz
#   - Instalou, mas num Python/venv DIFERENTE do que está rodando?
#     (muito comum!) Confira com:  python -m pip install xyz
#     O "python -m pip" garante que o pip é o do MESMO python.
#   - Seu módulo está em outra pasta que não está no sys.path?
try:
    import modulo_que_nao_existe  # noqa: F401
except ModuleNotFoundError as e:
    print("ERRO 1 ->", e)

# ERRO 2: dar ao SEU arquivo o nome de um módulo da biblioteca padrão.
#   Se você criar "random.py" na sua pasta e fizer "import random", o
#   Python acha o SEU arquivo primeiro (sys.path!) e não o verdadeiro:
#     AttributeError: module 'random' has no attribute 'randint'
#   Nomes perigosos: random.py, math.py, json.py, csv.py, email.py,
#   test.py, string.py, statistics.py, requests.py...
print("ERRO 2 -> nunca nomeie seu arquivo como random.py, math.py, json.py...")

# ERRO 3: ImportError: cannot import name 'x' from 'modulo'
#   O módulo existe, mas não tem nada chamado 'x' (nome errado?).
try:
    from math import raiz_quadrada  # noqa: F401
except ImportError as e:
    print("ERRO 3 ->", e)

# ERRO 4: import circular. a.py importa b.py, e b.py importa a.py.
#   Sintoma: ImportError "partially initialized module". Solução:
#   reorganizar, movendo o código compartilhado para um terceiro módulo.

# ERRO 5: esquecer o prefixo
#   import math
#   sqrt(9)        -> NameError. O certo é math.sqrt(9)

# ERRO 6: tentar importar arquivo com hífen ou começando com número
#   (seção 4)
print()


# =====================================================================
# 11. NAMING CONVENTIONS E BOAS PRÁTICAS
# =====================================================================
# NOMES (PEP 8):
#   - Módulos: snake_case, curtos, minúsculos:  calculos.py, banco_dados.py
#   - Pacotes: minúsculos, curtos, de preferência sem "_": utilidades/
#   - Nunca use hífen, espaço, acento ou número no início
#   - Nunca use nome de módulo da biblioteca padrão (seção 10, erro 2)
#   - "_" no início de função/variável = uso interno do módulo
#       def _arredondar_interno(): ...   (veja em calculos.py)
#
# ORGANIZAÇÃO DOS IMPORTS (PEP 8):
#   1. Sempre no TOPO do arquivo (depois da docstring do módulo)
#   2. Um import por linha:  import os  /  import sys
#      (from x import a, b na mesma linha é ok)
#   3. Em 3 grupos, separados por uma linha em branco:
#
#        import json                 # 1. biblioteca padrão
#        from pathlib import Path
#
#        import requests             # 2. terceiros (instalados com pip)
#
#        from meus_modulos import calculos   # 3. seus módulos
#
#   4. Em ordem alfabética dentro de cada grupo
#      (ferramentas como "ruff" e "isort" organizam sozinhas)
#   5. Evite "from x import *"
#
# BOAS PRÁTICAS:
#   1. Um módulo = um assunto (calculos, textos, banco_dados...).
#   2. No nível do módulo, só definições. Código de teste vai dentro de
#      if __name__ == "__main__".
#   3. Prefira "import modulo" quando o prefixo ajudar a entender de
#      onde vem a função (json.load deixa claro que é JSON).
#   4. Use "from modulo import nome" para nomes muito usados e claros.
#   5. Use venv em TODO projeto e mantenha um requirements.txt.
#   6. Antes de criar algo do zero, procure na biblioteca padrão.

print("=" * 60)
print("FIM! Agora vá para os exercícios no final do arquivo.")
print("=" * 60)


# =====================================================================
# 12. EXERCÍCIOS PARA PRATICAR
# =====================================================================
#
#  1. Usando o módulo math, crie area_circulo(raio) e
#     perimetro_circulo(raio). Use math.pi.
#  2. Usando random, crie sortear_senha(tamanho) que gera uma senha
#     com letras e números. Dica: import string -> string.ascii_letters,
#     string.digits. Depois troque por "secrets" e pesquise o porquê.
#  3. Usando datetime, crie calcular_idade(data_nascimento) que recebe
#     um texto "dd/mm/aaaa" e retorna a idade em anos completos.
#  4. Usando datetime, crie dias_ate(data_texto) que retorna quantos
#     dias faltam até uma data. Teste com o seu próximo aniversário.
#  5. Crie o pacote "utilidades/" com __init__.py e dois módulos:
#     - conversoes.py: celsius_para_fahrenheit, km_para_milhas,
#       reais_para_dolar(valor, cotacao)
#     - validacoes.py: eh_email_valido(texto) (tem "@" e "." depois
#       do "@"), eh_cpf_formatado(texto) (formato 000.000.000-00)
#     Importe e use num script principal.
#  6. Adicione um bloco if __name__ == "__main__" em conversoes.py
#     com testes usando assert. Rode o módulo diretamente e depois
#     importe-o, e confirme que os testes só rodam no primeiro caso.
#  7. No __init__.py de "utilidades", exponha as funções mais usadas
#     para permitir "from utilidades import celsius_para_fahrenheit".
#  8. Crie um arquivo "random.py" numa pasta de teste, com uma linha
#     print("sou o falso!"), e ao lado um "teste.py" com import random e
#     random.randint(1, 6). Rode e observe o erro. Depois apague o
#     random.py falso. (Agora você nunca mais esquece!)
#  9. Crie um ambiente virtual numa pasta de teste, ative, instale o
#     pacote "requests" e gere o requirements.txt. Abra o arquivo e veja
#     o que foi gerado.
# 10. (Desafio) Com o venv do exercício 9, use requests para buscar
#     https://api.github.com/users/SEU_USUARIO e mostre nome, número de
#     repositórios públicos e data de criação da conta (o retorno é
#     JSON: resposta.json() devolve um dict). Trate erros de conexão
#     com try/except requests.RequestException.
# 11. (Desafio) Reorganize o mini projeto de tarefas (09_arquivos.py,
#     seção 13) em um pacote "tarefas/" com os módulos armazenamento.py
#     (carregar/salvar JSON) e operacoes.py (adicionar, concluir,
#     listar), e um main.py com um menu interativo.
