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

        with open(nome_arquivo, "r") as f:
            return json.load(f)

    except json.JSONDecodeError:
        console.print(f"[red]Erro: JSON inválido em {nome_arquivo}[/red]")
        return {}

    except Exception as e:
        console.print(f"[red]Erro ao carregar {nome_arquivo}: {e}[/red]")
        return {}


def salvar_json(nome_arquivo, dados):
    try:
        with open(nome_arquivo, "w") as f:
            json.dump(dados, f, indent=4)

    except Exception as e:
        console.print(f"[red]Erro ao salvar {nome_arquivo}: {e}[/red]")


def input_float(msg):
    while True:
        try:
            valor = Prompt.ask(msg)
            return float(valor.replace(",", "."))
        except ValueError:
            console.print("[red]Digite um número válido![/red]")


# =========================
# ESTOQUE
# =========================

def mostrar_estoque(estoque):
    table = Table(title="📦 Estoque")
    table.add_column("Ingrediente", style="cyan")
    table.add_column("Quantidade", style="magenta")

    if not estoque:
        console.print("[yellow]Estoque vazio[/yellow]")
        return

    for k, v in estoque.items():
        table.add_row(k, str(v))

    console.print(table)


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
                title="📦 ESTOQUE",
                style="bold blue"
            ))

            op = Prompt.ask("Escolha")

            if op == "1":
                nome = Prompt.ask("Ingrediente").strip().lower()
                qtd = input_float("Quantidade")

                estoque[nome] = estoque.get(nome, 0) + qtd
                salvar_json(ARQUIVO_ESTOQUE, estoque)
                console.print("[green]Adicionado![/green]")

            elif op == "2":
                nome = Prompt.ask("Ingrediente").strip().lower()

                if nome in estoque:
                    del estoque[nome]
                    salvar_json(ARQUIVO_ESTOQUE, estoque)
                    console.print("[red]Removido totalmente![/red]")
                else:
                    console.print("[yellow]Não encontrado[/yellow]")

            elif op == "3":
                nome = Prompt.ask("Ingrediente").strip().lower()

                if nome in estoque:
                    qtd = input_float("Quantidade para remover")

                    if qtd >= estoque[nome]:
                        del estoque[nome]
                        console.print("[red]Ingrediente zerado e removido![/red]")
                    else:
                        estoque[nome] -= qtd
                        console.print("[yellow]Quantidade atualizada![/yellow]")

                    salvar_json(ARQUIVO_ESTOQUE, estoque)
                else:
                    console.print("[yellow]Não encontrado[/yellow]")

            elif op == "4":
                mostrar_estoque(estoque)

            elif op == "5":
                break

            else:
                console.print("[yellow]Opção inválida[/yellow]")

        except Exception as e:
            console.print(f"[red]Erro no estoque: {e}[/red]")


# =========================
# RECEITAS
# =========================

def mostrar_receitas(receitas):
    if not receitas:
        console.print("[yellow]Nenhuma receita cadastrada[/yellow]")
        return

    for nome, ingredientes in receitas.items():
        table = Table(title=f"🍰 {nome}")
        table.add_column("Ingrediente", style="cyan")
        table.add_column("Quantidade", style="magenta")

        for ing, qtd in ingredientes.items():
            table.add_row(ing, str(qtd))

        console.print(table)


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

            op = Prompt.ask("Escolha")

            if op == "1":
                nome = Prompt.ask("Nome da receita").strip().lower()

                if nome in receitas:
                    console.print("[yellow]Receita já existe[/yellow]")
                    continue

                receita = {}

                while True:
                    ing = Prompt.ask("Ingrediente (ou 'fim')").strip().lower()

                    if ing == "fim":
                        break

                    if ing in receita:
                        console.print("[yellow]Ingrediente já existe na receita[/yellow]")
                        continue

                    qtd = input_float("Quantidade")
                    receita[ing] = qtd

                receitas[nome] = receita
                salvar_json(ARQUIVO_RECEITAS, receitas)
                console.print("[green]Receita criada![/green]")

            elif op == "2":
                nome = Prompt.ask("Receita").strip().lower()

                if nome in receitas:
                    del receitas[nome]
                    salvar_json(ARQUIVO_RECEITAS, receitas)
                    console.print("[red]Receita removida![/red]")
                else:
                    console.print("[yellow]Não encontrada[/yellow]")

            elif op == "3":
                nome = Prompt.ask("Receita").strip().lower()

                if nome not in receitas:
                    console.print("[red]Receita não existe[/red]")
                    continue

                receita = receitas[nome]

                console.print(Panel(
                    "1 - Remover ingrediente\n2 - Diminuir quantidade",
                    title="EDITAR RECEITA"
                ))

                escolha = Prompt.ask("Escolha")

                if escolha == "1":
                    ing = Prompt.ask("Ingrediente").strip().lower()

                    if ing in receita:
                        del receita[ing]
                        console.print("[red]Ingrediente removido[/red]")
                    else:
                        console.print("[yellow]Não existe[/yellow]")

                elif escolha == "2":
                    ing = Prompt.ask("Ingrediente").strip().lower()

                    if ing in receita:
                        qtd = input_float("Quantidade para remover")

                        if qtd >= receita[ing]:
                            del receita[ing]
                            console.print("[red]Ingrediente removido da receita[/red]")
                        else:
                            receita[ing] -= qtd
                            console.print("[yellow]Quantidade atualizada[/yellow]")
                    else:
                        console.print("[yellow]Não existe[/yellow]")

                receitas[nome] = receita
                salvar_json(ARQUIVO_RECEITAS, receitas)

            elif op == "4":
                mostrar_receitas(receitas)

            elif op == "5":
                break

            else:
                console.print("[yellow]Opção inválida[/yellow]")

        except Exception as e:
            console.print(f"[red]Erro nas receitas: {e}[/red]")


# =========================
# PRODUÇÃO
# =========================

def menu_producao():
    try:
        estoque = carregar_json(ARQUIVO_ESTOQUE)
        receitas = carregar_json(ARQUIVO_RECEITAS)

        console.print(Panel("Produção", style="bold yellow"))

        nome = Prompt.ask("Receita").strip().lower()

        if nome not in receitas:
            console.print("[red]Receita não encontrada![/red]")
            return

        receita = receitas[nome]

        for ing, qtd in receita.items():
            if estoque.get(ing, 0) < qtd:
                console.print(f"[red]Falta {ing}![/red]")
                return

        for ing, qtd in receita.items():
            estoque[ing] -= qtd

        salvar_json(ARQUIVO_ESTOQUE, estoque)
        console.print("[green]Produção concluída![/green]")

    except Exception as e:
        console.print(f"[red]Erro na produção: {e}[/red]")


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

            op = Prompt.ask("Escolha")

            if op == "1":
                menu_estoque()
            elif op == "2":
                menu_receitas()
            elif op == "3":
                menu_producao()
            elif op == "4":
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