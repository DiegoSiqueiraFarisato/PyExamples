"""
=====================================================================
  MATERIAL DE ESTUDO PYTHON — NumPy
  Por que NumPy -> Criando arrays -> shape e dtype -> Indexação e
  fatiamento -> View vs cópia -> Máscaras booleanas -> Vetorização e
  broadcasting -> Funções universais -> Agregações e axis -> Reshape e
  empilhamento -> Álgebra linear -> Números aleatórios -> NaN ->
  Exemplo prático -> Erros comuns -> Boas práticas
=====================================================================

PRÉ-REQUISITOS: 01 a 13 (principalmente listas, loops, funções e
classes).

INSTALAÇÃO (se ainda não tiver):
  python -m pip install numpy
  (ou, na pasta App: python -m pip install -r requirements.txt)

COMO USAR ESTE ARQUIVO:
  1. Leia os comentários de cima para baixo.
  2. Rode:   python 19_numpy.py
  3. NumPy é a BASE de pandas, statsmodels e scikit-learn (os próximos
     materiais). Vale a pena dominar bem.
"""

import time

try:
    import numpy as np
except ImportError:
    print("O NumPy não está instalado neste Python. Instale com:")
    print("  python -m pip install numpy")
    raise SystemExit(1)


def secao(titulo: str) -> None:
    print()
    print("=" * 60)
    print(titulo)
    print("=" * 60)


# =====================================================================
# 1. POR QUE NumPy?
# =====================================================================
# Listas Python são flexíveis (guardam qualquer coisa misturada), mas
# lentas para CÁLCULOS com muitos números. O NumPy traz o ndarray
# (N-dimensional array): uma estrutura com
#   - elementos de UM ÚNICO TIPO (todos float64, por exemplo)
#   - guardados juntos na memória, como em C
#   - operações VETORIZADAS: a conta é aplicada no array inteiro de uma
#     vez, sem loop em Python (o loop acontece em C, muito mais rápido)
#
# Convenção universal:  import numpy as np

secao("1. LISTA vs ARRAY")

precos_lista = [10.0, 20.0, 30.0]
precos_array = np.array([10.0, 20.0, 30.0])

# Com lista, "* 2" REPETE a lista; com array, multiplica cada elemento
print("lista * 2:", precos_lista * 2)
print("array * 2:", precos_array * 2)

# Para aplicar 10% de aumento numa lista, precisa de loop/comprehension
print("lista + 10%:", [p * 1.1 for p in precos_lista])
print("array + 10%:", precos_array * 1.1)       # vetorizado

# Velocidade: somar o quadrado de 2 milhões de números
numeros_lista = list(range(2_000_000))
numeros_array = np.arange(2_000_000)

inicio = time.perf_counter()
sum(n * n for n in numeros_lista)
tempo_lista = time.perf_counter() - inicio

inicio = time.perf_counter()
(numeros_array * numeros_array).sum()
tempo_array = time.perf_counter() - inicio

print(f"loop Python: {tempo_lista * 1000:.1f} ms | NumPy: {tempo_array * 1000:.1f} ms "
      f"(~{tempo_lista / tempo_array:.0f}x mais rápido)")


# =====================================================================
# 2. CRIANDO ARRAYS
# =====================================================================
secao("2. CRIANDO ARRAYS")

print("np.array([1, 2, 3])     ->", np.array([1, 2, 3]))
print("np.zeros(4)             ->", np.zeros(4))
print("np.ones(3)              ->", np.ones(3))
print("np.full(3, 7)           ->", np.full(3, 7))
print("np.arange(0, 10, 2)     ->", np.arange(0, 10, 2))      # como range()
print("np.linspace(0, 1, 5)    ->", np.linspace(0, 1, 5))     # 5 pontos de 0 a 1
# arange: você escolhe o PASSO | linspace: você escolhe a QUANTIDADE

matriz = np.array([[1, 2, 3],
                   [4, 5, 6]])                 # lista de listas = 2D
print("matriz 2x3:\n", matriz)
print("np.zeros((2, 3)):\n", np.zeros((2, 3)))  # repare: a forma é uma TUPLA
print("np.eye(3) (identidade):\n", np.eye(3))


# =====================================================================
# 3. ATRIBUTOS: shape, ndim, size, dtype
# =====================================================================
#   shape -> tamanho de cada dimensão: (linhas, colunas)
#   ndim  -> número de dimensões
#   size  -> total de elementos
#   dtype -> o TIPO dos elementos (int64, float64, bool...)

secao("3. shape, ndim, size, dtype")

print("matriz.shape:", matriz.shape, "| ndim:", matriz.ndim, "| size:", matriz.size)
print("matriz.dtype:", matriz.dtype)

# Todos os elementos têm o MESMO tipo. Misturou? O NumPy converte tudo
# para o tipo mais "amplo" (int -> float -> str):
print("np.array([1, 2.5]).dtype     ->", np.array([1, 2.5]).dtype)
print("np.array([1, 'a'])           ->", np.array([1, "a"]))   # virou tudo texto!

# Convertendo com astype (cria um NOVO array)
notas = np.array([7.8, 5.2, 9.9])
print("astype(int) corta a parte decimal:", notas.astype(int))
print("np.round antes de converter:     ", np.round(notas).astype(int))


# =====================================================================
# 4. INDEXAÇÃO E FATIAMENTO
# =====================================================================
# 1D: igual às listas (índice começa em 0, negativos contam do fim).
# 2D: array[linha, coluna]  (uma vírgula, e não [linha][coluna])

secao("4. INDEXAÇÃO E FATIAMENTO")

a = np.arange(10, 20)
print("a          ->", a)
print("a[0], a[-1]->", a[0], a[-1])
print("a[2:5]     ->", a[2:5])
print("a[::2]     ->", a[::2])
print("a[::-1]    ->", a[::-1])                # invertido, como em strings

m = np.arange(1, 13).reshape(3, 4)           # 3 linhas x 4 colunas
print("m:\n", m)
print("m[1, 2]      (linha 1, coluna 2) ->", m[1, 2])
print("m[0]         (linha 0 inteira)   ->", m[0])
print("m[:, 1]      (coluna 1 inteira)  ->", m[:, 1])
print("m[:2, 1:3]   (sub-matriz):\n", m[:2, 1:3])
# ":" sozinho = "todas" naquela dimensão


# =====================================================================
# 5. VIEW vs CÓPIA (pegadinha importantíssima!)
# =====================================================================
# Uma FATIA de array NÃO é uma cópia: é uma VIEW ("janela") para os
# MESMOS dados. Alterar a fatia altera o original!
# (Com listas é diferente: lista[1:3] cria uma lista nova.)

secao("5. VIEW vs CÓPIA")

original = np.array([1, 2, 3, 4, 5])
fatia = original[1:4]
fatia[0] = 999
print("alterei a fatia, e o original mudou:", original)

original = np.array([1, 2, 3, 4, 5])
copia = original[1:4].copy()                # .copy() = cópia independente
copia[0] = 999
print("com .copy(), o original fica intacto:", original)

# Por que o NumPy faz assim? Desempenho: arrays podem ter milhões de
# elementos, e copiar a cada fatia seria caro. Na dúvida, use .copy().


# =====================================================================
# 6. MÁSCARAS BOOLEANAS E FANCY INDEXING
# =====================================================================
# Comparar um array com um valor gera um array de True/False (máscara).
# Usar a máscara como índice FILTRA os elementos.
#   Lógica: & (e), | (ou), ~ (não), COM PARÊNTESES em cada condição.
#   (and/or/not do Python NÃO funcionam com arrays)

secao("6. MÁSCARAS BOOLEANAS")

notas = np.array([4.5, 8.0, 6.5, 9.5, 3.0, 7.0])
aprovado = notas >= 7
print("notas            ->", notas)
print("notas >= 7       ->", aprovado)
print("notas[aprovado]  ->", notas[aprovado])
print("quantos aprovados:", aprovado.sum())       # True conta como 1
print("% aprovados:      ", aprovado.mean() * 100)

recuperacao = (notas >= 5) & (notas < 7)          # parênteses obrigatórios!
print("recuperação (5 <= nota < 7):", notas[recuperacao])

# np.where(condição, valor_se_true, valor_se_false): um "if" vetorizado
print("np.where:", np.where(notas >= 7, "aprovado", "reprovado"))

# Alterando só os elementos que atendem a condição
notas_com_bonus = notas.copy()
notas_com_bonus[notas_com_bonus < 5] += 1
print("bônus de 1 ponto para notas < 5:", notas_com_bonus)

# Fancy indexing: escolher posições com uma LISTA de índices
print("notas[[0, 2, 4]] ->", notas[[0, 2, 4]])


# =====================================================================
# 7. OPERAÇÕES VETORIZADAS E BROADCASTING
# =====================================================================
# Operações entre arrays do MESMO tamanho são feitas elemento a elemento.
# BROADCASTING: quando os tamanhos são diferentes, o NumPy "estica" o
# menor para combinar, se as formas forem compatíveis.
#
# Regra: comparando as dimensões DA DIREITA PARA A ESQUERDA, cada par
# deve ser IGUAL ou um deles ser 1.
#   (3, 4) com (4,)   -> compatível: a linha é repetida para as 3 linhas
#   (3, 4) com (3, 1) -> compatível: a coluna é repetida nas 4 colunas
#   (3, 4) com (3,)   -> ERRO: 4 != 3

secao("7. VETORIZAÇÃO E BROADCASTING")

x = np.array([1, 2, 3])
y = np.array([10, 20, 30])
print("x + y  ->", x + y)
print("x * y  ->", x * y)
print("y / x  ->", y / x)
print("x ** 2 ->", x ** 2)
print("x + 100 (escalar é 'esticado') ->", x + 100)

vendas = np.array([[100, 200, 300],      # loja A: jan, fev, mar
                   [150, 250, 350]])     # loja B
reajuste_por_mes = np.array([1.0, 1.1, 1.2])   # forma (3,)
print("vendas * reajuste (cada mês com seu fator):\n", vendas * reajuste_por_mes)

meta_por_loja = np.array([[200], [250]])       # forma (2, 1)
print("vendas - meta da loja (cada loja com sua meta):\n", vendas - meta_por_loja)

try:
    vendas + np.array([1, 2])                  # (2, 3) com (2,) -> erro
except ValueError as e:
    print("ERRO de broadcasting:", e)


# =====================================================================
# 8. FUNÇÕES UNIVERSAIS (ufuncs)
# =====================================================================
# Funções matemáticas que já trabalham no array inteiro:
#   np.sqrt, np.exp, np.log, np.abs, np.round, np.sin, np.maximum...
# Use as do NumPy, e não as do módulo math (math.sqrt não aceita array).

secao("8. FUNÇÕES UNIVERSAIS")

valores = np.array([1, 4, 9, 16])
print("np.sqrt  ->", np.sqrt(valores))
print("np.log   ->", np.round(np.log(valores), 3))
print("np.abs   ->", np.abs(np.array([-3, 2, -1])))
print("np.clip(valores, 2, 10) (limita ao intervalo) ->", np.clip(valores, 2, 10))
print("np.maximum(x, 2) (elemento a elemento)        ->", np.maximum(x, 2))


# =====================================================================
# 9. AGREGAÇÕES E O PARÂMETRO axis
# =====================================================================
# sum, mean, std, min, max, argmin, argmax, cumsum, median...
#
# axis diz AO LONGO de qual dimensão a conta é feita:
#   axis=None (padrão) -> o array inteiro vira UM número
#   axis=0             -> "desce" pelas linhas: um resultado POR COLUNA
#   axis=1             -> "anda" pelas colunas: um resultado POR LINHA
# Dica: o axis informado é a dimensão que DESAPARECE no resultado.

secao("9. AGREGAÇÕES E axis")

print("vendas:\n", vendas)
print("total geral          vendas.sum()       ->", vendas.sum())
print("total por mês        vendas.sum(axis=0) ->", vendas.sum(axis=0))
print("total por loja       vendas.sum(axis=1) ->", vendas.sum(axis=1))
print("média por loja       vendas.mean(axis=1)->", vendas.mean(axis=1))
print("mês de maior venda (índice) da loja A   ->", vendas[0].argmax())
print("acumulado da loja A  cumsum             ->", vendas[0].cumsum())

amostra = np.array([2, 4, 4, 4, 5, 5, 7, 9])
print("média:", amostra.mean(), "| mediana:", np.median(amostra),
      "| desvio padrão:", amostra.std())
# ATENÇÃO: std() usa por padrão ddof=0 (desvio da POPULAÇÃO). Para o
# desvio de uma AMOSTRA (o que estatística e pandas usam), use ddof=1:
print("desvio padrão amostral (ddof=1):", round(amostra.std(ddof=1), 4))


# =====================================================================
# 10. RESHAPE, TRANSPOSIÇÃO E EMPILHAMENTO
# =====================================================================
secao("10. RESHAPE E EMPILHAMENTO")

numeros = np.arange(12)
print("reshape(3, 4):\n", numeros.reshape(3, 4))
print("reshape(2, -1) (-1 = 'calcule para mim'):\n", numeros.reshape(2, -1))
# O total precisa bater: 12 elementos não viram (5, 3) -> ValueError

grade = numeros.reshape(3, 4)
print("transposta .T (linhas viram colunas), shape", grade.T.shape)
print("ravel() (achata para 1D):", grade.ravel())

# Vetor 1D -> coluna 2D. Muito comum em machine learning, onde X precisa
# ser 2D (linhas = amostras, colunas = variáveis):
idades = np.array([25, 32, 47])
print("idades.shape:", idades.shape, "-> reshape(-1, 1):", idades.reshape(-1, 1).shape)

a1 = np.array([1, 2, 3])
a2 = np.array([4, 5, 6])
print("np.concatenate([a1, a2]) ->", np.concatenate([a1, a2]))
print("np.vstack (uma em cima da outra):\n", np.vstack([a1, a2]))
print("np.column_stack (lado a lado como colunas):\n", np.column_stack([a1, a2]))


# =====================================================================
# 11. ÁLGEBRA LINEAR
# =====================================================================
# "*" é multiplicação ELEMENTO A ELEMENTO.
# "@" é multiplicação de MATRIZES (produto matricial).
# Por baixo dos panos, regressão linear (statsmodels) e muitos modelos
# do scikit-learn são álgebra linear.

secao("11. ÁLGEBRA LINEAR")

A = np.array([[2, 1],
              [1, 3]])
B = np.array([[1, 0],
              [0, 2]])
print("A * B (elemento a elemento):\n", A * B)
print("A @ B (produto matricial):\n", A @ B)

# Resolvendo um sistema linear:
#   2x + 1y = 5
#   1x + 3y = 10
b = np.array([5, 10])
solucao = np.linalg.solve(A, b)
print("solução do sistema (x, y):", solucao)
print("conferindo A @ solucao == b:", np.allclose(A @ solucao, b))

# Regressão linear "na mão" pelo método dos mínimos quadrados:
# encontrar a reta y = a + b*x que melhor passa pelos pontos.
horas_estudo = np.array([1, 2, 3, 4, 5])
nota_prova = np.array([5.1, 5.9, 7.2, 7.8, 9.1])
X = np.column_stack([np.ones(len(horas_estudo)), horas_estudo])  # coluna de 1s = intercepto
coeficientes, *_ = np.linalg.lstsq(X, nota_prova)
intercepto, inclinacao = coeficientes
print(f"reta ajustada: nota = {intercepto:.2f} + {inclinacao:.2f} * horas")
# No material de statsmodels, você fará isso com uma linha e ganhará
# p-valores, intervalos de confiança e um relatório completo.


# =====================================================================
# 12. NÚMEROS ALEATÓRIOS
# =====================================================================
# Forma MODERNA: crie um gerador com np.random.default_rng(semente).
# A semente (seed) torna os resultados REPRODUZÍVEIS: essencial em
# ciência de dados, para outra pessoa obter os mesmos números.
# (Você verá muito código antigo com np.random.seed() e np.random.rand().
# Funciona, mas o default_rng é o recomendado.)

secao("12. NÚMEROS ALEATÓRIOS")

rng = np.random.default_rng(42)
print("integers(1, 7, 5) (5 dados):     ", rng.integers(1, 7, size=5))
print("random(3) (uniforme entre 0 e 1):", np.round(rng.random(3), 3))
alturas = rng.normal(loc=1.70, scale=0.08, size=1000)   # distribuição normal
print(f"1000 alturas normais: média {alturas.mean():.3f}, desvio {alturas.std():.3f}")
print("choice:", rng.choice(["cara", "coroa"], size=6))

baralho = np.arange(1, 11)
rng.shuffle(baralho)
print("shuffle:", baralho)

# Mesma semente = mesmos números
print("seed 7:", np.random.default_rng(7).integers(0, 100, 3),
      "| seed 7 de novo:", np.random.default_rng(7).integers(0, 100, 3))


# =====================================================================
# 13. NaN (dados faltantes) E COMPARAÇÃO DE FLOATS
# =====================================================================
# np.nan ("Not a Number") representa um valor FALTANTE ou indefinido.
# Ele "contamina" as contas: qualquer operação com NaN dá NaN.

secao("13. NaN E FLOATS")

temperaturas = np.array([22.5, np.nan, 25.0, 23.5, np.nan])
print("mean() com NaN    ->", temperaturas.mean())
print("np.nanmean()      ->", np.nanmean(temperaturas))   # ignora os NaN
print("np.isnan()        ->", np.isnan(temperaturas))
print("quantos faltando  ->", np.isnan(temperaturas).sum())
print("sem os NaN        ->", temperaturas[~np.isnan(temperaturas)])
print("np.nan == np.nan  ->", np.nan == np.nan, " <- NaN não é igual nem a si mesmo!")

# Floats: nunca compare com == (lembra do 0.1 + 0.2?)
print("0.1 + 0.2 == 0.3          ->", 0.1 + 0.2 == 0.3)
print("np.isclose(0.1 + 0.2, 0.3)->", np.isclose(0.1 + 0.2, 0.3))
print("np.allclose (arrays)      ->", np.allclose([0.1 + 0.2, 1.0], [0.3, 1.0]))


# =====================================================================
# 14. EXEMPLO PRÁTICO: BOLETIM DE UMA TURMA
# =====================================================================
secao("14. EXEMPLO PRÁTICO: BOLETIM")

alunos = np.array(["Ana", "Bruno", "Carla", "Diego", "Elisa"])
disciplinas = np.array(["Matemática", "Português", "História"])
# linhas = alunos, colunas = disciplinas
notas = np.array([
    [8.5, 7.0, 9.0],
    [5.0, 6.5, 4.5],
    [9.5, 9.0, 8.5],
    [6.0, 7.5, 7.0],
    [4.0, 5.5, 6.0],
])

media_aluno = notas.mean(axis=1)
media_disciplina = notas.mean(axis=0)

for aluno, media in zip(alunos, media_aluno):
    situacao = "aprovado" if media >= 7 else "reprovado"
    print(f"  {aluno:<6} média {media:.2f}  {situacao}")

print("média por disciplina:", dict(zip(disciplinas.tolist(), np.round(media_disciplina, 2).tolist())))
print("melhor aluno:", alunos[media_aluno.argmax()])
print("disciplina mais difícil:", disciplinas[media_disciplina.argmin()])
print("aprovados:", alunos[media_aluno >= 7].tolist())

# Padronização (z-score): quantos desvios padrão cada nota está da
# média da disciplina. Broadcasting em ação: (5, 3) com (3,).
z = (notas - media_disciplina) / notas.std(axis=0)
print("z-score (positivo = acima da média da disciplina):\n", np.round(z, 2))
# .tolist() converte para lista Python normal (bom para imprimir/JSON)


# =====================================================================
# 15. ERROS COMUNS
# =====================================================================
# ERRO 1: esperar que lista + lista some. [1, 2] + [3, 4] CONCATENA.
#         Converta para array.
# ERRO 2: alterar uma fatia achando que é cópia (seção 5).
# ERRO 3: usar and/or/not com arrays:
#           notas[notas > 5 and notas < 8]   -> ValueError
#         Use & | ~ com parênteses.
# ERRO 4: if array:  -> "The truth value of an array ... is ambiguous".
#         Diga o que quer: if array.any(), if array.all(), if array.size.
# ERRO 5: shapes incompatíveis no broadcasting (seção 7). Confira .shape.
# ERRO 6: loop Python sobre o array para fazer contas. Quase sempre
#         existe uma forma vetorizada (mais curta e muito mais rápida).
# ERRO 7: np.float64 aparecendo ao imprimir listas:
#           [np.mean(x)]  ->  [np.float64(2.0)]
#         É só a representação. Use float(...) ou .tolist() para exibir.
# ERRO 8: comparar floats com ==. Use np.isclose / np.allclose.

secao("15. ERROS COMUNS (demonstração)")

try:
    if np.array([1, 2, 3]) > 2:
        pass
except ValueError as e:
    print("ERRO 4 ->", e)

print("ERRO 7 -> [np.mean(x)] =", [np.mean(x)], "| float(...) =", [float(np.mean(x))])


# =====================================================================
# 16. NAMING CONVENTIONS E BOAS PRÁTICAS
# =====================================================================
# CONVENÇÕES DA COMUNIDADE DE DADOS:
#   - import numpy as np    (sempre assim, todo mundo reconhece)
#   - rng = np.random.default_rng(semente)  para números aleatórios
#   - X maiúsculo para a MATRIZ de variáveis (2D) e y minúsculo para o
#     VETOR alvo (1D). Isso "quebra" o snake_case da PEP 8, mas é a
#     convenção da matemática e do scikit-learn, e todo mundo usa.
#   - Nomes descritivos para o resto: notas, vendas_por_mes,
#     media_por_aluno (e não arr, a1, temp)
#
# BOAS PRÁTICAS:
#   1. Vetorize: troque loops por operações no array inteiro.
#   2. Confira .shape SEMPRE que algo der errado (ou antes de dar).
#   3. Use axis conscientemente: "qual dimensão deve sumir?"
#   4. .copy() quando for alterar uma fatia sem querer mexer no original.
#   5. Fixe a semente (default_rng(42)) para resultados reproduzíveis.
#   6. Use as funções nan* (nanmean, nansum...) quando houver faltantes.
#   7. Prefira np.isclose a == para floats.
#   8. Para dados em TABELA, com nomes de colunas, tipos diferentes por
#      coluna e datas, use pandas (o próximo material), que é construído
#      em cima do NumPy.

print()
print("=" * 60)
print("FIM! Agora vá para os exercícios no final do arquivo.")
print("=" * 60)


# =====================================================================
# 17. EXERCÍCIOS PARA PRATICAR
# =====================================================================
# Resolva SEM loops Python (for/while), sempre que possível.
#
#  1. Crie um array com os números de 1 a 20 e mostre: os pares, os
#     múltiplos de 3, a soma dos ímpares e o array invertido.
#  2. Crie uma matriz 4x4 com os números de 1 a 16. Mostre a diagonal
#     principal (dica: np.diag), a soma de cada linha, a soma de cada
#     coluna e a sub-matriz central 2x2.
#  3. Dadas as temperaturas da semana em Celsius
#     [22.5, 25.1, 19.8, 30.2, 28.7, 21.0, 24.4], converta todas para
#     Fahrenheit, mostre os dias acima de 25 °C (índices, com
#     np.where ou np.flatnonzero) e a amplitude (máxima - mínima).
#  4. Normalize o array [10, 20, 30, 40, 50] para o intervalo [0, 1]
#     (min-max: (x - min) / (max - min)) e também calcule o z-score.
#  5. Mostre, com um exemplo, que uma fatia é uma VIEW: altere a fatia e
#     imprima o original. Depois refaça com .copy().
#  6. Simule 10.000 lançamentos de dois dados (rng.integers) e calcule a
#     frequência de cada soma de 2 a 12 (dica: np.bincount). Qual soma
#     é a mais frequente?
#  7. Tabela de vendas: 3 produtos (linhas) x 4 trimestres (colunas) com
#     valores aleatórios inteiros entre 100 e 500 (semente 0). Calcule o
#     total por produto, o total por trimestre, o trimestre de maior
#     venda de cada produto (argmax com axis) e o percentual de cada
#     célula em relação ao total da linha (broadcasting!).
#  8. Dado um array com NaN [3.5, np.nan, 4.0, 5.5, np.nan, 2.0],
#     substitua os NaN pela média dos valores válidos.
#  9. Resolva o sistema:  x + y + z = 6 | 2y + 5z = -4 | 2x + 5y - z = 27
#     com np.linalg.solve e confira a resposta com np.allclose.
# 10. (Desafio) Gere 200 pontos com rng: x uniforme entre 0 e 10 e
#     y = 3 + 2x + ruído normal (desvio 1). Estime o intercepto e a
#     inclinação com np.linalg.lstsq (seção 11). Os valores ficam
#     perto de 3 e 2?
# 11. (Desafio) Escreva uma função que recebe a matriz de notas da seção
#     14 e devolve, sem loops, um array de strings com o conceito de
#     cada aluno pela média: "A" (>= 9), "B" (>= 7), "C" (>= 5) ou "D".
#     Dica: np.select(condicoes, escolhas, default="D").
