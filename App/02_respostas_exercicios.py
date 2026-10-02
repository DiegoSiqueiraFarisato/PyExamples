"""
=====================================================================
  RESPOSTAS DOS EXERCÍCIOS — 01_fundamentos_python.py
=====================================================================

COMO USAR ESTE ARQUIVO:
  Tente resolver SOZINHO antes de olhar! Depois compare com a resposta.
  Existem várias formas certas de resolver cada exercício; a sua pode
  ser diferente e estar correta.

  Rode:   python 02_respostas_exercicios.py
  Um menu vai perguntar qual exercício você quer executar.

SOBRE O "def":
  Cada exercício está dentro de uma FUNÇÃO (def exercicio_1(): ...).
  Funções são o próximo tópico de estudo. Por enquanto, entenda só isto:
  "def" agrupa um bloco de código com um nome, e esse bloco só roda
  quando chamamos o nome, ex: exercicio_1(). Assim o menu escolhe qual
  exercício rodar, em vez de rodar todos de uma vez.
  O código DENTRO de cada função é exatamente o que você escreveria
  solto no arquivo.
"""

import random   # módulo nativo do Python para gerar números aleatórios


# =====================================================================
# EXERCÍCIO 1
# Crie variáveis com seu nome, idade e cidade e imprima uma frase
# usando f-string.
# =====================================================================
def exercicio_1():
    nome = "Diego"
    idade = 31
    cidade = "São Paulo"

    print(f"Meu nome é {nome}, tenho {idade} anos e moro em {cidade}.")


# =====================================================================
# EXERCÍCIO 2
# Peça dois números com input(), converta para int e mostre soma,
# subtração, multiplicação e divisão.
# =====================================================================
def exercicio_2():
    # input() sempre retorna str, por isso o int(...) em volta
    numero_1 = int(input("Digite o primeiro número: "))
    numero_2 = int(input("Digite o segundo número: "))

    print(f"{numero_1} + {numero_2} = {numero_1 + numero_2}")
    print(f"{numero_1} - {numero_2} = {numero_1 - numero_2}")
    print(f"{numero_1} * {numero_2} = {numero_1 * numero_2}")

    # Dividir por zero gera erro (ZeroDivisionError), então verificamos antes
    if numero_2 != 0:
        print(f"{numero_1} / {numero_2} = {numero_1 / numero_2:.2f}")
    else:
        print("Não é possível dividir por zero.")


# =====================================================================
# EXERCÍCIO 3
# Peça um número e diga se ele é par ou ímpar.
# =====================================================================
def exercicio_3():
    numero = int(input("Digite um número: "))

    # Um número é par quando o RESTO da divisão por 2 é zero
    if numero % 2 == 0:
        print(f"{numero} é PAR")
    else:
        print(f"{numero} é ÍMPAR")


# =====================================================================
# EXERCÍCIO 4
# Peça uma nota de 0 a 10 e mostre o conceito (A, B, C ou Reprovado).
# =====================================================================
def exercicio_4():
    nota = float(input("Digite a nota (0 a 10): "))   # float aceita 7.5

    # Primeiro validamos se a nota faz sentido
    if nota < 0 or nota > 10:
        print("Nota inválida! Digite um valor entre 0 e 10.")
    elif nota >= 9:
        print("Conceito A")
    elif nota >= 7:
        print("Conceito B")
    elif nota >= 5:
        print("Conceito C")
    else:
        print("Reprovado")


# =====================================================================
# EXERCÍCIO 5
# Imprima a tabuada de um número de 1 a 10 usando for + range.
# a diferença entre uma procedure e uma função é que a função retorna um valor, enquanto a procedure não retorna nada.
# =====================================================================
def exercicio_5():
    numero = int(input("Tabuada de qual número? "))

    # range(1, 11) gera 1, 2, ..., 10 (o 11 NÃO entra)
    for multiplicador in range(1, 11):    
        print(f"{numero} x {multiplicador:2} = {numero * multiplicador}")
        # :2 reserva 2 espaços para o número, deixando a tabuada alinhada
    
# =====================================================================
# EXERCÍCIO 6
# Some todos os números de 1 a 100 usando um loop (resposta: 5050).
# =====================================================================
def exercicio_6():
    # Solução 1: com for (padrão acumulador)
    total = 0
    for numero in range(1, 101):
        total += numero
    print(f"Soma com for:   {total}")

    # Solução 2: com while
    total = 0
    numero = 1
    while numero <= 100:
        total += numero
        numero += 1
    print(f"Soma com while: {total}")

    # Solução 3: jeito pythônico (sem loop explícito)
    print(f"Soma com sum(): {sum(range(1, 101))}")


# =====================================================================
# EXERCÍCIO 7
# Dada a lista [3, 8, 1, 9, 4], encontre o maior número SEM usar max().
# =====================================================================
def exercicio_7():
    numeros = [3, 8, 1, 9, 4]

    # Ideia: assumir que o primeiro é o maior e comparar com os outros.
    # Sempre que achar um número maior, ele vira o novo "maior".
    maior = numeros[0]
    for numero in numeros:
        if numero > maior:
            maior = numero

    print(f"Lista: {numeros}")
    print(f"Maior número: {maior}")


# =====================================================================
# EXERCÍCIO 8
# "Adivinhe o número": o programa guarda um número secreto e pede
# palpites com while até o usuário acertar, dizendo "maior" ou "menor"
# a cada tentativa. Conte as tentativas.
# =====================================================================
def exercicio_8():
    # random.randint(1, 100) sorteia um inteiro entre 1 e 100 (incluindo ambos)
    numero_secreto = random.randint(1, 100)
    tentativas = 0

    print("Pensei em um número entre 1 e 100. Tente adivinhar!")

    while True:
        palpite = int(input("Seu palpite: "))
        tentativas += 1

        if palpite < numero_secreto:
            print("O número secreto é MAIOR.")
        elif palpite > numero_secreto:
            print("O número secreto é MENOR.")
        else:
            print(f"Acertou! O número era {numero_secreto}.")
            print(f"Você precisou de {tentativas} tentativa(s).")
            break   # sai do while True


# =====================================================================
# EXERCÍCIO 9
# Peça uma palavra e diga se é palíndromo (ex: "arara").
# =====================================================================
def exercicio_9():
    palavra = input("Digite uma palavra: ")

    # Normalizamos para que "Arara" e "arara" sejam tratadas igual,
    # e removemos espaços para funcionar com frases ("ame o poema")
    palavra_normalizada = palavra.lower().replace(" ", "")

    # [::-1] inverte a string
    if palavra_normalizada == palavra_normalizada[::-1]:
        print(f"'{palavra}' É um palíndromo!")
    else:
        print(f"'{palavra}' NÃO é um palíndromo.")


# =====================================================================
# EXERCÍCIO 10
# Percorra os números de 1 a 30: imprima "Fizz" se for múltiplo de 3,
# "Buzz" se múltiplo de 5, "FizzBuzz" se de ambos, senão o número.
# =====================================================================
def exercicio_10():
    for numero in range(1, 31):
        # A ORDEM IMPORTA: testamos "ambos" primeiro. Se testássemos
        # "múltiplo de 3" antes, o 15 imprimiria só "Fizz".
        if numero % 3 == 0 and numero % 5 == 0:
            print("FizzBuzz")
        elif numero % 3 == 0:
            print("Fizz")
        elif numero % 5 == 0:
            print("Buzz")
        else:
            print(numero)


# =====================================================================
# MENU — escolhe qual exercício rodar
# =====================================================================
EXERCICIOS = {
    "1": exercicio_1,
    "2": exercicio_2,
    "3": exercicio_3,
    "4": exercicio_4,
    "5": exercicio_5,
    "6": exercicio_6,
    "7": exercicio_7,
    "8": exercicio_8,
    "9": exercicio_9,
    "10": exercicio_10,
}

while True:
    print()
    print("=" * 40)
    escolha = input("Qual exercício rodar? (1 a 10, ou 's' para sair): ").strip()

    if escolha.lower() == "s":
        print("Até mais!")
        break

    if escolha in EXERCICIOS:
        print("=" * 40)
        EXERCICIOS[escolha]()   # os () no final CHAMAM a função escolhida
    else:
        print("Opção inválida.")
