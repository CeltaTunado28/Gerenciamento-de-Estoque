import json
import os
import traceback
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

ARQUIVO_ESTOQUE = "confeitaria_estoque.json"
ARQUIVO_RECEITAS = "confeitaria_receitas.json"

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
        console.print(f"[red]Erro: JSON inválido em {nome_arquivo}[/red]")
        return {}

    except Exception as erro:
        console.print(f"[red]Erro ao carregar {nome_arquivo}: {erro}[/red]")
        return {}


def salvar_json(nome_arquivo, dados):
    try:
        with open(nome_arquivo, "w") as arquivo:
            json.dump(dados, arquivo, indent=4)

    except Exception as erro:
        console.print(f"[red]Erro ao salvar {nome_arquivo}: {erro}[/red]")


def input_float(mensagem):
    while True:
        try:
            valor_digitado = Prompt.ask(mensagem)
            return float(valor_digitado.replace(",", "."))
        except ValueError:
            console.print("[red]Digite um número válido![/red]")


# =========================
# ESTOQUE
# =========================

def mostrar_estoque(estoque):
    tabela = Table(title="📦 Estoque")
    tabela.add_column("Ingrediente", style="cyan")
    tabela.add_column("Quantidade", style="magenta")

    if not estoque:
        console.print("[yellow]Estoque vazio[/yellow]")
        return

    for ingrediente, quantidade in estoque.items():
        tabela.add_row(ingrediente, str(quantidade))

    console.print(tabela)


def menu_estoque():
    while True:
        try:
            estoque = carregar_json(ARQUIVO_ESTOQUE)

            console.print(Panel(
                "1 - Adicionar\n"
                "2 - Remover ingrediente (total)\n"
                "3 - Remover quantidade\n"
                "4 - Ver estoque\n"
                "5 - Voltar",
                title="ESTOQUE",
                style="bold blue"
            ))

            opcao = Prompt.ask("Escolha")

            if opcao == "1":
                nome_ingrediente = Prompt.ask("Ingrediente").strip().lower()
                quantidade = input_float("Quantidade")

                estoque[nome_ingrediente] = estoque.get(nome_ingrediente, 0) + quantidade
                salvar_json(ARQUIVO_ESTOQUE, estoque)
                console.print("[green]Adicionado![/green]")

            elif opcao == "2":
                nome_ingrediente = Prompt.ask("Ingrediente").strip().lower()

                if nome_ingrediente in estoque:
                    del estoque[nome_ingrediente]
                    salvar_json(ARQUIVO_ESTOQUE, estoque)
                    console.print("[red]Removido totalmente![/red]")
                else:
                    console.print("[yellow]Não encontrado[/yellow]")

            elif opcao == "3":
                nome_ingrediente = Prompt.ask("Ingrediente").strip().lower()

                if nome_ingrediente in estoque:
                    quantidade = input_float("Quantidade para remover")

                    if quantidade >= estoque[nome_ingrediente]:
                        del estoque[nome_ingrediente]
                        console.print("[red]Ingrediente zerado e removido![/red]")
                    else:
                        estoque[nome_ingrediente] -= quantidade
                        console.print("[yellow]Quantidade atualizada![/yellow]")

                    salvar_json(ARQUIVO_ESTOQUE, estoque)
                else:
                    console.print("[yellow]Não encontrado[/yellow]")

            elif opcao == "4":
                mostrar_estoque(estoque)

            elif opcao == "5":
                break

            else:
                console.print("[yellow]Opção inválida[/yellow]")

        except Exception as erro:
            console.print(f"[red]Erro no estoque: {erro}[/red]")


# =========================
# RECEITAS
# =========================

def mostrar_receitas(receitas):
    if not receitas:
        console.print("[yellow]Nenhuma receita cadastrada[/yellow]")
        return

    for nome_receita, ingredientes in receitas.items():
        tabela = Table(title=f"🍰 {nome_receita}")
        tabela.add_column("Ingrediente", style="cyan")
        tabela.add_column("Quantidade", style="magenta")

        for ingrediente, quantidade in ingredientes.items():
            tabela.add_row(ingrediente, str(quantidade))

        console.print(tabela)


def menu_receitas():
    while True:
        try:
            receitas = carregar_json(ARQUIVO_RECEITAS)

            console.print(Panel(
                "1 - Criar receita\n"
                "2 - Remover receita (total)\n"
                "3 - Editar receita\n"
                "4 - Ver receitas\n"
                "5 - Voltar",
                title="🍰 RECEITAS",
                style="bold green"
            ))

            opcao = Prompt.ask("Escolha")

            if opcao == "1":
                nome_receita = Prompt.ask("Nome da receita").strip().lower()

                if nome_receita in receitas:
                    console.print("[yellow]Receita já existe[/yellow]")
                    continue

                nova_receita = {}

                while True:
                    ingrediente = Prompt.ask("Ingrediente (ou 'fim')").strip().lower()

                    if ingrediente == "fim":
                        break

                    if ingrediente in nova_receita:
                        console.print("[yellow]Ingrediente já existe na receita[/yellow]")
                        continue

                    quantidade = input_float("Quantidade")
                    nova_receita[ingrediente] = quantidade

                receitas[nome_receita] = nova_receita
                salvar_json(ARQUIVO_RECEITAS, receitas)
                console.print("[green]Receita criada![/green]")

            elif opcao == "2":
                nome_receita = Prompt.ask("Receita").strip().lower()

                if nome_receita in receitas:
                    del receitas[nome_receita]
                    salvar_json(ARQUIVO_RECEITAS, receitas)
                    console.print("[red]Receita removida![/red]")
                else:
                    console.print("[yellow]Não encontrada[/yellow]")

            elif opcao == "3":
                nome_receita = Prompt.ask("Receita").strip().lower()

                if nome_receita not in receitas:
                    console.print("[red]Receita não existe[/red]")
                    continue

                receita = receitas[nome_receita]

                console.print(Panel(
                    "1 - Remover ingrediente\n2 - Diminuir quantidade",
                    title="EDITAR RECEITA"
                ))

                escolha = Prompt.ask("Escolha")

                if escolha == "1":
                    ingrediente = Prompt.ask("Ingrediente").strip().lower()

                    if ingrediente in receita:
                        del receita[ingrediente]
                        console.print("[red]Ingrediente removido[/red]")
                    else:
                        console.print("[yellow]Não existe[/yellow]")

                elif escolha == "2":
                    ingrediente = Prompt.ask("Ingrediente").strip().lower()

                    if ingrediente in receita:
                        quantidade = input_float("Quantidade para remover")

                        if quantidade >= receita[ingrediente]:
                            del receita[ingrediente]
                            console.print("[red]Ingrediente removido da receita[/red]")
                        else:
                            receita[ingrediente] -= quantidade
                            console.print("[yellow]Quantidade atualizada[/yellow]")
                    else:
                        console.print("[yellow]Não existe[/yellow]")

                receitas[nome_receita] = receita
                salvar_json(ARQUIVO_RECEITAS, receitas)

            elif opcao == "4":
                mostrar_receitas(receitas)

            elif opcao == "5":
                break

            else:
                console.print("[yellow]Opção inválida[/yellow]")

        except Exception as erro:
            console.print(f"[red]Erro nas receitas: {erro}[/red]")


# =========================
# PRODUÇÃO
# =========================

def menu_producao():
    try:
        estoque = carregar_json(ARQUIVO_ESTOQUE)
        receitas = carregar_json(ARQUIVO_RECEITAS)

        if not receitas:
            console.print("[yellow]Nenhuma receita cadastrada[/yellow]")
            return

        console.print(Panel("🍳 PRODUÇÃO - Escolha a receita", style="bold yellow"))

        lista_receitas = list(receitas.items())

        for indice, (nome_receita, ingredientes) in enumerate(lista_receitas, start=1):
            tabela = Table(title=f"{indice} - 🍰 {nome_receita}")
            tabela.add_column("Ingrediente", style="cyan")
            tabela.add_column("Quantidade", style="magenta")

            for ingrediente, quantidade in ingredientes.items():
                tabela.add_row(ingrediente, str(quantidade))

            console.print(tabela)

        escolha = Prompt.ask("\nDigite o número da receita")

        if not escolha.isdigit():
            console.print("[red]Digite um número válido![/red]")
            return

        indice_escolhido = int(escolha) - 1

        if indice_escolhido < 0 or indice_escolhido >= len(lista_receitas):
            console.print("[red]Opção inválida![/red]")
            return

        nome_receita, receita = lista_receitas[indice_escolhido]

        quantidade_producao = input_float("Quantas unidades deseja produzir?")

        if quantidade_producao <= 0:
            console.print("[red]Quantidade inválida![/red]")
            return

        for ingrediente, quantidade in receita.items():
            if estoque.get(ingrediente, 0) < quantidade * quantidade_producao:
                console.print(f"[red]Falta {ingrediente}! Necessário: {quantidade * quantidade_producao}[/red]")
                return

        for ingrediente, quantidade in receita.items():
            estoque[ingrediente] -= quantidade * quantidade_producao

        salvar_json(ARQUIVO_ESTOQUE, estoque)
        console.print(f"[green]Produção de {quantidade_producao}x '{nome_receita}' concluída![/green]")

    except Exception as erro:
        console.print(f"[red]Erro na produção: {erro}[/red]")


# =========================
# MENU PRINCIPAL
# =========================

def main():
    while True:
        try:
            console.print(Panel(
                "1 - Estoque\n2 - Receitas\n3 - Produção\n4 - Sair",
                title="🍩 SISTEMA DE CONFEITARIA",
                style="bold magenta"
            ))

            opcao = Prompt.ask("Escolha")

            if opcao == "1":
                menu_estoque()
            elif opcao == "2":
                menu_receitas()
            elif opcao == "3":
                menu_producao()
            elif opcao == "4":
                console.print("[bold red]Saindo...[/bold red]")
                break
            else:
                console.print("[yellow]Opção inválida[/yellow]")

        except KeyboardInterrupt:
            console.print("\n[red]Encerrado pelo usuário[/red]")
            break

        except Exception:
            console.print("[red]Erro inesperado:[/red]")
            console.print(traceback.format_exc())


if __name__ == "__main__":
    main()
