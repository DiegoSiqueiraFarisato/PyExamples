"""
=====================================================================
  RESPOSTAS DOS EXERCÍCIOS — 13_classes.py
=====================================================================

COMO USAR ESTE ARQUIVO:
  Tente resolver SOZINHO antes de olhar! Depois compare com a resposta.
  Existem várias formas certas de resolver cada exercício; a sua pode
  ser diferente e estar correta.

  Rode:   python 14_respostas_classes.py
"""

import json
import math
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path


def imprimir_cabecalho(titulo: str) -> None:
    """Função auxiliar só para separar as respostas na saída."""
    print()
    print("=" * 60)
    print(titulo)
    print("=" * 60)


# =====================================================================
# EXERCÍCIO 1
# Pessoa com nome e idade, apresentar() e fazer_aniversario().
# =====================================================================
class Pessoa:
    def __init__(self, nome: str, idade: int):
        self.nome = nome
        self.idade = idade

    def apresentar(self) -> str:
        return f"Olá, sou {self.nome} e tenho {self.idade} anos"

    def fazer_aniversario(self) -> None:
        self.idade += 1


imprimir_cabecalho("EXERCÍCIO 1 — Pessoa")
diego = Pessoa("Diego", 31)
print(diego.apresentar())
diego.fazer_aniversario()
print(diego.apresentar())


# =====================================================================
# EXERCÍCIO 2
# Retangulo com area(), perimetro(), eh_quadrado(), __str__ e __repr__.
# =====================================================================
class Retangulo:
    def __init__(self, base: float, altura: float):
        if base <= 0 or altura <= 0:
            raise ValueError("base e altura devem ser positivas")
        self.base = base
        self.altura = altura

    def area(self) -> float:
        return self.base * self.altura

    def perimetro(self) -> float:
        return 2 * (self.base + self.altura)

    def eh_quadrado(self) -> bool:
        return self.base == self.altura

    def __str__(self) -> str:
        forma = "Quadrado" if self.eh_quadrado() else "Retângulo"
        return f"{forma} {self.base} x {self.altura}"

    def __repr__(self) -> str:
        return f"Retangulo(base={self.base!r}, altura={self.altura!r})"


imprimir_cabecalho("EXERCÍCIO 2 — Retangulo")
for retangulo in [Retangulo(4, 3), Retangulo(5, 5)]:
    print(f"{retangulo} -> área {retangulo.area()}, perímetro {retangulo.perimetro()}")
print("repr numa lista:", [Retangulo(2, 1)])


# =====================================================================
# EXERCÍCIO 3
# Contador com incrementar(), decrementar() (sem passar de zero) e
# zerar(). Atributo de classe para contar quantos foram criados.
# =====================================================================
class Contador:
    total_criados = 0                    # atributo de CLASSE

    def __init__(self, valor_inicial: int = 0):
        self.valor = max(valor_inicial, 0)
        Contador.total_criados += 1
        # Atenção: "self.total_criados += 1" estaria ERRADO. Isso criaria
        # um atributo NOVO no objeto, em vez de alterar o da classe.

    def incrementar(self, passo: int = 1) -> None:
        self.valor += passo

    def decrementar(self, passo: int = 1) -> None:
        self.valor = max(self.valor - passo, 0)   # nunca abaixo de zero

    def zerar(self) -> None:
        self.valor = 0


imprimir_cabecalho("EXERCÍCIO 3 — Contador")
visitas = Contador()
cliques = Contador(10)
visitas.incrementar()
visitas.incrementar(5)
cliques.decrementar(50)
print("visitas:", visitas.valor, "| cliques (não passou de 0):", cliques.valor)
visitas.zerar()
print("visitas após zerar:", visitas.valor)
print("contadores criados:", Contador.total_criados)


# =====================================================================
# EXERCÍCIOS 4 e 5
# Temperatura com @property celsius (setter valida), fahrenheit e kelvin
# somente leitura e @classmethod de_fahrenheit(valor).
# =====================================================================
class Temperatura:
    ZERO_ABSOLUTO = -273.15

    def __init__(self, celsius: float):
        self.celsius = celsius            # passa pelo setter (validação!)

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, valor: float) -> None:
        if valor < self.ZERO_ABSOLUTO:
            raise ValueError(f"{valor} °C está abaixo do zero absoluto")
        self._celsius = valor

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    @property
    def kelvin(self) -> float:
        return self._celsius - self.ZERO_ABSOLUTO

    @classmethod
    def de_fahrenheit(cls, fahrenheit: float) -> "Temperatura":
        return cls((fahrenheit - 32) * 5 / 9)

    def __repr__(self) -> str:
        return f"Temperatura({self._celsius:.2f} °C)"


imprimir_cabecalho("EXERCÍCIOS 4 e 5 — Temperatura")
agua = Temperatura(100)
print(f"{agua.celsius} °C = {agua.fahrenheit} °F = {agua.kelvin} K")

corpo = Temperatura.de_fahrenheit(98.6)
print("de_fahrenheit(98.6):", corpo)

try:
    agua.celsius = -300               # o setter recusa
except ValueError as e:
    print("agua.celsius = -300 ->", e)

try:
    agua.kelvin = 0                   # kelvin não tem setter
except AttributeError as e:
    print("agua.kelvin = 0 ->", e)


# =====================================================================
# EXERCÍCIO 6
# Livro (titulo, autor, paginas) e Biblioteca, que TEM uma lista de
# livros, com adicionar, buscar_por_autor, total_paginas e __len__.
# =====================================================================
class Livro:
    def __init__(self, titulo: str, autor: str, paginas: int):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas

    def __repr__(self) -> str:
        return f"Livro({self.titulo!r}, {self.autor!r}, {self.paginas})"


class Biblioteca:
    def __init__(self, nome: str):
        self.nome = nome
        self._livros: list[Livro] = []    # composição: Biblioteca TEM livros

    def adicionar(self, livro: Livro) -> None:
        self._livros.append(livro)

    def buscar_por_autor(self, autor: str) -> list[Livro]:
        # busca sem diferenciar maiúsculas e aceitando parte do nome
        termo = autor.lower()
        return [livro for livro in self._livros if termo in livro.autor.lower()]

    def total_paginas(self) -> int:
        return sum(livro.paginas for livro in self._livros)

    def __len__(self) -> int:
        return len(self._livros)


imprimir_cabecalho("EXERCÍCIO 6 — Livro e Biblioteca (composição)")
biblioteca = Biblioteca("Minha estante")
biblioteca.adicionar(Livro("Dom Casmurro", "Machado de Assis", 256))
biblioteca.adicionar(Livro("Memórias Póstumas de Brás Cubas", "Machado de Assis", 368))
biblioteca.adicionar(Livro("Grande Sertão: Veredas", "Guimarães Rosa", 624))

print("livros na biblioteca:", len(biblioteca))        # __len__
print("de 'machado':", biblioteca.buscar_por_autor("machado"))
print("total de páginas:", biblioteca.total_paginas())


# =====================================================================
# EXERCÍCIO 7
# Herança: Veiculo (marca, modelo, ano) com descrever(); Carro (portas)
# e Moto (cilindradas) usam super().__init__ e sobrescrevem descrever().
# =====================================================================
class Veiculo:
    def __init__(self, marca: str, modelo: str, ano: int):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano

    def descrever(self) -> str:
        return f"{self.marca} {self.modelo} ({self.ano})"


class Carro(Veiculo):
    def __init__(self, marca: str, modelo: str, ano: int, portas: int = 4):
        super().__init__(marca, modelo, ano)
        self.portas = portas

    def descrever(self) -> str:
        # Reaproveita a descrição da mãe e só ACRESCENTA a parte nova
        return f"Carro: {super().descrever()}, {self.portas} portas"


class Moto(Veiculo):
    def __init__(self, marca: str, modelo: str, ano: int, cilindradas: int):
        super().__init__(marca, modelo, ano)
        self.cilindradas = cilindradas

    def descrever(self) -> str:
        return f"Moto: {super().descrever()}, {self.cilindradas} cc"


imprimir_cabecalho("EXERCÍCIO 7 — Veiculo, Carro e Moto (herança)")
garagem = [
    Carro("Fiat", "Pulse", 2024),
    Carro("VW", "Up", 2019, portas=2),
    Moto("Honda", "CB 500", 2023, cilindradas=500),
]
for veiculo in garagem:
    print(" ", veiculo.descrever())


# =====================================================================
# EXERCÍCIO 8
# Polimorfismo: Funcionario.calcular_salario() e as filhas Clt,
# Freelancer e Vendedor. Folha de pagamento total.
# =====================================================================
class Funcionario:
    def __init__(self, nome: str):
        self.nome = nome

    def calcular_salario(self) -> float:
        raise NotImplementedError("cada tipo de funcionário calcula o seu")


class Clt(Funcionario):
    def __init__(self, nome: str, salario_fixo: float):
        super().__init__(nome)
        self.salario_fixo = salario_fixo

    def calcular_salario(self) -> float:
        return self.salario_fixo


class Freelancer(Funcionario):
    def __init__(self, nome: str, horas: float, valor_hora: float):
        super().__init__(nome)
        self.horas = horas
        self.valor_hora = valor_hora

    def calcular_salario(self) -> float:
        return self.horas * self.valor_hora


class Vendedor(Clt):
    # Vendedor É UM Clt (tem salário fixo) + comissão. Herdar de Clt
    # reaproveita o fixo, e o super() soma a comissão por cima.
    def __init__(self, nome: str, salario_fixo: float, vendas: float, comissao: float = 0.05):
        super().__init__(nome, salario_fixo)
        self.vendas = vendas
        self.comissao = comissao

    def calcular_salario(self) -> float:
        return super().calcular_salario() + self.vendas * self.comissao


imprimir_cabecalho("EXERCÍCIO 8 — folha de pagamento (polimorfismo)")
equipe = [
    Clt("Ana", 6000),
    Freelancer("Bruno", horas=80, valor_hora=75),
    Vendedor("Carla", 2500, vendas=90000),
]
for funcionario in equipe:
    # Mesma chamada para todos. Nenhum if para saber o tipo!
    print(f"  {funcionario.nome:<6} ({type(funcionario).__name__:<10}) R$ {funcionario.calcular_salario():>8.2f}")
folha = sum(funcionario.calcular_salario() for funcionario in equipe)
print(f"  {'TOTAL':<19} R$ {folha:>8.2f}")


# =====================================================================
# EXERCÍCIO 9
# Livro com @dataclass. Compare o tamanho do código.
# =====================================================================
@dataclass
class LivroDC:
    titulo: str
    autor: str
    paginas: int


imprimir_cabecalho("EXERCÍCIO 9 — Livro com @dataclass")
livro_a = LivroDC("Dom Casmurro", "Machado de Assis", 256)
print(livro_a)                                            # __repr__ grátis
print("== grátis:", livro_a == LivroDC("Dom Casmurro", "Machado de Assis", 256))
print("o Livro normal NÃO tem __eq__:",
      Livro("X", "Y", 1) == Livro("X", "Y", 1))

# COMPARAÇÃO:
#   Livro (classe normal): 8 linhas (__init__ + __repr__) e sem __eq__
#   LivroDC (dataclass):   4 linhas, com __init__, __repr__ e __eq__
# Quanto mais campos, maior a economia.


# =====================================================================
# EXERCÍCIO 10
# Vetor2D com __add__, __sub__, __eq__, __repr__ e tamanho().
# =====================================================================
class Vetor2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, outro: "Vetor2D") -> "Vetor2D":
        return Vetor2D(self.x + outro.x, self.y + outro.y)

    def __sub__(self, outro: "Vetor2D") -> "Vetor2D":
        return Vetor2D(self.x - outro.x, self.y - outro.y)

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Vetor2D):
            return NotImplemented     # "não sei comparar com isso"
        return self.x == outro.x and self.y == outro.y

    def __repr__(self) -> str:
        return f"Vetor2D({self.x}, {self.y})"

    def tamanho(self) -> float:
        return math.hypot(self.x, self.y)


imprimir_cabecalho("EXERCÍCIO 10 — Vetor2D")
v1 = Vetor2D(1, 2)
v2 = Vetor2D(3, 4)
print(f"{v1} + {v2} = {v1 + v2}")
print(f"{v2} - {v1} = {v2 - v1}")
print("Vetor2D(1, 2) + Vetor2D(3, 4) == Vetor2D(4, 6)?", v1 + v2 == Vetor2D(4, 6))
print("tamanho de", v2, "=", v2.tamanho())
print("comparar com texto:", v1 == "abc")    # False, sem erro (NotImplemented)


# =====================================================================
# EXERCÍCIO 11 (Desafio)
# ContaBancaria com _saldo + @property, extrato com data/hora,
# SaldoInsuficienteError e ContaEspecial com limite.
# =====================================================================
class SaldoInsuficienteError(Exception):
    pass


class ContaBancaria:
    def __init__(self, titular: str):
        self.titular = titular
        self._saldo = 0.0
        self._extrato: list[str] = []

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def extrato(self) -> list[str]:
        return list(self._extrato)   # devolve uma CÓPIA: quem recebe não
                                     # consegue alterar o extrato real

    def _registrar(self, descricao: str, valor: float) -> None:
        momento = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self._extrato.append(f"[{momento}] {descricao:<9} {valor:>9.2f} | saldo {self._saldo:>9.2f}")

    def _disponivel_para_saque(self) -> float:
        # Método "gancho": a filha ContaEspecial muda SÓ isto
        return self._saldo

    def depositar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("o depósito deve ser positivo")
        self._saldo += valor
        self._registrar("depósito", valor)

    def sacar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("o saque deve ser positivo")
        if valor > self._disponivel_para_saque():
            raise SaldoInsuficienteError(
                f"saque de {valor:.2f}, disponível {self._disponivel_para_saque():.2f}"
            )
        self._saldo -= valor
        self._registrar("saque", -valor)


class ContaEspecial(ContaBancaria):
    def __init__(self, titular: str, limite: float):
        super().__init__(titular)
        self.limite = limite

    def _disponivel_para_saque(self) -> float:
        return self._saldo + self.limite     # pode ficar negativo até o limite


imprimir_cabecalho("EXERCÍCIO 11 — ContaBancaria e ContaEspecial")
for conta in [ContaBancaria("Ana"), ContaEspecial("Bruno", limite=500)]:
    print(f"--- {type(conta).__name__} de {conta.titular} ---")
    conta.depositar(300)
    try:
        conta.sacar(600)
        print("  saque de 600 aprovado")
    except SaldoInsuficienteError as e:
        print("  saque negado:", e)
    print(f"  saldo final: {conta.saldo:.2f}")
    for linha in conta.extrato:
        print("  ", linha)

# Repare: a ContaEspecial NÃO reescreveu o sacar(). Ela mudou só o
# método _disponivel_para_saque(), e toda a validação do sacar() da mãe
# passou a usar o limite automaticamente.


# =====================================================================
# EXERCÍCIO 12 (Desafio)
# Mini projeto de tarefas em classes: @dataclass Tarefa e classe
# ListaDeTarefas com adicionar, concluir, remover, listar, salvar e
# carregar (JSON).
# =====================================================================
@dataclass
class Tarefa:
    titulo: str
    feita: bool = False
    criada_em: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    # default_factory com lambda: a data é gerada na hora em que CADA
    # tarefa é criada (e não uma vez só, quando a classe foi definida)

    def __str__(self) -> str:
        return f"[{'x' if self.feita else ' '}] {self.titulo}"


class ListaDeTarefas:
    def __init__(self, caminho: Path):
        self.caminho = caminho
        self.tarefas: list[Tarefa] = []

    def adicionar(self, titulo: str) -> Tarefa:
        titulo = titulo.strip()
        if not titulo:
            raise ValueError("o título não pode ser vazio")
        tarefa = Tarefa(titulo)
        self.tarefas.append(tarefa)
        return tarefa

    def _buscar(self, numero: int) -> Tarefa:
        if not 1 <= numero <= len(self.tarefas):
            raise IndexError(f"não existe tarefa nº {numero}")
        return self.tarefas[numero - 1]

    def concluir(self, numero: int) -> None:
        self._buscar(numero).feita = True

    def remover(self, numero: int) -> Tarefa:
        self._buscar(numero)                  # valida o número
        return self.tarefas.pop(numero - 1)

    def listar(self) -> list[str]:
        return [f"{numero}. {tarefa}" for numero, tarefa in enumerate(self.tarefas, start=1)]

    def salvar(self) -> None:
        # asdict() transforma o dataclass em dict, pronto para o JSON
        dados = [asdict(tarefa) for tarefa in self.tarefas]
        self.caminho.write_text(json.dumps(dados, indent=2, ensure_ascii=False), encoding="utf-8")

    def carregar(self) -> None:
        try:
            dados = json.loads(self.caminho.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            dados = []
        # Tarefa(**dict) desempacota o dict nos parâmetros do __init__
        self.tarefas = [Tarefa(**item) for item in dados]

    def __len__(self) -> int:
        return len(self.tarefas)


imprimir_cabecalho("EXERCÍCIO 12 — tarefas com classes")
with tempfile.TemporaryDirectory() as pasta:
    caminho = Path(pasta) / "tarefas.json"

    lista = ListaDeTarefas(caminho)
    lista.adicionar("Estudar classes")
    lista.adicionar("Fazer os exercícios")
    lista.adicionar("Tarefa que vou apagar")
    lista.concluir(1)
    print("removida:", lista.remover(3).titulo)
    lista.salvar()

    # Um objeto NOVO, lendo do arquivo: prova que salvou e carregou
    outra_lista = ListaDeTarefas(caminho)
    outra_lista.carregar()
    print(f"carregadas {len(outra_lista)} tarefas do JSON:")
    for linha in outra_lista.listar():
        print(" ", linha)

    try:
        outra_lista.concluir(99)
    except IndexError as e:
        print("concluir(99) ->", e)

# Compare com o pacote tarefas/ (exercício 11 de módulos): lá, cada
# operação abria e salvava o arquivo. Aqui, o objeto guarda as tarefas
# na memória e você decide QUANDO salvar. É o estado + comportamento
# juntos, que é justamente a ideia das classes.

print()
print("=" * 60)
print("FIM DAS RESPOSTAS!")
print("=" * 60)
