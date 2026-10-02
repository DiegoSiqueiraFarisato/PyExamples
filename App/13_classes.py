"""
=====================================================================
  MATERIAL DE ESTUDO PYTHON — CLASSES E ORIENTAÇÃO A OBJETOS (POO)
  Por que classes -> class e objetos -> __init__ e self -> Atributos ->
  Métodos -> __str__/__repr__ -> Atributos de classe -> Encapsulamento
  e @property -> @classmethod/@staticmethod -> Herança e super() ->
  Polimorfismo -> Composição -> Métodos especiais -> dataclass ->
  Erros comuns -> Boas práticas
=====================================================================

PRÉ-REQUISITOS: 01 a 11 (principalmente funções, dicionários e erros).

COMO USAR ESTE ARQUIVO:
  1. Leia os comentários de cima para baixo.
  2. Rode no terminal:   python 13_classes.py
  3. Este é o assunto mais "conceitual" até agora. Não se preocupe se
     não entender tudo de primeira. Releia, rode, mude os exemplos.
"""

from dataclasses import dataclass, field


# =====================================================================
# 1. POR QUE CLASSES?
# =====================================================================
# Até agora, representamos "coisas" com dicionários e funções soltas:
#
#   conta = {"titular": "Ana", "saldo": 100}
#   def depositar(conta, valor): conta["saldo"] += valor
#
# Funciona, mas:
#   - Nada impede alguém de fazer conta["saldo"] = -999999
#   - Nada garante que todo dict de conta tenha "titular" e "saldo"
#     (e se alguém escrever "Saldo" ou "saldos"?)
#   - Os DADOS (o dict) e os COMPORTAMENTOS (as funções) ficam separados
#
# Uma CLASSE junta DADOS + COMPORTAMENTOS num único lugar.
#
# ANALOGIA:
#   CLASSE = a PLANTA de uma casa (o projeto, o molde)
#   OBJETO = cada CASA construída a partir da planta
#   Uma planta, várias casas. Cada casa tem a mesma estrutura, mas cor,
#   dono e endereço próprios.
#
# Você já usa objetos desde o primeiro material! Em Python, TUDO é
# objeto: "texto".upper() chama o método upper de um objeto da classe
# str. lista.append(x) chama o método append de um objeto da classe list.

print("=" * 60)
print("1. VOCÊ JÁ USA OBJETOS")
print("=" * 60)

print(type("olá"), type([1, 2]), type({}), type(42))
print('"olá".upper() ->', "olá".upper(), "  (método da classe str)")
print()


# =====================================================================
# 2. CRIANDO UMA CLASSE E OBJETOS
# =====================================================================
# Sintaxe:
#   class NomeDaClasse:      <- nome em PascalCase (CadaPalavraMaiúscula)
#       ...
#
# Criar um objeto (também chamado de INSTÂNCIA) = "chamar" a classe:
#   objeto = NomeDaClasse()

print("=" * 60)
print("2. CLASSE E OBJETOS")
print("=" * 60)


class Cachorro:
    pass                     # classe vazia, só para começar


rex = Cachorro()             # um objeto
bidu = Cachorro()            # outro objeto, independente

print("rex é:", rex)                     # <__main__.Cachorro object at 0x...>
print("tipo:", type(rex).__name__)
print("rex e bidu são o mesmo objeto?", rex is bidu)
print("rex é um Cachorro?", isinstance(rex, Cachorro))
print()


# =====================================================================
# 3. __init__ E self: DANDO DADOS AO OBJETO
# =====================================================================
# __init__ é o "construtor" (na verdade, o INICIALIZADOR): um método
# especial que roda AUTOMATICAMENTE quando você cria o objeto. É onde
# você define os dados (ATRIBUTOS) que todo objeto da classe terá.
#
# self = "o próprio objeto". É sempre o PRIMEIRO parâmetro de todo
# método. Você NÃO passa o self na chamada: o Python passa sozinho.
#
#   rex = Cachorro("Rex", 3)
#   é como se o Python fizesse:  Cachorro.__init__(rex, "Rex", 3)
#
# self.nome = nome
#   self.nome -> atributo do objeto (fica guardado nele)
#   nome      -> o parâmetro recebido (some quando o __init__ termina)

print("=" * 60)
print("3. __init__ E self")
print("=" * 60)


class Cachorro:
    def __init__(self, nome: str, idade: int):
        print(f"  (criando o cachorro {nome}...)")
        self.nome = nome
        self.idade = idade


rex = Cachorro("Rex", 3)
bidu = Cachorro("Bidu", 7)

# Acessando atributos com objeto.atributo
print(f"{rex.nome} tem {rex.idade} anos")
print(f"{bidu.nome} tem {bidu.idade} anos")

# Atributos podem ser alterados (cada objeto tem os SEUS)
rex.idade = 4
print(f"Rex fez aniversário: {rex.idade} | Bidu continua: {bidu.idade}")

# vars() mostra os atributos do objeto como um dict
print("vars(rex):", vars(rex))
print()


# =====================================================================
# 4. MÉTODOS: O COMPORTAMENTO DO OBJETO
# =====================================================================
# Método = função DEFINIDA DENTRO da classe. Ele recebe self, então
# pode ler e alterar os atributos do próprio objeto.
#
# Atributos -> o que o objeto TEM (substantivos: nome, saldo, idade)
# Métodos   -> o que o objeto FAZ (verbos: depositar, latir, calcular)

print("=" * 60)
print("4. MÉTODOS")
print("=" * 60)


class ContaBancaria:
    def __init__(self, titular: str, saldo_inicial: float = 0):
        self.titular = titular
        self.saldo = saldo_inicial
        self.extrato = []                 # cada conta tem a SUA lista

    def depositar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("o depósito deve ser positivo")
        self.saldo += valor
        self.extrato.append(f"+ {valor:.2f}")

    def sacar(self, valor: float) -> None:
        if valor > self.saldo:
            raise ValueError(f"saldo insuficiente (saldo: {self.saldo:.2f})")
        self.saldo -= valor
        self.extrato.append(f"- {valor:.2f}")

    def transferir(self, destino: "ContaBancaria", valor: float) -> None:
        self.sacar(valor)                 # um método pode chamar outro
        destino.depositar(valor)

    def resumo(self) -> str:
        return f"{self.titular}: R$ {self.saldo:.2f}"


conta_ana = ContaBancaria("Ana", 100)
conta_bruno = ContaBancaria("Bruno")

conta_ana.depositar(50)
conta_ana.transferir(conta_bruno, 30)
print(conta_ana.resumo(), "| extrato:", conta_ana.extrato)
print(conta_bruno.resumo(), "| extrato:", conta_bruno.extrato)

try:
    conta_bruno.sacar(1000)
except ValueError as e:
    print("Erro:", e)

# Compare com a versão de dict + funções da seção 1: agora as regras
# (não sacar mais do que tem, não depositar valor negativo) ficam
# DENTRO da classe e valem para TODA conta.
print()


# =====================================================================
# 5. __str__ E __repr__: COMO O OBJETO APARECE NO print
# =====================================================================
# Por padrão, print(objeto) mostra algo inútil: <__main__.X object at 0x...>
# Dois métodos especiais resolvem:
#
#   __str__  -> texto AMIGÁVEL para o usuário. Usado por print() e str()
#   __repr__ -> texto TÉCNICO para o programador (debug). Usado no
#               terminal interativo, em listas e por repr(). O ideal é
#               parecer o código que recria o objeto.
#
# Se você só implementar um, implemente o __repr__. O print usa ele
# quando não existe __str__.

print("=" * 60)
print("5. __str__ E __repr__")
print("=" * 60)


class Produto:
    def __init__(self, nome: str, preco: float):
        self.nome = nome
        self.preco = preco

    def __str__(self) -> str:
        return f"{self.nome} - R$ {self.preco:.2f}"

    def __repr__(self) -> str:
        return f"Produto(nome={self.nome!r}, preco={self.preco!r})"


cafe = Produto("Café", 17.9)
print(cafe)                    # usa __str__
print(repr(cafe))              # usa __repr__
print([cafe, Produto("Pão", 1.2)])   # listas mostram o __repr__ dos itens
print(f"f-string: {cafe} | com !r: {cafe!r}")
print()


# =====================================================================
# 6. ATRIBUTOS DE CLASSE vs ATRIBUTOS DE INSTÂNCIA
# =====================================================================
#   Atributo de INSTÂNCIA -> definido com self.x no __init__.
#                            Cada objeto tem o SEU valor.
#   Atributo de CLASSE    -> definido direto no corpo da classe.
#                            COMPARTILHADO por todos os objetos.
#
# Use atributo de classe para constantes e informações que são da
# classe toda (ex: taxa padrão, contador de objetos criados).

print("=" * 60)
print("6. ATRIBUTOS DE CLASSE")
print("=" * 60)


class Funcionario:
    empresa = "TechCorp"           # atributo de CLASSE
    total_funcionarios = 0         # atributo de CLASSE
    AUMENTO_PADRAO = 0.05          # constante da classe

    def __init__(self, nome: str, salario: float):
        self.nome = nome           # atributo de INSTÂNCIA
        self.salario = salario     # atributo de INSTÂNCIA
        Funcionario.total_funcionarios += 1   # altera o da CLASSE

    def aplicar_aumento(self) -> None:
        self.salario *= 1 + self.AUMENTO_PADRAO


ana = Funcionario("Ana", 5000)
bruno = Funcionario("Bruno", 4000)

print("empresa da Ana:", ana.empresa, "| do Bruno:", bruno.empresa)
print("total de funcionários:", Funcionario.total_funcionarios)
ana.aplicar_aumento()
print(f"salário da Ana após aumento: {ana.salario:.2f}")

Funcionario.empresa = "MegaCorp"       # muda para TODOS
print("depois de mudar na classe:", ana.empresa, bruno.empresa)
print()


# =====================================================================
# 7. ENCAPSULAMENTO E @property
# =====================================================================
# Encapsular = proteger os dados internos do objeto, para que só sejam
# alterados de formas VÁLIDAS.
#
# Python não tem "private" de verdade (como Java/C#). Usa CONVENÇÕES:
#   nome      -> público: pode usar à vontade
#   _nome     -> "protegido": uso INTERNO, por favor não mexa de fora
#   __nome    -> "privado": o Python embaralha o nome (name mangling)
#                para dificultar o acesso de fora. Pouco usado.
#
# @property: permite acessar um MÉTODO como se fosse ATRIBUTO, e
# controlar a leitura e a escrita com validação.

print("=" * 60)
print("7. ENCAPSULAMENTO E @property")
print("=" * 60)


class Termometro:
    def __init__(self, celsius: float):
        self.celsius = celsius        # já passa pelo setter abaixo!

    @property
    def celsius(self) -> float:       # GETTER: roda ao LER t.celsius
        return self._celsius

    @celsius.setter
    def celsius(self, valor: float) -> None:   # SETTER: roda ao ESCREVER
        if valor < -273.15:
            raise ValueError(f"abaixo do zero absoluto: {valor}")
        self._celsius = valor

    @property
    def fahrenheit(self) -> float:    # property SEM setter = somente leitura
        return self._celsius * 9 / 5 + 32


t = Termometro(25)
print(f"{t.celsius} °C = {t.fahrenheit} °F")   # sem parênteses!
t.celsius = 100                                # usa o setter
print(f"{t.celsius} °C = {t.fahrenheit} °F")

try:
    t.celsius = -500
except ValueError as e:
    print("Erro no setter:", e)

try:
    t.fahrenheit = 50
except AttributeError as e:
    print("fahrenheit é somente leitura:", e)

# Versão melhorada da conta: o saldo não pode ser alterado diretamente
class ContaSegura:
    def __init__(self, titular: str):
        self.titular = titular
        self._saldo = 0.0             # "_" = não mexa de fora

    @property
    def saldo(self) -> float:         # pode LER, mas não tem setter
        return self._saldo

    def depositar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("o depósito deve ser positivo")
        self._saldo += valor


conta = ContaSegura("Carla")
conta.depositar(200)
print("saldo:", conta.saldo)
try:
    conta.saldo = 1_000_000           # tentando "roubar"
except AttributeError:
    print("conta.saldo = 1_000_000 -> bloqueado! Só via depositar().")
print()


# =====================================================================
# 8. @classmethod E @staticmethod
# =====================================================================
#   método normal     -> recebe self (o OBJETO). O mais comum.
#   @classmethod      -> recebe cls (a CLASSE). Muito usado como
#                        "construtor alternativo": outra forma de criar
#                        objetos (a partir de texto, de dict...).
#   @staticmethod     -> não recebe nem self nem cls. É uma função comum
#                        que fica dentro da classe por organização.

print("=" * 60)
print("8. @classmethod E @staticmethod")
print("=" * 60)


class Data:
    def __init__(self, dia: int, mes: int, ano: int):
        if not Data.eh_data_valida(dia, mes, ano):
            raise ValueError(f"data inválida: {dia}/{mes}/{ano}")
        self.dia = dia
        self.mes = mes
        self.ano = ano

    @classmethod
    def de_texto(cls, texto: str) -> "Data":
        """Construtor alternativo: Data.de_texto("25/12/2026")."""
        dia, mes, ano = (int(parte) for parte in texto.split("/"))
        return cls(dia, mes, ano)        # cls(...) é o mesmo que Data(...)

    @staticmethod
    def eh_data_valida(dia: int, mes: int, ano: int) -> bool:
        # Simplificado: não trata ano bissexto nem meses de 30 dias
        return 1 <= dia <= 31 and 1 <= mes <= 12 and ano > 0

    def __str__(self) -> str:
        return f"{self.dia:02d}/{self.mes:02d}/{self.ano}"


natal = Data(25, 12, 2026)
ano_novo = Data.de_texto("1/1/2027")     # chamado na CLASSE, não no objeto
print("natal:", natal, "| ano novo:", ano_novo)
print("31/13/2026 é válida?", Data.eh_data_valida(31, 13, 2026))
print()


# =====================================================================
# 9. HERANÇA: REAPROVEITANDO UMA CLASSE
# =====================================================================
# Uma classe FILHA herda TUDO da classe MÃE (atributos e métodos) e
# pode:
#   - ADICIONAR coisas novas
#   - SOBRESCREVER (override) métodos para mudar o comportamento
#
#   class Filha(Mae):
#
# super() acessa a classe mãe. O uso mais comum: chamar o __init__ da
# mãe para não repetir código.
#
# Teste da herança: a frase "Filha É UM(A) Mãe" precisa fazer sentido.
#   Gerente É UM Funcionário       -> herança faz sentido
#   Carro É UM Motor               -> NÃO! (Carro TEM um motor -> seção 11)

print("=" * 60)
print("9. HERANÇA")
print("=" * 60)


class Animal:
    def __init__(self, nome: str):
        self.nome = nome

    def falar(self) -> str:
        return "..."

    def apresentar(self) -> str:
        # self.falar() chama a versão da CLASSE DO OBJETO (polimorfismo!)
        return f"Eu sou {self.nome} e faço: {self.falar()}"


class Gato(Animal):
    def falar(self) -> str:              # sobrescreve o da mãe
        return "Miau"


class Cao(Animal):
    def __init__(self, nome: str, raca: str):
        super().__init__(nome)           # reaproveita o __init__ do Animal
        self.raca = raca                 # e adiciona um atributo novo

    def falar(self) -> str:
        return "Au au"

    def buscar_bolinha(self) -> str:     # método novo, só do Cao
        return f"{self.nome} buscou a bolinha!"


class Peixe(Animal):
    pass                                 # não sobrescreve nada: usa o da mãe


mimi = Gato("Mimi")
thor = Cao("Thor", "Labrador")
nemo = Peixe("Nemo")

print(mimi.apresentar())
print(thor.apresentar(), f"(raça: {thor.raca})")
print(nemo.apresentar())
print(thor.buscar_bolinha())

print("thor é Cao?", isinstance(thor, Cao), "| é Animal?", isinstance(thor, Animal))
print("mimi é Cao?", isinstance(mimi, Cao))
print("Cao é subclasse de Animal?", issubclass(Cao, Animal))

# Lembra do material de erros? Exceções próprias usam herança:
#   class SaldoInsuficienteError(Exception): pass
# SaldoInsuficienteError É UMA Exception, por isso funciona no except.
print()


# =====================================================================
# 10. POLIMORFISMO: MESMA CHAMADA, COMPORTAMENTOS DIFERENTES
# =====================================================================
# Poli = muitas, morfo = formas. Objetos de classes diferentes respondem
# ao MESMO método, cada um do seu jeito. Quem chama não precisa saber
# qual é a classe exata: só precisa saber que o método existe.
#
# Isso elimina cadeias de if/elif do tipo:
#   if tipo == "gato": ... elif tipo == "cao": ... elif ...

print("=" * 60)
print("10. POLIMORFISMO")
print("=" * 60)


class Forma:
    def area(self) -> float:
        raise NotImplementedError("cada forma deve implementar area()")

    def descrever(self) -> str:
        return f"{type(self).__name__} com área {self.area():.2f}"


class Retangulo(Forma):
    def __init__(self, base: float, altura: float):
        self.base = base
        self.altura = altura

    def area(self) -> float:
        return self.base * self.altura


class Circulo(Forma):
    def __init__(self, raio: float):
        self.raio = raio

    def area(self) -> float:
        return 3.14159 * self.raio ** 2


class Triangulo(Forma):
    def __init__(self, base: float, altura: float):
        self.base = base
        self.altura = altura

    def area(self) -> float:
        return self.base * self.altura / 2


formas = [Retangulo(4, 5), Circulo(3), Triangulo(6, 2)]

for forma in formas:
    print(" ", forma.descrever())      # mesma chamada, resultados diferentes

print("área total:", round(sum(forma.area() for forma in formas), 2))
maior = max(formas, key=lambda forma: forma.area())
print("maior forma:", type(maior).__name__)

# "Duck typing" (tipagem pato): "se anda como pato e grasna como pato,
# é um pato". Em Python, nem precisa de herança: qualquer objeto que
# tenha o método area() funcionaria no loop acima.
print()


# =====================================================================
# 11. COMPOSIÇÃO: OBJETOS DENTRO DE OBJETOS
# =====================================================================
# Herança = relação "É UM"   (Gato é um Animal)
# Composição = relação "TEM UM" (Pedido TEM itens, Carro TEM motor)
#
# Na prática, composição é usada MUITO mais que herança. Regra famosa:
# "prefira composição a herança". Use herança só quando a relação
# "é um" for realmente verdadeira.

print("=" * 60)
print("11. COMPOSIÇÃO")
print("=" * 60)


class ItemPedido:
    def __init__(self, produto: Produto, quantidade: int):
        self.produto = produto              # ItemPedido TEM um Produto
        self.quantidade = quantidade

    def subtotal(self) -> float:
        return self.produto.preco * self.quantidade


class Pedido:
    def __init__(self, cliente: str):
        self.cliente = cliente
        self.itens: list[ItemPedido] = []   # Pedido TEM vários itens

    def adicionar(self, produto: Produto, quantidade: int = 1) -> None:
        self.itens.append(ItemPedido(produto, quantidade))

    def total(self) -> float:
        return sum(item.subtotal() for item in self.itens)

    def imprimir(self) -> None:
        print(f"  Pedido de {self.cliente}")
        for item in self.itens:
            print(f"    {item.quantidade}x {item.produto.nome:<8} R$ {item.subtotal():>6.2f}")
        print(f"    {'TOTAL':<11} R$ {self.total():>6.2f}")


pedido = Pedido("Diego")
pedido.adicionar(Produto("Café", 17.90), 2)
pedido.adicionar(Produto("Pão", 1.20), 6)
pedido.adicionar(Produto("Leite", 4.80))
pedido.imprimir()
print()


# =====================================================================
# 12. MÉTODOS ESPECIAIS (dunder methods)
# =====================================================================
# "Dunder" = Double UNDERscore: __init__, __str__, __repr__... Eles
# fazem seus objetos funcionarem com recursos NATIVOS do Python:
#
#   __eq__   -> a == b          __lt__  -> a < b  (e permite sorted())
#   __len__  -> len(a)          __add__ -> a + b
#   __contains__ -> x in a      __iter__ -> for x in a
#   __getitem__  -> a[0]        __bool__ -> if a:

print("=" * 60)
print("12. MÉTODOS ESPECIAIS")
print("=" * 60)


class Dinheiro:
    def __init__(self, valor: float):
        self.valor = round(valor, 2)

    def __add__(self, outro: "Dinheiro") -> "Dinheiro":
        return Dinheiro(self.valor + outro.valor)

    def __eq__(self, outro: object) -> bool:
        return isinstance(outro, Dinheiro) and self.valor == outro.valor

    def __lt__(self, outro: "Dinheiro") -> bool:
        return self.valor < outro.valor

    def __repr__(self) -> str:
        return f"Dinheiro({self.valor})"

    def __str__(self) -> str:
        return f"R$ {self.valor:.2f}"


a = Dinheiro(10.5)
b = Dinheiro(4.5)
print("a + b =", a + b)                            # __add__
print("a == Dinheiro(10.5)?", a == Dinheiro(10.5)) # __eq__
print("b < a?", b < a)                             # __lt__
print("ordenado:", sorted([a, b, Dinheiro(7)]))    # sorted usa __lt__

# SEM __eq__, == compara se é o MESMO objeto na memória, e não o valor:
print("sem __eq__, Produto('x', 1) == Produto('x', 1)?", Produto("x", 1) == Produto("x", 1))


class Playlist:
    def __init__(self, nome: str):
        self.nome = nome
        self._musicas: list[str] = []

    def adicionar(self, musica: str) -> None:
        self._musicas.append(musica)

    def __len__(self) -> int:
        return len(self._musicas)

    def __contains__(self, musica: str) -> bool:
        return musica in self._musicas

    def __iter__(self):
        return iter(self._musicas)

    def __getitem__(self, posicao: int) -> str:
        return self._musicas[posicao]


rock = Playlist("Rock")
for musica in ["Bohemian Rhapsody", "Stairway to Heaven", "Hotel California"]:
    rock.adicionar(musica)

print("len(rock):", len(rock))                                  # __len__
print("'Hotel California' in rock?", "Hotel California" in rock)  # __contains__
print("rock[0]:", rock[0], "| rock[-1]:", rock[-1])              # __getitem__
for numero, musica in enumerate(rock, start=1):                 # __iter__
    print(f"  {numero}. {musica}")
print()


# =====================================================================
# 13. @dataclass: CLASSES DE DADOS SEM REPETIÇÃO
# =====================================================================
# Muitas classes só guardam dados e o __init__ é só "self.x = x" para
# cada campo. O @dataclass gera AUTOMATICAMENTE o __init__, __repr__ e
# __eq__ a partir das anotações de tipo.
#
# É o substituto natural dos dicionários "com sempre os mesmos campos"
# (lembra da dica no material de dicionários?).

print("=" * 60)
print("13. @dataclass")
print("=" * 60)


@dataclass
class Aluno:
    nome: str
    turma: str
    notas: list[float] = field(default_factory=list)   # lista padrão segura
    ativo: bool = True                                  # valor padrão

    # Pode ter métodos e properties normalmente
    @property
    def media(self) -> float:
        return sum(self.notas) / len(self.notas) if self.notas else 0.0

    def esta_aprovado(self, minimo: float = 7.0) -> bool:
        return self.media >= minimo


carla = Aluno("Carla", "3A", [8, 9.5, 7])
diego = Aluno("Diego", "3B")

print(carla)                                       # __repr__ automático
print(diego)
print(f"média da Carla: {carla.media:.2f} | aprovada? {carla.esta_aprovado()}")
print("== automático:", Aluno("X", "1A") == Aluno("X", "1A"))

# field(default_factory=list): por que não "notas: list = []"?
# É a MESMA armadilha da lista como valor padrão em funções (material
# 03, erro 5): a lista seria compartilhada. O dataclass até dá erro se
# você tentar.

# frozen=True: objeto IMUTÁVEL (não deixa alterar depois de criado)
@dataclass(frozen=True)
class Ponto:
    x: float
    y: float


p = Ponto(3, 4)
try:
    p.x = 10
except AttributeError as e:          # FrozenInstanceError é um AttributeError
    print("Ponto é imutável:", type(e).__name__)
print()


# =====================================================================
# 14. ERROS COMUNS
# =====================================================================

print("=" * 60)
print("14. ERROS COMUNS")
print("=" * 60)

# ERRO 1: esquecer o self no método
#   class X:
#       def metodo():          # falta self
#           ...
#   X().metodo()  -> TypeError: X.metodo() takes 0 positional arguments but 1 was given
#   ("but 1 was given" = o Python passou o self, e o método não aceita)

# ERRO 2: esquecer o "self." ao usar um atributo
#   def depositar(self, valor):
#       saldo += valor         # NameError/UnboundLocalError: cadê o saldo?
#       self.saldo += valor    # CERTO

# ERRO 3: esquecer os parênteses ao criar o objeto ou chamar o método
#   conta = ContaBancaria      # conta é a CLASSE, não um objeto!
#   conta.resumo               # é o método, não o resultado dele

# ERRO 4: lista/dict como atributo de CLASSE quando devia ser de INSTÂNCIA
class TurmaErrada:
    alunos = []                       # compartilhada por TODAS as turmas!

    def matricular(self, nome: str) -> None:
        self.alunos.append(nome)


class TurmaCerta:
    def __init__(self):
        self.alunos = []              # cada turma com a sua lista

    def matricular(self, nome: str) -> None:
        self.alunos.append(nome)


t1, t2 = TurmaErrada(), TurmaErrada()
t1.matricular("Ana")
print("ERRO 4 -> turma 2 (errada) tem:", t2.alunos, "<- mas a Ana foi matriculada só na turma 1!")
t1, t2 = TurmaCerta(), TurmaCerta()
t1.matricular("Ana")
print("          turma 2 (certa) tem:", t2.alunos)

# ERRO 5: esquecer super().__init__() na classe filha
#   Os atributos definidos no __init__ da mãe NÃO são criados, e depois
#   dá AttributeError ao acessá-los.

# ERRO 6: herança onde devia ser composição ("Carro herda de Motor")

# ERRO 7: criar classe para TUDO. Se é só uma função que recebe dados e
# devolve um resultado, uma função basta. Classes são para quando há
# ESTADO (dados que mudam) + COMPORTAMENTO juntos.
print()


# =====================================================================
# 15. NAMING CONVENTIONS E BOAS PRÁTICAS
# =====================================================================
# NOMES (PEP 8):
#   - Classes: PascalCase, SUBSTANTIVO no SINGULAR
#       ContaBancaria, Produto, ItemPedido   (não: contas, gerenciar_conta)
#   - Métodos e atributos: snake_case
#       Métodos com VERBO: depositar(), calcular_total()
#       Atributos com SUBSTANTIVO: saldo, data_criacao
#   - Booleanos: ativo, esta_aprovado(), tem_estoque
#   - Constantes da classe: UPPER_SNAKE_CASE (AUMENTO_PADRAO)
#   - Uso interno: _prefixo (_saldo, _validar())
#   - Exceções: PascalCase terminando em Error (SaldoInsuficienteError)
#   - Primeiro parâmetro: SEMPRE "self" nos métodos e "cls" nos
#     @classmethod (é convenção, mas ninguém usa outro nome)
#
# BOAS PRÁTICAS:
#   1. Uma classe = uma responsabilidade. Se o nome precisa de "E"
#      (GerenciadorDeUsuariosEEmails), divida.
#   2. Todos os atributos de instância devem ser criados no __init__.
#   3. Valide os dados na entrada (no __init__ ou em setters), e não
#      deixe o objeto nascer num estado inválido.
#   4. Implemente __repr__ (ou use @dataclass): facilita MUITO o debug.
#   5. Use @dataclass para classes que são principalmente dados.
#   6. Prefira composição a herança.
#   7. Use _atributo + @property quando precisar proteger um dado.
#   8. Não crie getters/setters "à la Java" (get_nome, set_nome) sem
#      necessidade. Em Python, acesse o atributo direto e só use
#      @property quando precisar de validação ou cálculo.
#   9. Se for só uma função, não crie uma classe (erro 7).

print("=" * 60)
print("FIM! Agora vá para os exercícios no final do arquivo.")
print("=" * 60)


# =====================================================================
# 16. EXERCÍCIOS PARA PRATICAR
# =====================================================================
# Crie um arquivo novo (ex: exercicios_classes.py).
#
#  1. Crie a classe Pessoa com nome e idade, um método apresentar() que
#     retorna "Olá, sou X e tenho Y anos" e um método
#     fazer_aniversario() que aumenta a idade em 1.
#  2. Crie a classe Retangulo com base e altura e os métodos area(),
#     perimetro() e eh_quadrado(). Implemente __str__ e __repr__.
#  3. Crie a classe Contador com os métodos incrementar(),
#     decrementar() (sem passar de zero) e zerar(). Use um atributo de
#     classe para contar quantos contadores foram criados.
#  4. Crie a classe Temperatura com um @property celsius (com setter
#     que impede valores abaixo de -273.15) e properties somente
#     leitura para fahrenheit e kelvin.
#  5. Adicione à Temperatura um @classmethod de_fahrenheit(valor) que
#     cria uma Temperatura a partir de um valor em Fahrenheit.
#  6. Crie a classe Livro (titulo, autor, paginas) e a classe
#     Biblioteca, que TEM uma lista de livros (composição), com os
#     métodos adicionar(livro), buscar_por_autor(autor) e
#     total_paginas(). Implemente __len__ na Biblioteca.
#  7. Herança: crie a classe Veiculo (marca, modelo, ano) com o método
#     descrever(). Crie Carro (com portas) e Moto (com cilindradas) que
#     herdam de Veiculo, usam super().__init__ e sobrescrevem
#     descrever().
#  8. Polimorfismo: crie a classe Funcionario com o método
#     calcular_salario() e as filhas Clt (salário fixo), Freelancer
#     (horas * valor_hora) e Vendedor (fixo + comissão sobre vendas).
#     Coloque vários numa lista e calcule a folha de pagamento total.
#  9. Reescreva a classe Livro do exercício 6 usando @dataclass e
#     compare o tamanho do código.
# 10. Crie a classe Vetor2D (x, y) com __add__, __sub__, __eq__,
#     __repr__ e um método tamanho() (dica: math.hypot). Faça
#     Vetor2D(1, 2) + Vetor2D(3, 4) == Vetor2D(4, 6) dar True.
# 11. (Desafio) Reescreva a ContaBancaria com: saldo protegido
#     (_saldo + @property), extrato com data/hora de cada operação,
#     a exceção SaldoInsuficienteError e uma classe filha
#     ContaEspecial que tem um limite (permite saldo negativo até o
#     limite).
# 12. (Desafio) Transforme o mini projeto de tarefas (pacote tarefas/)
#     em classes: um @dataclass Tarefa (titulo, feita, criada_em) e uma
#     classe ListaDeTarefas com adicionar, concluir, remover, listar,
#     salvar e carregar (JSON).
