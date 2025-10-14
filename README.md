# Prompt Cookbook CLI

A CLI tool for running and managing AI prompts across different tasks and models. It offers a collection of pre-built prompts, curated from various sources and tested for common tasks such as summarization and coding. The tool supports multiple AI providers, including OpenAI and Groq.

## Features

- **Pre-built Prompts**: Curated collection of prompts for summarization and coding tasks
- **Multi-Provider Support**: Works with OpenAI and Groq models
- **Task Management**: Organize prompts by task type (summarization, coding)
- **Logging**: Track prompt runs with performance metrics and results
- **CLI Interface**: Easy-to-use command-line interface with rich output
- **Prompt Engineering**: Apply advanced prompt engineering techniques
  - Single-shot prompting
  - Meta-prompting
  - Chain-of-thought prompting
  - Few-shot prompting
- **Evaluation Metrics**: Comprehensive evaluation of prompt outputs
  - BLEU score for text similarity
  - Word overlap analysis
  - Length metrics
  - Keyword presence checking

## Available Tasks

### Summarization
- Article summarization
- Meeting notes summarization  
- Technical documentation summarization
- Research paper summarization

### Coding
- Python development
- JavaScript/TypeScript code review
- Node.js development
- DevOps engineering

## Dev Setup

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd prompt-cookbook
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Usage

**Run a prompt:**
```bash
python cli.py run --task summarization --type article-summarization --input "Your text here" --model gpt-4o
```

**List available tasks:**
```bash
python cli.py list
```

**List available models:**
```bash
python cli.py list-models
```

**List models by provider:**
```bash
python cli.py list-models --provider openai
```

### Prompt Engineering

**Single-shot prompting** (provide one example to guide the model):
```bash
python cli.py prompt-engineer --technique single-shot --config examples/single_shot_config.json --model gpt-4o
```

Or with inline parameters:
```bash
python cli.py prompt-engineer -t single-shot -p '{"task_description": "Translate to French", "example_input": "Hello", "example_output": "Bonjour", "actual_input": "Good morning"}' -m gpt-4o
```

**Meta-prompting** (generate optimized prompts):
```bash
python cli.py prompt-engineer --technique meta-prompting --config examples/meta_prompting_config.json
```

**Chain-of-thought prompting** (encourage step-by-step reasoning):
```bash
python cli.py prompt-engineer -t chain-of-thought --config examples/chain_of_thought_config.json
```

**Few-shot prompting** (provide multiple examples):
```bash
python cli.py prompt-engineer -t few-shot --config examples/few_shot_config.json
```

**With evaluation metrics:**
```bash
python cli.py prompt-engineer -t single-shot -c examples/single_shot_config.json -r "Bonjour, passez une excellente journée!" -k "Bonjour,journée"
```

Options:
- `--technique, -t`: Technique to apply (required)
- `--config, -c`: Path to JSON config file
- `--params, -p`: JSON string with parameters
- `--model, -m`: Model to use (default: gpt-3.5-turbo)
- `--reference, -r`: Reference text for evaluation
- `--keywords, -k`: Comma-separated keywords for evaluation
- `--evaluate/--no-evaluate`: Enable/disable evaluation (default: enabled)

### Contributions

All contributions for the project are welcomed. To get started, please refer to the [Contribution Guidelines](./CONTRIBUTING.md).

### Project Structure

```
prompt-cookbook-cli/
├── cli.py                        # Main CLI interface
├── constants.py                  # Supported models configuration
├── utils.py                      # Core utility functions
├── prompt_engineering.py         # Prompt engineering techniques
├── evaluation.py                 # Evaluation metrics
├── models/
│   ├── prompt_log.py            # Data models for standard logging
│   └── prompt_engineering_log.py # Data models for prompt engineering logs
├── prompts/                      # JSON files containing prompt templates
│   ├── coding.json
│   └── summarization.json
├── examples/                     # Example configuration files
│   ├── single_shot_config.json
│   ├── meta_prompting_config.json
│   ├── chain_of_thought_config.json
│   └── few_shot_config.json
└── logs/                        # Experiment logs
    ├── prompt_runs.jsonl
    └── prompt_engineering_runs.jsonl
```

## Prompt Engineering Techniques

### Single-Shot Prompting
Provides one example to guide the model's response. Useful when you have a clear example of the desired input-output format.

**Required parameters:**
- `task_description`: Description of the task
- `example_input`: Example input
- `example_output`: Expected output for the example
- `actual_input`: The actual input to process

### Meta-Prompting
Uses prompts to generate or improve other prompts. Helps create optimized prompts for specific tasks.

**Required parameters:**
- `goal`: The main objective

**Optional parameters:**
- `context`: Additional background information
- `constraints`: Requirements or limitations
- `output_format`: Desired format for the output

### Chain-of-Thought Prompting
Encourages the model to show step-by-step reasoning, improving accuracy on complex tasks.

**Required parameters:**
- `task`: Description of the task
- `input_text`: The input to process

### Few-Shot Prompting
Provides multiple examples to guide the model, useful for pattern recognition and consistency.

**Required parameters:**
- `task_description`: Description of the task
- `examples`: List of dicts with 'input' and 'output' keys
- `actual_input`: The actual input to process

## Evaluation Metrics

The tool provides comprehensive evaluation metrics to assess prompt engineering outputs:

### BLEU Score
Measures n-gram overlap between candidate and reference text. Scores range from 0 to 1, with higher scores indicating better similarity.

### Word Overlap
Calculates the ratio of overlapping words between candidate and reference text.

### Length Metrics
Compares word counts and length ratios between candidate and reference outputs.

### Keyword Presence
Checks for the presence of important keywords in the generated output, useful for ensuring key concepts are covered.
