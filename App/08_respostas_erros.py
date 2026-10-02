"""
=====================================================================
  RESPOSTAS DOS EXERCÍCIOS — 07_tratamento_erros.py
=====================================================================

COMO USAR ESTE ARQUIVO:
  Tente resolver SOZINHO antes de olhar! Depois compare com a resposta.
  Existem várias formas certas de resolver cada exercício; a sua pode
  ser diferente e estar correta.

  Rode:   python 08_respostas_erros.py

  Os exercícios que NÃO usam input() rodam automaticamente.
  Os que usam input() (2, 3 e 10) ficam num menu no final do arquivo,
  para você testar digitando.
"""

import os
import tempfile


def imprimir_cabecalho(titulo: str) -> None:
    """Função auxiliar só para separar as respostas na saída."""
    print()
    print("=" * 60)
    print(titulo)
    print("=" * 60)


# =====================================================================
# EXERCÍCIO 1
# Crie dividir(a, b) que retorna a / b ou None se b for zero.
# Use try/except (não use if).
# =====================================================================
def dividir(a: float, b: float) -> float | None:
    try:
        return a / b
    except ZeroDivisionError:
        return None


imprimir_cabecalho("EXERCÍCIO 1 — dividir")
print("dividir(10, 4) =", dividir(10, 4))
print("dividir(10, 0) =", dividir(10, 0))


# =====================================================================
# EXERCÍCIO 2
# Crie pedir_inteiro(mensagem) que usa while + input e só retorna
# quando o usuário digitar um inteiro válido.
# =====================================================================
def pedir_inteiro(mensagem: str) -> int:
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Valor inválido, digite um número inteiro.")

# Como funciona:
#   - Se int() der certo, o return SAI da função (e do while).
#   - Se der ValueError, o except avisa e o while repete a pergunta.
# (Teste no menu do final do arquivo.)


# =====================================================================
# EXERCÍCIO 3
# pedir_inteiro_intervalo(mensagem, minimo, maximo) que também rejeita
# números fora do intervalo.
# =====================================================================
def pedir_inteiro_intervalo(mensagem: str, minimo: int, maximo: int) -> int:
    while True:
        # REUTILIZANDO o exercício 2: ele já garante que é um inteiro.
        # Aqui só falta checar o intervalo.
        numero = pedir_inteiro(mensagem)
        if minimo <= numero <= maximo:
            return numero
        print(f"Digite um número entre {minimo} e {maximo}.")

# Repare: "fora do intervalo" não é exceção do Python, é uma REGRA do
# nosso programa. Por isso um simples if resolve. Nem tudo precisa de
# try/except.


# =====================================================================
# EXERCÍCIO 4
# converter_lista(["10", "abc", "5", "x2"]) -> ([10, 5], ["abc", "x2"])
# =====================================================================
def converter_lista(textos: list[str]) -> tuple[list[int], list[str]]:
    validos = []
    invalidos = []
    for texto in textos:
        try:
            validos.append(int(texto))
        except ValueError:
            invalidos.append(texto)
    return validos, invalidos


imprimir_cabecalho("EXERCÍCIO 4 — converter_lista")
numeros, falhas = converter_lista(["10", "abc", "5", "x2"])
print("válidos:  ", numeros)
print("inválidos:", falhas)

# O try fica DENTRO do for: assim um erro afeta só aquele item e o loop
# continua. Se o try envolvesse o for inteiro, o primeiro erro pararia
# tudo. Teste mudar e veja a diferença!


# =====================================================================
# EXERCÍCIO 5
# pegar_elemento(lista, posicao) retorna o elemento ou a mensagem
# "Posição X não existe (a lista tem N itens)".
# =====================================================================
def pegar_elemento(lista: list, posicao: int):
    try:
        return lista[posicao]
    except IndexError:
        return f"Posição {posicao} não existe (a lista tem {len(lista)} itens)"


imprimir_cabecalho("EXERCÍCIO 5 — pegar_elemento")
cores = ["vermelho", "verde", "azul"]
print(pegar_elemento(cores, 1))
print(pegar_elemento(cores, -1))     # índice negativo é válido!
print(pegar_elemento(cores, 10))

# Observação de design: retornar ÀS VEZES o elemento e ÀS VEZES uma
# mensagem de erro (um texto) é arriscado. Quem chama não sabe se
# recebeu "azul" de verdade ou uma mensagem. Em código real, prefira
# retornar None ou deixar o IndexError subir. Aqui fizemos assim porque
# o exercício pediu.


# =====================================================================
# EXERCÍCIO 6
# calcular_imc(peso, altura) faz raise ValueError com mensagem clara se
# peso ou altura forem <= 0. Chame dentro de try/except.
# =====================================================================
def calcular_imc(peso: float, altura: float) -> float:
    if peso <= 0:
        raise ValueError(f"peso deve ser maior que zero, recebi {peso}")
    if altura <= 0:
        raise ValueError(f"altura deve ser maior que zero, recebi {altura}")
    return round(peso / altura ** 2, 2)


imprimir_cabecalho("EXERCÍCIO 6 — calcular_imc com raise")
for peso, altura in [(70, 1.75), (-70, 1.75), (70, 0)]:
    try:
        print(f"IMC({peso}, {altura}) = {calcular_imc(peso, altura)}")
    except ValueError as e:
        print(f"IMC({peso}, {altura}) -> Erro: {e}")

# Por que não retornar None em vez de raise? Porque peso negativo é um
# erro de quem CHAMOU a função. O raise obriga o erro a ser visto. Um
# None poderia passar despercebido e virar um bug lá na frente.


# =====================================================================
# EXERCÍCIO 7
# Função com try/except/else/finally que mostra qual bloco está rodando.
# =====================================================================
def demonstrar_blocos(texto: str) -> None:
    print(f"--- testando com '{texto}' ---")
    try:
        print("  [try]     tentando converter...")
        numero = float(texto)
    except ValueError:
        print("  [except]  deu erro: não é número")
    else:
        print(f"  [else]    deu certo: {numero}")
    finally:
        print("  [finally] sempre roda")


imprimir_cabecalho("EXERCÍCIO 7 — try/except/else/finally")
demonstrar_blocos("3.14")
demonstrar_blocos("pi")


# =====================================================================
# EXERCÍCIO 8
# ler_numero_do_arquivo(caminho): abre, lê e converte para float.
# Trate FileNotFoundError e ValueError com mensagens diferentes.
# =====================================================================
def ler_numero_do_arquivo(caminho: str) -> float | None:
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
        return float(conteudo)          # float ignora espaços e \n nas pontas
    except FileNotFoundError:
        print(f"  Erro: o arquivo '{os.path.basename(caminho)}' não existe.")
    except ValueError:
        print(f"  Erro: o conteúdo {conteudo!r} não é um número.")
    return None


imprimir_cabecalho("EXERCÍCIO 8 — ler_numero_do_arquivo")

# Para testar, criamos arquivos temporários na pasta temp do sistema.
# (Escrever arquivos é o assunto do próximo material: 09_arquivos.py)
pasta_temp = tempfile.gettempdir()
arquivo_ok = os.path.join(pasta_temp, "numero_ok.txt")
arquivo_ruim = os.path.join(pasta_temp, "numero_ruim.txt")

with open(arquivo_ok, "w", encoding="utf-8") as f:
    f.write("42.5\n")
with open(arquivo_ruim, "w", encoding="utf-8") as f:
    f.write("quarenta e dois")

print("arquivo ok:", ler_numero_do_arquivo(arquivo_ok))
print("arquivo ruim:", ler_numero_do_arquivo(arquivo_ruim))
print("arquivo inexistente:", ler_numero_do_arquivo(os.path.join(pasta_temp, "nao_existe.txt")))

os.remove(arquivo_ok)        # limpando os arquivos de teste
os.remove(arquivo_ruim)


# =====================================================================
# EXERCÍCIO 9
# Exceção EstoqueInsuficienteError e retirar_do_estoque(estoque,
# produto, quantidade):
#   - raise KeyError se o produto não existir
#   - raise EstoqueInsuficienteError se não houver quantidade
#   - senão, diminui o estoque
# =====================================================================
class EstoqueInsuficienteError(Exception):
    pass


def retirar_do_estoque(estoque: dict[str, int], produto: str, quantidade: int) -> None:
    if produto not in estoque:
        raise KeyError(f"produto '{produto}' não cadastrado")
    disponivel = estoque[produto]
    if quantidade > disponivel:
        raise EstoqueInsuficienteError(
            f"'{produto}': pedido {quantidade}, disponível {disponivel}"
        )
    estoque[produto] -= quantidade


imprimir_cabecalho("EXERCÍCIO 9 — EstoqueInsuficienteError")
estoque = {"caneta": 10, "caderno": 2}

pedidos = [
    ("caneta", 3),      # cenário 1: dá certo
    ("caderno", 5),     # cenário 2: estoque insuficiente
    ("borracha", 1),    # cenário 3: produto não existe
]

for produto, quantidade in pedidos:
    try:
        retirar_do_estoque(estoque, produto, quantidade)
        print(f"  OK: retirou {quantidade}x {produto}")
    except EstoqueInsuficienteError as e:
        print(f"  Estoque insuficiente -> {e}")
    except KeyError as e:
        # Curiosidade: a mensagem do KeyError aparece com aspas extras
        # quando impressa direto. e.args[0] pega o texto "limpo".
        print(f"  Produto inválido -> {e.args[0]}")

print("  estoque final:", estoque)


# =====================================================================
# EXERCÍCIO 10 (Desafio)
# Calculadora segura: lê "10 / 2" e trata formato inválido, número
# inválido, operador desconhecido e divisão por zero. Repete até "sair".
# =====================================================================
# A ideia mais importante aqui: SEPARAR a lógica (avaliar_expressao,
# que recebe texto e devolve texto) da interação com o usuário (o loop
# com input). Assim a lógica pode ser testada sem digitar nada.

OPERACOES = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


def avaliar_expressao(expressao: str) -> str:
    partes = expressao.split()
    if len(partes) != 3:
        return "Formato inválido. Use: número operador número (ex: 10 / 2)"

    texto_a, operador, texto_b = partes

    try:
        a = float(texto_a)
        b = float(texto_b)
    except ValueError:
        return f"Número inválido em '{expressao}'"

    if operador not in OPERACOES:
        return f"Operador desconhecido: '{operador}'. Use + - * /"

    try:
        resultado = OPERACOES[operador](a, b)
    except ZeroDivisionError:
        return "Não é possível dividir por zero"

    return f"{expressao} = {resultado:g}"   # :g tira o ".0" desnecessário


def calculadora() -> None:
    print("Calculadora segura. Digite 'sair' para encerrar.")
    while True:
        expressao = input("> ").strip()
        if expressao.lower() == "sair":
            print("Até mais!")
            break
        print(avaliar_expressao(expressao))


imprimir_cabecalho("EXERCÍCIO 10 — calculadora segura (testes automáticos)")
for teste in ["10 / 2", "3 * 1.5", "10/2", "dez + 2", "5 % 2", "8 / 0", "7 - 10"]:
    print(f"  {teste!r:<11} -> {avaliar_expressao(teste)}")


# =====================================================================
# MENU — exercícios interativos (com input)
# =====================================================================
INTERATIVOS = {
    "2": lambda: print("Você digitou:", pedir_inteiro("Digite um inteiro: ")),
    "3": lambda: print("Você digitou:", pedir_inteiro_intervalo("Nota de 0 a 10: ", 0, 10)),
    "10": calculadora,
}

imprimir_cabecalho("EXERCÍCIOS INTERATIVOS")
while True:
    escolha = input("Testar qual? (2, 3, 10 ou Enter para sair): ").strip()
    if escolha == "":
        print("Fim das respostas!")
        break
    if escolha in INTERATIVOS:
        INTERATIVOS[escolha]()
    else:
        print("Opção inválida.")
