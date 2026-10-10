"""
=====================================================================
  MATERIAL DE ESTUDO PYTHON — DO ABSOLUTO ZERO
  Variáveis -> Tipos -> Operadores -> Strings -> Entrada/Saída ->
  Condicionais -> Listas -> Loops -> Naming Conventions
=====================================================================

COMO USAR ESTE ARQUIVO:
  1. Leia os comentários de cima para baixo, com calma.
  2. Rode o arquivo no terminal:   python 01_fundamentos_python.py
  3. Compare o que aparece no terminal com o código.
  4. Mude valores, quebre coisas, rode de novo. É assim que se aprende.

Tudo que começa com # é um COMENTÁRIO: o Python ignora. Serve para humanos.
Este bloco entre três aspas é uma "docstring": também é ignorado na execução.
"""


# =====================================================================
# 0. O PRIMEIRO PROGRAMA: print()
# =====================================================================
# print() mostra algo na tela. É a ferramenta nº 1 para ver o que acontece.

print("=" * 60)          # "=" * 60 repete o caractere "=" 60 vezes
print("0. PRIMEIRO PROGRAMA")
print("=" * 60)

print("Olá, mundo!")
print("Posso imprimir", "várias coisas", "separadas por vírgula")
print()                  # print vazio = linha em branco


# =====================================================================
# 1. VARIÁVEIS — DECLARAÇÃO E ATRIBUIÇÃO
# =====================================================================
# Uma variável é um NOME que aponta para um VALOR guardado na memória.
# Pense numa etiqueta colada numa caixa.
#
# Em Python você NÃO declara o tipo (diferente de Java/C#).
# Basta escrever:   nome = valor
# O "=" significa ATRIBUIÇÃO ("guarde isso aqui"), NÃO "igual a".

print("=" * 60)
print("1. VARIÁVEIS")
print("=" * 60)

nome = "Diego"
idade = 30
altura = 1.78
estudando_python = True

print(nome)
print(idade)
print(altura)
print(estudando_python)

# Uma variável pode receber um novo valor a qualquer momento (reatribuição)
idade = 31
print("Nova idade:", idade)

# Python é de TIPAGEM DINÂMICA: a mesma variável pode até mudar de tipo
# (é permitido, mas evite — deixa o código confuso)
coisa = 10
coisa = "agora sou texto"
print(coisa)

# Atribuição múltipla
a, b, c = 1, 2, 3
print("a, b, c =", a, b, c)

# Mesmo valor para várias variáveis
x = y = z = 0
print("x, y, z =", x, y, z)

# Troca de valores (swap) — truque clássico do Python
a, b = b, a
print("Depois do swap: a =", a, "b =", b)

# Constantes: Python não tem constante "de verdade".
# Por CONVENÇÃO, escrevemos em MAIÚSCULAS para dizer "não mude isso".
PI = 3.14159
MAX_TENTATIVAS = 3
print("PI =", PI, "| MAX_TENTATIVAS =", MAX_TENTATIVAS)
print()


# =====================================================================
# 2. TIPOS DE DADOS BÁSICOS
# =====================================================================
#   int    -> número inteiro           ex: 10, -3, 0
#   float  -> número com casa decimal  ex: 3.14, -0.5  (use PONTO, não vírgula)
#   str    -> texto (string)           ex: "olá", 'python'
#   bool   -> verdadeiro/falso         ex: True, False  (com maiúscula!)
#   None   -> "nada", ausência de valor
#
# type(x) mostra o tipo de qualquer valor.

print("=" * 60)
print("2. TIPOS DE DADOS")
print("=" * 60)

inteiro = 42
decimal = 3.14
texto = "Python"
verdadeiro = True
vazio = None

print(inteiro, "->", type(inteiro))
print(decimal, "->", type(decimal))
print(texto, "->", type(texto))
print(verdadeiro, "->", type(verdadeiro))
print(vazio, "->", type(vazio))

# CONVERSÃO DE TIPOS (casting)
numero_em_texto = "123"
numero_de_verdade = int(numero_em_texto)       # str -> int
print("int('123') + 1 =", numero_de_verdade + 1)

print("float('2.5') =", float("2.5"))           # str -> float
print("str(99) =", str(99), type(str(99)))      # int -> str
print("int(7.9) =", int(7.9))                   # corta a parte decimal (não arredonda!)
print("round(7.9) =", round(7.9))               # arredonda

# Valores "falsos" em Python: 0, 0.0, "", [], None, False
# Todo o resto é "verdadeiro". bool() mostra isso:
print("bool(0) =", bool(0), "| bool(5) =", bool(5))
print("bool('') =", bool(""), "| bool('oi') =", bool("oi"))
print()


# =====================================================================
# 3. OPERADORES
# =====================================================================

print("=" * 60)
print("3. OPERADORES")
print("=" * 60)

# --- 3.1 Aritméticos ---
print("10 + 3  =", 10 + 3)    # soma
print("10 - 3  =", 10 - 3)    # subtração
print("10 * 3  =", 10 * 3)    # multiplicação
print("10 / 3  =", 10 / 3)    # divisão (SEMPRE retorna float)
print("10 // 3 =", 10 // 3)   # divisão inteira (descarta o resto)
print("10 % 3  =", 10 % 3)    # módulo = RESTO da divisão
print("2 ** 3  =", 2 ** 3)    # potência

# Dica: n % 2 == 0 significa "n é par"
print("8 é par?", 8 % 2 == 0)

# --- 3.2 Atribuição composta (atalhos) ---
pontos = 10
pontos += 5     # mesmo que: pontos = pontos + 5
pontos -= 2     # pontos = pontos - 2
pontos *= 3     # pontos = pontos * 3
print("pontos =", pontos)     # (10 + 5 - 2) * 3 = 39
# Obs: Python NÃO tem pontos++ nem pontos--

# --- 3.3 Comparação (sempre retornam True ou False) ---
print("5 == 5 ->", 5 == 5)    # igual  (== compara, = atribui!)
print("5 != 3 ->", 5 != 3)    # diferente
print("5 > 3  ->", 5 > 3)
print("5 < 3  ->", 5 < 3)
print("5 >= 5 ->", 5 >= 5)
print("5 <= 4 ->", 5 <= 4)
print("1 < 5 < 10 ->", 1 < 5 < 10)   # Python permite encadear!

# --- 3.4 Lógicos: and, or, not ---
tem_ingresso = True
maior_de_idade = False
print("and:", tem_ingresso and maior_de_idade)   # True só se AMBOS forem True
print("or: ", tem_ingresso or maior_de_idade)    # True se PELO MENOS UM for True
print("not:", not tem_ingresso)                  # inverte
print()


# =====================================================================
# 4. STRINGS (TEXTO)
# =====================================================================

print("=" * 60)
print("4. STRINGS")
print("=" * 60)

linguagem = "Python"

# Aspas simples ou duplas: tanto faz, só seja consistente
s1 = 'texto'
s2 = "texto"
print(s1 == s2)

# Texto com várias linhas: três aspas
poema = """Linha 1
Linha 2
Linha 3"""
print(poema)

# Concatenação (juntar) e repetição
print("Py" + "thon")
print("ha" * 3)

# len() -> tamanho
print("len('Python') =", len(linguagem))

# Índices: cada caractere tem uma posição, COMEÇANDO EM 0
#   P  y  t  h  o  n
#   0  1  2  3  4  5
#  -6 -5 -4 -3 -2 -1   (índices negativos contam do fim)
print("linguagem[0]  =", linguagem[0])
print("linguagem[-1] =", linguagem[-1])

# Fatiamento (slicing): [início:fim]  -> o "fim" NÃO entra
print("linguagem[0:3] =", linguagem[0:3])    # Pyt
print("linguagem[2:]  =", linguagem[2:])     # thon
print("linguagem[::-1] =", linguagem[::-1])  # inverte: nohtyP

# Métodos úteis
frase = "  Aprendendo Python do Zero  "
print(frase.upper())                 # TUDO MAIÚSCULO
print(frase.lower())                 # tudo minúsculo
print(frase.strip())                 # remove espaços das pontas
print(frase.replace("Zero", "0"))    # substitui
print(frase.split())                 # quebra em lista de palavras
print("Python" in frase)             # verifica se contém

# f-strings: A FORMA MODERNA E RECOMENDADA de montar textos
# Coloque um f antes das aspas e as variáveis entre { }
nome = "Diego"
idade = 31
print(f"Meu nome é {nome} e tenho {idade} anos.")
print(f"Ano que vem terei {idade + 1} anos.")      # aceita expressões
preco = 19.9
print(f"Preço: R$ {preco:.2f}")                    # :.2f = 2 casas decimais

# Strings são IMUTÁVEIS: não dá para mudar um caractere direto
# linguagem[0] = "J"   # <- isso daria ERRO
print()


# =====================================================================
# 5. ENTRADA DE DADOS: input()
# =====================================================================
# input() pausa o programa e espera o usuário digitar algo.
# IMPORTANTE: input() SEMPRE retorna str. Converta se precisar de número.
#
# Exemplo (descomente para testar):
#
#   nome_usuario = input("Qual seu nome? ")
#   idade_usuario = int(input("Qual sua idade? "))
#   print(f"Olá {nome_usuario}, daqui 10 anos você terá {idade_usuario + 10}")
#
# Está comentado para que este arquivo rode sem parar esperando você.


# =====================================================================
# 6. CONDICIONAIS: if / elif / else
# =====================================================================
# Permitem que o programa tome DECISÕES.
#
# ATENÇÃO À INDENTAÇÃO! Em Python, os 4 espaços no início da linha
# definem o que está "dentro" do bloco. Não existe { } como em outras
# linguagens. Indentação errada = erro ou comportamento errado.

print("=" * 60)
print("6. CONDICIONAIS")
print("=" * 60)

nota = 7.5

if nota >= 9:
    print("Conceito A")
elif nota >= 7:              # elif = "senão, se..."
    print("Conceito B")
elif nota >= 5:
    print("Conceito C")
else:                        # se nenhuma condição acima foi verdadeira
    print("Reprovado")

# Python testa de cima para baixo e PARA no primeiro True.

# Condições combinadas
idade = 20
tem_carteira = True
if idade >= 18 and tem_carteira:
    print("Pode dirigir")

# Condicional em uma linha (operador ternário)
status = "maior" if idade >= 18 else "menor"
print(f"Status: {status}")

# Verificando se algo está vazio/None
lista_vazia = []
if not lista_vazia:
    print("A lista está vazia")

valor = None
if valor is None:            # para None, use "is", não "=="
    print("valor é None")
print()


# =====================================================================
# 7. LISTAS (necessário para entender loops)
# =====================================================================
# Lista = coleção ORDENADA e MUTÁVEL de itens, entre [ ].

print("=" * 60)
print("7. LISTAS")
print("=" * 60)

frutas = ["maçã", "banana", "uva"]
print(frutas)
print("Primeira fruta:", frutas[0])
print("Última fruta:", frutas[-1])
print("Quantidade:", len(frutas))

frutas.append("laranja")      # adiciona no fim
print("append:", frutas)

frutas.insert(1, "manga")     # insere na posição 1
print("insert:", frutas)

frutas.remove("banana")       # remove pelo valor
print("remove:", frutas)

ultima = frutas.pop()         # remove e retorna o último
print("pop retornou:", ultima, "| lista:", frutas)

frutas[0] = "pera"            # listas SÃO mutáveis (diferente de strings)
print("alterada:", frutas)

print("'uva' está na lista?", "uva" in frutas)

numeros = [5, 2, 9, 1]
numeros.sort()
print("ordenada:", numeros)
print("soma:", sum(numeros), "| maior:", max(numeros), "| menor:", min(numeros))

# Outras coleções que você verá em breve (só para conhecer):
coordenada = (10, 20)                        # tupla: como lista, mas IMUTÁVEL
pessoa = {"nome": "Ana", "idade": 25}        # dicionário: pares chave -> valor
cores = {"azul", "verde", "azul"}            # set: sem repetição
print(coordenada, pessoa["nome"], cores)
print()


# =====================================================================
# 8. LOOP for
# =====================================================================
# "for" repete um bloco PARA CADA item de uma sequência.
# Use quando você sabe sobre O QUE vai iterar.

print("=" * 60)
print("8. LOOP for")
print("=" * 60)

# Percorrendo uma lista
for fruta in ["maçã", "banana", "uva"]:
    print("Fruta:", fruta)

# Percorrendo uma string (letra por letra)
for letra in "Py":
    print("Letra:", letra)

# range(): gera uma sequência de números
#   range(fim)               -> 0 até fim-1
#   range(inicio, fim)       -> inicio até fim-1
#   range(inicio, fim, passo)
print("range(5):", list(range(5)))
print("range(2, 6):", list(range(2, 6)))
print("range(0, 10, 2):", list(range(0, 10, 2)))
print("range(5, 0, -1):", list(range(5, 0, -1)))

for i in range(3):
    print(f"Repetição número {i}")

# enumerate(): quando você precisa do ÍNDICE e do VALOR
linguagens = ["Python", "Java", "Go"]
for indice, item in enumerate(linguagens):
    print(f"{indice} -> {item}")

# Percorrendo um dicionário
pessoa = {"nome": "Ana", "idade": 25, "cidade": "SP"}
for chave, valor in pessoa.items():
    print(f"{chave}: {valor}")

# Acumulador: padrão MUITO comum
total = 0
for n in [10, 20, 30]:
    total += n
print("Total acumulado:", total)

# Tabuada com loop dentro de loop (loops aninhados)
for i in range(1, 3):
    for j in range(1, 4):
        print(f"{i} x {j} = {i * j}")

# List comprehension: jeito "pythônico" de criar listas com um for
quadrados = [n ** 2 for n in range(1, 6)]
print("Quadrados:", quadrados)
pares = [n for n in range(10) if n % 2 == 0]
print("Pares:", pares)
print()
#---
#Essa linha cria uma lista com os quadrados dos números de 1 a 5. O resultado é [1, 4, 9, 16, 25].
#Como ler
#O jeito mais fácil é começar pelo for, que fica no meio, e depois voltar para o começo:
#quadrados = [n ** 2   for n in range(1, 6)]
##            ───┬──   ─────────┬──────────
##               │              └─ 1º leia isto: "para cada n de 1 até 5"
##               └─ 2º depois isto: "calcule n ao quadrado"
#
#Em português: "para cada n de 1 até 5, calcule n² e guarde numa lista chamada quadrados".
#
#Parte por parte
#
#┌─────────────┬──────────────────────────────────────────────────────────────┐
#│   Pedaço    │                         Significado                          │
#├─────────────┼──────────────────────────────────────────────────────────────┤
#│ quadrados = │ guarda o resultado na variável quadrados                     │
#├─────────────┼──────────────────────────────────────────────────────────────┤
#│ [ ... ]     │ os colchetes dizem que o resultado vai ser uma lista         │
#├─────────────┼──────────────────────────────────────────────────────────────┤
#│ n ** 2      │ o que fazer com cada número: elevar ao quadrado              │
#├─────────────┼──────────────────────────────────────────────────────────────┤
#│ for n in    │ cada número, um de cada vez, se chama n                      │
#├─────────────┼──────────────────────────────────────────────────────────────┤
#│ range(1, 6) │ gera 1, 2, 3, 4, 5 (o 6 não entra, porque o fim é exclusivo) │
#└─────────────┴──────────────────────────────────────────────────────────────┘
#
#O que acontece a cada passo
#
#┌─────┬────────┬───────────────────┐
#│  n  │ n ** 2 │  lista até aqui   │
#├─────┼────────┼───────────────────┤
#│ 1   │ 1      │ [1]               │
#├─────┼────────┼───────────────────┤
#│ 2   │ 4      │ [1, 4]            │
#├─────┼────────┼───────────────────┤
#│ 3   │ 9      │ [1, 4, 9]         │
#├─────┼────────┼───────────────────┤
#│ 4   │ 16     │ [1, 4, 9, 16]     │
#├─────┼────────┼───────────────────┤
#│ 5   │ 25     │ [1, 4, 9, 16, 25] │
#└─────┴────────┴───────────────────┘
#
#A mesma coisa escrita do jeito "longo"
#
#quadrados = []                 # 1. começa com uma lista vazia
#for n in range(1, 6):          # 2. para cada n de 1 a 5
#    quadrados.append(n ** 2)   # 3. adiciona n² na lista
#print(quadrados)               # [1, 4, 9, 16, 25]
#
#As duas versões fazem exatamente a mesma coisa. A forma curta se chama list comprehension. É criar uma lista usando um for".
#
#Para fixar, troque a expressão
#
#[n * 10 for n in range(1, 6)]   # [10, 20, 30, 40, 50]
#[n + 1  for n in range(1, 6)]   # [2, 3, 4, 5, 6]
#[n      for n in range(1, 6)]   # [1, 2, 3, 4, 5]
#
#Só a parte antes do for mudou. Ela é a "receita" aplicada a cada número.
    
#----

# =====================================================================
# 9. LOOP while
# =====================================================================
# "while" repete ENQUANTO a condição for verdadeira.
# Use quando você NÃO sabe quantas vezes vai repetir.
#
# CUIDADO: se a condição nunca ficar False -> LOOP INFINITO.
# (Para parar um programa travado no terminal: Ctrl + C)

print("=" * 60)
print("9. LOOP while")
print("=" * 60)

contador = 1
while contador <= 5:
    print("Contador:", contador)
    contador += 1             # SEM ESTA LINHA o loop nunca termina!

# Exemplo prático: quantos anos até dobrar um investimento a 10% ao ano?
saldo = 1000
anos = 0
while saldo < 2000:
    saldo *= 1.10
    anos += 1
print(f"Leva {anos} anos para dobrar (saldo final: R$ {saldo:.2f})")

# Padrão "while True" + break (muito usado com input):
#
#   while True:
#       resposta = input("Digite 'sair' para encerrar: ")
#       if resposta == "sair":
#           break
print()


# =====================================================================
# 10. CONTROLE DE LOOP: break, continue, else
# =====================================================================

print("=" * 60)
print("10. break / continue / else")
print("=" * 60)

# break -> SAI do loop imediatamente
for n in range(10):
    if n == 4:
        print("Achei o 4, saindo com break")
        break
    print("n =", n)

# continue -> PULA para a próxima repetição
for n in range(6):
    if n % 2 == 0:
        continue              # ignora os pares
    print("Ímpar:", n)

# else no loop -> executa se o loop terminou SEM break
procurado = 7
for n in [1, 3, 5]:
    if n == procurado:
        print("Encontrado!")
        break
else:
    print(f"{procurado} não foi encontrado na lista")

# pass -> "não faça nada" (placeholder para código que virá depois)
for n in range(3):
    pass
print()


# =====================================================================
# 11. NAMING CONVENTIONS (PEP 8)
# =====================================================================
# PEP 8 é o guia de estilo OFICIAL do Python. Seguir ele faz seu código
# parecer profissional e ser fácil de ler por qualquer pessoa.
#
# ---------------------------------------------------------------------
#  O QUE                  | ESTILO              | EXEMPLO
# ---------------------------------------------------------------------
#  Variáveis              | snake_case          | nome_completo, total_vendas
#  Funções                | snake_case          | calcular_media()
#  Constantes             | UPPER_SNAKE_CASE    | TAXA_JUROS, MAX_USUARIOS
#  Classes                | PascalCase          | ContaBancaria, Usuario
#  Módulos (arquivos .py) | snake_case curto    | utils.py, banco_dados.py
#  Pacotes (pastas)       | minúsculo           | meupacote
#  "Privado" (interno)    | _prefixo            | _cache, _validar()
# ---------------------------------------------------------------------
#
# REGRAS OBRIGATÓRIAS (senão dá erro):
#   - Só letras, números e _ (underline)
#   - NÃO pode começar com número         -> 2nome  (ERRO)   nome2 (OK)
#   - Sem espaços nem hífen               -> meu-nome (ERRO) meu_nome (OK)
#   - Não pode ser palavra reservada      -> if, for, class, True, None...
#   - Python diferencia maiúsculas/minúsculas: idade, Idade e IDADE são
#     três variáveis DIFERENTES.
#
# BOAS PRÁTICAS (não dá erro, mas faz MUITA diferença):
#   - Nomes DESCRITIVOS:  x = 1500         -> ruim
#                         salario = 1500   -> bom
#   - Booleanos soam como pergunta: is_ativo, tem_permissao, esta_logado
#   - Listas no plural: usuarios, produtos ; item no singular: usuario
#   - Evite l (L minúsculo), O e I sozinhos: parecem 1 e 0
#   - Não sobrescreva nomes nativos: list, str, sum, max, input, type...
#       list = [1, 2]   # <- péssimo: agora list() não funciona mais!
#   - Letras únicas (i, j, n) só em loops curtos e óbvios
#   - Use _ para variável que você vai ignorar:  for _ in range(3):
#   - Escolha UM idioma para os nomes (português OU inglês) e mantenha.
#     No mercado, inglês é o padrão.
#
# OUTRAS REGRAS DE ESTILO DA PEP 8:
#   - Indentação de 4 espaços (nunca TAB misturado com espaço)
#   - Espaço ao redor de operadores:  x = a + b   (não x=a+b)
#   - Linhas com no máximo ~79 caracteres
#   - Duas linhas em branco entre funções/classes no topo do arquivo

print("=" * 60)
print("11. NAMING CONVENTIONS")
print("=" * 60)

# RUIM ❌
# a = 5000
# b = 0.1
# c = a * b
# NomeDoCliente = "Ana"     # PascalCase é para classes, não variáveis
# nomedocliente = "Ana"     # ilegível

# BOM ✅
salario_mensal = 5000
TAXA_BONUS = 0.1
valor_bonus = salario_mensal * TAXA_BONUS
nome_cliente = "Ana"
esta_ativo = True
clientes = ["Ana", "Bruno", "Carla"]

for cliente in clientes:
    print(f"Cliente: {cliente}")

print(f"{nome_cliente} recebe bônus de R$ {valor_bonus:.2f} | ativo: {esta_ativo}")

for _ in range(2):
    print("O _ indica que não uso a variável do loop")

# Prévia de funções e classes (próximos estudos), só para ver o naming:
def calcular_media(lista_numeros):
    return sum(lista_numeros) / len(lista_numeros)


class ContaBancaria:
    pass


print("Média:", calcular_media([7, 8, 9]))
print()


# =====================================================================
# 12. EXERCÍCIOS PARA PRATICAR
# =====================================================================
# Crie um arquivo novo (ex: exercicios.py) e tente resolver SEM olhar
# respostas. Errar faz parte!
#
#  1. Crie variáveis com seu nome, idade e cidade e imprima uma frase
#     usando f-string.
#  2. Peça dois números com input(), converta para int e mostre soma,
#     subtração, multiplicação e divisão.
#  3. Peça um número e diga se ele é par ou ímpar.
#  4. Peça uma nota de 0 a 10 e mostre o conceito (A, B, C ou Reprovado).
#  5. Imprima a tabuada de um número de 1 a 10 usando for + range.
#  6. Some todos os números de 1 a 100 usando um loop (resposta: 5050).
#  7. Dada a lista [3, 8, 1, 9, 4], encontre o maior número SEM usar max().
#  8. Faça um "adivinhe o número": o programa guarda um número secreto e
#     pede palpites com while até o usuário acertar, dizendo "maior" ou
#     "menor" a cada tentativa. Conte as tentativas.
#  9. Peça uma palavra e diga se é palíndromo (ex: "arara").
#     Dica: palavra[::-1]
# 10. Percorra os números de 1 a 30: imprima "Fizz" se for múltiplo de 3,
#     "Buzz" se múltiplo de 5, "FizzBuzz" se de ambos, senão o número.
#
# Próximos tópicos sugeridos: funções, dicionários a fundo, tratamento de
# erros (try/except), arquivos, módulos e classes.

print("=" * 60)
print("FIM! Agora vá para os exercícios no final do arquivo.")
print("=" * 60)
