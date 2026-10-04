"""
=====================================================================
  MATERIAL DE ESTUDO PYTHON — TESTES AUTOMATIZADOS COM pytest
  Por que testar -> assert -> Primeiro teste -> Rodando o pytest ->
  Lendo falhas -> Padrão AAA -> pytest.raises -> pytest.approx ->
  parametrize -> fixtures -> conftest.py -> tmp_path -> Testando
  classes -> O que testar -> TDD -> Boas práticas
=====================================================================

PRÉ-REQUISITOS: 01 a 13 (principalmente funções, erros, módulos e
classes).

ARQUIVOS DESTE MATERIAL:
  15_testes.py           <- você está aqui
  pytest.ini             <- configuração do pytest
  loja/                  <- o CÓDIGO que vamos testar
      precos.py
      carrinho.py
  tests/                 <- os TESTES
      conftest.py
      test_precos.py
      test_carrinho.py
  Leia os arquivos de loja/ e tests/ junto com este material!

INSTALAÇÃO (se ainda não tiver):
  python -m pip install pytest

COMO USAR ESTE ARQUIVO:
  1. Leia os comentários de cima para baixo.
  2. Rode:   python 15_testes.py
     (ele mesmo executa o pytest e mostra os resultados)
  3. Depois rode o pytest você mesmo, da pasta App:
       python -m pytest -v
"""

import subprocess
import sys
import tempfile
from pathlib import Path

PASTA_APP = Path(__file__).resolve().parent

try:
    import pytest
except ImportError:
    pytest = None


def rodar_pytest(*argumentos: str, pasta: Path = PASTA_APP) -> str:
    """Roda "python -m pytest <argumentos>" e devolve o texto da saída."""
    resultado = subprocess.run(
        [sys.executable, "-m", "pytest", *argumentos],
        capture_output=True, text=True, encoding="utf-8", cwd=pasta,
    )
    return resultado.stdout


# =====================================================================
# 1. POR QUE TESTES AUTOMATIZADOS?
# =====================================================================
# Até agora, você testou seu código MANUALMENTE: roda, olha o print e
# confere "de olho". Funciona com 10 linhas. Com 10 mil, não:
#   - Você muda uma função e quebra outra lá longe sem perceber
#   - Conferir tudo de novo a cada mudança leva horas
#   - "Funcionava ontem!" e ninguém sabe o que mudou
#
# Um TESTE AUTOMATIZADO é um código que verifica outro código. Você
# escreve uma vez e roda centenas de testes em segundos, quantas vezes
# quiser. Se algo quebrar, ele avisa EXATAMENTE onde.
#
# Benefícios:
#   - Coragem para mudar e melhorar o código (refatorar)
#   - Os testes documentam como o código deve se comportar
#   - Bugs aparecem na hora, e não em produção
#   - Pensar nos testes melhora o design das suas funções


# =====================================================================
# 2. A BASE DE TUDO: assert
# =====================================================================
# Você já usou assert nos materiais anteriores:
#   assert condicao, "mensagem opcional"
# Se a condição for True, nada acontece. Se for False, levanta
# AssertionError e o programa para.

print("=" * 60)
print("2. assert")
print("=" * 60)


def dobro(numero: int) -> int:
    return numero * 2


assert dobro(2) == 4
assert dobro(0) == 0
assert dobro(-3) == -6
print("os 3 asserts passaram (nada acontece quando passa)")

try:
    assert dobro(2) == 5, "dobro(2) deveria ser 5?"
except AssertionError as e:
    print("assert falhou ->", e)

# Asserts soltos no arquivo têm limites:
#   - O PRIMEIRO que falha para tudo (você não vê os outros)
#   - Não há relatório: quantos passaram? quais falharam?
#   - Testes misturados com o código do programa
# O pytest resolve todos esses problemas.
print()


# =====================================================================
# 3. O PRIMEIRO TESTE COM pytest
# =====================================================================
# Com pytest, um teste é só uma FUNÇÃO comum com assert dentro:
#
#   # arquivo: tests/test_precos.py
#   from loja.precos import aplicar_desconto
#
#   def test_aplicar_desconto_de_10_por_cento():
#       assert aplicar_desconto(100, 10) == 90.0
#
# Sem classes obrigatórias, sem imports especiais. As REGRAS são de
# NOMES. O pytest encontra sozinho:
#   - arquivos  test_*.py  (ou *_test.py)
#   - funções   test_*
#   - classes   Test* (sem __init__), com métodos test_*
#
# Se o nome não começar com "test", o pytest IGNORA. (Esse é o erro nº 1
# de iniciante: "escrevi o teste e ele não rodou".)


# =====================================================================
# 4. RODANDO O pytest
# =====================================================================
# No terminal, na pasta App:
#
#   python -m pytest             -> roda todos os testes
#   python -m pytest -v          -> verbose: mostra o nome de cada teste
#   python -m pytest -q          -> quiet: saída resumida
#   python -m pytest tests/test_precos.py           -> só um arquivo
#   python -m pytest tests/test_precos.py::test_formatar_preco  -> um teste
#   python -m pytest -k desconto -> só testes com "desconto" no nome
#   python -m pytest -x          -> para no PRIMEIRO teste que falhar
#   python -m pytest --lf        -> roda só os que falharam da última vez
#
# Por que "python -m pytest" e não só "pytest"? Pelo mesmo motivo do
# "python -m pip" (material de módulos): garante que é o pytest do
# MESMO Python que você está usando.
#
# O pytest.ini (abra o arquivo!) diz onde ficam os testes (testpaths)
# e coloca a pasta App no sys.path (pythonpath), para os testes
# conseguirem importar o pacote loja.

print("=" * 60)
print("4. RODANDO OS TESTES DA PASTA tests/")
print("=" * 60)

if pytest is None:
    print("O pytest NÃO está instalado neste Python.")
    print("Instale com:  python -m pip install pytest")
    print("Depois rode este arquivo de novo.")
else:
    print(f"(pytest {pytest.__version__} encontrado)\n")
    print(rodar_pytest("-v", "--no-header", "-p", "no:cacheprovider"))
    # Cada linha é um teste. PASSED = passou | FAILED = falhou
    # Os testes com [colchetes] vêm do parametrize (seção 8).


# =====================================================================
# 5. LENDO UMA FALHA
# =====================================================================
# Quando um teste falha, o pytest mostra:
#   - QUAL teste falhou (arquivo::nome_do_teste)
#   - a LINHA do assert que falhou
#   - os VALORES dos dois lados da comparação (o grande diferencial do
#     pytest em relação ao assert puro)
#
# Abaixo, criamos de propósito um teste que encontra um BUG: uma função
# de média que divide pelo número errado.

print("=" * 60)
print("5. UM TESTE PEGANDO UM BUG")
print("=" * 60)

CODIGO_COM_BUG = '''
def calcular_media(notas):
    return sum(notas) / 2          # BUG: deveria ser len(notas)


def test_media_de_duas_notas():
    assert calcular_media([6, 8]) == 7       # passa (por sorte!)


def test_media_de_tres_notas():
    assert calcular_media([6, 7, 8]) == 7    # pega o bug
'''

if pytest is not None:
    with tempfile.TemporaryDirectory() as pasta:
        (Path(pasta) / "test_media.py").write_text(CODIGO_COM_BUG, encoding="utf-8")
        saida = rodar_pytest("-q", "--no-header", "-p", "no:cacheprovider", pasta=Path(pasta))
    print(saida)

# COMO LER (de baixo para cima, como o traceback):
#   - "1 failed, 1 passed": o resumo
#   - "assert 10.5 == 7": o valor OBTIDO (10.5) e o ESPERADO (7)
#   - "+  where 10.5 = calcular_media([6, 7, 8])": de onde veio o valor
#
# LIÇÃO: o teste com duas notas PASSOU, porque, com 2 notas, dividir por
# 2 coincide com dividir por len(notas). Testar só um caso pode esconder
# bugs. Teste VÁRIOS cenários (seção 8 e seção 13).


# =====================================================================
# 6. O PADRÃO AAA: Arrange, Act, Assert
# =====================================================================
# Um bom teste tem três partes bem separadas:
#
#   def test_adicionar_mesmo_item_soma_quantidade():
#       # Arrange (preparar): monta o cenário
#       carrinho = Carrinho()
#       carrinho.adicionar("livro", 40.0, quantidade=1)
#
#       # Act (agir): executa O QUE está sendo testado
#       carrinho.adicionar("livro", 40.0, quantidade=2)
#
#       # Assert (verificar): confere o resultado
#       assert carrinho.quantidade_itens() == 3
#
# (Em inglês também se fala "Given / When / Then": dado / quando /
# então.)
#
# Cada teste deve verificar UM comportamento. Vários asserts no mesmo
# teste são ok se verificarem o MESMO comportamento.


# =====================================================================
# 7. TESTANDO ERROS (pytest.raises) E FLOATS (pytest.approx)
# =====================================================================
# Testar que o código DÁ ERRO quando deve é tão importante quanto
# testar que ele funciona.
#
#   def test_desconto_acima_de_100_da_erro():
#       with pytest.raises(ValueError, match="entre 0 e 100"):
#           aplicar_desconto(100, 150)
#
#   - O teste PASSA se o código dentro do with levantar ValueError
#   - O teste FALHA se não levantar nada (ou levantar outro tipo de erro)
#   - match= confere se a mensagem do erro contém aquele texto
#
# FLOATS: lembra que 0.1 + 0.2 dá 0.30000000000000004? Comparar float
# com == é perigoso. Use pytest.approx:
#
#   assert 0.1 + 0.2 == pytest.approx(0.3)
#
# Veja os dois em tests/test_precos.py.


# =====================================================================
# 8. PARAMETRIZE: UM TESTE, VÁRIOS CASOS
# =====================================================================
# Em vez de copiar e colar o mesmo teste mudando só os valores:
#
#   @pytest.mark.parametrize(
#       ("valor_compra", "frete_esperado"),
#       [
#           (0, 19.90),
#           (199.99, 19.90),    # logo ANTES do limite
#           (200.00, 0.0),      # EXATAMENTE no limite
#           (1000, 0.0),
#       ],
#   )
#   def test_calcular_frete(valor_compra, frete_esperado):
#       assert calcular_frete(valor_compra) == frete_esperado
#
# O pytest roda o teste uma vez para CADA linha da lista, e cada uma
# aparece separada no relatório: test_calcular_frete[199.99-19.9].
#
# Repare nos casos escolhidos: valores NA FRONTEIRA (199.99 e 200.00).
# É ali que os bugs moram (>= trocado por >, por exemplo).


# =====================================================================
# 9. FIXTURES: PREPARANDO O CENÁRIO SEM REPETIR CÓDIGO
# =====================================================================
# Vários testes precisam do mesmo "ponto de partida" (um carrinho com
# itens, um usuário cadastrado...). Uma FIXTURE é uma função que
# PREPARA esse cenário:
#
#   @pytest.fixture
#   def carrinho_com_itens():
#       carrinho = Carrinho()
#       carrinho.adicionar("caderno", 25.00, quantidade=2)
#       return carrinho
#
# Para usar, o teste só PEDE a fixture pelo NOME do parâmetro:
#
#   def test_remover_item(carrinho_com_itens):
#       carrinho_com_itens.remover("caderno")
#       ...
#
# O pytest vê o parâmetro, encontra a fixture com esse nome, executa e
# passa o resultado. Cada teste recebe uma cópia NOVA, então um teste
# nunca interfere no outro.
#
# conftest.py: fixtures colocadas nesse arquivo (abra tests/conftest.py)
# ficam disponíveis para TODOS os testes da pasta, sem import.


# =====================================================================
# 10. FIXTURES PRONTAS: tmp_path E OUTRAS
# =====================================================================
# O pytest já vem com fixtures úteis. A mais usada é tmp_path: uma
# pasta temporária (um Path), diferente para cada teste e apagada
# depois. Perfeita para testar código que lê e grava arquivos:
#
#   def test_salvar_e_carregar(carrinho_com_itens, tmp_path):
#       caminho = tmp_path / "carrinho.json"
#       carrinho_com_itens.salvar(caminho)
#       carregado = Carrinho.carregar(caminho)
#       assert carregado.subtotal() == carrinho_com_itens.subtotal()
#
# Outras que valem conhecer:
#   capsys      -> captura o que foi impresso com print()
#   monkeypatch -> troca temporariamente funções, variáveis de ambiente
#                  etc. (ex: simular o input() do usuário)


# =====================================================================
# 11. TESTANDO CLASSES E AGRUPANDO TESTES
# =====================================================================
# Para testar uma classe, você cria o objeto (geralmente numa fixture),
# chama os métodos e confere o ESTADO e os RETORNOS.
#
# Testes relacionados podem ser agrupados numa classe Test*:
#
#   class TestTotal:
#       def test_subtotal(self, carrinho_com_itens): ...
#       def test_total_com_frete(self, carrinho_com_itens): ...
#
# A classe é só ORGANIZAÇÃO: não tem __init__ e cada método continua
# sendo um teste independente. Veja tests/test_carrinho.py.


# =====================================================================
# 12. CÓDIGO TESTÁVEL: O QUE O DESIGN TEM A VER COM ISSO
# =====================================================================
# Lembra das dicas dos materiais anteriores?
#   - "Prefira RETORNAR valores a imprimir dentro da função"
#   - "Separe a lógica da interação com o usuário (input/print)"
#   - "Uma função = uma responsabilidade"
# Agora você vê o PORQUÊ: funções assim são FÁCEIS de testar.
#
#   DIFÍCIL de testar:                  FÁCIL de testar:
#   def mostrar_media():                def calcular_media(notas):
#       n1 = float(input("Nota 1: "))       return sum(notas) / len(notas)
#       n2 = float(input("Nota 2: "))
#       print((n1 + n2) / 2)            assert calcular_media([6, 8]) == 7
#
# Funções que recebem dados e devolvem resultados, sem input, print,
# arquivo ou internet no meio, se chamam FUNÇÕES PURAS. São as mais
# fáceis de testar. Deixe o input/print/arquivo nas "bordas" do
# programa.


# =====================================================================
# 13. O QUE TESTAR (E O QUE NÃO TESTAR)
# =====================================================================
# Para cada função, pense em:
#   1. O caso NORMAL (o "caminho feliz")
#   2. Os LIMITES: zero, vazio, um item só, valor exato da fronteira
#      (o 200.00 do frete), números negativos
#   3. Os ERROS: entradas inválidas devem dar o erro certo
#   4. Casos ESPECIAIS do seu domínio (ano bissexto, acentos, preço
#      com centavos quebrados...)
#
# NÃO precisa testar:
#   - O próprio Python ou bibliotecas famosas (o sum() funciona)
#   - Código trivial sem lógica (um __init__ que só guarda atributos)
#
# COBERTURA (coverage): mede quais linhas do seu código foram executadas
# pelos testes. Com o plugin pytest-cov:
#   python -m pip install pytest-cov
#   python -m pytest --cov=loja
# 100% de cobertura NÃO garante ausência de bugs (o teste da média com
# 2 notas "cobria" a linha com bug!), mas cobertura baixa mostra partes
# que NINGUÉM testou.


# =====================================================================
# 14. TDD: ESCREVER O TESTE ANTES DO CÓDIGO
# =====================================================================
# TDD (Test-Driven Development) é uma prática em que você escreve o
# teste ANTES da função, num ciclo curto:
#
#   1. VERMELHO: escreva um teste para algo que ainda não existe.
#                Rode: ele falha (claro!).
#   2. VERDE:    escreva o MÍNIMO de código para o teste passar.
#   3. REFATORE: melhore o código com segurança, porque o teste avisa
#                se quebrar alguma coisa.
#   Repita para o próximo comportamento.
#
# Vantagens: você pensa em COMO a função será usada antes de escrevê-la,
# e todo código nasce testado. Experimente nos exercícios!


# =====================================================================
# 15. ERROS COMUNS
# =====================================================================
# ERRO 1: o teste não roda. O nome do arquivo ou da função não começa
#         com "test". (testar_soma, soma_test dentro de main.py...)
# ERRO 2: ModuleNotFoundError ao importar o seu código nos testes.
#         Rode da pasta certa, com "python -m pytest", e confira o
#         pythonpath no pytest.ini.
# ERRO 3: teste que nunca falha. Um teste sem assert sempre "passa".
#         Dica: quebre o código de propósito e veja se o teste pega.
# ERRO 4: testes que dependem uns dos outros (um teste usa o que o
#         outro criou). Cada teste deve funcionar SOZINHO e em qualquer
#         ordem. Use fixtures.
# ERRO 5: comparar float com ==. Use pytest.approx.
# ERRO 6: testar arquivo/pasta reais do seu computador. Use tmp_path.
# ERRO 7: testar só o caminho feliz. Teste os limites e os erros.


# =====================================================================
# 16. NAMING CONVENTIONS E BOAS PRÁTICAS
# =====================================================================
# NOMES:
#   - Pasta: tests/ (convenção da comunidade, em inglês)
#   - Arquivo: test_<modulo_testado>.py  -> test_precos.py
#   - Função: test_<o_que>_<cenario>_<resultado_esperado>
#       test_aplicar_desconto_acima_de_100_da_erro
#       test_calcular_frete_no_limite_e_gratis
#     Nome LONGO é bom em teste: quando falhar, o nome já diz o que
#     quebrou. Ninguém chama essas funções na mão.
#   - Classe de agrupamento: Test<Assunto>  -> TestTotal
#   - Fixture: substantivo que descreve o cenário -> carrinho_com_itens
#
# BOAS PRÁTICAS:
#   1. Rode os testes SEMPRE antes de commitar.
#   2. Testes rápidos e independentes (sem internet, sem ordem).
#   3. Um comportamento por teste, no padrão AAA.
#   4. Teste o caminho feliz, os limites e os erros.
#   5. Achou um bug? Primeiro escreva um teste que o reproduz (vermelho),
#      depois corrija (verde). Assim ele nunca mais volta.
#   6. Use parametrize em vez de copiar e colar testes.
#   7. Use fixtures (e conftest.py) para preparar cenários.
#   8. Escreva código testável: funções puras, lógica separada de
#      input/print.

print("=" * 60)
print("FIM! Agora rode você mesmo:  python -m pytest -v")
print("Depois vá para os exercícios no final deste arquivo.")
print("=" * 60)


# =====================================================================
# 17. EXERCÍCIOS PARA PRATICAR
# =====================================================================
# Crie os testes dentro da pasta tests/ (ex: tests/test_exercicios.py)
# e rode com:  python -m pytest -v
#
#  1. Escreva 3 testes para a função eh_palindromo do pacote
#     meus_modulos.textos: uma palavra que é palíndromo, uma que não é e
#     uma frase com espaços e maiúsculas.
#  2. Use parametrize para testar celsius_para_fahrenheit (pacote
#     utilidades) com pelo menos 4 pares (celsius, fahrenheit).
#  3. Teste eh_email_valido (utilidades) com parametrize: 4 e-mails
#     válidos e 4 inválidos. Dica: dois parâmetros (email, esperado).
#  4. Teste que reais_para_dolar (utilidades) levanta ValueError quando
#     a cotação é zero ou negativa, conferindo a mensagem com match=.
#  5. Teste calcular_media (meus_modulos.calculos): o caso normal, a
#     lista com um só número, e o ValueError com lista vazia.
#  6. Crie uma fixture lista_tarefas_temporaria que usa tmp_path e teste
#     o pacote tarefas.operacoes: adicionar, concluir, remover e o erro
#     ao adicionar título vazio. (As funções aceitam o caminho do
#     arquivo como parâmetro. Use isso!)
#  7. Teste a classe Carrinho: adicione um teste que verifique que um
#     preço negativo dá erro, e outro que verifique o total de um
#     carrinho exatamente no limite do frete grátis (200.00).
#  8. TDD: escreva PRIMEIRO os testes de uma função
#     calcular_parcelas(valor, vezes) que retorna o valor de cada
#     parcela (arredondado em 2 casas), aceita de 1 a 12 vezes e dá
#     ValueError fora disso. Rode (vermelho), implemente em loja/precos.py
#     (verde) e melhore (refatore).
#  9. Use a fixture capsys para testar uma função que IMPRIME algo:
#        def test_saudacao(capsys):
#            saudar("Ana")
#            assert capsys.readouterr().out == "Olá, Ana!\n"
# 10. (Desafio) Use monkeypatch para testar uma função que usa input().
#     Dica: monkeypatch.setattr("builtins.input", lambda _: "42")
#     Teste o pedir_inteiro do material de erros, simulando primeiro uma
#     entrada inválida e depois uma válida (use um iter() com as
#     respostas).
# 11. (Desafio) Instale o pytest-cov, rode com --cov=loja
#     --cov-report=term-missing e escreva testes até a cobertura do
#     pacote loja chegar a 100%. Depois responda: 100% de cobertura
#     garante que não há bugs? (Lembre da seção 5.)
