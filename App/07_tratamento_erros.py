"""
=====================================================================
  MATERIAL DE ESTUDO PYTHON — TRATAMENTO DE ERROS (try/except)
  Tipos de erro -> Lendo o traceback -> try/except -> Exceções
  específicas -> as e -> else/finally -> raise -> Exceções próprias ->
  Validação de entrada -> EAFP vs LBYL -> with -> Boas práticas
=====================================================================

PRÉ-REQUISITOS: 01_fundamentos, 03_funcoes e 05_dicionarios.

COMO USAR ESTE ARQUIVO:
  1. Leia os comentários de cima para baixo.
  2. Rode no terminal:   python 07_tratamento_erros.py
  3. Repare que o programa NÃO quebra, mesmo provocando vários erros.
     Esse é justamente o objetivo do tratamento de erros.
  4. Experimente tirar um try/except e veja o programa quebrar.
"""


# =====================================================================
# 1. ERROS EXISTEM, E TUDO BEM
# =====================================================================
# Existem dois grandes tipos de erro em Python:
#
# 1) ERRO DE SINTAXE (SyntaxError): o código está escrito errado.
#    O Python nem começa a rodar o arquivo. Ex: esquecer os dois pontos.
#        if idade > 18        <- falta o ":"
#    Esse você CORRIGE no código, não "trata".
#
# 2) EXCEÇÃO (exception): o código está escrito certo, mas algo dá
#    errado DURANTE a execução. Ex: dividir por zero, abrir um arquivo
#    que não existe, converter "abc" para int, acessar chave inexistente.
#    Essas você pode TRATAR com try/except.
#
# Sem tratamento, uma exceção PARA o programa inteiro na hora.
# Com tratamento, você decide o que fazer: avisar o usuário, tentar de
# novo, usar um valor padrão, registrar o erro...


# =====================================================================
# 2. LENDO UMA MENSAGEM DE ERRO (TRACEBACK)
# =====================================================================
# Quando um erro não é tratado, o Python mostra um "traceback".
# Iniciantes costumam ter medo dele, mas ele diz EXATAMENTE o que houve.
# LEIA DE BAIXO PARA CIMA:
#
#   Traceback (most recent call last):
#     File "exemplo.py", line 7, in <module>
#       resultado = calcular_media([])
#     File "exemplo.py", line 3, in calcular_media
#       return sum(notas) / len(notas)
#              ~~~~~~~~~~~^~~~~~~~~~~~
#   ZeroDivisionError: division by zero
#
#   - ÚLTIMA LINHA: o TIPO do erro (ZeroDivisionError) e a MENSAGEM
#     (division by zero). Comece sempre por aqui.
#   - Logo acima: o ARQUIVO, a LINHA e o código exato onde quebrou.
#   - Mais acima: o "caminho" de chamadas que levou até lá (a linha 7
#     chamou calcular_media, que quebrou na linha 3).
#
# Dica de ouro: copie a ÚLTIMA linha do erro e pesquise. Alguém já teve
# o mesmo problema.


# =====================================================================
# 3. AS EXCEÇÕES MAIS COMUNS
# =====================================================================
# ---------------------------------------------------------------------
#  EXCEÇÃO            | QUANDO ACONTECE                | EXEMPLO
# ---------------------------------------------------------------------
#  ValueError         | tipo certo, valor inválido     | int("abc")
#  TypeError          | tipo errado para a operação    | "5" + 3
#  ZeroDivisionError  | divisão por zero               | 10 / 0
#  KeyError           | chave não existe no dict       | {}["x"]
#  IndexError         | posição não existe na lista    | [1, 2][5]
#  NameError          | variável/função não existe     | print(xyz)
#  AttributeError     | método/atributo não existe     | "abc".push()
#  FileNotFoundError  | arquivo não encontrado         | open("nada.txt")
#  ImportError /      | módulo não encontrado          | import modulo_x
#  ModuleNotFoundError|                                |
#  RecursionError     | recursão profunda demais       | (visto em funções)
# ---------------------------------------------------------------------

print("=" * 60)
print("3. PROVOCANDO (E CAPTURANDO) OS ERROS MAIS COMUNS")
print("=" * 60)

# Não se preocupe com a sintaxe ainda, ela é explicada logo abaixo.
# Aqui é só para VER o nome de cada erro sem o programa quebrar.
exemplos_de_erro = [
    ('int("abc")', lambda: int("abc")),
    ('"5" + 3', lambda: "5" + 3),
    ("10 / 0", lambda: 10 / 0),
    ('{}["x"]', lambda: {}["x"]),
    ("[1, 2][5]", lambda: [1, 2][5]),
    ('"abc".push()', lambda: "abc".push()),
    ('open("nada.txt")', lambda: open("nada.txt")),
]

for codigo, funcao in exemplos_de_erro:
    try:
        funcao()
    except Exception as erro:
        print(f"{codigo:<18} -> {type(erro).__name__}: {erro}")
print()


# =====================================================================
# 4. try / except: O BÁSICO
# =====================================================================
# Sintaxe:
#
#   try:
#       código que PODE dar erro
#   except TipoDoErro:
#       o que fazer SE der esse erro
#
# Funcionamento:
#   - O Python executa o bloco try.
#   - Se NÃO der erro: pula o except inteiro e segue a vida.
#   - Se der erro: PARA o try naquele ponto (o resto do try não roda),
#     pula para o except e depois continua normalmente o programa.

print("=" * 60)
print("4. try / except BÁSICO")
print("=" * 60)

texto_digitado = "abc"       # imagine que veio de um input()

try:
    numero = int(texto_digitado)
    print("Esta linha NÃO roda, porque a de cima deu erro")
except ValueError:
    print(f"'{texto_digitado}' não é um número válido!")

print("O programa continuou normalmente depois do erro")

texto_digitado = "42"
try:
    numero = int(texto_digitado)
    print(f"Convertido com sucesso: {numero}")
except ValueError:
    print("Isto não roda, porque não houve erro")
print()


# =====================================================================
# 5. CAPTURANDO EXCEÇÕES ESPECÍFICAS
# =====================================================================
# SEMPRE diga QUAL erro você espera. Um mesmo try pode ter vários
# except, cada um tratando um tipo diferente. O Python testa de cima
# para baixo e usa o PRIMEIRO que combinar.

print("=" * 60)
print("5. VÁRIOS except")
print("=" * 60)


def dividir_textos(a: str, b: str) -> None:
    try:
        resultado = int(a) / int(b)
        print(f"  {a} / {b} = {resultado}")
    except ValueError:
        print(f"  Erro: '{a}' ou '{b}' não é número")
    except ZeroDivisionError:
        print("  Erro: não dá para dividir por zero")


dividir_textos("10", "2")
dividir_textos("10", "x")
dividir_textos("10", "0")


# Vários erros com o MESMO tratamento: use uma tupla
def pegar_item(colecao, posicao):
    try:
        return colecao[posicao]
    except (IndexError, KeyError):
        return "item não encontrado"


print("lista[0]:", pegar_item([10, 20], 0))
print("lista[9]:", pegar_item([10, 20], 9))
print("dict['x']:", pegar_item({"a": 1}, "x"))
print()


# =====================================================================
# 6. ACESSANDO O ERRO: except ... as erro
# =====================================================================
# "as nome" guarda o objeto da exceção numa variável. Com ela você pode
# mostrar a mensagem original, registrar em log etc.

print("=" * 60)
print("6. except ... as erro")
print("=" * 60)

try:
    int("doze")
except ValueError as erro:
    print("Mensagem do erro:", erro)
    print("Tipo do erro:", type(erro).__name__)

# Convenção de nome: "erro", "e", "exc" ou "error". O mais comum em
# código profissional é "e" ou "exc". Escolha um e seja consistente.
print()


# =====================================================================
# 7. else E finally
# =====================================================================
#   try:      tenta
#   except:   roda SE deu erro
#   else:     roda SE NÃO deu erro
#   finally:  roda SEMPRE (dando erro ou não). Usado para "limpeza":
#             fechar arquivo, fechar conexão, liberar recurso...

print("=" * 60)
print("7. else E finally")
print("=" * 60)


def converter_idade(texto: str) -> None:
    print(f"  Convertendo '{texto}'...")
    try:
        idade = int(texto)
    except ValueError:
        print("  [except]  valor inválido")
    else:
        # Por que não colocar isto dentro do try? Para deixar o try
        # PEQUENO, só com a linha que pode dar o erro esperado.
        print(f"  [else]    sucesso! idade = {idade}")
    finally:
        print("  [finally] fim da tentativa (sempre roda)")


converter_idade("30")
converter_idade("trinta")

# O finally roda até se tiver um return no meio do try!
def exemplo_finally_com_return() -> str:
    try:
        return "valor do try"
    finally:
        print("  finally rodou ANTES de a função devolver o valor")


print(" ", exemplo_finally_com_return())
print()


# =====================================================================
# 8. TRATAMENTO DE ERROS DENTRO DE FUNÇÕES
# =====================================================================
# Uma função que pode falhar tem basicamente duas opções:
#   a) TRATAR e devolver um valor padrão (None, 0, "")
#   b) DEIXAR o erro subir para quem chamou decidir o que fazer
#
# Os erros "sobem" pela pilha de chamadas até alguém capturá-los. Se
# ninguém capturar, o programa quebra (e aparece o traceback).

print("=" * 60)
print("8. ERROS EM FUNÇÕES")
print("=" * 60)


# Opção a) trata e devolve padrão
def converter_para_int(texto: str, padrao: int = 0) -> int:
    try:
        return int(texto)
    except ValueError:
        return padrao


print("converter_para_int('15'):", converter_para_int("15"))
print("converter_para_int('xx'):", converter_para_int("xx"))
print("converter_para_int('xx', -1):", converter_para_int("xx", padrao=-1))


# Opção b) a função não trata, quem chama trata
def calcular_media(notas: list[float]) -> float:
    return sum(notas) / len(notas)       # pode dar ZeroDivisionError


def gerar_relatorio(notas: list[float]) -> str:
    try:
        return f"Média: {calcular_media(notas):.1f}"
    except ZeroDivisionError:            # o erro "subiu" de calcular_media
        return "Sem notas para calcular a média"


print(gerar_relatorio([7, 8, 9]))
print(gerar_relatorio([]))
print()


# =====================================================================
# 9. LANÇANDO ERROS: raise
# =====================================================================
# Você também pode CRIAR erros de propósito com raise. Use quando sua
# função recebe algo que ela não consegue (ou não deve) processar.
#
# É melhor quebrar cedo com uma mensagem clara do que seguir com dados
# errados e quebrar lá na frente com um erro confuso.
# (Princípio "fail fast": falhe rápido.)

print("=" * 60)
print("9. raise")
print("=" * 60)


def definir_idade(idade: int) -> int:
    if not isinstance(idade, int):       # isinstance verifica o tipo
        raise TypeError(f"idade deve ser int, recebi {type(idade).__name__}")
    if idade < 0 or idade > 150:
        raise ValueError(f"idade fora do intervalo válido: {idade}")
    return idade


for valor in [30, -5, "trinta"]:
    try:
        print(f"  definir_idade({valor!r}) = {definir_idade(valor)}")
    except (ValueError, TypeError) as e:
        print(f"  definir_idade({valor!r}) -> {type(e).__name__}: {e}")
# {valor!r} mostra a "representação" do valor: strings aparecem com aspas


# Relançando: tratar parcialmente (ex: registrar) e deixar o erro seguir
def processar(valor: str) -> int:
    try:
        return int(valor)
    except ValueError:
        print("  [log] falha ao processar, repassando o erro...")
        raise           # raise sozinho relança o MESMO erro


try:
    processar("abc")
except ValueError as e:
    print("  Quem chamou recebeu:", e)


# Trocando o tipo do erro, mas mantendo a causa original com "from"
def ler_config(config: dict) -> int:
    try:
        return int(config["porta"])
    except KeyError as e:
        raise ValueError("configuração sem o campo 'porta'") from e


try:
    ler_config({"host": "localhost"})
except ValueError as e:
    print("  Erro:", e, "| causa original:", repr(e.__cause__))
print()


# =====================================================================
# 10. CRIANDO SUAS PRÓPRIAS EXCEÇÕES
# =====================================================================
# Em sistemas maiores, é útil ter erros com nomes do SEU domínio:
# SaldoInsuficienteError, UsuarioNaoEncontradoError...
#
# Isso usa "class", que é um assunto futuro. Por enquanto, copie o
# padrão: é só uma linha com "class NomeError(Exception): pass".
# Convenção: o nome termina com "Error" e é em PascalCase.

print("=" * 60)
print("10. EXCEÇÕES PRÓPRIAS")
print("=" * 60)


class SaldoInsuficienteError(Exception):
    pass


def sacar(saldo: float, valor: float) -> float:
    if valor <= 0:
        raise ValueError("o valor do saque deve ser positivo")
    if valor > saldo:
        raise SaldoInsuficienteError(f"saldo R$ {saldo:.2f}, saque R$ {valor:.2f}")
    return saldo - valor


saldo = 100.0
for valor_saque in [30, 500, -10]:
    try:
        saldo = sacar(saldo, valor_saque)
        print(f"  Sacou R$ {valor_saque}. Novo saldo: R$ {saldo:.2f}")
    except SaldoInsuficienteError as e:
        print(f"  Saque negado. {e}")
    except ValueError as e:
        print(f"  Valor inválido: {e}")
print()


# =====================================================================
# 11. PADRÃO REAL: VALIDAR ENTRADA DO USUÁRIO ATÉ ACERTAR
# =====================================================================
# Este é provavelmente o uso nº 1 de try/except para iniciantes:
#
#   def pedir_inteiro(mensagem: str) -> int:
#       while True:
#           try:
#               return int(input(mensagem))
#           except ValueError:
#               print("Valor inválido, digite um número inteiro.")
#
#   idade = pedir_inteiro("Sua idade: ")
#
# O return dentro do try sai da função (e do loop) quando dá certo.
# Se der erro, o except avisa e o while pede de novo.
#
# Abaixo, a mesma lógica SIMULANDO o que o usuário digitaria, para o
# arquivo rodar sem parar esperando você.

print("=" * 60)
print("11. VALIDANDO ENTRADA (simulada)")
print("=" * 60)


def pedir_inteiro_simulado(respostas: list[str]) -> int:
    for resposta in respostas:           # no código real: while True + input
        print(f"  Sua idade: {resposta}")
        try:
            return int(resposta)
        except ValueError:
            print("  Valor inválido, digite um número inteiro.")
    raise ValueError("o usuário não digitou nenhum número válido")


idade = pedir_inteiro_simulado(["vinte", "", "20.5", "20"])
print(f"  Idade aceita: {idade}")
print()


# =====================================================================
# 12. EAFP vs LBYL (dois estilos de lidar com problemas)
# =====================================================================
# LBYL: "Look Before You Leap" (olhe antes de pular)
#   -> verifica com if ANTES de fazer
# EAFP: "Easier to Ask Forgiveness than Permission"
#   (é mais fácil pedir perdão do que permissão)
#   -> tenta fazer e trata o erro SE acontecer
#
# O estilo EAFP é considerado mais "pythônico", mas os dois são válidos.
# Use o que deixar o código mais claro em cada caso.

print("=" * 60)
print("12. EAFP vs LBYL")
print("=" * 60)

estoque = {"maçã": 10}

# LBYL
if "banana" in estoque:
    quantidade = estoque["banana"]
else:
    quantidade = 0
print("LBYL:", quantidade)

# EAFP
try:
    quantidade = estoque["banana"]
except KeyError:
    quantidade = 0
print("EAFP:", quantidade)

# E nesse caso específico, o mais simples de todos:
print("get: ", estoque.get("banana", 0))

# Onde EAFP brilha: converter texto. Verificar ANTES se "texto é um
# número válido" é difícil ("-3", "1e5", " 7 "...). Tentar e tratar
# é muito mais simples.
texto = " -7 "
print("isdigit diz:", texto.isdigit(), "| mas int() consegue:", converter_para_int(texto))
print()


# =====================================================================
# 13. with: LIMPEZA AUTOMÁTICA (prévia de arquivos)
# =====================================================================
# Ao abrir um arquivo, ele precisa ser FECHADO, mesmo se der erro no
# meio. Dá para fazer com try/finally:
#
#   arquivo = open("dados.txt")
#   try:
#       conteudo = arquivo.read()
#   finally:
#       arquivo.close()
#
# Mas o Python tem o "with", que faz isso automaticamente. É a forma
# correta e recomendada (você verá a fundo no material de arquivos):
#
#   with open("dados.txt") as arquivo:
#       conteudo = arquivo.read()
#   # aqui o arquivo já está fechado, com erro ou sem erro

print("=" * 60)
print("13. with + try/except")
print("=" * 60)


def ler_arquivo(caminho: str) -> str:
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        return f"(arquivo '{caminho}' não encontrado)"


print(ler_arquivo("config_inexistente.txt"))
print("Este próprio arquivo tem", len(ler_arquivo(__file__).splitlines()), "linhas")
# __file__ é uma variável especial com o caminho do arquivo atual
print()


# =====================================================================
# 14. A HIERARQUIA DAS EXCEÇÕES (por que a ordem do except importa)
# =====================================================================
# Exceções formam uma "árvore familiar". Capturar a "mãe" também
# captura todas as "filhas". Um pedaço da árvore:
#
#   BaseException
#    ├── KeyboardInterrupt      (Ctrl + C)
#    ├── SystemExit             (sys.exit())
#    └── Exception              <- a mãe de quase todos os erros comuns
#         ├── ArithmeticError
#         │    └── ZeroDivisionError
#         ├── LookupError
#         │    ├── IndexError
#         │    └── KeyError
#         ├── OSError
#         │    └── FileNotFoundError
#         ├── TypeError
#         └── ValueError
#
# Por isso: coloque os except mais ESPECÍFICOS PRIMEIRO e os mais
# genéricos DEPOIS. Senão o genérico "rouba" todos os erros.

print("=" * 60)
print("14. HIERARQUIA")
print("=" * 60)

try:
    [1, 2, 3][10]
except LookupError as e:          # captura IndexError E KeyError
    print("LookupError capturou um", type(e).__name__)

print("IndexError é um LookupError?", issubclass(IndexError, LookupError))
print("ValueError é um Exception?", issubclass(ValueError, Exception))
print()


# =====================================================================
# 15. ERROS COMUNS (e más práticas)
# =====================================================================

print("=" * 60)
print("15. MÁS PRÁTICAS")
print("=" * 60)

# ❌ RUIM 1: except "pelado" (sem tipo). Captura TUDO, até Ctrl+C e
#    erros de digitação no SEU código, escondendo bugs.
#
#    try:
#        resultado = calcular()
#    except:
#        pass

# ❌ RUIM 2: engolir o erro em silêncio com pass. O erro acontece e
#    ninguém fica sabendo. Bugs assim levam HORAS para serem achados.
#    Se for ignorar um erro, que seja um erro ESPECÍFICO e de propósito.

# ❌ RUIM 3: try gigante. Se 30 linhas estão no try, você não sabe qual
#    linha deu o erro esperado, e pode capturar um erro que não devia.
#    Deixe no try SÓ a(s) linha(s) que podem dar o erro esperado.

# ❌ RUIM 4: usar try/except para controlar o fluxo normal quando um
#    simples if resolve de forma clara. (Bom senso: veja a seção 12.)

# ❌ RUIM 5: except Exception logo no começo, tratando tudo igual.
#    Às vezes é necessário (ex: no nível mais alto do programa, para
#    registrar qualquer erro inesperado), mas não como padrão.

# Demonstrando por que except "pelado" esconde bugs:
def bugada():
    return variavel_que_nao_existe     # bug de digitação: NameError


try:
    bugada()
except Exception:
    print("❌ 'Algo deu errado'... mas O QUÊ? Um NameError foi escondido!")

try:
    bugada()
except ValueError:
    print("Isto não roda")
except NameError as e:
    print(f"✅ Sendo específico, eu vejo o bug real: {e}")
print()


# =====================================================================
# 16. NAMING CONVENTIONS E BOAS PRÁTICAS
# =====================================================================
# NOMES:
#   - Exceções próprias: PascalCase terminando em "Error"
#       SaldoInsuficienteError, UsuarioNaoEncontradoError
#   - Variável do erro: e, exc, erro (seja consistente)
#       except ValueError as e:
#
# BOAS PRÁTICAS:
#   1. Capture SEMPRE exceções específicas (ValueError, KeyError...).
#   2. Deixe o bloco try o MENOR possível.
#   3. Nunca silencie erros sem motivo (except: pass).
#   4. Mensagens de erro claras e úteis: diga O QUE e QUAL valor.
#       ruim: raise ValueError("erro")
#       bom:  raise ValueError(f"idade deve estar entre 0 e 150, recebi {idade}")
#   5. Use raise para validar entradas das suas funções (fail fast).
#   6. Use finally ou with para liberar recursos (arquivos, conexões).
#   7. Trate o erro onde você SABE o que fazer com ele. Se a função não
#      sabe o que fazer, deixe o erro subir.
#   8. Erros esperados do usuário (digitou letra em vez de número) ->
#      trate e explique. Bugs do programador (NameError, TypeError por
#      erro seu) -> NÃO esconda. Corrija o código.

print("=" * 60)
print("FIM! Agora vá para os exercícios no final do arquivo.")
print("=" * 60)


# =====================================================================
# 17. EXERCÍCIOS PARA PRATICAR
# =====================================================================
# Crie um arquivo novo (ex: exercicios_erros.py).
#
#  1. Crie dividir(a, b) que retorna a / b ou None se b for zero.
#     Use try/except (não use if).
#  2. Crie pedir_inteiro(mensagem) que usa while + input e só retorna
#     quando o usuário digitar um inteiro válido.
#  3. Melhore o anterior: pedir_inteiro_intervalo(mensagem, minimo,
#     maximo) que também rejeita números fora do intervalo.
#  4. Crie converter_lista(textos) que recebe ["10", "abc", "5", "x2"]
#     e retorna ([10, 5], ["abc", "x2"]): os números válidos e os que
#     falharam.
#  5. Crie pegar_elemento(lista, posicao) que retorna o elemento ou a
#     mensagem "Posição X não existe (a lista tem N itens)".
#  6. Crie calcular_imc(peso, altura) que faz raise ValueError com
#     mensagem clara se peso ou altura forem <= 0. Depois chame dentro
#     de um try/except e mostre a mensagem.
#  7. Crie uma função com try/except/else/finally que mostre na tela
#     qual bloco está rodando. Teste com e sem erro.
#  8. Crie ler_numero_do_arquivo(caminho) que abre um arquivo, lê o
#     conteúdo e converte para float. Trate FileNotFoundError e
#     ValueError com mensagens diferentes.
#  9. Crie a exceção EstoqueInsuficienteError e a função
#     retirar_do_estoque(estoque, produto, quantidade), que:
#       - faz raise KeyError se o produto não existir
#       - faz raise EstoqueInsuficienteError se não houver quantidade
#       - senão, diminui o estoque
#     Teste os três cenários.
# 10. (Desafio) Calculadora segura: leia uma expressão no formato
#     "10 / 2" (número, espaço, operador, espaço, número). Trate:
#     formato inválido, número inválido, operador desconhecido e divisão
#     por zero, cada um com uma mensagem diferente. Repita até o
#     usuário digitar "sair".
