from typing import Required
import click
from utils import get_prompt_by_type
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

table = Table(title="Prompts", box=box.ROUNDED, show_lines=True)
table.add_column("Name", justify="center")
table.add_column("Type", justify="center")
table.add_column("Prompt", justify="center")
table.add_column("Model", justify="center")
table.add_column("Response", justify="center")

@click.group()
def cli():
    pass

@cli.command()
@click.option("--task", "-t", default="summarization", help="The task you want to perform")
@click.option("--type", "-ty", default="article-summarization", help="The type of prompt you want to perform")
@click.option("--input", "-i", default="", help="The input you want to perform")
@click.option("--model", "-m", default="gpt-3.5-turbo", required=False, help="The model you want to use")
def run(task, type, input, model):    
    title = Text("Prompt Cookbook", style="bold magenta")
    console.print(title, justify="center")
    console.print()
    
    console.print(f"Running [bold blue]{task}[/bold blue] with [bold green]{model}[/bold green] model...")
    
    prompt = get_prompt_by_type(task, type)
    prompt["prompt"] = prompt["prompt"].format(input=input)
    table.add_row(prompt["name"], prompt["type"], prompt["prompt"])
    console.print(table)
    
if __name__ == "__main__":
    cli()