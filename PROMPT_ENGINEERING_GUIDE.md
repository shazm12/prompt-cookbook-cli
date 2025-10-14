# Prompt Engineering Guide

This guide provides detailed information about using the prompt engineering features in the Prompt Cookbook CLI.

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [Techniques](#techniques)
- [Evaluation Metrics](#evaluation-metrics)
- [Best Practices](#best-practices)
- [Examples](#examples)

## Overview

Prompt engineering is the practice of designing and optimizing prompts to get better results from language models. This CLI tool provides four powerful techniques:

1. **Single-Shot Prompting**: Learn from one example
2. **Meta-Prompting**: Generate optimized prompts
3. **Chain-of-Thought**: Encourage step-by-step reasoning
4. **Few-Shot Prompting**: Learn from multiple examples

## Getting Started

### Basic Command Structure

```bash
python cli.py prompt-engineer --technique <TECHNIQUE> --config <CONFIG_FILE> [OPTIONS]
```

### Quick Start Example

```bash
# Try single-shot prompting with the provided example
python cli.py prompt-engineer -t single-shot -c examples/single_shot_config.json
```

## Techniques

### 1. Single-Shot Prompting

**When to use:**
- You have one clear example of the desired behavior
- The task is straightforward and can be demonstrated with a single example
- You want to establish a pattern quickly

**Configuration format:**
```json
{
  "task_description": "Translate English to French",
  "example_input": "Hello",
  "example_output": "Bonjour",
  "actual_input": "Good morning"
}
```

**Example command:**
```bash
python cli.py prompt-engineer -t single-shot -c examples/single_shot_config.json -m gpt-4o
```

**Use cases:**
- Translation tasks
- Format conversion
- Simple classification
- Style transformation

---

### 2. Meta-Prompting

**When to use:**
- You need to create a prompt for a complex task
- You want to optimize an existing prompt
- You need to ensure the prompt follows specific guidelines

**Configuration format:**
```json
{
  "goal": "Create a prompt for summarizing technical documentation",
  "context": "For junior developers with less than 1 year experience",
  "constraints": "Keep under 200 words, use simple language",
  "output_format": "Bullet points with clear sections"
}
```

**Example command:**
```bash
python cli.py prompt-engineer -t meta-prompting -c examples/meta_prompting_config.json
```

**Use cases:**
- Creating prompts for new tasks
- Optimizing existing prompts
- Establishing prompt templates
- Documenting prompt requirements

---

### 3. Chain-of-Thought Prompting

**When to use:**
- The task requires reasoning or multiple steps
- You want to see the model's thought process
- Accuracy is more important than brevity

**Configuration format:**
```json
{
  "task": "Solve a mathematical word problem",
  "input_text": "A store has 120 apples. They sell 35% in the morning and 20% of the remaining in the afternoon. How many are left?"
}
```

**Example command:**
```bash
python cli.py prompt-engineer -t chain-of-thought -c examples/chain_of_thought_config.json
```

**Use cases:**
- Mathematical problems
- Logical reasoning
- Multi-step analysis
- Debugging code
- Complex decision-making

---

### 4. Few-Shot Prompting

**When to use:**
- You have multiple examples showing the pattern
- The task requires consistency across varied inputs
- Single-shot isn't providing enough guidance

**Configuration format:**
```json
{
  "task_description": "Classify customer feedback sentiment",
  "examples": [
    {
      "input": "The product is amazing!",
      "output": "Positive"
    },
    {
      "input": "Terrible quality, very disappointed.",
      "output": "Negative"
    },
    {
      "input": "It's okay, nothing special.",
      "output": "Neutral"
    }
  ],
  "actual_input": "Great value for money, though shipping took longer than expected."
}
```

**Example command:**
```bash
python cli.py prompt-engineer -t few-shot -c examples/few_shot_config.json
```

**Use cases:**
- Sentiment analysis
- Text classification
- Pattern recognition
- Consistent formatting
- Complex categorization

## Evaluation Metrics

### Enabling Evaluation

Add evaluation parameters to your command:

```bash
python cli.py prompt-engineer \
  -t single-shot \
  -c examples/single_shot_config.json \
  -r "Expected reference output" \
  -k "keyword1,keyword2,keyword3"
```

### Available Metrics

#### 1. BLEU Score
- **Range**: 0.0 to 1.0
- **Interpretation**:
  - 0.7+: Excellent similarity
  - 0.5-0.7: Good similarity
  - 0.3-0.5: Fair similarity
  - <0.3: Poor similarity

#### 2. Word Overlap
- Percentage of reference words present in the output
- Useful for checking coverage of key terms

#### 3. Length Metrics
- Word count comparison
- Length ratio (candidate/reference)
- Helps ensure appropriate output length

#### 4. Keyword Presence
- Tracks presence of important keywords
- Shows coverage percentage
- Lists missing keywords

### Evaluation Report

The tool generates a comprehensive evaluation report showing:
- Output statistics (word count, character count, sentence count)
- BLEU score with quality assessment
- Word overlap percentage
- Length comparison
- Keyword analysis

## Best Practices

### 1. Choosing the Right Technique

| Task Type | Recommended Technique | Why |
|-----------|----------------------|-----|
| Simple transformations | Single-shot | One example is sufficient |
| Creating new prompts | Meta-prompting | Optimizes for specific goals |
| Complex reasoning | Chain-of-thought | Shows step-by-step logic |
| Pattern learning | Few-shot | Multiple examples establish pattern |

### 2. Writing Effective Examples

**For Single-Shot and Few-Shot:**
- Use clear, representative examples
- Ensure examples match your actual use case
- Keep examples concise but complete
- Show the exact format you want

**For Meta-Prompting:**
- Be specific about your goal
- Provide relevant context
- List all constraints clearly
- Specify the desired output format

### 3. Evaluation Best Practices

- Always provide reference text when possible
- Include relevant keywords for your domain
- Use multiple metrics for comprehensive assessment
- Compare results across different techniques

### 4. Iterative Improvement

1. Start with a basic configuration
2. Run the prompt and evaluate
3. Analyze the evaluation metrics
4. Adjust parameters based on results
5. Re-run and compare

## Examples

### Example 1: Translation Task

```bash
# Single-shot prompting for translation
python cli.py prompt-engineer \
  -t single-shot \
  -p '{"task_description": "Translate English to Spanish", "example_input": "Good morning", "example_output": "Buenos días", "actual_input": "Have a great day"}' \
  -m gpt-4o \
  -r "Que tengas un gran día" \
  -k "día,gran"
```

### Example 2: Code Review

```bash
# Few-shot prompting for code review
python cli.py prompt-engineer \
  -t few-shot \
  -c examples/code_review_config.json \
  -m gpt-4o \
  --evaluate
```

### Example 3: Creating a Summarization Prompt

```bash
# Meta-prompting to create a summarization prompt
python cli.py prompt-engineer \
  -t meta-prompting \
  -p '{"goal": "Summarize research papers", "context": "For academic audiences", "constraints": "Include methodology and findings", "output_format": "Structured abstract"}' \
  -m gpt-4o
```

### Example 4: Math Problem Solving

```bash
# Chain-of-thought for reasoning
python cli.py prompt-engineer \
  -t chain-of-thought \
  -p '{"task": "Calculate compound interest", "input_text": "Principal: $1000, Rate: 5% annual, Time: 3 years, Compounded quarterly"}' \
  -m gpt-4o
```

## Troubleshooting

### Common Issues

**Issue**: "Either --config or --params must be provided"
- **Solution**: Provide either a config file with `-c` or inline parameters with `-p`

**Issue**: "Invalid JSON"
- **Solution**: Ensure your JSON is properly formatted. Use a JSON validator or config file instead of inline parameters

**Issue**: Low BLEU scores
- **Solution**: Check if reference text matches the expected output format. BLEU is sensitive to exact wording.

**Issue**: Missing keywords in output
- **Solution**: Try few-shot prompting with examples that include the keywords, or adjust your prompt to emphasize those terms

## Advanced Usage

### Comparing Techniques

Run the same task with different techniques and compare results:

```bash
# Single-shot
python cli.py prompt-engineer -t single-shot -c config.json -r "reference" > single_shot_result.txt

# Few-shot
python cli.py prompt-engineer -t few-shot -c config.json -r "reference" > few_shot_result.txt

# Compare the evaluation metrics
```

### Custom Evaluation

For specialized evaluation needs, you can:
1. Run without evaluation: `--no-evaluate`
2. Access the logs in `logs/prompt_engineering_runs.jsonl`
3. Implement custom analysis scripts

### Batch Processing

Create multiple config files and process them in sequence:

```bash
for config in examples/*.json; do
  echo "Processing $config"
  python cli.py prompt-engineer -t single-shot -c "$config"
done
```

## Contributing

We welcome contributions to improve prompt engineering techniques! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Ideas for Contributions

- New prompt engineering techniques
- Additional evaluation metrics
- Example configurations for specific domains
- Performance optimizations
- Documentation improvements

## Resources

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Prompt Engineering Papers](https://github.com/dair-ai/Prompt-Engineering-Guide)

## License

This project is open source. See [LICENSE](./LICENSE) for details.
