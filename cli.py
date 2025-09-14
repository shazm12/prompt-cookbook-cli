from typing import Required
import click
from utils import get_prompt_by_type, run_prompt, create_prompt_log, log_prompt_run
from rich.console import Console
from rich.text import Text


console = Console()


@click.group()
def cli():
    pass

@cli.command()
@click.option("--task", "-t", default="summarization", help="The task you want to perform")
@click.option("--type", "-ty", default="article-summarization", help="The type of prompt you want to perform")
@click.option("--input", "-i", default="", help="The input you want to perform")
@click.option("--model", "-m", default="gpt-3.5-turbo", required=False, help="The model you want to use")
def run(task, type, input, model):
    """ 
    Run a prompt with inputs and model you want to use and get response from the model \n
    
    Args: \n
        task: The task you want to perform \n
        type: The type of prompt you want to perform \n
        input: The input you want to perform \n
        model: The model you want to use \n
    
    """    
    title = Text("Prompt Cookbook", style="bold magenta")
    console.print(title, justify="center")
    console.print()
    
    console.print(f"Running [bold blue]{task}[/bold blue] task with [bold green]{model}[/bold green] model...")
    
    prompt = get_prompt_by_type(task, type, input)
    console.print(f"[bold blue]Prompt to run:[/bold blue] \n {prompt['prompt']}", new_line_start=True)
    console.print()
    
    status = "success"
    try:
        response, latency = run_prompt(prompt['prompt'], model)
        console.print(f"[bold yellow]Response:[/bold yellow] \n {response}")
    except Exception as e:
        console.print(f"Error: {e}", style="bold red")
        status = "error"
        return

    console.print()
    console.print("[bold green]Logging the prompt run results...")

    prompt_log = create_prompt_log("run", prompt['name'], prompt['prompt'], task, type, input, model, response, latency, status)
    status, result = log_prompt_run(prompt_log)
    
    console.print()
    if status == "success":
        console.print(f"[bold green]{result}[/bold green]")
    else:
        console.print(f"[bold red]{result}[/bold red]")
    
if __name__ == "__main__":
    cli()