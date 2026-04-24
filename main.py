import json
import os
import traceback
import msvcrt
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

ARQUIVO_ESTOQUE = "estoque.json"
ARQUIVO_RECEITAS = "receita.json"

# =========================
# MENU COM SETAS
# =========================

def menu_setas(opcoes, titulo=""):
    atual = 0

    while True:
        os.system("cls")  # limpa corretamente no Windows

        linhas = []
        for i, opcao in enumerate(opcoes):
            if i == atual:
                linhas.append(f"[black on white]> {opcao}[/black on white]")
            else:
                linhas.append(f"  {opcao}")

        console.print(Panel("\n".join(linhas), title=titulo))

        tecla = msvcrt.getch()

        if tecla == b'\xe0':
            tecla = msvcrt.getch()

            if tecla == b'H':
                atual -= 1
            elif tecla == b'P':
                atual += 1

        elif tecla == b'\r':
            return atual

        atual %= len(opcoes)

# =========================
# UTIL
# =========================

def carregar_json(nome_arquivo):
    try:
        if not os.path.exists(nome_arquivo):
            return {}

        with open(nome_arquivo, "r") as arquivo:
            return json.load(arquivo)

    except json.JSONDecodeError:
        console.print(f"[red]JSON inválido em {nome_arquivo}[/red]")
        return {}

    except Exception as e:
        console.print(f"[red]Erro ao carregar: {e}[/red]")
        return {}


def salvar_json(nome_arquivo, dados):
    with open(nome_arquivo, "w") as arquivo:
        json.dump(dados, arquivo, indent=4)


def input_float(mensagem):
    while True:
        try:
            valor = Prompt.ask(mensagem)
            return float(valor.replace(",", "."))
        except:
            console.print("[red]Número inválido[/red]")

# =========================
# ESTOQUE
# =========================

def mostrar_estoque(estoque):
    tabela = Table(title="Estoque")
    tabela.add_column("Ingrediente")
    tabela.add_column("Quantidade")

    if not estoque:
        console.print("[yellow]Estoque vazio[/yellow]")
        return

    for i, q in estoque.items():
        tabela.add_row(i, str(q))

    console.print(tabela)


def menu_estoque():
    while True:
        estoque = carregar_json(ARQUIVO_ESTOQUE)

        opcao = menu_setas(
            ["Adicionar", "Remover total", "Remover quantidade", "Ver estoque", "Voltar"],
            "ESTOQUE"
        )

        if opcao == 0:
            nome = Prompt.ask("Ingrediente").strip().lower()
            q = input_float("Quantidade")
            estoque[nome] = estoque.get(nome, 0) + q
            salvar_json(ARQUIVO_ESTOQUE, estoque)

        elif opcao == 1:
            nome = Prompt.ask("Ingrediente").strip().lower()
            if nome in estoque:
                del estoque[nome]
                salvar_json(ARQUIVO_ESTOQUE, estoque)

        elif opcao == 2:
            nome = Prompt.ask("Ingrediente").strip().lower()
            if nome in estoque:
                q = input_float("Quantidade")
                estoque[nome] -= q
                if estoque[nome] <= 0:
                    del estoque[nome]
                salvar_json(ARQUIVO_ESTOQUE, estoque)

        elif opcao == 3:
            mostrar_estoque(estoque)
            input("Pressione Enter...")

        elif opcao == 4:
            break

# =========================
# RECEITAS
# =========================

def mostrar_receitas(receitas):
    if not receitas:
        console.print("[yellow]Nenhuma receita[/yellow]")
        return

    for nome, ingredientes in receitas.items():
        tabela = Table(title=nome)
        tabela.add_column("Ingrediente")
        tabela.add_column("Quantidade")

        for i, q in ingredientes.items():
            tabela.add_row(i, str(q))

        console.print(tabela)


def menu_receitas():
    while True:
        receitas = carregar_json(ARQUIVO_RECEITAS)

        opcao = menu_setas(
            ["Criar", "Remover", "Editar", "Ver", "Voltar"],
            "RECEITAS"
        )

        if opcao == 0:
            nome = Prompt.ask("Nome").strip().lower()
            nova = {}

            while True:
                ing = Prompt.ask("Ingrediente (fim p/ sair)").strip().lower()
                if ing == "fim":
                    break
                q = input_float("Quantidade")
                nova[ing] = q

            receitas[nome] = nova
            salvar_json(ARQUIVO_RECEITAS, receitas)

        elif opcao == 1:
            nomes = list(receitas.keys())
            if not nomes:
                console.print("[yellow]Sem receitas[/yellow]")
                input("Enter...")
                continue

            i = menu_setas(nomes, "Remover receita")
            del receitas[nomes[i]]
            salvar_json(ARQUIVO_RECEITAS, receitas)

        elif opcao == 2:
            nomes = list(receitas.keys())
            if not nomes:
                console.print("[yellow]Sem receitas[/yellow]")
                input("Enter...")
                continue

            i = menu_setas(nomes, "Editar receita")
            nome = nomes[i]
            receita = receitas[nome]

            ingredientes = list(receita.keys())
            if not ingredientes:
                console.print("[yellow]Sem ingredientes[/yellow]")
                input("Enter...")
                continue

            j = menu_setas(ingredientes, "Escolha ingrediente")
            ing = ingredientes[j]

            q = input_float("Remover quanto?")
            receita[ing] -= q

            if receita[ing] <= 0:
                del receita[ing]

            receitas[nome] = receita
            salvar_json(ARQUIVO_RECEITAS, receitas)

        elif opcao == 3:
            mostrar_receitas(receitas)
            input("Pressione Enter...")

        elif opcao == 4:
            break

# =========================
# PRODUÇÃO
# =========================

def menu_producao():
    estoque = carregar_json(ARQUIVO_ESTOQUE)
    receitas = carregar_json(ARQUIVO_RECEITAS)

    if not receitas:
        console.print("[yellow]Sem receitas[/yellow]")
        input("Enter...")
        return

    nomes = list(receitas.keys())

    i = menu_setas(nomes, "Escolha receita")
    nome = nomes[i]
    receita = receitas[nome]

    qtd = input_float("Quantidade")

    for ing, q in receita.items():
        if estoque.get(ing, 0) < q * qtd:
            console.print(f"[red]Falta {ing}[/red]")
            input("Enter...")
            return

    for ing, q in receita.items():
        estoque[ing] -= q * qtd

    salvar_json(ARQUIVO_ESTOQUE, estoque)
    console.print("[green]Produção concluída[/green]")
    input("Enter...")

# =========================
# MAIN
# =========================

def main():
    while True:
        opcao = menu_setas(
            ["Estoque", "Receitas", "Produção", "Sair"],
            "SISTEMA DE CONFEITARIA"
        )

        if opcao == 0:
            menu_estoque()
        elif opcao == 1:
            menu_receitas()
        elif opcao == 2:
            menu_producao()
        elif opcao == 3:
            break


if __name__ == "__main__":
    main()
