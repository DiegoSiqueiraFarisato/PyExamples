"""
=====================================================================
  RESPOSTAS DOS EXERCÍCIOS — 15_testes.py
=====================================================================

COMO USAR ESTE ARQUIVO:
  Tente resolver SOZINHO antes de olhar! Depois compare com a resposta.

  Rode:   python 16_respostas_testes.py

ONDE ESTÃO AS RESPOSTAS:
  Testes não são "rodados" como um script comum: eles são encontrados
  e executados pelo pytest. Por isso, as respostas dos exercícios 1 a 10
  estão num arquivo de testes de verdade:

    tests/test_respostas_exercicios.py   <- leia este arquivo!

  Alguns exercícios também mudaram o código testado:
    loja/precos.py         <- exercício 8: calcular_parcelas (feita com TDD)
    utilidades/entrada.py  <- exercício 10: pedir_inteiro, num módulo
                              importável (veja a explicação lá dentro)

  Este script roda os testes das respostas e responde o exercício 11.
"""

import subprocess
import sys
from pathlib import Path

PASTA_APP = Path(__file__).resolve().parent
ARQUIVO_RESPOSTAS = "tests/test_respostas_exercicios.py"


def rodar_pytest(*argumentos: str) -> tuple[int, str]:
    resultado = subprocess.run(
        [sys.executable, "-m", "pytest", *argumentos],
        capture_output=True, text=True, encoding="utf-8", cwd=PASTA_APP,
    )
    return resultado.returncode, resultado.stdout


def imprimir_cabecalho(titulo: str) -> None:
    print()
    print("=" * 60)
    print(titulo)
    print("=" * 60)


try:
    import pytest  # noqa: F401
except ImportError:
    print("O pytest não está instalado. Instale com:")
    print("  python -m pip install pytest")
    sys.exit(1)


# =====================================================================
# EXERCÍCIOS 1 a 10
# =====================================================================
# Resumo do que cada resposta mostra (detalhes nos comentários do
# arquivo de testes):
#
#   1. Testes simples. "assert eh_palindromo(...)" sem "== True".
#   2. parametrize + approx (37 °C dá 98.60000000000001 °F!).
#   3. parametrize com dois parâmetros (email, esperado), 4 válidos e
#      6 inválidos, cada um com um comentário dizendo POR QUE é inválido.
#   4. pytest.raises com match= e parametrize nos valores inválidos.
#   5. Caso normal, caso limite (um só número) e caso de erro.
#   6. Fixture que USA outra fixture (tmp_path), e um teste extra para
#      a "primeira execução", sem arquivo nenhum.
#   7. O teste no limite EXATO do frete grátis e um centavo abaixo.
#      Esses dois testes pegam o bug clássico de trocar >= por >.
#   8. TDD: os testes vieram primeiro, depois a função. E a reflexão:
#      3 x 33.33 = 99.99 (some um centavo!).
#   9. capsys.readouterr() para conferir o que foi impresso.
#  10. monkeypatch + iter() simulando várias respostas do input(), e
#      capsys contando quantos avisos de erro apareceram.

imprimir_cabecalho("EXERCÍCIOS 1 a 10 — rodando tests/test_respostas_exercicios.py")
codigo_saida, saida = rodar_pytest(ARQUIVO_RESPOSTAS, "-v", "--no-header", "-p", "no:cacheprovider")
print(saida)
print("Todos passaram!" if codigo_saida == 0 else "Algum teste falhou, veja acima.")
# O código de saída do pytest: 0 = tudo passou | 1 = algum teste falhou.
# Ferramentas de CI (como GitHub Actions) usam esse número para saber se
# podem aceitar uma mudança.


# =====================================================================
# EXERCÍCIO 11 (Desafio) — cobertura com pytest-cov
# =====================================================================
# Comandos:
#   python -m pip install pytest-cov
#   python -m pytest --cov=loja --cov-report=term-missing
#
# --cov=loja                -> mede só o pacote loja
# --cov-report=term-missing -> mostra no terminal os NÚMEROS DAS LINHAS
#                              que nenhum teste executou (coluna Missing)
#
# RESULTADO: com os testes de exemplo + as respostas, o pacote loja
# chega a 100%. Só com os testes de exemplo, ficavam de fora:
#   - o raise de preço negativo em Carrinho.adicionar (coberto pelo
#     exercício 7)
#   - a calcular_parcelas inteira (criada e coberta no exercício 8)
#
# 100% DE COBERTURA GARANTE QUE NÃO HÁ BUGS?  NÃO!
# Cobertura mede quais linhas RODARAM, e não se o resultado foi
# CONFERIDO direito. Lembre da seção 5 do material: o teste da média
# com 2 notas executava a linha com o bug (cobertura 100%) e PASSAVA,
# porque dividir por 2 coincidia com dividir por len(notas).
# E ainda: um teste sem assert também "cobre" as linhas!
#
# Cobertura é ótima para achar o que NINGUÉM testou. Mas a qualidade dos
# testes vem dos CASOS escolhidos: limites, erros e casos especiais.

imprimir_cabecalho("EXERCÍCIO 11 — cobertura do pacote loja")
try:
    import pytest_cov  # noqa: F401
except ImportError:
    print("O plugin pytest-cov não está instalado neste Python.")
    print("Para fazer este exercício:")
    print("  python -m pip install pytest-cov")
    print("  python -m pytest --cov=loja --cov-report=term-missing")
    print("(veja a resposta completa nos comentários deste arquivo)")
else:
    _, saida = rodar_pytest("--cov=loja", "--cov-report=term-missing", "-q", "-p", "no:cacheprovider")
    print(saida)

print()
print("=" * 60)
print("FIM DAS RESPOSTAS! Leia tests/test_respostas_exercicios.py")
print("=" * 60)
