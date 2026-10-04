"""Funções de entrada do usuário (input).

Resposta do exercício 10 do material 15_testes.py. O pedir_inteiro
original está em 08_respostas_erros.py, mas aquele arquivo NÃO pode ser
importado: o nome começa com número e, ao ser importado, ele executaria
todos os exemplos e o menu. Para testar a função, ela precisou morar
num módulo de verdade. Isso também é uma lição de "código testável".
"""


def pedir_inteiro(mensagem: str) -> int:
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Valor inválido, digite um número inteiro.")
