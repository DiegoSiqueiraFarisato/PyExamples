"""
=====================================================================
  RESPOSTAS DOS EXERCÍCIOS — 05_dicionarios.py
=====================================================================

COMO USAR ESTE ARQUIVO:
  Tente resolver SOZINHO antes de olhar! Depois compare com a resposta.
  Existem várias formas certas de resolver cada exercício; a sua pode
  ser diferente e estar correta.

  Rode:   python 06_respostas_dicionarios.py

  As funções RETORNAM valores. Os print() ficam fora delas, logo abaixo
  de cada resposta, para mostrar o resultado.
"""

from collections import Counter


def imprimir_cabecalho(titulo: str) -> None:
    """Função auxiliar só para separar as respostas na saída."""
    print()
    print("=" * 60)
    print(titulo)
    print("=" * 60)


# =====================================================================
# EXERCÍCIO 1
# Crie um dict representando você (nome, idade, cidade, linguagens que
# estuda como lista). Imprima cada par no formato "chave: valor".
# =====================================================================
imprimir_cabecalho("EXERCÍCIO 1 — dict sobre você")

eu = {
    "nome": "Diego",
    "idade": 31,
    "cidade": "São Paulo",
    "linguagens": ["Python", "SQL"],
}

for chave, valor in eu.items():
    print(f"{chave}: {valor}")

# Bônus: mostrar a lista de forma mais bonita
print("Estudando:", ", ".join(eu["linguagens"]))


# =====================================================================
# EXERCÍCIO 2
# Crie uma agenda {nome: telefone} com 3 contatos. Adicione um, altere
# outro e remova um terceiro. Imprima a agenda a cada passo.
# =====================================================================
imprimir_cabecalho("EXERCÍCIO 2 — agenda")

agenda = {
    "Ana": "11 91111-1111",
    "Bruno": "21 92222-2222",
    "Carla": "31 93333-3333",
}
print("inicial:  ", agenda)

agenda["Diego"] = "11 94444-4444"      # chave nova -> adiciona
print("adicionou:", agenda)

agenda["Ana"] = "11 98888-8888"        # chave existente -> altera
print("alterou:  ", agenda)

del agenda["Bruno"]                    # remove
print("removeu:  ", agenda)

# Por que o telefone é str e não int?
# Porque não fazemos contas com telefone, e ele tem espaço, traço e
# pode começar com 0. Regra: se não faz conta, provavelmente é texto
# (vale também para CPF, CEP, número de cartão...).


# =====================================================================
# EXERCÍCIO 3
# Crie buscar_telefone(agenda, nome) que retorna o telefone ou
# "Contato não encontrado" (sem usar if, use get).
# =====================================================================
def buscar_telefone(agenda: dict[str, str], nome: str) -> str:
    return agenda.get(nome, "Contato não encontrado")


imprimir_cabecalho("EXERCÍCIO 3 — buscar_telefone")
print("Carla:", buscar_telefone(agenda, "Carla"))
print("Bruno:", buscar_telefone(agenda, "Bruno"))   # foi removido no ex. 2


# =====================================================================
# EXERCÍCIO 4
# Crie contar_letras(texto) que retorna um dict {letra: quantidade},
# ignorando espaços e sem diferenciar maiúsculas. Faça SEM Counter.
# =====================================================================
def contar_letras(texto: str) -> dict[str, int]:
    contagem = {}
    for letra in texto.lower():
        if letra == " ":
            continue                       # pula espaços
        contagem[letra] = contagem.get(letra, 0) + 1
    return contagem


# Variação: contar SÓ letras (ignora números e pontuação também).
# .isalpha() retorna True se o caractere for uma letra.
def contar_somente_letras(texto: str) -> dict[str, int]:
    contagem = {}
    for letra in texto.lower():
        if letra.isalpha():
            contagem[letra] = contagem.get(letra, 0) + 1
    return contagem


imprimir_cabecalho("EXERCÍCIO 4 — contar_letras")
print(contar_letras("Banana Nanica"))
print(contar_somente_letras("Olá, Mundo! 123"))
# Conferindo com Counter (deve dar o mesmo resultado)
print("igual ao Counter?", contar_letras("Banana Nanica") == dict(Counter("banana nanica".replace(" ", ""))))


# =====================================================================
# EXERCÍCIO 5
# Dado o dict de notas, crie um NOVO dict {aluno: média} usando dict
# comprehension.
# =====================================================================
imprimir_cabecalho("EXERCÍCIO 5 — médias com dict comprehension")

notas_por_aluno = {
    "Ana": [8, 9],
    "Bruno": [5, 6, 7],
    "Carla": [10, 9.5],
}

media_por_aluno = {
    aluno: sum(notas) / len(notas)
    for aluno, notas in notas_por_aluno.items()
}
print(media_por_aluno)

# Repare no naming: notas_por_aluno e media_por_aluno. Só pelo nome
# você sabe que a chave é o aluno.


# =====================================================================
# EXERCÍCIO 6
# Com o resultado do exercício 5, imprima o ranking dos alunos da maior
# para a menor média.
# =====================================================================
imprimir_cabecalho("EXERCÍCIO 6 — ranking")

ranking = sorted(media_por_aluno.items(), key=lambda item: item[1], reverse=True)
# ranking é uma LISTA de tuplas: [("Carla", 9.75), ("Ana", 8.5), ...]

for posicao, (aluno, media) in enumerate(ranking, start=1):
    print(f"{posicao}º {aluno:<6} {media:.2f}")


# =====================================================================
# Dados usados nos exercícios 7 e 8
# =====================================================================
produtos = [
    {"nome": "Arroz", "categoria": "Mercearia", "preco": 25.90},
    {"nome": "Feijão", "categoria": "Mercearia", "preco": 8.50},
    {"nome": "Detergente", "categoria": "Limpeza", "preco": 2.99},
    {"nome": "Sabão em pó", "categoria": "Limpeza", "preco": 18.00},
    {"nome": "Maçã", "categoria": "Hortifruti", "preco": 9.90},
    {"nome": "Café", "categoria": "Mercearia", "preco": 17.40},
]


# =====================================================================
# EXERCÍCIO 7
# Crie agrupar_por_categoria(produtos) que retorna {categoria: [nomes]}.
# =====================================================================
def agrupar_por_categoria(produtos: list[dict]) -> dict[str, list[str]]:
    nomes_por_categoria = {}
    for produto in produtos:
        categoria = produto["categoria"]
        if categoria not in nomes_por_categoria:
            nomes_por_categoria[categoria] = []
        nomes_por_categoria[categoria].append(produto["nome"])
    return nomes_por_categoria


# Mesma coisa com setdefault (mais curto)
def agrupar_por_categoria_curto(produtos: list[dict]) -> dict[str, list[str]]:
    nomes_por_categoria = {}
    for produto in produtos:
        nomes_por_categoria.setdefault(produto["categoria"], []).append(produto["nome"])
    return nomes_por_categoria


imprimir_cabecalho("EXERCÍCIO 7 — agrupar_por_categoria")
for categoria, nomes in agrupar_por_categoria(produtos).items():
    print(f"{categoria}: {nomes}")
print("versões iguais?", agrupar_por_categoria(produtos) == agrupar_por_categoria_curto(produtos))


# =====================================================================
# EXERCÍCIO 8
# Crie total_por_categoria(produtos) que retorna
# {categoria: soma_dos_precos}.
# =====================================================================
def total_por_categoria(produtos: list[dict]) -> dict[str, float]:
    total = {}
    for produto in produtos:
        categoria = produto["categoria"]
        total[categoria] = total.get(categoria, 0) + produto["preco"]
    # round() no final para evitar coisas como 51.800000000000004
    return {categoria: round(valor, 2) for categoria, valor in total.items()}


imprimir_cabecalho("EXERCÍCIO 8 — total_por_categoria")
for categoria, valor in total_por_categoria(produtos).items():
    print(f"{categoria:<11} R$ {valor:>6.2f}")

# Por que o round? Números float não são exatos no computador:
print("curiosidade: 0.1 + 0.2 =", 0.1 + 0.2)
# Para dinheiro em sistemas reais, usa-se o módulo decimal (Decimal).


# =====================================================================
# EXERCÍCIO 9
# Crie inverter_dict(d) que troca chaves e valores. O que acontece se
# dois valores forem iguais?
# =====================================================================
def inverter_dict(d: dict) -> dict:
    return {valor: chave for chave, valor in d.items()}


# Resposta à pergunta: como chaves são ÚNICAS, se dois valores forem
# iguais, o ÚLTIMO sobrescreve os anteriores e dados se PERDEM.
# Solução: guardar uma LISTA de chaves para cada valor.
def inverter_dict_sem_perda(d: dict) -> dict[object, list]:
    invertido = {}
    for chave, valor in d.items():
        invertido.setdefault(valor, []).append(chave)
    return invertido


imprimir_cabecalho("EXERCÍCIO 9 — inverter_dict")
siglas = {"SP": "São Paulo", "RJ": "Rio de Janeiro"}
print("simples:", inverter_dict(siglas))

turma_por_aluno = {"Ana": "A", "Bruno": "B", "Carla": "A"}
print("com repetição (perdeu a Ana!):", inverter_dict(turma_por_aluno))
print("sem perda:", inverter_dict_sem_perda(turma_por_aluno))

# Outro problema possível: se algum VALOR for uma lista, ele não pode
# virar chave (TypeError: unhashable type: 'list').


# =====================================================================
# EXERCÍCIO 10
# Crie mesclar_somando(d1, d2): mescla dois dicts de contagem e, quando
# a chave existir nos dois, SOMA os valores.
# =====================================================================
def mesclar_somando(d1: dict[str, int], d2: dict[str, int]) -> dict[str, int]:
    resultado = d1.copy()      # copy para NÃO alterar o d1 original!
    for chave, valor in d2.items():
        resultado[chave] = resultado.get(chave, 0) + valor
    return resultado


imprimir_cabecalho("EXERCÍCIO 10 — mesclar_somando")
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
print("resultado:", mesclar_somando(d1, d2))
print("d1 continua intacto:", d1)

# Por que não usar d1 | d2? Porque o | SUBSTITUI o valor, não soma:
print("com | (errado aqui):", d1 | d2)

# Com Counter, somar contagens é nativo:
print("com Counter:", dict(Counter(d1) + Counter(d2)))


# =====================================================================
# EXERCÍCIO 11 (Desafio)
# Carrinho de compras: CATALOGO {produto: preço} e carrinho
# {produto: quantidade}. Funções adicionar_ao_carrinho,
# remover_do_carrinho e calcular_total. Ignore produtos que não estão
# no catálogo.
# =====================================================================
CATALOGO = {
    "camiseta": 49.90,
    "calça": 129.90,
    "tênis": 299.00,
    "meia": 15.00,
}


def adicionar_ao_carrinho(carrinho: dict[str, int], produto: str, quantidade: int = 1) -> bool:
    """Adiciona ao carrinho. Retorna False se o produto não existir."""
    if produto not in CATALOGO:
        return False
    carrinho[produto] = carrinho.get(produto, 0) + quantidade
    return True


def remover_do_carrinho(carrinho: dict[str, int], produto: str, quantidade: int = 1) -> bool:
    """Remove do carrinho. Se a quantidade zerar, tira o produto.
    Retorna False se o produto não estiver no carrinho."""
    if produto not in carrinho:
        return False
    carrinho[produto] -= quantidade
    if carrinho[produto] <= 0:
        del carrinho[produto]
    return True


def calcular_total(carrinho: dict[str, int]) -> float:
    total = 0
    for produto, quantidade in carrinho.items():
        total += CATALOGO[produto] * quantidade
    return round(total, 2)


def mostrar_carrinho(carrinho: dict[str, int]) -> None:
    if not carrinho:
        print("  (carrinho vazio)")
        return
    for produto, quantidade in carrinho.items():
        subtotal = CATALOGO[produto] * quantidade
        print(f"  {quantidade}x {produto:<9} R$ {subtotal:>7.2f}")
    print(f"  {'TOTAL':<12} R$ {calcular_total(carrinho):>7.2f}")


imprimir_cabecalho("EXERCÍCIO 11 — carrinho de compras")

# Repare: as funções ALTERAM o dict recebido, sem precisar de return.
# Lembra da seção 13 (dicts são passados por referência)? Aqui isso é
# proposital. Por isso elas retornam só um bool dizendo se deu certo.
carrinho = {}
adicionar_ao_carrinho(carrinho, "camiseta", 2)
adicionar_ao_carrinho(carrinho, "tênis")
adicionar_ao_carrinho(carrinho, "meia", 3)
adicionar_ao_carrinho(carrinho, "camiseta")       # soma com as 2 que já tinha
print("adicionou 'boné'?", adicionar_ao_carrinho(carrinho, "boné"))   # não existe
mostrar_carrinho(carrinho)

print("Removendo 1 meia e o tênis...")
remover_do_carrinho(carrinho, "meia")
remover_do_carrinho(carrinho, "tênis")
mostrar_carrinho(carrinho)


# =====================================================================
# EXERCÍCIO 12 (Desafio)
# Crie contar_palavras(texto) que retorna as 3 palavras mais frequentes,
# ignorando maiúsculas e pontuação (.,!?). Primeiro "na mão", depois
# com Counter.
# =====================================================================
def limpar_texto(texto: str) -> list[str]:
    """Deixa minúsculo, tira pontuação e devolve a lista de palavras."""
    texto = texto.lower()
    for sinal in ".,!?":
        texto = texto.replace(sinal, "")
    return texto.split()


def contar_palavras(texto: str) -> list[tuple[str, int]]:
    contagem = {}
    for palavra in limpar_texto(texto):
        contagem[palavra] = contagem.get(palavra, 0) + 1

    # Ordena os pares (palavra, quantidade) pela quantidade, maior
    # primeiro, e pega os 3 primeiros com fatiamento [:3]
    ordenado = sorted(contagem.items(), key=lambda item: item[1], reverse=True)
    return ordenado[:3]


def contar_palavras_counter(texto: str) -> list[tuple[str, int]]:
    return Counter(limpar_texto(texto)).most_common(3)


imprimir_cabecalho("EXERCÍCIO 12 — palavras mais frequentes")
texto = (
    "Python é simples. Python é poderoso! "
    "Aprender Python é divertido, e Python é usado em tudo. "
    "Simples, poderoso e divertido."
)
print("na mão:     ", contar_palavras(texto))
print("com Counter:", contar_palavras_counter(texto))

# Repare que separei a limpeza numa função própria (limpar_texto) e as
# duas versões a reutilizam: uma função, uma responsabilidade.

print()
print("=" * 60)
print("FIM DAS RESPOSTAS!")
print("=" * 60)
