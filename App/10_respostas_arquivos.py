"""
=====================================================================
  RESPOSTAS DOS EXERCÍCIOS — 09_arquivos.py
=====================================================================

COMO USAR ESTE ARQUIVO:
  Tente resolver SOZINHO antes de olhar! Depois compare com a resposta.
  Existem várias formas certas de resolver cada exercício; a sua pode
  ser diferente e estar correta.

  Rode:   python 10_respostas_arquivos.py

  Os arquivos criados ficam na pasta "saida_10_respostas", ao lado deste
  script. Diferente do material 09, esta pasta NÃO é apagada a cada
  execução, para você ver duas coisas acontecendo:
    - o app.log (exercício 3) CRESCE a cada execução (modo "a")
    - a agenda (exercício 10) CONTINUA salva depois de fechar o programa

  O exercício 10 (agenda com menu) é interativo e fica no final.
"""

import csv
import json
from datetime import datetime
from pathlib import Path

PASTA_SCRIPT = Path(__file__).resolve().parent
PASTA_SAIDA = PASTA_SCRIPT / "saida_10_respostas"
PASTA_SAIDA.mkdir(exist_ok=True)


def imprimir_cabecalho(titulo: str) -> None:
    """Função auxiliar só para separar as respostas na saída."""
    print()
    print("=" * 60)
    print(titulo)
    print("=" * 60)


# =====================================================================
# EXERCÍCIO 1
# Escreva "diario.txt" com 3 linhas sobre o seu dia. Depois leia e
# imprima cada linha numerada.
# =====================================================================
imprimir_cabecalho("EXERCÍCIO 1 — diario.txt")

caminho_diario = PASTA_SAIDA / "diario.txt"

with open(caminho_diario, "w", encoding="utf-8") as arquivo:
    arquivo.write("Acordei cedo e tomei café.\n")
    arquivo.write("Estudei arquivos em Python.\n")
    arquivo.write("Fiz os exercícios e conferi as respostas.\n")

with open(caminho_diario, encoding="utf-8") as arquivo:
    for numero, linha in enumerate(arquivo, start=1):
        print(f"{numero}. {linha.strip()}")


# =====================================================================
# EXERCÍCIO 2
# contar_linhas_palavras(caminho) -> (quantidade_de_linhas,
# quantidade_de_palavras)
# =====================================================================
def contar_linhas_palavras(caminho: Path) -> tuple[int, int]:
    total_linhas = 0
    total_palavras = 0
    with open(caminho, encoding="utf-8") as arquivo:
        for linha in arquivo:                  # linha a linha: serve até
            total_linhas += 1                  # para arquivos gigantes
            total_palavras += len(linha.split())
    return total_linhas, total_palavras


imprimir_cabecalho("EXERCÍCIO 2 — contar_linhas_palavras")
linhas, palavras = contar_linhas_palavras(caminho_diario)
print(f"diario.txt: {linhas} linhas, {palavras} palavras")

linhas, palavras = contar_linhas_palavras(Path(__file__))
print(f"este script: {linhas} linhas, {palavras} palavras")


# =====================================================================
# EXERCÍCIO 3
# registrar_log(mensagem) ACRESCENTA em "app.log" no formato
# "[2026-10-02 14:30:00] mensagem".
# =====================================================================
CAMINHO_LOG = PASTA_SAIDA / "app.log"


def registrar_log(mensagem: str) -> None:
    momento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # strftime = "string format time": transforma data em texto.
    #   %Y ano | %m mês | %d dia | %H hora | %M minuto | %S segundo
    with open(CAMINHO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"[{momento}] {mensagem}\n")


imprimir_cabecalho("EXERCÍCIO 3 — registrar_log")
registrar_log("respostas de arquivos executadas")
registrar_log("exercício 3 testado")

conteudo_log = CAMINHO_LOG.read_text(encoding="utf-8").splitlines()
print(f"app.log tem {len(conteudo_log)} linhas. Últimas 2:")
for linha in conteudo_log[-2:]:            # [-2:] = os 2 últimos itens
    print(" ", linha)
print("(rode o script de novo e veja o log crescer)")


# =====================================================================
# EXERCÍCIO 4
# copiar_arquivo(origem, destino). Se a origem não existir, mostre uma
# mensagem amigável.
# =====================================================================
def copiar_arquivo(origem: Path, destino: Path) -> bool:
    try:
        with open(origem, encoding="utf-8") as arquivo_origem:
            conteudo = arquivo_origem.read()
    except FileNotFoundError:
        print(f"  Não encontrei o arquivo '{origem.name}' para copiar.")
        return False

    with open(destino, "w", encoding="utf-8") as arquivo_destino:
        arquivo_destino.write(conteudo)
    return True


imprimir_cabecalho("EXERCÍCIO 4 — copiar_arquivo")
copia = PASTA_SAIDA / "diario_copia.txt"
print("copiou diario?", copiar_arquivo(caminho_diario, copia))
print("cópia idêntica?", copia.read_text(encoding="utf-8") == caminho_diario.read_text(encoding="utf-8"))
print("copiou fantasma?", copiar_arquivo(PASTA_SAIDA / "fantasma.txt", PASTA_SAIDA / "x.txt"))

# Na vida real, para copiar arquivos (inclusive imagens/PDF), use:
#   import shutil
#   shutil.copy(origem, destino)
# Este exercício só serve para treinar leitura + escrita.


# =====================================================================
# EXERCÍCIO 5
# "numeros.txt" com um número por linha (com linhas inválidas e vazias):
# soma e média apenas dos números válidos.
# =====================================================================
def somar_e_media_do_arquivo(caminho: Path) -> tuple[float, float | None]:
    validos = []
    with open(caminho, encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            texto = linha.strip()
            if not texto:                      # linha vazia: só pula
                continue
            try:
                validos.append(float(texto))
            except ValueError:
                print(f"  linha {numero_linha} ignorada: {texto!r}")

    if not validos:
        return 0, None                         # evita divisão por zero
    return sum(validos), sum(validos) / len(validos)


imprimir_cabecalho("EXERCÍCIO 5 — soma e média de numeros.txt")
caminho_numeros = PASTA_SAIDA / "numeros.txt"
caminho_numeros.write_text("10\n20\nabc\n\n30.5\n  \n-5\n1,5\n", encoding="utf-8")

soma, media = somar_e_media_do_arquivo(caminho_numeros)
print(f"soma = {soma} | média = {media:.2f}")

# Repare no "1,5": é ignorado porque o Python usa PONTO decimal. Se
# quisesse aceitar vírgula: float(texto.replace(",", "."))


# =====================================================================
# EXERCÍCIO 6
# "produtos.csv" com nome, categoria e preço de 5 produtos (DictWriter).
# Depois leia com DictReader e mostre o produto mais caro.
# =====================================================================
imprimir_cabecalho("EXERCÍCIO 6 — produtos.csv")

CAMINHO_PRODUTOS = PASTA_SAIDA / "produtos.csv"
CAMPOS_PRODUTO = ["nome", "categoria", "preco"]

produtos = [
    {"nome": "Teclado", "categoria": "Periféricos", "preco": 150.00},
    {"nome": "Mouse", "categoria": "Periféricos", "preco": 80.00},
    {"nome": "Monitor", "categoria": "Telas", "preco": 1200.00},
    {"nome": "Notebook", "categoria": "Computadores", "preco": 4500.00},
    {"nome": "Webcam", "categoria": "Periféricos", "preco": 250.00},
]

with open(CAMINHO_PRODUTOS, "w", encoding="utf-8", newline="") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_PRODUTO)
    escritor.writeheader()
    escritor.writerows(produtos)

with open(CAMINHO_PRODUTOS, encoding="utf-8", newline="") as arquivo:
    produtos_lidos = list(csv.DictReader(arquivo))

# O preço vem como TEXTO. Comparar textos daria resultado errado:
# "80.0" > "1200.0" é True, porque compara letra por letra ("8" > "1")!
mais_caro = max(produtos_lidos, key=lambda produto: float(produto["preco"]))
print(f"Mais caro: {mais_caro['nome']} (R$ {float(mais_caro['preco']):.2f})")
print("Comparando como texto, '80.0' > '1200.0' ->", "80.0" > "1200.0", "(errado!)")


# =====================================================================
# EXERCÍCIO 7
# Leia "produtos.csv" e gere "resumo_categorias.csv" com categoria,
# quantidade de produtos e preço médio.
# =====================================================================
def gerar_resumo_categorias(origem: Path, destino: Path) -> list[dict]:
    precos_por_categoria = {}               # {categoria: [preços]}
    with open(origem, encoding="utf-8", newline="") as arquivo:
        for produto in csv.DictReader(arquivo):
            precos_por_categoria.setdefault(produto["categoria"], []).append(
                float(produto["preco"])
            )

    resumo = []
    for categoria, precos in precos_por_categoria.items():
        resumo.append({
            "categoria": categoria,
            "quantidade": len(precos),
            "preco_medio": round(sum(precos) / len(precos), 2),
        })

    with open(destino, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["categoria", "quantidade", "preco_medio"])
        escritor.writeheader()
        escritor.writerows(resumo)

    return resumo


imprimir_cabecalho("EXERCÍCIO 7 — resumo_categorias.csv")
caminho_resumo = PASTA_SAIDA / "resumo_categorias.csv"
gerar_resumo_categorias(CAMINHO_PRODUTOS, caminho_resumo)
print(caminho_resumo.read_text(encoding="utf-8"), end="")


# =====================================================================
# EXERCÍCIO 8
# salvar_contatos(contatos) e carregar_contatos() em "contatos.json".
# carregar_contatos() retorna {} se o arquivo não existir.
# =====================================================================
CAMINHO_CONTATOS = PASTA_SAIDA / "contatos.json"


def salvar_contatos(contatos: dict[str, str]) -> None:
    with open(CAMINHO_CONTATOS, "w", encoding="utf-8") as arquivo:
        json.dump(contatos, arquivo, indent=2, ensure_ascii=False)


def carregar_contatos() -> dict[str, str]:
    try:
        with open(CAMINHO_CONTATOS, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("  Aviso: contatos.json corrompido, começando vazio.")
        return {}


imprimir_cabecalho("EXERCÍCIO 8 — contatos.json")
contatos = carregar_contatos()
print("ao carregar:", contatos if contatos else "(vazio ou inexistente)")

# setdefault: só adiciona se ainda não existir (não estraga o que você
# salvou pela agenda do exercício 10)
contatos.setdefault("Ana", "11 91111-1111")
contatos.setdefault("Bruno", "21 92222-2222")
salvar_contatos(contatos)
print("depois de salvar e carregar de novo:", carregar_contatos())


# =====================================================================
# EXERCÍCIO 9
# listar_arquivos(pasta, extensao) retorna os nomes dos arquivos com
# aquela extensão na pasta, ordenados.
# =====================================================================
def listar_arquivos(pasta: Path, extensao: str) -> list[str]:
    return sorted(
        item.name
        for item in pasta.iterdir()
        if item.is_file() and item.suffix == extensao
    )


# Alternativa com glob (mais curta):
def listar_arquivos_glob(pasta: Path, extensao: str) -> list[str]:
    return sorted(item.name for item in pasta.glob(f"*{extensao}"))


imprimir_cabecalho("EXERCÍCIO 9 — listar_arquivos")
for nome in listar_arquivos(PASTA_SCRIPT, ".py"):
    print(" ", nome)
print("glob dá o mesmo resultado?", listar_arquivos(PASTA_SCRIPT, ".py") == listar_arquivos_glob(PASTA_SCRIPT, ".py"))
print(".csv em saida_10_respostas:", listar_arquivos(PASTA_SAIDA, ".csv"))


# =====================================================================
# EXERCÍCIO 11 (Desafio)  [o 10 é interativo e fica no final]
# substituir_no_arquivo(caminho, antigo, novo) troca todas as
# ocorrências e retorna quantas substituições foram feitas.
# =====================================================================
def substituir_no_arquivo(caminho: Path, antigo: str, novo: str) -> int:
    conteudo = caminho.read_text(encoding="utf-8")
    quantidade = conteudo.count(antigo)     # conta ANTES de substituir
    if quantidade > 0:                      # só reescreve se precisar
        caminho.write_text(conteudo.replace(antigo, novo), encoding="utf-8")
    return quantidade


imprimir_cabecalho("EXERCÍCIO 11 — substituir_no_arquivo")
caminho_texto = PASTA_SAIDA / "texto_substituicao.txt"
caminho_texto.write_text("Java é legal. Eu gosto de Java.\nJava!\n", encoding="utf-8")

print("antes: ", caminho_texto.read_text(encoding="utf-8").splitlines())
trocas = substituir_no_arquivo(caminho_texto, "Java", "Python")
print("depois:", caminho_texto.read_text(encoding="utf-8").splitlines())
print("substituições:", trocas)
print("de novo (já não tem 'Java'):", substituir_no_arquivo(caminho_texto, "Java", "Python"))


# =====================================================================
# EXERCÍCIO 10 (Desafio) — interativo
# Agenda persistente com menu: listar, adicionar, buscar e remover
# contatos, salvando em JSON a cada alteração.
# =====================================================================
# Reaproveita salvar_contatos() e carregar_contatos() do exercício 8.

def listar(contatos: dict[str, str]) -> None:
    if not contatos:
        print("  Agenda vazia.")
        return
    for nome, telefone in sorted(contatos.items()):
        print(f"  {nome:<15} {telefone}")


def adicionar(contatos: dict[str, str]) -> None:
    nome = input("  Nome: ").strip()
    if not nome:
        print("  Nome não pode ser vazio.")
        return
    if nome in contatos:
        print(f"  '{nome}' já existe (telefone: {contatos[nome]}).")
        return
    contatos[nome] = input("  Telefone: ").strip()
    salvar_contatos(contatos)               # salva a CADA alteração
    print(f"  '{nome}' adicionado e salvo.")


def buscar(contatos: dict[str, str]) -> None:
    termo = input("  Buscar por: ").strip().lower()
    encontrados = {nome: tel for nome, tel in contatos.items() if termo in nome.lower()}
    if encontrados:
        listar(encontrados)
    else:
        print("  Nenhum contato encontrado.")


def remover(contatos: dict[str, str]) -> None:
    nome = input("  Nome a remover: ").strip()
    if contatos.pop(nome, None) is None:
        print(f"  '{nome}' não está na agenda.")
        return
    salvar_contatos(contatos)
    print(f"  '{nome}' removido.")


OPCOES_AGENDA = {
    "1": ("Listar", listar),
    "2": ("Adicionar", adicionar),
    "3": ("Buscar", buscar),
    "4": ("Remover", remover),
}


def agenda() -> None:
    contatos = carregar_contatos()          # carrega UMA vez ao abrir
    print(f"Agenda carregada com {len(contatos)} contato(s) de '{CAMINHO_CONTATOS.name}'.")
    while True:
        print()
        for chave, (descricao, _) in OPCOES_AGENDA.items():
            print(f"  {chave}. {descricao}")
        print("  0. Sair")
        escolha = input("Opção: ").strip()

        if escolha == "0":
            print("Até mais! (seus contatos estão salvos)")
            break
        if escolha in OPCOES_AGENDA:
            _, funcao = OPCOES_AGENDA[escolha]
            funcao(contatos)
        else:
            print("  Opção inválida.")


imprimir_cabecalho("EXERCÍCIO 10 — agenda persistente (interativo)")
if input("Abrir a agenda? (s/N): ").strip().lower() == "s":
    agenda()
else:
    print("Ok! Rode de novo e digite 's' quando quiser testar.")

print()
print("=" * 60)
print(f"FIM DAS RESPOSTAS! Veja os arquivos em '{PASTA_SAIDA.name}'.")
print("=" * 60)
