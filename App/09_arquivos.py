"""
=====================================================================
  MATERIAL DE ESTUDO PYTHON — ARQUIVOS
  O que são -> Caminhos -> open() e modos -> with -> Ler -> Escrever ->
  Acrescentar -> Encoding -> pathlib -> Pastas -> CSV -> JSON ->
  Erros comuns -> Mini projeto -> Boas práticas
=====================================================================

PRÉ-REQUISITOS: 01 a 07 (principalmente funções, dicionários e
try/except).

COMO USAR ESTE ARQUIVO:
  1. Leia os comentários de cima para baixo.
  2. Rode no terminal:   python 09_arquivos.py
  3. Este arquivo CRIA uma pasta chamada "saida_09_arquivos" ao lado
     dele, com todos os arquivos dos exemplos. Abra essa pasta e olhe
     os arquivos no editor/Bloco de Notas/Excel depois de rodar!
  4. Pode apagar a pasta quando quiser. Ela é recriada a cada execução.
"""

import csv
import json
import shutil
from pathlib import Path


# =====================================================================
# 1. POR QUE ARQUIVOS?
# =====================================================================
# Tudo que fica em variáveis vive na memória RAM e SOME quando o
# programa termina. Para guardar dados de forma PERMANENTE (salvar uma
# lista de tarefas, um relatório, configurações...), você grava em
# ARQUIVOS no disco.
#
# Tipos principais:
#   - Arquivos de TEXTO: .txt, .csv, .json, .py, .html... (você abre no
#     Bloco de Notas e entende)
#   - Arquivos BINÁRIOS: imagens, PDF, .xlsx, .zip... (precisam de
#     programas ou bibliotecas específicas)
# Este material foca em arquivos de texto, que são 90% do dia a dia.


# =====================================================================
# 2. CAMINHOS (PATHS)
# =====================================================================
# Caminho = o "endereço" de um arquivo.
#
#   ABSOLUTO -> endereço completo, desde a raiz do disco
#               Windows: E:\dev\pythonStudies\notas.txt
#               Linux/Mac: /home/diego/notas.txt
#   RELATIVO -> endereço a partir da PASTA ATUAL de onde o programa foi
#               executado (o "diretório de trabalho")
#               notas.txt, dados/notas.txt, ../outra_pasta/notas.txt
#               (".." significa "a pasta de cima")
#
# PEGADINHA: caminho relativo depende de ONDE você rodou o comando
# "python", e não de onde o .py está. Se você rodar de outra pasta, o
# arquivo "some". Solução: montar caminhos a partir da pasta do script
# (usando __file__), como faremos abaixo.
#
# PEGADINHA DO WINDOWS: a barra invertida \ é caractere especial em
# strings ("\n" = nova linha, "\t" = tab). Então "C:\novos\teste.txt"
# vira lixo! Soluções:
#   - usar barra normal: "C:/novos/teste.txt"  (Python aceita no Windows)
#   - usar raw string:   r"C:\novos\teste.txt"
#   - usar pathlib (o melhor, ver abaixo)

print("=" * 60)
print("2. CAMINHOS")
print("=" * 60)

print("Pasta atual (onde rodei o python):", Path.cwd())
print("Este arquivo está em:", Path(__file__).resolve().parent)

# pathlib.Path: a forma MODERNA de trabalhar com caminhos.
# O operador / junta pedaços de caminho, no padrão certo de cada sistema.
PASTA_SCRIPT = Path(__file__).resolve().parent
PASTA_SAIDA = PASTA_SCRIPT / "saida_09_arquivos"

# Recria a pasta de saída do zero a cada execução
if PASTA_SAIDA.exists():
    shutil.rmtree(PASTA_SAIDA)        # apaga a pasta e tudo dentro
PASTA_SAIDA.mkdir()

print("Pasta de saída dos exemplos:", PASTA_SAIDA)

exemplo = PASTA_SAIDA / "relatorios" / "vendas_2026.csv"
print("Caminho montado:", exemplo)
print("  .name   ->", exemplo.name)       # vendas_2026.csv
print("  .stem   ->", exemplo.stem)       # vendas_2026
print("  .suffix ->", exemplo.suffix)     # .csv
print("  .parent ->", exemplo.parent.name)  # relatorios
print()


# =====================================================================
# 3. open() E OS MODOS DE ABERTURA
# =====================================================================
# open(caminho, modo, encoding="utf-8")
#
# ---------------------------------------------------------------------
#  MODO | NOME      | O QUE FAZ
# ---------------------------------------------------------------------
#  "r"  | read      | LÊ. Erro se o arquivo não existir. (é o padrão)
#  "w"  | write     | ESCREVE. Cria o arquivo, ou APAGA TUDO se já
#       |           | existir! Cuidado.
#  "a"  | append    | ACRESCENTA no final. Cria se não existir.
#  "x"  | exclusive | CRIA. Erro se o arquivo JÁ existir (protege
#       |           | contra sobrescrever sem querer).
# ---------------------------------------------------------------------
#  + "b" para binário: "rb", "wb" (imagens, PDF...)
#
# ENCODING: SEMPRE passe encoding="utf-8" em arquivos de texto.
# No Windows, o padrão é outro (cp1252), e acentos viram "Ã§Ã£o" ou dão
# UnicodeDecodeError ao abrir o arquivo em outro sistema.


# =====================================================================
# 4. with: SEMPRE USE
# =====================================================================
# Todo arquivo aberto precisa ser FECHADO (.close()). Se não fechar,
# dados podem não ser gravados e o arquivo fica "preso".
#
#   SEM with (evite):              COM with (use sempre):
#   arquivo = open(...)            with open(...) as arquivo:
#   arquivo.write("oi")                arquivo.write("oi")
#   arquivo.close()                # fechado automaticamente aqui,
#   # e se der erro antes do           # MESMO se der erro
#   # close? fica aberto!
#
# Visto no material de erros: o with é um try/finally automático.


# =====================================================================
# 5. ESCREVENDO ARQUIVOS: "w"
# =====================================================================

print("=" * 60)
print("5. ESCREVENDO")
print("=" * 60)

caminho_notas = PASTA_SAIDA / "anotacoes.txt"

with open(caminho_notas, "w", encoding="utf-8") as arquivo:
    arquivo.write("Estudando Python\n")      # \n = quebra de linha
    arquivo.write("Hoje: arquivos\n")        # write NÃO coloca \n sozinho!
    arquivo.write("Próximo: módulos\n")

print("Criado:", caminho_notas.name)

# writelines(): escreve uma LISTA de strings (também sem \n automático)
tarefas = ["Ler material", "Fazer exercícios", "Revisar respostas"]
caminho_tarefas = PASTA_SAIDA / "tarefas.txt"
with open(caminho_tarefas, "w", encoding="utf-8") as arquivo:
    arquivo.writelines(f"{tarefa}\n" for tarefa in tarefas)
print("Criado:", caminho_tarefas.name)

# print() também escreve em arquivo, com o parâmetro file=
# (e esse sim põe o \n sozinho)
with open(PASTA_SAIDA / "com_print.txt", "w", encoding="utf-8") as arquivo:
    print("Linha escrita com print", file=arquivo)
    print("Total:", 42, file=arquivo)
print("Criado: com_print.txt")

# ATENÇÃO: "w" APAGA o conteúdo anterior.
with open(caminho_tarefas, "w", encoding="utf-8") as arquivo:
    arquivo.write("só sobrou esta linha\n")
print("Depois de abrir com 'w' de novo:", caminho_tarefas.read_text(encoding="utf-8").strip())

# Recolocando as tarefas para os próximos exemplos
with open(caminho_tarefas, "w", encoding="utf-8") as arquivo:
    arquivo.writelines(f"{tarefa}\n" for tarefa in tarefas)
print()


# =====================================================================
# 6. LENDO ARQUIVOS: "r"
# =====================================================================

print("=" * 60)
print("6. LENDO")
print("=" * 60)

# 6.1 read(): o arquivo INTEIRO numa única string
with open(caminho_notas, "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()
print("read() ->", repr(conteudo))     # repr mostra os \n escondidos

# 6.2 Loop linha a linha: a forma MAIS USADA e a mais eficiente
# (lê uma linha por vez, então funciona até com arquivos gigantes)
print("loop linha a linha:")
with open(caminho_notas, encoding="utf-8") as arquivo:   # "r" é o padrão
    for numero, linha in enumerate(arquivo, start=1):
        # Cada linha VEM COM o \n no final. strip() remove.
        print(f"  {numero}: {linha.strip()}")

# 6.3 readlines(): lista com todas as linhas (cada uma com \n)
with open(caminho_notas, encoding="utf-8") as arquivo:
    linhas = arquivo.readlines()
print("readlines() ->", linhas)

# 6.4 Truque comum: lista de linhas JÁ SEM o \n
with open(caminho_notas, encoding="utf-8") as arquivo:
    linhas_limpas = arquivo.read().splitlines()
print("splitlines() ->", linhas_limpas)

# 6.5 readline(): uma linha por vez, manualmente
with open(caminho_notas, encoding="utf-8") as arquivo:
    primeira = arquivo.readline()
    segunda = arquivo.readline()
print("readline() x2 ->", repr(primeira), repr(segunda))

# O arquivo tem um "cursor": depois de lido até o fim, um novo read()
# devolve "" (vazio). Para ler de novo, abra de novo.
print()


# =====================================================================
# 7. ACRESCENTANDO: "a"
# =====================================================================
# Ideal para LOGS e históricos: cada execução adiciona no final, sem
# apagar o que já estava lá.

print("=" * 60)
print("7. ACRESCENTANDO (append)")
print("=" * 60)

caminho_log = PASTA_SAIDA / "log.txt"
for evento in ["programa iniciado", "usuário logou", "relatório gerado"]:
    with open(caminho_log, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"[INFO] {evento}\n")

print(caminho_log.read_text(encoding="utf-8"), end="")


# Modo "x": protege contra sobrescrever
try:
    with open(caminho_log, "x", encoding="utf-8") as arquivo:
        arquivo.write("nunca vai rodar")
except FileExistsError:
    print("modo 'x': log.txt já existe, nada foi sobrescrito")
print()


# =====================================================================
# 8. ATALHOS DO pathlib: read_text() E write_text()
# =====================================================================
# Para ler/escrever um arquivo pequeno INTEIRO de uma vez, sem with:

print("=" * 60)
print("8. ATALHOS DO pathlib")
print("=" * 60)

caminho_rapido = PASTA_SAIDA / "rapido.txt"
caminho_rapido.write_text("Escrito com write_text\nSegunda linha\n", encoding="utf-8")
print(caminho_rapido.read_text(encoding="utf-8").splitlines())

# Use os atalhos para casos simples; use with + open para ler linha a
# linha, usar append ou processar arquivos grandes.
print()


# =====================================================================
# 9. TRABALHANDO COM PASTAS E VERIFICANDO ARQUIVOS
# =====================================================================

print("=" * 60)
print("9. PASTAS E VERIFICAÇÕES")
print("=" * 60)

pasta_relatorios = PASTA_SAIDA / "relatorios" / "2026"
pasta_relatorios.mkdir(parents=True, exist_ok=True)
# parents=True  -> cria as pastas intermediárias que faltarem
# exist_ok=True -> não dá erro se a pasta já existir

for mes in ["janeiro", "fevereiro", "marco"]:
    (pasta_relatorios / f"{mes}.txt").write_text(f"Relatório de {mes}\n", encoding="utf-8")

print("existe anotacoes.txt?", caminho_notas.exists())
print("existe fantasma.txt?", (PASTA_SAIDA / "fantasma.txt").exists())
print("é arquivo?", caminho_notas.is_file(), "| é pasta?", pasta_relatorios.is_dir())
print("tamanho de anotacoes.txt:", caminho_notas.stat().st_size, "bytes")

# Listar o conteúdo de uma pasta
print("Conteúdo da pasta de saída:")
for item in sorted(PASTA_SAIDA.iterdir()):
    tipo = "pasta" if item.is_dir() else "arquivo"
    print(f"  [{tipo}] {item.name}")

# glob: buscar por padrão. * = qualquer coisa | ** = qualquer subpasta
print("Todos os .txt (inclusive subpastas):")
for arquivo in sorted(PASTA_SAIDA.glob("**/*.txt")):
    print("  ", arquivo.relative_to(PASTA_SAIDA))

# Renomear e apagar
renomeado = caminho_rapido.rename(PASTA_SAIDA / "rapido_renomeado.txt")
print("renomeado para:", renomeado.name)
renomeado.unlink()                      # unlink = apagar arquivo
print("apagado? ", not renomeado.exists())
# Para apagar pasta VAZIA: pasta.rmdir()
# Para apagar pasta COM conteúdo: shutil.rmtree(pasta)  (cuidado!)
print()


# =====================================================================
# 10. CSV: DADOS EM TABELA
# =====================================================================
# CSV (Comma-Separated Values) = tabela em texto puro. Cada linha é um
# registro, e os campos são separados por vírgula (ou ponto e vírgula).
# Abre direto no Excel/Google Sheets.
#
#   nome,setor,salario
#   Ana,TI,8000
#   Bruno,RH,5000
#
# Use o módulo csv, NÃO split(","). Ele trata casos difíceis, como
# campos que contêm vírgula: "Silva, Ana".
#
# Ao abrir CSV para escrita, use newline="" (senão o Windows cria
# linhas em branco extras entre os registros).

print("=" * 60)
print("10. CSV")
print("=" * 60)

funcionarios = [
    {"nome": "Ana", "setor": "TI", "salario": 8000},
    {"nome": "Bruno", "setor": "RH", "salario": 5000},
    {"nome": "Carla", "setor": "TI", "salario": 9500},
    {"nome": "Silva, Diego", "setor": "Vendas", "salario": 6000},  # tem vírgula!
]

# 10.1 ESCREVER com DictWriter (a partir de uma lista de dicts)
caminho_csv = PASTA_SAIDA / "funcionarios.csv"
with open(caminho_csv, "w", encoding="utf-8", newline="") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=["nome", "setor", "salario"])
    escritor.writeheader()                 # escreve a linha de cabeçalho
    escritor.writerows(funcionarios)       # escreve todos os registros

print("Conteúdo bruto do CSV:")
print(caminho_csv.read_text(encoding="utf-8"))
# Repare: "Silva, Diego" foi salvo entre aspas automaticamente.

# 10.2 LER com DictReader: cada linha vira um dict
with open(caminho_csv, encoding="utf-8", newline="") as arquivo:
    leitor = csv.DictReader(arquivo)
    dados_lidos = list(leitor)

print("Primeiro registro lido:", dados_lidos[0])

# ATENÇÃO: tudo que vem do CSV é TEXTO (str). Converta números!
print("tipo do salário lido:", type(dados_lidos[0]["salario"]).__name__)
folha = sum(int(f["salario"]) for f in dados_lidos)
print("folha total:", folha)

# 10.3 writer/reader simples (listas em vez de dicts)
caminho_notas_csv = PASTA_SAIDA / "notas.csv"
with open(caminho_notas_csv, "w", encoding="utf-8", newline="") as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(["aluno", "nota1", "nota2"])
    escritor.writerow(["Ana", 8, 9])
    escritor.writerow(["Bruno", 6, 7])

with open(caminho_notas_csv, encoding="utf-8", newline="") as arquivo:
    leitor = csv.reader(arquivo)
    cabecalho = next(leitor)            # next() pega a 1ª linha (cabeçalho)
    for aluno, nota1, nota2 in leitor:
        media = (float(nota1) + float(nota2)) / 2
        print(f"  {aluno}: média {media}")

# DICA BRASIL: o Excel em português costuma usar ";" como separador.
# Para gerar um CSV que abre certinho no Excel BR:
#   csv.writer(arquivo, delimiter=";")
#   e encoding="utf-8-sig" (o "-sig" faz o Excel reconhecer os acentos)
caminho_excel = PASTA_SAIDA / "funcionarios_excel_br.csv"
with open(caminho_excel, "w", encoding="utf-8-sig", newline="") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=["nome", "setor", "salario"], delimiter=";")
    escritor.writeheader()
    escritor.writerows(funcionarios)
print("Criado:", caminho_excel.name, "(abra no Excel!)")
print()


# =====================================================================
# 11. JSON: SALVANDO ESTRUTURAS PYTHON
# =====================================================================
# Visto no material de dicionários: JSON ≈ dict/list do Python.
# json.dumps / json.loads -> convertem para/de TEXTO (string)
# json.dump  / json.load  -> escrevem/leem direto de ARQUIVO (sem o "s")
#
# Ótimo para: configurações, salvar o estado de um programa, trocar
# dados com APIs. Mantém tipos (número continua número, lista continua
# lista), diferente do CSV.

print("=" * 60)
print("11. JSON")
print("=" * 60)

configuracao = {
    "usuario": "diego",
    "tema": "escuro",
    "tamanho_fonte": 14,
    "notificacoes": True,
    "atalhos": ["ctrl+s", "ctrl+z"],
}

caminho_json = PASTA_SAIDA / "config.json"
with open(caminho_json, "w", encoding="utf-8") as arquivo:
    json.dump(configuracao, arquivo, indent=2, ensure_ascii=False)
    # indent=2           -> arquivo legível, com quebras de linha
    # ensure_ascii=False -> mantém acentos como "ç" em vez de "\u00e7"
print("Criado:", caminho_json.name)

with open(caminho_json, encoding="utf-8") as arquivo:
    config_lida = json.load(arquivo)

print("tamanho_fonte:", config_lida["tamanho_fonte"], type(config_lida["tamanho_fonte"]).__name__)
print("igual ao original?", config_lida == configuracao)

# CSV ou JSON?
#   CSV  -> dados em TABELA (linhas e colunas iguais), abrir no Excel
#   JSON -> dados ANINHADOS (dict dentro de lista dentro de dict),
#           configurações, comunicação com APIs
print()


# =====================================================================
# 12. ERROS COMUNS COM ARQUIVOS (e como tratar)
# =====================================================================
#   FileNotFoundError   -> arquivo/pasta não existe (caminho errado?)
#   FileExistsError     -> modo "x" e o arquivo já existe
#   PermissionError     -> sem permissão, ou arquivo aberto em outro
#                          programa (no Windows, Excel trava o arquivo!)
#   IsADirectoryError   -> tentou abrir uma PASTA como arquivo
#   UnicodeDecodeError  -> encoding errado na leitura
#   json.JSONDecodeError-> o arquivo não é um JSON válido

print("=" * 60)
print("12. ERROS COMUNS")
print("=" * 60)


def carregar_json(caminho: Path, padrao: dict | None = None) -> dict:
    """Carrega um JSON. Se não existir ou estiver corrompido, devolve o padrão."""
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print(f"  '{caminho.name}' não existe, usando padrão")
    except json.JSONDecodeError as e:
        print(f"  '{caminho.name}' está corrompido ({e.msg}), usando padrão")
    return padrao if padrao is not None else {}


print(carregar_json(caminho_json)["tema"])
print(carregar_json(PASTA_SAIDA / "nao_existe.json", {"tema": "claro"}))

corrompido = PASTA_SAIDA / "corrompido.json"
corrompido.write_text('{"tema": "escuro",', encoding="utf-8")   # JSON incompleto
print(carregar_json(corrompido, {"tema": "claro"}))

# Demonstrando o problema de encoding: grava em utf-8, lê com outro
texto_acentuado = PASTA_SAIDA / "acentos.txt"
texto_acentuado.write_text("Ação, coração, pão", encoding="utf-8")
print("lido com utf-8:  ", texto_acentuado.read_text(encoding="utf-8"))
print("lido com cp1252: ", texto_acentuado.read_text(encoding="cp1252"), " <- quebrado!")
print()


# =====================================================================
# 13. MINI PROJETO: LISTA DE TAREFAS QUE NÃO SE PERDE
# =====================================================================
# Juntando tudo: funções + dicionários + try/except + JSON.
# Os dados sobrevivem entre execuções do programa porque ficam salvos
# em arquivo.

print("=" * 60)
print("13. MINI PROJETO: TAREFAS SALVAS EM JSON")
print("=" * 60)

CAMINHO_TAREFAS = PASTA_SAIDA / "tarefas.json"


def carregar_tarefas() -> list[dict]:
    try:
        with open(CAMINHO_TAREFAS, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_tarefas(tarefas: list[dict]) -> None:
    with open(CAMINHO_TAREFAS, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, indent=2, ensure_ascii=False)


def adicionar_tarefa(titulo: str) -> None:
    tarefas = carregar_tarefas()
    tarefas.append({"titulo": titulo, "feita": False})
    salvar_tarefas(tarefas)


def concluir_tarefa(titulo: str) -> bool:
    tarefas = carregar_tarefas()
    for tarefa in tarefas:
        if tarefa["titulo"] == titulo:
            tarefa["feita"] = True
            salvar_tarefas(tarefas)
            return True
    return False


def listar_tarefas() -> None:
    tarefas = carregar_tarefas()
    if not tarefas:
        print("  (nenhuma tarefa)")
    for tarefa in tarefas:
        marcador = "x" if tarefa["feita"] else " "
        print(f"  [{marcador}] {tarefa['titulo']}")


listar_tarefas()
adicionar_tarefa("Estudar arquivos")
adicionar_tarefa("Fazer exercícios de arquivos")
adicionar_tarefa("Estudar módulos")
concluir_tarefa("Estudar arquivos")
listar_tarefas()
print(f"  (salvo em {CAMINHO_TAREFAS.name}: abra o arquivo e veja!)")
print()


# =====================================================================
# 14. NAMING CONVENTIONS E BOAS PRÁTICAS
# =====================================================================
# NOMES DE VARIÁVEIS:
#   - Diferencie CAMINHO de CONTEÚDO de ARQUIVO ABERTO:
#       caminho_relatorio = Path("relatorio.txt")   # o endereço
#       with open(caminho_relatorio) as arquivo:     # o arquivo aberto
#           conteudo = arquivo.read()                # o texto
#     Usar "arquivo" para as três coisas confunde muito.
#   - Constantes de caminho em MAIÚSCULAS: PASTA_DADOS, CAMINHO_CONFIG
#   - Variável do with: arquivo, f (muito comum), ou algo específico
#     como arquivo_csv, arquivo_log
#
# NOMES DE ARQUIVOS NO DISCO:
#   - Minúsculas, sem espaços e sem acentos: relatorio_vendas_2026.csv
#     (espaços e acentos dão problema em terminal, servidores e URLs)
#   - Datas no formato ANO-MÊS-DIA para ordenar certo: log_2026-10-02.txt
#   - A extensão deve refletir o conteúdo (.csv, .json, .txt)
#
# BOAS PRÁTICAS:
#   1. SEMPRE use with para abrir arquivos.
#   2. SEMPRE passe encoding="utf-8" (e newline="" para CSV).
#   3. Prefira pathlib (Path) para montar caminhos, em vez de juntar
#      strings com "+" ou "\\".
#   4. Monte caminhos a partir da pasta do script (Path(__file__)) para
#      não depender de onde o programa foi executado.
#   5. Cuidado com o modo "w": ele apaga tudo. Na dúvida, use "x" ou
#      verifique com .exists() antes.
#   6. Trate FileNotFoundError e JSONDecodeError ao carregar dados.
#   7. Use os módulos csv e json em vez de "parsear" texto na mão.
#   8. Lembre que tudo que vem de .txt/.csv é str: converta números.
#   9. Para arquivos grandes, leia linha a linha (for linha in arquivo)
#      em vez de read(), para não carregar tudo na memória.

print("=" * 60)
print(f"FIM! Abra a pasta '{PASTA_SAIDA.name}' para ver os arquivos criados.")
print("Depois vá para os exercícios no final deste arquivo.")
print("=" * 60)


# =====================================================================
# 15. EXERCÍCIOS PARA PRATICAR
# =====================================================================
# Crie um arquivo novo (ex: exercicios_arquivos.py). Use with,
# encoding="utf-8" e pathlib em todos.
#
#  1. Escreva um arquivo "diario.txt" com 3 linhas sobre o seu dia.
#     Depois leia e imprima cada linha numerada.
#  2. Crie contar_linhas_palavras(caminho) que retorna uma tupla
#     (quantidade_de_linhas, quantidade_de_palavras).
#  3. Crie registrar_log(mensagem) que ACRESCENTA a mensagem em
#     "app.log" no formato "[2026-10-02 14:30:00] mensagem".
#     Dica: from datetime import datetime
#           datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#  4. Crie copiar_arquivo(origem, destino) que lê um arquivo e escreve
#     uma cópia. Se a origem não existir, mostre uma mensagem amigável.
#  5. Dado um arquivo "numeros.txt" com um número por linha (inclua
#     algumas linhas inválidas, como "abc" e linhas vazias), calcule a
#     soma e a média apenas dos números válidos.
#  6. Crie um CSV "produtos.csv" com nome, categoria e preço de 5
#     produtos usando DictWriter. Depois leia com DictReader e mostre o
#     produto mais caro.
#  7. Leia o "produtos.csv" do exercício 6 e gere um NOVO CSV
#     "resumo_categorias.csv" com categoria, quantidade de produtos e
#     preço médio.
#  8. Crie salvar_contatos(contatos) e carregar_contatos() que salvam e
#     carregam uma agenda {nome: telefone} em "contatos.json".
#     carregar_contatos() deve retornar {} se o arquivo não existir.
#  9. Crie listar_arquivos(pasta, extensao) que retorna os nomes de
#     todos os arquivos com aquela extensão (ex: ".py") na pasta,
#     ordenados. Teste na sua pasta pythonStudies.
# 10. (Desafio) Agenda persistente com menu (while + input): listar,
#     adicionar, buscar e remover contatos, salvando em JSON a cada
#     alteração. Feche o programa, abra de novo e confira que os
#     contatos continuam lá.
# 11. (Desafio) Crie substituir_no_arquivo(caminho, antigo, novo) que
#     troca todas as ocorrências de um texto dentro do arquivo e retorna
#     quantas substituições foram feitas.
