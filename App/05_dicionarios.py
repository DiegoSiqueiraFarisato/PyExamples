"""
=====================================================================
  MATERIAL DE ESTUDO PYTHON — DICIONÁRIOS A FUNDO
  O que são -> Criar -> Acessar ([] vs get) -> Adicionar/Alterar ->
  Remover -> Percorrer -> Mesclar -> Aninhados -> Lista de dicts ->
  Comprehension -> Padrões (contar, agrupar) -> Cópias -> Ordenar ->
  Counter/defaultdict -> Erros comuns -> Boas práticas
=====================================================================

PRÉ-REQUISITOS: 01_fundamentos_python.py e 03_funcoes.py

COMO USAR ESTE ARQUIVO:
  1. Leia os comentários de cima para baixo.
  2. Rode no terminal:   python 05_dicionarios.py
  3. Compare o que aparece no terminal com o código.
  4. Mude valores, crie seus próprios dicionários, quebre e conserte.
"""


# =====================================================================
# 1. O QUE É UM DICIONÁRIO
# =====================================================================
# Um dicionário (dict) guarda PARES de CHAVE -> VALOR.
#
# Pense num dicionário de verdade: você procura a PALAVRA (chave) e
# encontra o SIGNIFICADO (valor). Ou numa agenda: NOME -> TELEFONE.
#
# LISTA vs DICIONÁRIO:
#   lista -> acessa pela POSIÇÃO:  pessoa[0], pessoa[1]  (o que é 0?)
#   dict  -> acessa pelo NOME:     pessoa["nome"], pessoa["idade"]
#
# Características:
#   - Chaves são ÚNICAS (não existem duas chaves iguais)
#   - É MUTÁVEL (dá para adicionar, alterar e remover)
#   - Mantém a ORDEM de inserção (desde o Python 3.7)
#   - Buscar por chave é MUITO rápido, mesmo com milhões de itens

print("=" * 60)
print("1. LISTA vs DICIONÁRIO")
print("=" * 60)

pessoa_lista = ["Ana", 25, "São Paulo"]
pessoa_dict = {"nome": "Ana", "idade": 25, "cidade": "São Paulo"}

print("lista:", pessoa_lista[1])          # 1 é o quê? idade? precisa lembrar
print("dict: ", pessoa_dict["idade"])     # óbvio!
print()


# =====================================================================
# 2. CRIANDO DICIONÁRIOS
# =====================================================================

print("=" * 60)
print("2. CRIANDO")
print("=" * 60)

# Forma mais comum: chaves { } com pares chave: valor
produto = {
    "nome": "Notebook",
    "preco": 3500.00,
    "estoque": 12,
    "ativo": True,
}
# Dica: em dicts com várias linhas, deixe a vírgula no último item
# também. Fica mais fácil adicionar itens e o diff do git fica limpo.
print(produto)

# Dicionário vazio
vazio = {}
print("vazio:", vazio, type(vazio))

# Com a função dict() e argumentos nomeados (chaves viram strings)
config = dict(tema="escuro", idioma="pt-BR", fonte=14)
print("dict():", config)

# A partir de uma lista de pares
pares = [("a", 1), ("b", 2)]
print("de pares:", dict(pares))

# Juntando duas listas com zip()
chaves = ["nome", "idade"]
valores = ["Bruno", 30]
print("zip:", dict(zip(chaves, valores)))

# QUE TIPOS PODEM SER CHAVE?
# Só tipos IMUTÁVEIS: str, int, float, bool, tupla.
# Lista NÃO pode ser chave (é mutável) -> TypeError.
coordenadas = {
    (0, 0): "origem",
    (10, 20): "ponto A",
}
print("chave tupla:", coordenadas[(10, 20)])
# {[1, 2]: "x"}   # ERRO: TypeError: unhashable type: 'list'

# VALORES podem ser QUALQUER coisa: lista, outro dict, função, None...
print()


# =====================================================================
# 3. ACESSANDO VALORES: [] vs .get()
# =====================================================================

print("=" * 60)
print("3. ACESSANDO: [] vs get()")
print("=" * 60)

aluno = {"nome": "Carla", "nota": 8.5}

# Com colchetes: se a chave NÃO existir -> KeyError (o programa quebra)
print(aluno["nome"])
# print(aluno["email"])   # ERRO: KeyError: 'email'

# Com .get(): se a chave NÃO existir -> retorna None (ou o padrão que
# você escolher). O programa NÃO quebra.
print("get email:", aluno.get("email"))
print("get email com padrão:", aluno.get("email", "sem email"))
print("get nome:", aluno.get("nome", "sem nome"))   # existe: retorna o valor

# QUANDO USAR CADA UM?
#   []    -> quando a chave TEM que existir. Se não existir é um bug, e
#            é melhor o programa avisar com erro do que seguir errado.
#   get() -> quando a chave é OPCIONAL e você tem um valor padrão.

# Verificando se uma chave existe: operador "in" (olha as CHAVES)
print("'nome' in aluno ->", "nome" in aluno)
print("'email' in aluno ->", "email" in aluno)
print("'Carla' in aluno ->", "Carla" in aluno)   # False! in olha chaves, não valores
print("'Carla' in valores ->", "Carla" in aluno.values())

print("len(aluno) =", len(aluno))   # quantidade de PARES
print()


# =====================================================================
# 4. ADICIONANDO E ALTERANDO
# =====================================================================
# A mesma sintaxe faz as duas coisas:
#   dicionario[chave] = valor
#   - se a chave NÃO existe -> ADICIONA
#   - se a chave JÁ existe  -> SUBSTITUI o valor

print("=" * 60)
print("4. ADICIONANDO E ALTERANDO")
print("=" * 60)

carro = {"marca": "Fiat", "ano": 2020}
print("original:", carro)

carro["cor"] = "prata"      # adiciona
print("adicionou cor:", carro)

carro["ano"] = 2022         # altera
print("alterou ano:", carro)

# update(): adiciona/altera VÁRIOS de uma vez
carro.update({"ano": 2023, "km": 15000})
print("update:", carro)

# setdefault(): só adiciona se a chave NÃO existir, e retorna o valor
carro.setdefault("cor", "preto")       # já existe: não muda
carro.setdefault("portas", 4)          # não existe: adiciona
print("setdefault:", carro)
print()


# =====================================================================
# 5. REMOVENDO
# =====================================================================

print("=" * 60)
print("5. REMOVENDO")
print("=" * 60)

estoque = {"maçã": 10, "banana": 5, "uva": 0, "pera": 7, "kiwi": 3}
print("original:", estoque)

del estoque["uva"]                  # remove (KeyError se não existir)
print("del uva:", estoque)

qtd_banana = estoque.pop("banana")  # remove E retorna o valor
print("pop banana retornou:", qtd_banana, "->", estoque)

# pop com padrão: não dá erro se a chave não existir
print("pop inexistente:", estoque.pop("manga", "não tinha manga"))

ultimo = estoque.popitem()          # remove e retorna o ÚLTIMO par inserido
print("popitem:", ultimo, "->", estoque)

estoque.clear()                     # esvazia tudo
print("clear:", estoque)
print()


# =====================================================================
# 6. PERCORRENDO (LOOPS)
# =====================================================================
#   .keys()   -> as chaves
#   .values() -> os valores
#   .items()  -> os pares (chave, valor)  <- o MAIS usado

print("=" * 60)
print("6. PERCORRENDO")
print("=" * 60)

precos = {"café": 5.50, "pão": 1.20, "leite": 4.80}

print("keys:", list(precos.keys()))
print("values:", list(precos.values()))
print("items:", list(precos.items()))

# Loop direto no dict percorre as CHAVES
for produto_nome in precos:
    print(" chave:", produto_nome)

# Valores
print(" total de todos os preços:", sum(precos.values()))

# Chave E valor ao mesmo tempo (desempacotando a tupla)
for nome_produto, preco in precos.items():
    print(f" {nome_produto:<8} R$ {preco:>6.2f}")
    # :<8 alinha à esquerda em 8 espaços | :>6.2f alinha à direita

# Com enumerate, para ter também a posição
for posicao, (nome_produto, preco) in enumerate(precos.items(), start=1):
    print(f" {posicao}. {nome_produto}")
print()


# =====================================================================
# 7. MESCLANDO DICIONÁRIOS
# =====================================================================

print("=" * 60)
print("7. MESCLANDO")
print("=" * 60)

padrao = {"tema": "claro", "fonte": 12, "idioma": "pt-BR"}
usuario = {"tema": "escuro", "fonte": 16}

# Operador | (Python 3.9+): cria um NOVO dict. Em caso de chave
# repetida, vence o da DIREITA.
final = padrao | usuario
print("padrao | usuario:", final)

# Forma antiga (você vai ver em código mais velho): **desempacotamento
final_antigo = {**padrao, **usuario}
print("{**a, **b}:", final_antigo)

# |= altera o dict da esquerda (igual ao update)
padrao |= {"fonte": 20}
print("padrao |= ...:", padrao)
print()


# =====================================================================
# 8. DICIONÁRIOS ANINHADOS (dict dentro de dict)
# =====================================================================
# Muito comum para representar dados reais, como respostas de APIs.

print("=" * 60)
print("8. ANINHADOS")
print("=" * 60)

empresa = {
    "nome": "TechCorp",
    "endereco": {
        "rua": "Av. Paulista",
        "numero": 1000,
        "cidade": "São Paulo",
    },
    "funcionarios": ["Ana", "Bruno", "Carla"],
}

# Acessando "em camadas"
print("cidade:", empresa["endereco"]["cidade"])
print("1º funcionário:", empresa["funcionarios"][0])

# Alterando um nível interno
empresa["endereco"]["numero"] = 1500
empresa["funcionarios"].append("Diego")
print("número novo:", empresa["endereco"]["numero"])
print("funcionários:", empresa["funcionarios"])

# Acesso seguro em vários níveis com get encadeado
# (o {} como padrão evita erro se "endereco" não existir)
cep = empresa.get("endereco", {}).get("cep", "CEP não informado")
print("cep:", cep)

# Dicionário de dicionários: "tabela" indexada por um id
usuarios = {
    101: {"nome": "Ana", "admin": True},
    102: {"nome": "Bruno", "admin": False},
}
for id_usuario, dados in usuarios.items():
    tipo = "admin" if dados["admin"] else "comum"
    print(f" #{id_usuario} {dados['nome']} ({tipo})")
    # Atenção: dentro da f-string com aspas duplas, use aspas SIMPLES
    # na chave: dados['nome']
print()


# =====================================================================
# 9. LISTA DE DICIONÁRIOS (a estrutura mais comum do dia a dia)
# =====================================================================
# Cada dict é um "registro" (como uma linha de uma tabela/planilha).
# É exatamente o formato de JSON que APIs retornam.

print("=" * 60)
print("9. LISTA DE DICIONÁRIOS")
print("=" * 60)

funcionarios = [
    {"nome": "Ana", "setor": "TI", "salario": 8000},
    {"nome": "Bruno", "setor": "RH", "salario": 5000},
    {"nome": "Carla", "setor": "TI", "salario": 9500},
    {"nome": "Diego", "setor": "Vendas", "salario": 6000},
    {"nome": "Elisa", "setor": "RH", "salario": 5500},
]

# Percorrer
for funcionario in funcionarios:
    print(f" {funcionario['nome']:<6} | {funcionario['setor']:<6} | R$ {funcionario['salario']}")

# Filtrar (com list comprehension)
equipe_ti = [f for f in funcionarios if f["setor"] == "TI"]
print("TI:", [f["nome"] for f in equipe_ti])

# Somar um campo
folha_total = sum(f["salario"] for f in funcionarios)
print("folha total:", folha_total)

# Buscar um registro específico
def buscar_por_nome(lista: list[dict], nome: str) -> dict | None:
    for item in lista:
        if item["nome"] == nome:
            return item
    return None


print("busca Carla:", buscar_por_nome(funcionarios, "Carla"))
print("busca Zé:", buscar_por_nome(funcionarios, "Zé"))

# Maior salário: max() com key (lembra do lambda do material de funções?)
mais_bem_pago = max(funcionarios, key=lambda f: f["salario"])
print("maior salário:", mais_bem_pago["nome"])
print()


# =====================================================================
# 10. DICT COMPREHENSION
# =====================================================================
# Igual à list comprehension, mas com { } e chave: valor
#   {chave: valor for item in sequencia if condicao}

print("=" * 60)
print("10. DICT COMPREHENSION")
print("=" * 60)

quadrados = {n: n ** 2 for n in range(1, 6)}
print("quadrados:", quadrados)

# Transformar valores
precos_reais = {"café": 5.50, "pão": 1.20, "leite": 4.80}
precos_com_aumento = {item: round(valor * 1.1, 2) for item, valor in precos_reais.items()}
print("com 10% de aumento:", precos_com_aumento)

# Filtrar
caros = {item: valor for item, valor in precos_reais.items() if valor > 2}
print("só os caros:", caros)

# Inverter chave <-> valor (cuidado: valores repetidos se perdem)
siglas = {"SP": "São Paulo", "RJ": "Rio de Janeiro"}
estados_para_sigla = {nome: sigla for sigla, nome in siglas.items()}
print("invertido:", estados_para_sigla)

# Criar índice a partir da lista de dicts: nome -> salário
salario_por_nome = {f["nome"]: f["salario"] for f in funcionarios}
print("índice:", salario_por_nome)
print()


# =====================================================================
# 11. PADRÕES CLÁSSICOS: CONTAR E AGRUPAR
# =====================================================================
# Esses dois padrões aparecem em TODO lugar (entrevistas, relatórios,
# análise de dados). Vale a pena decorar.

print("=" * 60)
print("11. PADRÕES: CONTAR E AGRUPAR")
print("=" * 60)

# --- CONTAR ocorrências ---
frase = "o rato roeu a roupa do rei de roma o rato"
contagem = {}
for palavra in frase.split():
    # get(palavra, 0): se ainda não contei, começa em 0
    contagem[palavra] = contagem.get(palavra, 0) + 1
print("contagem:", contagem)

# --- AGRUPAR itens por uma característica ---
por_setor = {}
for f in funcionarios:
    setor = f["setor"]
    if setor not in por_setor:
        por_setor[setor] = []          # cria a lista na 1ª vez
    por_setor[setor].append(f["nome"])
print("agrupado:", por_setor)

# Mesma coisa, mais curta, com setdefault
por_setor_2 = {}
for f in funcionarios:
    por_setor_2.setdefault(f["setor"], []).append(f["nome"])
print("com setdefault:", por_setor_2)

# --- SOMAR por grupo ---
salario_por_setor = {}
for f in funcionarios:
    salario_por_setor[f["setor"]] = salario_por_setor.get(f["setor"], 0) + f["salario"]
print("soma por setor:", salario_por_setor)
print()


# =====================================================================
# 12. Counter E defaultdict (atalhos da biblioteca padrão)
# =====================================================================
# O módulo collections já tem versões prontas desses padrões.
# (import traz código de um módulo; será o assunto de um material futuro)

print("=" * 60)
print("12. Counter E defaultdict")
print("=" * 60)

from collections import Counter, defaultdict

# Counter: conta tudo automaticamente
contagem_pronta = Counter(frase.split())
print("Counter:", contagem_pronta)
print("3 mais comuns:", contagem_pronta.most_common(3))
print("letras de 'banana':", Counter("banana"))

# defaultdict: um dict que cria o valor padrão sozinho quando a chave
# não existe. defaultdict(list) cria [] | defaultdict(int) cria 0
grupos = defaultdict(list)
for f in funcionarios:
    grupos[f["setor"]].append(f["nome"])   # sem if, sem setdefault
print("defaultdict:", dict(grupos))

# DICA: aprenda primeiro os padrões "na mão" (seção 11) para entender
# o que acontece. Depois use Counter/defaultdict no dia a dia.
print()


# =====================================================================
# 13. CÓPIA vs REFERÊNCIA (pegadinha importante!)
# =====================================================================
# Fazer  b = a  NÃO copia o dicionário. As duas variáveis passam a
# apontar para o MESMO dicionário na memória. Mudou um, mudou o outro.
# (Vale o mesmo para listas.)

print("=" * 60)
print("13. CÓPIA vs REFERÊNCIA")
print("=" * 60)

original = {"a": 1, "b": 2}
referencia = original              # NÃO é cópia!
referencia["a"] = 999
print("original mudou junto:", original)

original = {"a": 1, "b": 2}
copia = original.copy()            # cópia de verdade (rasa)
copia["a"] = 999
print("original intacto:", original, "| cópia:", copia)

# CÓPIA RASA (.copy()) vs CÓPIA PROFUNDA (deepcopy)
# A cópia rasa copia só o "primeiro nível". Listas/dicts DENTRO dela
# continuam compartilhados.
import copy

time_a = {"nome": "Time A", "membros": ["Ana", "Bruno"]}
rasa = time_a.copy()
profunda = copy.deepcopy(time_a)

rasa["membros"].append("Carla")    # mexe na lista interna...
print("time_a após mexer na RASA:", time_a["membros"])    # mudou também!
profunda["membros"].append("Zé")
print("time_a após mexer na PROFUNDA:", time_a["membros"])  # não mudou

# Isso também acontece ao passar dict para uma FUNÇÃO: a função recebe
# o MESMO dict, e se alterar, altera o de fora.
def aplicar_bonus(funcionario: dict) -> None:
    funcionario["salario"] *= 1.1


ana = {"nome": "Ana", "salario": 1000}
aplicar_bonus(ana)
print("ana depois da função:", ana)   # mudou!
print()


# =====================================================================
# 14. ORDENANDO DICIONÁRIOS
# =====================================================================

print("=" * 60)
print("14. ORDENANDO")
print("=" * 60)

notas = {"Carla": 9.0, "Ana": 7.5, "Bruno": 6.2}

# sorted() em um dict retorna uma LISTA das chaves ordenadas
print("chaves ordenadas:", sorted(notas))

# Ordenar por CHAVE e manter como dict
print("por nome:", dict(sorted(notas.items())))

# Ordenar por VALOR: key=lambda item: item[1]  (item = (chave, valor))
print("por nota:", dict(sorted(notas.items(), key=lambda item: item[1])))
print("ranking:", dict(sorted(notas.items(), key=lambda item: item[1], reverse=True)))

# Ordenar lista de dicts por um campo
por_salario = sorted(funcionarios, key=lambda f: f["salario"], reverse=True)
print("top 3 salários:", [f["nome"] for f in por_salario[:3]])
print()


# =====================================================================
# 15. DICIONÁRIO NO LUGAR DE MUITOS if/elif
# =====================================================================
# Quando você tem um if/elif que só "traduz" um valor em outro, um dict
# costuma ser mais limpo. (O menu do 1º arquivo de respostas e a
# calculadora do exercício 10 de funções usaram essa ideia.)

print("=" * 60)
print("15. DICT NO LUGAR DE if/elif")
print("=" * 60)


# Com if/elif
def nome_do_dia_if(numero: int) -> str:
    if numero == 1:
        return "Domingo"
    elif numero == 2:
        return "Segunda"
    elif numero == 3:
        return "Terça"
    # ... e por aí vai
    return "Inválido"


# Com dicionário
DIAS_DA_SEMANA = {
    1: "Domingo", 2: "Segunda", 3: "Terça", 4: "Quarta",
    5: "Quinta", 6: "Sexta", 7: "Sábado",
}


def nome_do_dia(numero: int) -> str:
    return DIAS_DA_SEMANA.get(numero, "Inválido")


print("if:", nome_do_dia_if(2), "| dict:", nome_do_dia(2), "| inválido:", nome_do_dia(9))
print()


# =====================================================================
# 16. DICIONÁRIOS E JSON
# =====================================================================
# JSON é o formato de texto mais usado para trocar dados na web (APIs,
# arquivos de configuração). Ele é praticamente igual a um dict Python.
# O módulo json converte um no outro.

print("=" * 60)
print("16. DICT <-> JSON")
print("=" * 60)

import json

dados = {"nome": "Ana", "idade": 25, "ativo": True, "tags": ["dev", "python"]}

texto_json = json.dumps(dados, ensure_ascii=False)     # dict -> texto JSON
print("JSON:", texto_json, type(texto_json))
# Repare: True virou true. JSON tem pequenas diferenças de sintaxe.

de_volta = json.loads(texto_json)                      # texto JSON -> dict
print("de volta:", de_volta["tags"], type(de_volta))

print(json.dumps(dados, indent=2, ensure_ascii=False))  # formatado bonito
print()


# =====================================================================
# 17. ERROS COMUNS
# =====================================================================

print("=" * 60)
print("17. ERROS COMUNS")
print("=" * 60)

# ERRO 1: KeyError ao acessar chave que não existe
#   aluno["email"]  -> use aluno.get("email") ou verifique com "in"

# ERRO 2: alterar o tamanho do dict ENQUANTO percorre ele
#   for chave in estoque:
#       if estoque[chave] == 0:
#           del estoque[chave]   # RuntimeError: dictionary changed size
# Solução: percorrer uma CÓPIA das chaves, ou criar um dict novo
estoque = {"maçã": 10, "uva": 0, "pera": 7, "kiwi": 0}
for chave in list(estoque.keys()):        # list(...) faz uma cópia
    if estoque[chave] == 0:
        del estoque[chave]
print("sem zerados (cópia das chaves):", estoque)

estoque = {"maçã": 10, "uva": 0, "pera": 7, "kiwi": 0}
estoque = {k: v for k, v in estoque.items() if v != 0}   # mais pythônico
print("sem zerados (comprehension):", estoque)

# ERRO 3: esquecer que "in" olha só as CHAVES
# ERRO 4: achar que b = a copia (seção 13)
# ERRO 5: chave repetida na criação. A última vence, sem aviso nenhum:
repetido = {"a": 1, "a": 2}
print("chave repetida:", repetido)

# ERRO 6: confundir chave str com int
codigos = {1: "um"}
print("codigos.get('1'):", codigos.get("1"))   # None! "1" != 1
print()


# =====================================================================
# 18. NAMING CONVENTIONS E BOAS PRÁTICAS
# =====================================================================
# NOME DA VARIÁVEL:
#   - snake_case, como sempre: dados_usuario, config_sistema
#   - Um padrão MUITO claro para dicts que funcionam como "mapa":
#       valor_por_chave  ->  preco_por_produto, salario_por_nome,
#                            usuarios_por_id, alunos_por_turma
#     Só de ler o nome você sabe o que é chave e o que é valor.
#   - Dict que representa UMA coisa: nome no singular
#       usuario = {"nome": ..., "email": ...}
#   - Lista de dicts: plural -> usuarios = [{...}, {...}]
#   - Dict constante (não muda): UPPER_SNAKE_CASE -> DIAS_DA_SEMANA
#
# NOME DAS CHAVES:
#   - Strings em snake_case: "data_nascimento", não "Data Nascimento"
#   - Consistência: se um registro usa "nome", todos usam "nome"
#     (não misture "nome", "Nome" e "name")
#
# BOAS PRÁTICAS:
#   1. Use [] quando a chave é obrigatória, get() quando é opcional.
#   2. Use .items() para percorrer chave e valor juntos.
#   3. Prefira dict a vários if/elif que só traduzem valores.
#   4. Cuidado com dicts muito aninhados (3+ níveis): ficam difíceis de
#      ler. Considere funções auxiliares ou, mais pra frente, classes.
#   5. Lembre que dicts são passados por REFERÊNCIA para funções.
#   6. Quando um dict representa sempre a mesma "forma" de dado
#      (sempre nome, email, idade), em projetos maiores isso vira uma
#      CLASSE ou dataclass. É o caminho natural do seu estudo.

print("=" * 60)
print("FIM! Agora vá para os exercícios no final do arquivo.")
print("=" * 60)


# =====================================================================
# 19. EXERCÍCIOS PARA PRATICAR
# =====================================================================
# Crie um arquivo novo (ex: exercicios_dicionarios.py). Use funções com
# type hints e return sempre que fizer sentido.
#
#  1. Crie um dict representando você (nome, idade, cidade, linguagens
#     que estuda como lista). Imprima cada par no formato "chave: valor".
#  2. Crie uma agenda {nome: telefone} com 3 contatos. Adicione um,
#     altere outro e remova um terceiro. Imprima a agenda a cada passo.
#  3. Crie buscar_telefone(agenda, nome) que retorna o telefone ou
#     "Contato não encontrado" (sem usar if, use get).
#  4. Crie contar_letras(texto) que retorna um dict {letra: quantidade},
#     ignorando espaços e sem diferenciar maiúsculas. Faça SEM Counter.
#  5. Dado o dict de notas {"Ana": [8, 9], "Bruno": [5, 6, 7],
#     "Carla": [10, 9.5]}, crie um NOVO dict {aluno: média} usando
#     dict comprehension.
#  6. Com o resultado do exercício 5, imprima o ranking dos alunos da
#     maior para a menor média.
#  7. Dada uma lista de dicts de produtos (nome, categoria, preco),
#     crie agrupar_por_categoria(produtos) que retorna
#     {categoria: [nomes]}.
#  8. Com a mesma lista, crie total_por_categoria(produtos) que retorna
#     {categoria: soma_dos_precos}.
#  9. Crie inverter_dict(d) que troca chaves e valores. Depois pense:
#     o que acontece se dois valores forem iguais?
# 10. Crie mesclar_somando(d1, d2): mescla dois dicts de contagem e,
#     quando a chave existir nos dois, SOMA os valores.
#     {"a": 1, "b": 2} + {"b": 3, "c": 4} -> {"a": 1, "b": 5, "c": 4}
# 11. (Desafio) Carrinho de compras: um dict CATALOGO {produto: preço}
#     e um carrinho {produto: quantidade}. Crie funções
#     adicionar_ao_carrinho, remover_do_carrinho e calcular_total.
#     Ignore produtos que não estão no catálogo.
# 12. (Desafio) Crie contar_palavras(texto) que retorna as 3 palavras
#     mais frequentes de um texto, ignorando maiúsculas e pontuação
#     (.,!?). Faça primeiro "na mão" e depois com Counter.
