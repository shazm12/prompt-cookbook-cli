# Prompt Cookbook CLI

A CLI tool for running and managing AI prompts across different tasks and models. It offers a collection of pre-built prompts, curated from various sources and tested for common tasks such as summarization and coding. The tool supports multiple AI providers, including OpenAI and Groq.

## Features

- **Pre-built Prompts**: Curated collection of prompts for summarization and coding tasks
- **Multi-Provider Support**: Works with OpenAI and Groq models
- **Task Management**: Organize prompts by task type (summarization, coding)
- **Logging**: Track prompt runs with performance metrics and results
- **CLI Interface**: Easy-to-use command-line interface with rich output

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

### Project Structure

```
prompt-cookbook/
├── cli.py              # Main CLI interface
├── constants.py        # Supported models configuration
├── utils.py           # Core utility functions
├── models/
│   └── prompt_log.py  # Data models for logging
├── prompts/           # JSON files containing prompt templates
│   ├── coding.json
│   └── summarization.json
└── logs/             # Prompt run logs
    └── prompt_runs.jsonl
```
