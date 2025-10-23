from typing import Required
import click
import json
from utils import (
    get_prompt_by_type,
    run_prompt,
    create_prompt_log,
    log_prompt_run,
    list_tasks,
    list_models_by_provider,
    log_prompt_engineering_run,
)
from prompt_engineering import apply_technique
from evaluation import evaluate_output, generate_evaluation_report
from models.prompt_engineering_log import PromptEngineeringLog
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax


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


@cli.command()
@click.option(
    "--technique",
    "-t",
    required=True,
    type=click.Choice(
        ["single-shot", "meta-prompting", "chain-of-thought", "few-shot"],
        case_sensitive=False,
    ),
    help="Prompt engineering technique to apply",
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to JSON config file with technique parameters",
)
@click.option(
    "--params",
    "-p",
    help="JSON string with technique parameters (alternative to config file)",
)
@click.option(
    "--model",
    "-m",
    default="gpt-3.5-turbo",
    help="The model to use for generation",
)
@click.option(
    "--reference",
    "-r",
    help="Reference text for evaluation (optional)",
)
@click.option(
    "--keywords",
    "-k",
    help="Comma-separated keywords for evaluation (optional)",
)
@click.option(
    "--evaluate/--no-evaluate",
    default=True,
    help="Whether to evaluate the output (default: True)",
)
def prompt_engineer(technique, config, params, model, reference, keywords, evaluate):
    """
    Apply prompt engineering techniques to generate optimized prompts.\n
    Supports techniques: single-shot, meta-prompting, chain-of-thought, few-shot\n
    Examples:\n
    Single-shot prompting:\n
        python cli.py prompt-engineer -t single-shot -p '{"task_description": "Translate to French", "example_input": "Hello", "example_output": "Bonjour", "actual_input": "Good morning"}'\n
    Meta-prompting:\n
        python cli.py prompt-engineer -t meta-prompting -p '{"goal": "Summarize technical documentation", "context": "For junior developers"}'\n
    With evaluation:\n
        python cli.py prompt-engineer -t single-shot -c config.json -r "Expected output" -k "keyword1,keyword2"\n
    """
    title = Text("Prompt Engineering Lab", style="bold magenta")
    console.print(title, justify="center")
    console.print()

    # Parse parameters
    try:
        if config:
            with open(config, "r") as f:
                technique_params = json.load(f)
            console.print(f"[bold blue]Loaded config from:[/bold blue] {config}")
        elif params:
            technique_params = json.loads(params)
        else:
            console.print(
                "[bold red]Error:[/bold red] Either --config or --params must be provided",
                style="bold red",
            )
            return
    except json.JSONDecodeError as e:
        console.print(f"[bold red]Invalid JSON:[/bold red] {e}")
        return
    except Exception as e:
        console.print(f"[bold red]Error loading parameters:[/bold red] {e}")
        return

    console.print(
        f"\n[bold blue]Applying technique:[/bold blue] [bold cyan]{technique}[/bold cyan]"
    )
    console.print(f"[bold blue]Using model:[/bold blue] [bold green]{model}[/bold green]")
    console.print()

    # Apply prompt engineering technique
    try:
        generated_prompt, metadata = apply_technique(technique, technique_params)

        # Display the generated prompt
        console.print(Panel(
            Syntax(generated_prompt, "text", theme="monokai", word_wrap=True),
            title="[bold yellow]Generated Prompt[/bold yellow]",
            border_style="yellow",
        ))
        console.print()

    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")
        return

    # Run the prompt with the model
    status = "success"
    try:
        console.print("[bold blue]Running prompt with model...[/bold blue]")
        response, latency = run_prompt(generated_prompt, model)
        console.print()
        console.print(Panel(
            response,
            title="[bold green]Model Output[/bold green]",
            border_style="green",
        ))
        console.print()
        console.print(f"[dim]Latency: {latency:.2f}ms[/dim]")
    except Exception as e:
        console.print(f"[bold red]Error running prompt:[/bold red] {e}")
        status = "error"
        response = ""
        latency = None

    # Evaluate the output if requested
    evaluation_results = None
    if evaluate and status == "success" and response:
        console.print("\n[bold blue]Evaluating output...[/bold blue]")
        console.print()

        # Parse keywords if provided
        keyword_list = None
        if keywords:
            keyword_list = [kw.strip() for kw in keywords.split(",")]

        # Evaluate
        evaluation_results = evaluate_output(
            candidate=response,
            reference=reference,
            keywords=keyword_list,
        )

        # Generate and display report
        report = generate_evaluation_report(
            technique=technique,
            prompt=generated_prompt,
            output=response,
            evaluation_results=evaluation_results,
        )
        console.print(Panel(
            report,
            title="[bold cyan]Evaluation Report[/bold cyan]",
            border_style="cyan",
        ))

    # Log the experiment
    console.print("\n[bold green]Logging experiment...[/bold green]")
    prompt_log = PromptEngineeringLog(
        technique=technique,
        prompt=generated_prompt,
        model=model,
        output=response,
        latency_ms=latency,
        status=status,
        metadata=metadata,
        evaluation_metrics=evaluation_results,
        reference_text=reference,
        keywords=keyword_list,
    )

    log_status, log_result = log_prompt_engineering_run(prompt_log)
    if log_status == "success":
        console.print(f"[bold green]{log_result}[/bold green]")
    else:
        console.print(f"[bold red]Logging failed: {log_result}[/bold red]")

    console.print("\n[bold green]✓ Prompt engineering experiment completed![/bold green]")


if __name__ == "__main__":
    cli()
