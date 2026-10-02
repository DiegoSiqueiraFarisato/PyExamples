"""Menu interativo da lista de tarefas.

Rode a partir da pasta pythonStudies com:
    python -m tarefas.main

Por que "-m"? O "-m" executa o arquivo COMO MÓDULO do pacote, a partir
da pasta atual. Assim o "from tarefas import ..." funciona. Se rodar
"python tarefas/main.py", o Python coloca a pasta tarefas/ no sys.path
(e não a pythonStudies), e o import do pacote "tarefas" falha.
"""

from tarefas import operacoes


def pedir_numero(mensagem: str) -> int | None:
    try:
        return int(input(mensagem))
    except ValueError:
        print("  Digite um número.")
        return None


def main() -> None:
    while True:
        print()
        linhas = operacoes.listar()
        print("\n".join(linhas) if linhas else "(nenhuma tarefa)")
        print("\n[a] adicionar  [c] concluir  [r] remover  [s] sair")
        opcao = input("Opção: ").strip().lower()

        if opcao == "a":
            try:
                operacoes.adicionar(input("  Título: "))
            except ValueError as e:
                print(f"  Erro: {e}")
        elif opcao in ("c", "r"):
            numero = pedir_numero("  Número da tarefa: ")
            if numero is None:
                continue
            acao = operacoes.concluir if opcao == "c" else operacoes.remover
            if not acao(numero):
                print("  Tarefa não encontrada.")
        elif opcao == "s":
            print("Até mais!")
            break
        else:
            print("  Opção inválida.")


if __name__ == "__main__":
    main()
