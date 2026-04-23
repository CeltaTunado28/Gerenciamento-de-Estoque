import msvcrt
import sys

opcoes = ["Iniciar jogo", "Configurações", "Sair"]
atual = 0

def mover_cursor(linha, coluna):
    sys.stdout.write(f"\033[{linha};{coluna}H")

def limpar_tela():
    sys.stdout.write("\033[2J")

def desenhar_menu():
    for i, opcao in enumerate(opcoes):
        mover_cursor(i + 1, 1)

        if i == atual:
            print(f"> {opcao}  ")
        else:
            print(f"  {opcao}  ")

limpar_tela()

while True:
    desenhar_menu()

    tecla = msvcrt.getch()

    if tecla == b'\xe0':
        tecla = msvcrt.getch()

        if tecla == b'H':
            atual -= 1
        elif tecla == b'P':
            atual += 1

    elif tecla == b'\r':
        break

    atual %= len(opcoes)

mover_cursor(len(opcoes) + 2, 1)
print(f"Você escolheu: {opcoes[atual]}")
def menu_principal():
    return mostrar_menu(
        ["Jogar", "Configurações", "Estoque", "Relatórios", "Sair"],
        "Menu Principal"
    )


def menu_jogo():
    return mostrar_menu(
        ["Novo jogo", "Carregar", "Voltar"],
        "Jogo"
    )


def menu_config():
    return mostrar_menu(
        ["Áudio", "Vídeo", "Voltar"],
        "Configurações"
    )


def menu_estoque():
    return mostrar_menu(
        ["Ver itens", "Adicionar", "Remover", "Voltar"],
        "Estoque"
    )


def menu_relatorio():
    return mostrar_menu(
        ["Vendas", "Lucro", "Voltar"],
        "Relatórios"
    )

menu_principal()
