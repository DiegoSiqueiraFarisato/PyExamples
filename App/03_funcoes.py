"""
=====================================================================
  MATERIAL DE ESTUDO PYTHON — FUNÇÕES
  O que são -> def -> Parâmetros -> return -> Valores padrão ->
  Argumentos nomeados -> *args/**kwargs -> Escopo -> Docstrings ->
  Type hints -> Lambda -> Recursão -> Boas práticas e naming
=====================================================================

PRÉ-REQUISITO: 01_fundamentos_python.py (variáveis, tipos, if, loops).

COMO USAR ESTE ARQUIVO:
  1. Leia os comentários de cima para baixo.
  2. Rode no terminal:   python 03_funcoes.py
  3. Compare o que aparece no terminal com o código.
  4. Mude valores, crie suas próprias funções, quebre e conserte.
"""


# =====================================================================
# 1. O QUE É UMA FUNÇÃO E POR QUE USAR
# =====================================================================
# Uma função é um BLOCO DE CÓDIGO COM NOME, que você escreve uma vez e
# executa quantas vezes quiser, só chamando o nome.
#
# Você já usou várias funções prontas do Python:
#   print(), len(), input(), int(), sum(), max(), range()...
# Agora vai aprender a criar as SUAS.
#
# Por que usar funções?
#   - Evitar repetição: escreve uma vez, usa em vários lugares
#     (princípio DRY: "Don't Repeat Yourself", não se repita)
#   - Organização: quebra um problema grande em partes pequenas
#   - Legibilidade: calcular_imposto(salario) diz O QUE faz
#   - Manutenção: corrigiu um bug na função, corrigiu em todo lugar

print("=" * 60)
print("1. POR QUE FUNÇÕES?")
print("=" * 60)

# SEM função: o mesmo código repetido 3 vezes
print("-" * 30)
print("Relatório de Vendas")
print("-" * 30)
print("-" * 30)
print("Relatório de Estoque")
print("-" * 30)
# ... e se você quiser mudar o "-" para "=", tem que mudar em todo lugar.
print()


# =====================================================================
# 2. CRIANDO E CHAMANDO UMA FUNÇÃO: def
# =====================================================================
# Sintaxe:
#
#   def nome_da_funcao():
#       código indentado (4 espaços)
#       que faz parte da função
#
# - "def" vem de "define" (definir)
# - os parênteses () são obrigatórios
# - os dois pontos : no final também
# - o corpo da função é o que está INDENTADO abaixo dela
#
# DEFINIR uma função NÃO executa nada. Ela só passa a existir.
# Para executar, você CHAMA a função: nome_da_funcao()

print("=" * 60)
print("2. def E CHAMADA")
print("=" * 60)


def saudar():
    print("Olá! Bem-vindo ao estudo de funções.")


saudar()     # chamando a função
saudar()     # chamando de novo: o código roda de novo

# ATENÇÃO à diferença:
#   saudar     -> é a função em si (o "objeto" função), não executa
#   saudar()   -> EXECUTA a função
print(saudar)    # mostra algo como <function saudar at 0x...>

# A função precisa ser definida ANTES de ser chamada.
# Se você chamar antes do def, dá NameError.
print()


# =====================================================================
# 3. PARÂMETROS E ARGUMENTOS
# =====================================================================
# Parâmetros são "variáveis de entrada" da função. Eles permitem que a
# mesma função trabalhe com valores diferentes.
#
#   PARÂMETRO -> o nome na DEFINIÇÃO:     def saudar_pessoa(nome):
#   ARGUMENTO -> o valor na CHAMADA:      saudar_pessoa("Ana")
#
# (Muita gente usa as duas palavras como sinônimos, e tudo bem. Mas é
# bom saber a diferença.)

print("=" * 60)
print("3. PARÂMETROS E ARGUMENTOS")
print("=" * 60)


def saudar_pessoa(nome):
    print(f"Olá, {nome}!")


saudar_pessoa("Ana")
saudar_pessoa("Bruno")


# Vários parâmetros: separados por vírgula
def apresentar(nome, idade, cidade):
    print(f"{nome} tem {idade} anos e mora em {cidade}.")


apresentar("Carla", 28, "Recife")

# Agora sim: resolvendo o problema da seção 1 com função
def imprimir_titulo(texto):
    print("-" * 30)
    print(texto)
    print("-" * 30)


imprimir_titulo("Relatório de Vendas")
imprimir_titulo("Relatório de Estoque")

# Se passar a quantidade errada de argumentos -> TypeError
# apresentar("Carla", 28)   # ERRO: falta o argumento 'cidade'
print()


# =====================================================================
# 4. RETORNO: return
# =====================================================================
# Até agora as funções só IMPRIMIAM. Mas na maioria das vezes você quer
# que a função CALCULE algo e DEVOLVA o resultado para você usar depois.
# Para isso existe o "return".
#
# DIFERENÇA FUNDAMENTAL (a maior confusão de iniciantes):
#   print  -> MOSTRA na tela. O valor não pode ser reaproveitado.
#   return -> DEVOLVE o valor para quem chamou. Pode guardar em
#             variável, usar em conta, passar para outra função...

print("=" * 60)
print("4. return")
print("=" * 60)


def somar_com_print(a, b):
    print(a + b)          # só mostra


def somar(a, b):
    return a + b          # devolve


somar_com_print(2, 3)     # mostra 5, mas o valor "se perde"

resultado = somar(2, 3)   # o 5 fica guardado em 'resultado'
print("resultado =", resultado)
print("resultado * 10 =", resultado * 10)
print("somar dentro de somar:", somar(somar(1, 2), somar(3, 4)))   # 3 + 7

# Uma função SEM return devolve None automaticamente
valor = somar_com_print(1, 1)    # imprime 2
print("somar_com_print devolveu:", valor)   # None


# O return ENCERRA a função na hora. Nada depois dele roda.
def verificar_idade(idade):
    if idade < 0:
        return "Idade inválida"   # sai da função aqui
    if idade >= 18:
        return "Maior de idade"
    return "Menor de idade"
    print("Esta linha NUNCA executa")


print(verificar_idade(-5))
print(verificar_idade(20))
print(verificar_idade(10))


# Retornando vários valores (na verdade, retorna uma tupla)
def calcular_estatisticas(numeros):
    menor = min(numeros)
    maior = max(numeros)
    media = sum(numeros) / len(numeros)
    return menor, maior, media


menor, maior, media = calcular_estatisticas([4, 8, 15, 16, 23, 42])
print(f"menor={menor}, maior={maior}, media={media:.2f}")


# Funções que retornam bool são ótimas para usar em if
def eh_par(numero):
    return numero % 2 == 0     # a comparação já é True ou False


if eh_par(10):
    print("10 é par")
print()


# =====================================================================
# 5. PARÂMETROS COM VALOR PADRÃO (default)
# =====================================================================
# Você pode dar um valor padrão a um parâmetro. Se quem chamar não
# passar aquele argumento, o padrão é usado.
#
# REGRA: parâmetros com padrão vêm DEPOIS dos sem padrão.
#   def f(a, b=2):    OK
#   def f(a=1, b):    ERRO

print("=" * 60)
print("5. VALORES PADRÃO")
print("=" * 60)


def calcular_preco_final(preco, desconto=0.0, frete=10.0):
    return preco - (preco * desconto) + frete


print(calcular_preco_final(100))              # usa desconto=0 e frete=10
print(calcular_preco_final(100, 0.1))         # desconto 10%, frete padrão
print(calcular_preco_final(100, 0.1, 0))      # desconto 10%, frete grátis


# Exemplo real: o próprio print tem parâmetros com padrão (sep=" ", end="\n")
print("a", "b", "c", sep="-")
print("sem quebra de linha", end=" | ")
print("continua na mesma linha")
print()


# =====================================================================
# 6. ARGUMENTOS POSICIONAIS vs NOMEADOS (keyword arguments)
# =====================================================================
# Posicional: o valor vai para o parâmetro pela ORDEM.
# Nomeado:    você diz explicitamente nome_do_parametro=valor.
#
# Argumentos nomeados deixam a chamada mais clara e permitem mudar a
# ordem ou pular parâmetros que têm valor padrão.

print("=" * 60)
print("6. POSICIONAIS vs NOMEADOS")
print("=" * 60)

# Posicional: o que é 0 e o que é 5? Precisa olhar a definição.
print(calcular_preco_final(100, 0, 5))

# Nomeado: muito mais legível
print(calcular_preco_final(preco=100, frete=5))       # pulei o desconto
print(calcular_preco_final(frete=5, preco=100))       # ordem não importa

# Pode misturar, mas os POSICIONAIS vêm PRIMEIRO
print(calcular_preco_final(100, frete=0))
# calcular_preco_final(preco=100, 0.1)   # ERRO: posicional depois de nomeado
print()


# =====================================================================
# 7. *args E **kwargs (quantidade variável de argumentos)
# =====================================================================
# *args   -> recebe QUALQUER quantidade de argumentos posicionais,
#            empacotados numa TUPLA.
# **kwargs -> recebe QUALQUER quantidade de argumentos nomeados,
#            empacotados num DICIONÁRIO.
#
# Os nomes "args" e "kwargs" são convenção. O que importa são os * e **.
# Você vai ver isso muito em código de bibliotecas.

print("=" * 60)
print("7. *args E **kwargs")
print("=" * 60)


def somar_todos(*numeros):
    print("  recebi:", numeros, type(numeros))
    total = 0
    for numero in numeros:
        total += numero
    return total


print(somar_todos(1, 2))
print(somar_todos(1, 2, 3, 4, 5))
print(somar_todos())


def criar_perfil(nome, **dados_extras):
    print(f"  Perfil de {nome}")
    for chave, valor in dados_extras.items():
        print(f"    {chave}: {valor}")


criar_perfil("Ana", idade=25, profissao="Dev", cidade="SP")

# O * também DESEMPACOTA uma lista na hora de chamar
valores = [10, 20, 30]
print(somar_todos(*valores))   # mesmo que somar_todos(10, 20, 30)
print()


# =====================================================================
# 8. ESCOPO: VARIÁVEIS LOCAIS E GLOBAIS
# =====================================================================
# ESCOPO = onde uma variável "existe" e pode ser usada.
#
#   LOCAL  -> criada DENTRO da função. Só existe lá dentro, e some
#             quando a função termina.
#   GLOBAL -> criada FORA de qualquer função (no nível do arquivo).
#             Pode ser LIDA de dentro das funções.

print("=" * 60)
print("8. ESCOPO")
print("=" * 60)

mensagem = "eu sou global"


def mostrar_escopo():
    variavel_local = "eu sou local"
    print("  dentro:", variavel_local)
    print("  dentro:", mensagem)       # ler a global: OK


mostrar_escopo()
# print(variavel_local)   # ERRO: NameError, ela só existe dentro da função

# Se você ATRIBUIR a uma variável com o mesmo nome dentro da função,
# o Python cria uma NOVA variável local. A global não muda.
contador = 0


def tentar_incrementar():
    contador = 100            # esta é OUTRA variável, local
    print("  contador local:", contador)


tentar_incrementar()
print("contador global continua:", contador)

# Existe a palavra 'global' para alterar a variável de fora:
#
#   def incrementar():
#       global contador
#       contador += 1
#
# MAS EVITE. Funções que mexem em variáveis globais são difíceis de
# entender e testar. O jeito certo é RECEBER por parâmetro e DEVOLVER
# com return:


def incrementar(valor):
    return valor + 1


contador = incrementar(contador)
print("contador depois de incrementar:", contador)
print()


# =====================================================================
# 9. DOCSTRINGS E TYPE HINTS (documentando funções)
# =====================================================================
# DOCSTRING: texto entre """ """ logo na primeira linha da função,
# explicando o que ela faz. Aparece no help() e quando você passa o
# mouse em cima da função no editor (VS Code, PyCharm).
#
# TYPE HINTS: indicam o TIPO esperado dos parâmetros e do retorno.
#   def f(nome: str, idade: int) -> str:
# O Python NÃO obriga nem verifica os tipos na execução. É uma dica
# para quem lê o código e para o editor avisar erros. Mas é padrão em
# código profissional moderno, então acostume-se desde já.

print("=" * 60)
print("9. DOCSTRINGS E TYPE HINTS")
print("=" * 60)


def calcular_imc(peso: float, altura: float) -> float:
    """Calcula o Índice de Massa Corporal.

    Args:
        peso: peso em quilogramas.
        altura: altura em metros.

    Returns:
        O IMC arredondado com 2 casas decimais.
    """
    return round(peso / altura ** 2, 2)


def classificar_imc(imc: float) -> str:
    """Retorna a classificação do IMC segundo a OMS."""
    if imc < 18.5:
        return "Abaixo do peso"
    if imc < 25:
        return "Peso normal"
    if imc < 30:
        return "Sobrepeso"
    return "Obesidade"


imc = calcular_imc(70, 1.75)
print(f"IMC: {imc} -> {classificar_imc(imc)}")

# Lendo a docstring
print(calcular_imc.__doc__.splitlines()[0])
# No terminal interativo, experimente: help(calcular_imc)


# Type hints com listas e com "pode ser None"
def buscar_usuario(usuarios: list[str], nome: str) -> str | None:
    """Retorna o nome se ele estiver na lista, senão None."""
    if nome in usuarios:
        return nome
    return None


print(buscar_usuario(["ana", "bruno"], "ana"))
print(buscar_usuario(["ana", "bruno"], "zé"))
print()


# =====================================================================
# 10. FUNÇÕES CHAMANDO FUNÇÕES
# =====================================================================
# Funções pequenas que fazem UMA coisa podem ser combinadas para
# resolver problemas maiores. Repare como o código abaixo se lê quase
# como português.

print("=" * 60)
print("10. FUNÇÕES CHAMANDO FUNÇÕES")
print("=" * 60)


def calcular_media(notas: list[float]) -> float:
    return sum(notas) / len(notas)


def esta_aprovado(media: float, media_minima: float = 7.0) -> bool:
    return media >= media_minima


def gerar_boletim(aluno: str, notas: list[float]) -> str:
    media = calcular_media(notas)
    situacao = "Aprovado" if esta_aprovado(media) else "Reprovado"
    return f"{aluno}: média {media:.1f} -> {situacao}"


print(gerar_boletim("Ana", [8, 9, 7.5]))
print(gerar_boletim("Bruno", [5, 6, 4]))
print()


# =====================================================================
# 11. FUNÇÕES SÃO VALORES + LAMBDA
# =====================================================================
# Em Python, funções são valores como qualquer outro: dá para guardar em
# variável, colocar em lista/dicionário e passar como argumento.
# (Foi isso que o menu do arquivo de respostas usou!)

print("=" * 60)
print("11. FUNÇÕES COMO VALORES E LAMBDA")
print("=" * 60)


def dobrar(x):
    return x * 2


def triplicar(x):
    return x * 3


operacao = dobrar              # SEM parênteses: guardo a função, não executo
print("operacao(5) =", operacao(5))


def aplicar(funcao, valor):
    return funcao(valor)


print("aplicar(triplicar, 5) =", aplicar(triplicar, 5))

# LAMBDA: função anônima de UMA linha, para coisas bem simples.
#   lambda parametros: expressao_que_e_retornada
quadrado = lambda x: x ** 2     # (só para exemplo; ver nota abaixo)
print("quadrado(4) =", quadrado(4))

# O uso mais comum de lambda: passar como argumento, ex. no sort/sorted
pessoas = [("Ana", 30), ("Bruno", 22), ("Carla", 27)]
por_idade = sorted(pessoas, key=lambda pessoa: pessoa[1])
print("ordenado por idade:", por_idade)

palavras = ["banana", "kiwi", "abacaxi", "uva"]
print("ordenado por tamanho:", sorted(palavras, key=len))   # len é função!

# NOTA: guardar lambda numa variável (quadrado = lambda ...) funciona,
# mas a PEP 8 recomenda usar def nesse caso. Lambda é para usar "na hora".
print()


# =====================================================================
# 12. RECURSÃO (uma função que chama a si mesma)
# =====================================================================
# Toda função recursiva precisa de:
#   1. CASO BASE: quando parar (senão chama a si mesma para sempre)
#   2. PASSO RECURSIVO: chamar a si mesma com um problema MENOR
#
# É um tópico mais avançado. Não se preocupe se não entender de primeira.
# Quase tudo que se faz com recursão também se faz com loop.

print("=" * 60)
print("12. RECURSÃO")
print("=" * 60)


def fatorial(n: int) -> int:
    """5! = 5 * 4 * 3 * 2 * 1 = 120"""
    if n <= 1:                 # caso base
        return 1
    return n * fatorial(n - 1) # passo recursivo


print("fatorial(5) =", fatorial(5))


def contagem_regressiva(n: int) -> None:
    if n == 0:
        print("  Fogo!")
        return
    print(" ", n)
    contagem_regressiva(n - 1)


contagem_regressiva(3)
print()


# =====================================================================
# 13. ERROS COMUNS DE INICIANTE
# =====================================================================

print("=" * 60)
print("13. ERROS COMUNS")
print("=" * 60)

# ERRO 1: esquecer os parênteses ao chamar
#   saudar        # não faz nada (só "menciona" a função)
#   saudar()      # executa

# ERRO 2: usar print quando deveria usar return
def dobro_errado(x):
    print(x * 2)


def dobro_certo(x):
    return x * 2


# total = dobro_errado(5) + 1   # ERRO: None + 1 -> TypeError
total = dobro_certo(5) + 1
print("dobro_certo(5) + 1 =", total)

# ERRO 3: código depois do return (nunca executa)

# ERRO 4: indentação errada (o return fora do loop vs dentro do loop)
def tem_negativo_errado(numeros):
    for n in numeros:
        if n < 0:
            return True
        return False           # ERRADO: retorna já na 1ª volta do loop


def tem_negativo_certo(numeros):
    for n in numeros:
        if n < 0:
            return True
    return False               # CERTO: só depois de olhar todos


print("errado:", tem_negativo_errado([1, 2, -3]))   # False (bug!)
print("certo: ", tem_negativo_certo([1, 2, -3]))    # True


# ERRO 5: lista (ou dict) como valor padrão -> ARMADILHA CLÁSSICA
# O valor padrão é criado UMA vez só, e é compartilhado entre chamadas.
def adicionar_item_errado(item, lista=[]):
    lista.append(item)
    return lista


print(adicionar_item_errado("a"))   # ['a']
print(adicionar_item_errado("b"))   # ['a', 'b']  <- surpresa!


def adicionar_item_certo(item, lista=None):
    if lista is None:
        lista = []                  # cria uma lista NOVA a cada chamada
    lista.append(item)
    return lista


print(adicionar_item_certo("a"))    # ['a']
print(adicionar_item_certo("b"))    # ['b']
print()


# =====================================================================
# 14. NAMING CONVENTIONS E BOAS PRÁTICAS PARA FUNÇÕES
# =====================================================================
# NOMES:
#   - snake_case, sempre:          calcular_total, enviar_email
#   - Comece com um VERBO, porque função FAZ algo:
#       calcular_, buscar_, enviar_, validar_, gerar_, converter_, salvar_
#   - Funções que retornam bool soam como pergunta:
#       eh_valido(), esta_vazio(), tem_permissao(), pode_editar()
#       (em inglês: is_valid(), has_permission(), can_edit())
#   - Nome descritivo > nome curto:
#       f(x)              -> ruim
#       calc(x)           -> ruim
#       calcular_frete(x) -> bom
#   - "_" no início indica uso interno: _formatar_cpf()
#
# BOAS PRÁTICAS:
#   1. UMA função = UMA responsabilidade. Se o nome precisa de "e"
#      (validar_e_salvar_e_enviar), provavelmente são 3 funções.
#   2. Funções curtas. Se passou de ~20-30 linhas, considere dividir.
#   3. Prefira RETORNAR valores a imprimir dentro da função. Deixe o
#      print para quem chama. Assim a função serve em mais lugares.
#   4. Evite variáveis globais. Receba por parâmetro, devolva com return.
#   5. Poucos parâmetros (até ~3-4). Muitos? Use valores padrão ou
#      agrupe em uma estrutura (dicionário, e depois classes).
#   6. Escreva docstring nas funções que não são óbvias.
#   7. Use type hints.
#   8. Duas linhas em branco antes e depois de cada def no nível do
#      arquivo (PEP 8).

print("=" * 60)
print("14. BOAS PRÁTICAS (exemplo comparativo)")
print("=" * 60)


# RUIM ❌: nome vago, faz tudo junto, imprime em vez de retornar
def processa(l):
    t = 0
    for i in l:
        t += i
    print("Total:", t)
    print("Média:", t / len(l))


# BOM ✅: nomes claros, uma responsabilidade cada, retornam valores
def calcular_total(valores: list[float]) -> float:
    return sum(valores)


def calcular_media_valores(valores: list[float]) -> float:
    return calcular_total(valores) / len(valores)


vendas = [150.0, 200.0, 350.0]
processa(vendas)
print(f"Total: {calcular_total(vendas)} | Média: {calcular_media_valores(vendas):.2f}")
print()


# =====================================================================
# 15. if __name__ == "__main__"
# =====================================================================
# Você vai ver isto no final de MUITOS arquivos Python:
#
#   def main():
#       ...código principal...
#
#   if __name__ == "__main__":
#       main()
#
# Significa: "só rode main() se este arquivo foi executado DIRETAMENTE
# (python arquivo.py), e NÃO quando ele for importado por outro arquivo".
#
# Quando você estudar MÓDULOS (import), isso vai fazer todo sentido.
# Por enquanto, saiba que é a forma organizada de definir o "ponto de
# entrada" do programa.


def main():
    print("=" * 60)
    print("15. FIM! main() foi chamada pelo if __name__ == '__main__'")
    print("    Agora vá para os exercícios no final do arquivo.")
    print("=" * 60)


if __name__ == "__main__":
    main()


# =====================================================================
# 16. EXERCÍCIOS PARA PRATICAR
# =====================================================================
# Crie um arquivo novo (ex: exercicios_funcoes.py). Use type hints e
# return em todas as funções (deixe o print para fora delas).
#
#  1. Crie eh_impar(numero) que retorna True se o número for ímpar.
#  2. Crie celsius_para_fahrenheit(celsius). Fórmula: F = C * 9/5 + 32.
#     Teste com 0 (32.0) e 100 (212.0).
#  3. Crie area_retangulo(base, altura=None). Se a altura não for
#     passada, calcule a área de um QUADRADO de lado = base.
#  4. Crie contar_vogais(texto) que retorna quantas vogais tem o texto
#     (maiúsculas e minúsculas).
#  5. Crie maior_da_lista(numeros) SEM usar max(). Retorne None se a
#     lista estiver vazia.
#  6. Crie inverter_texto(texto) e eh_palindromo(texto). A segunda deve
#     USAR a primeira.
#  7. Crie media(*notas) que aceita qualquer quantidade de notas.
#     media(7, 8, 9) -> 8.0
#  8. Crie calcular_desconto(preco, percentual=10) que retorna o preço
#     com desconto. Chame usando argumento nomeado.
#  9. Crie fizzbuzz(numero) que RETORNA "Fizz", "Buzz", "FizzBuzz" ou o
#     número como texto. Depois use um loop de 1 a 30 para imprimir.
# 10. Crie uma calculadora: funções somar, subtrair, multiplicar e
#     dividir (dividir retorna None se o divisor for 0) e uma função
#     calcular(a, b, operador) que escolhe a operação certa pelo
#     operador ("+", "-", "*", "/").
# 11. (Desafio) Crie fibonacci(n) que retorna uma LISTA com os n
#     primeiros números da sequência: 0, 1, 1, 2, 3, 5, 8, 13...
# 12. (Desafio) Crie fatorial(n) com loop, e compare com a versão
#     recursiva da seção 12.
