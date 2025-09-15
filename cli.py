from typing import Required
import click
from utils import (
    get_prompt_by_type,
    run_prompt,
    create_prompt_log,
    log_prompt_run,
    list_tasks,
    list_models_by_provider,
)
from rich.console import Console
from rich.text import Text
from rich.table import Table


console = Console()


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--task", "-t", default="summarization", help="The task you want to perform"
)
@click.option(
    "--type",
    "-ty",
    default="article-summarization",
    help="The type of prompt you want to perform",
)
@click.option("--input", "-i", default="", help="The input you want to perform")
@click.option(
    "--model",
    "-m",
    default="gpt-3.5-turbo",
    required=False,
    help="The model you want to use",
)
def run(task, type, input, model):
    """
    Run a prompt with inputs and model you want to use and get response from the model \n

    """
    title = Text("Prompt Cookbook", style="bold magenta")
    console.print(title, justify="center")
    console.print()

    console.print(
        f"Running [bold blue]{task}[/bold blue] task with [bold green]{model}[/bold green] model..."
    )

    prompt = get_prompt_by_type(task, type, input)
    console.print(
        f"[bold blue]Prompt to run:[/bold blue] \n {prompt['prompt']}",
        new_line_start=True,
    )
    console.print()

    status = "success"
    try:
        response, latency = run_prompt(prompt["prompt"], model)
        console.print(f"[bold yellow]Response:[/bold yellow] \n {response}")
    except Exception as e:
        console.print(f"Error: {e if e else 'Unknown error'}", style="bold red")
        status = "error"
        return

    console.print()
    console.print("[bold green]Logging the prompt run results...")

    prompt_log = create_prompt_log(
        "run",
        prompt["name"],
        prompt["prompt"],
        task,
        type,
        input,
        model,
        response,
        latency,
        status,
    )
    status, result = log_prompt_run(prompt_log)

    console.print()
    if status == "success":
        console.print(f"[bold green]{result}[/bold green]")
    else:
        console.print(f"[bold red]{result}[/bold red]")


@cli.command()
@click.option(
    "--provider",
    default="all",
    help="The provider you want to list the models for (eg: openai, groq)",
)
def list_models(provider):
    """
    List all the supported models from the providers. \n
    """
    models = list_models_by_provider(provider)
    console.print(f"[bold green]Available models:[/bold green]")
    console.print()
    table = Table("Provider", "Model", show_lines=True)
    for [provider_name, model] in models.items():
        for model_name in model:
            table.add_row(provider_name, model_name)
    console.print(table)


@cli.command()
@click.option("--task", default="all", help="The tasks avaiable")
def list(task):
    """
    List all the available tasks and their types.\n
    """
    tasks = list_tasks(task)
    console.print(f"[bold green]Available tasks:[/bold green]")
    console.print()
    table = Table("Task", "Type", "Prompt", show_lines=True)
    for [task_name, prompts] in tasks.items():
        for prompt in prompts:
            table.add_row(task_name, prompt["type"], prompt["prompt"])
    console.print(table)


if __name__ == "__main__":
    cli()
