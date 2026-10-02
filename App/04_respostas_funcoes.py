"""
=====================================================================
  RESPOSTAS DOS EXERCÍCIOS — 03_funcoes.py
=====================================================================

COMO USAR ESTE ARQUIVO:
  Tente resolver SOZINHO antes de olhar! Depois compare com a resposta.
  Existem várias formas certas de resolver cada exercício; a sua pode
  ser diferente e estar correta.

  Rode:   python 04_respostas_funcoes.py

  Como pedido nos exercícios, as funções RETORNAM valores e não imprimem
  nada. Os print() ficam FORA delas, logo abaixo de cada resposta, só
  para testar e mostrar o resultado.
"""


def imprimir_cabecalho(titulo: str) -> None:
    """Função auxiliar só para separar as respostas na saída."""
    print()
    print("=" * 60)
    print(titulo)
    print("=" * 60)


# =====================================================================
# EXERCÍCIO 1
# Crie eh_impar(numero) que retorna True se o número for ímpar.
# =====================================================================
def eh_impar(numero: int) -> bool:
    # A comparação já resulta em True ou False, então dá para retornar
    # direto. Não precisa de if/else.
    return numero % 2 != 0


# Versão "verbosa" que iniciantes costumam escrever (funciona, mas é
# desnecessariamente longa):
#
#   def eh_impar(numero):
#       if numero % 2 != 0:
#           return True
#       else:
#           return False

imprimir_cabecalho("EXERCÍCIO 1 — eh_impar")
print("eh_impar(7) =", eh_impar(7))
print("eh_impar(10) =", eh_impar(10))
print("eh_impar(-3) =", eh_impar(-3))


# =====================================================================
# EXERCÍCIO 2
# Crie celsius_para_fahrenheit(celsius). Fórmula: F = C * 9/5 + 32.
# Teste com 0 (32.0) e 100 (212.0).
# =====================================================================
def celsius_para_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32


imprimir_cabecalho("EXERCÍCIO 2 — celsius_para_fahrenheit")
print("0 °C   =", celsius_para_fahrenheit(0), "°F")
print("100 °C =", celsius_para_fahrenheit(100), "°F")
print("37 °C  =", celsius_para_fahrenheit(37), "°F")

# Testes automáticos com assert: se a condição for False, o programa
# para com AssertionError. É o jeito mais simples de testar uma função.
assert celsius_para_fahrenheit(0) == 32.0
assert celsius_para_fahrenheit(100) == 212.0
print("Testes com assert passaram!")


# =====================================================================
# EXERCÍCIO 3
# Crie area_retangulo(base, altura=None). Se a altura não for passada,
# calcule a área de um QUADRADO de lado = base.
# =====================================================================
def area_retangulo(base: float, altura: float | None = None) -> float:
    # Usamos None como "não foi passado". Não dá para usar altura=base
    # na definição, porque o valor padrão não pode depender de outro
    # parâmetro.
    if altura is None:
        altura = base
    return base * altura


imprimir_cabecalho("EXERCÍCIO 3 — area_retangulo")
print("retângulo 4 x 3 =", area_retangulo(4, 3))
print("quadrado de lado 5 =", area_retangulo(5))
print("usando nome:", area_retangulo(base=2, altura=10))


# =====================================================================
# EXERCÍCIO 4
# Crie contar_vogais(texto) que retorna quantas vogais tem o texto
# (maiúsculas e minúsculas).
# =====================================================================
def contar_vogais(texto: str) -> int:
    vogais = "aeiouáéíóúâêôãõà"   # incluí as acentuadas do português
    quantidade = 0
    for letra in texto.lower():   # .lower() resolve as maiúsculas
        if letra in vogais:
            quantidade += 1
    return quantidade


# Versão pythônica, em uma linha (com o que você verá mais pra frente):
#   return sum(1 for letra in texto.lower() if letra in vogais)

imprimir_cabecalho("EXERCÍCIO 4 — contar_vogais")
print("'Python' ->", contar_vogais("Python"))
print("'Programação' ->", contar_vogais("Programação"))
print("'AEIOU aeiou' ->", contar_vogais("AEIOU aeiou"))


# =====================================================================
# EXERCÍCIO 5
# Crie maior_da_lista(numeros) SEM usar max(). Retorne None se a lista
# estiver vazia.
# =====================================================================
def maior_da_lista(numeros: list[float]) -> float | None:
    # Tratar o caso especial PRIMEIRO e sair cedo com return.
    # Sem isso, numeros[0] daria IndexError numa lista vazia.
    if not numeros:
        return None

    maior = numeros[0]
    for numero in numeros:
        if numero > maior:
            maior = numero
    return maior


imprimir_cabecalho("EXERCÍCIO 5 — maior_da_lista")
print("[3, 8, 1, 9, 4] ->", maior_da_lista([3, 8, 1, 9, 4]))
print("[-5, -2, -9] ->", maior_da_lista([-5, -2, -9]))
print("[] ->", maior_da_lista([]))

# Por que começar com numeros[0] e não com maior = 0?
# Porque numa lista só de negativos, 0 seria o "maior", e 0 nem está na
# lista! Começar com o primeiro elemento evita esse bug.


# =====================================================================
# EXERCÍCIO 6
# Crie inverter_texto(texto) e eh_palindromo(texto). A segunda deve
# USAR a primeira.
# =====================================================================
def inverter_texto(texto: str) -> str:
    return texto[::-1]


def eh_palindromo(texto: str) -> bool:
    texto_normalizado = texto.lower().replace(" ", "")
    return texto_normalizado == inverter_texto(texto_normalizado)


imprimir_cabecalho("EXERCÍCIO 6 — inverter_texto / eh_palindromo")
print("inverter_texto('Python') =", inverter_texto("Python"))
print("eh_palindromo('arara') =", eh_palindromo("arara"))
print("eh_palindromo('Ame o poema') =", eh_palindromo("Ame o poema"))
print("eh_palindromo('python') =", eh_palindromo("python"))


# =====================================================================
# EXERCÍCIO 7
# Crie media(*notas) que aceita qualquer quantidade de notas.
# media(7, 8, 9) -> 8.0
# =====================================================================
def media(*notas: float) -> float:
    # *notas chega como TUPLA. Se ninguém passar nada, a tupla fica
    # vazia e len(notas) seria 0 -> divisão por zero. Por isso o if.
    if not notas:
        return 0.0
    return sum(notas) / len(notas)


imprimir_cabecalho("EXERCÍCIO 7 — media(*notas)")
print("media(7, 8, 9) =", media(7, 8, 9))
print("media(10, 5) =", media(10, 5))
print("media(6) =", media(6))
print("media() =", media())

notas_do_bimestre = [6.5, 7.0, 9.5, 8.0]
print("media(*lista) =", media(*notas_do_bimestre))   # desempacotando


# =====================================================================
# EXERCÍCIO 8
# Crie calcular_desconto(preco, percentual=10) que retorna o preço com
# desconto. Chame usando argumento nomeado.
# =====================================================================
def calcular_desconto(preco: float, percentual: float = 10) -> float:
    return preco - preco * percentual / 100


imprimir_cabecalho("EXERCÍCIO 8 — calcular_desconto")
print("padrão (10%):", calcular_desconto(200))
print("nomeado (25%):", calcular_desconto(200, percentual=25))
print("tudo nomeado:", calcular_desconto(percentual=50, preco=80))


# =====================================================================
# EXERCÍCIO 9
# Crie fizzbuzz(numero) que RETORNA "Fizz", "Buzz", "FizzBuzz" ou o
# número como texto. Depois use um loop de 1 a 30 para imprimir.
# =====================================================================
def fizzbuzz(numero: int) -> str:
    # Múltiplo de 3 E de 5 é o mesmo que múltiplo de 15.
    # Como cada if tem return, nem precisamos de elif/else.
    if numero % 15 == 0:
        return "FizzBuzz"
    if numero % 3 == 0:
        return "Fizz"
    if numero % 5 == 0:
        return "Buzz"
    return str(numero)


imprimir_cabecalho("EXERCÍCIO 9 — fizzbuzz")
resultados = []
for numero in range(1, 31):
    resultados.append(fizzbuzz(numero))
print(", ".join(resultados))   # junta a lista em um texto, separado por ", "

# Vantagem de RETORNAR em vez de imprimir: dá para testar!
assert fizzbuzz(3) == "Fizz"
assert fizzbuzz(10) == "Buzz"
assert fizzbuzz(30) == "FizzBuzz"
assert fizzbuzz(7) == "7"
print("Testes com assert passaram!")


# =====================================================================
# EXERCÍCIO 10
# Calculadora: somar, subtrair, multiplicar e dividir (dividir retorna
# None se o divisor for 0) e calcular(a, b, operador) que escolhe a
# operação certa pelo operador ("+", "-", "*", "/").
# =====================================================================
def somar(a: float, b: float) -> float:
    return a + b


def subtrair(a: float, b: float) -> float:
    return a - b


def multiplicar(a: float, b: float) -> float:
    return a * b


def dividir(a: float, b: float) -> float | None:
    if b == 0:
        return None
    return a / b


# Solução 1: com if/elif
def calcular(a: float, b: float, operador: str) -> float | None:
    if operador == "+":
        return somar(a, b)
    elif operador == "-":
        return subtrair(a, b)
    elif operador == "*":
        return multiplicar(a, b)
    elif operador == "/":
        return dividir(a, b)
    return None    # operador desconhecido


# Solução 2: com dicionário de funções (funções são valores, seção 11!)
OPERACOES = {
    "+": somar,
    "-": subtrair,
    "*": multiplicar,
    "/": dividir,
}


def calcular_com_dicionario(a: float, b: float, operador: str) -> float | None:
    funcao = OPERACOES.get(operador)   # .get retorna None se não existir
    if funcao is None:
        return None
    return funcao(a, b)


imprimir_cabecalho("EXERCÍCIO 10 — calculadora")
for operador in ["+", "-", "*", "/", "%"]:
    print(f"10 {operador} 4 = {calcular(10, 4, operador)}")
print("10 / 0 =", calcular(10, 0, "/"))
print("com dicionário: 7 * 6 =", calcular_com_dicionario(7, 6, "*"))


# =====================================================================
# EXERCÍCIO 11 (Desafio)
# Crie fibonacci(n) que retorna uma LISTA com os n primeiros números da
# sequência: 0, 1, 1, 2, 3, 5, 8, 13...
# (cada número é a soma dos dois anteriores)
# =====================================================================
def fibonacci(n: int) -> list[int]:
    sequencia = []
    atual, proximo = 0, 1
    for _ in range(n):              # _ porque não usamos a variável
        sequencia.append(atual)
        atual, proximo = proximo, atual + proximo   # o swap do 1º material!
    return sequencia


imprimir_cabecalho("EXERCÍCIO 11 — fibonacci")
print("fibonacci(10) =", fibonacci(10))
print("fibonacci(1) =", fibonacci(1))
print("fibonacci(0) =", fibonacci(0))


# =====================================================================
# EXERCÍCIO 12 (Desafio)
# Crie fatorial(n) com loop, e compare com a versão recursiva.
# =====================================================================
def fatorial_loop(n: int) -> int:
    resultado = 1
    for numero in range(2, n + 1):
        resultado *= numero
    return resultado


def fatorial_recursivo(n: int) -> int:
    if n <= 1:
        return 1
    return n * fatorial_recursivo(n - 1)


imprimir_cabecalho("EXERCÍCIO 12 — fatorial loop vs recursivo")
for n in [0, 1, 5, 10]:
    print(f"{n}! -> loop: {fatorial_loop(n)} | recursivo: {fatorial_recursivo(n)}")

# COMPARAÇÃO:
#   - Recursivo: mais parecido com a definição matemática (n! = n * (n-1)!)
#   - Loop: geralmente mais rápido e não tem limite de profundidade.
#     O Python limita a recursão a ~1000 chamadas. fatorial_recursivo(1500)
#     daria RecursionError, enquanto fatorial_loop(1500) funciona.
print("fatorial_loop(1500) tem", len(str(fatorial_loop(1500))), "dígitos!")

print()
print("=" * 60)
print("FIM DAS RESPOSTAS!")
print("=" * 60)
