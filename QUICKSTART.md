# Quick Start Guide - Prompt Engineering Feature

## Installation

1. **Install dependencies** (if not already done):
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

## Test the Implementation

Run the test suite to verify everything works:
```bash
python3 test_prompt_engineering.py
```

You should see all tests pass with ✓ marks.

## Try Your First Prompt Engineering Command

### Example 1: Single-Shot Prompting (Translation)

```bash
python3 cli.py prompt-engineer \
  --technique single-shot \
  --config examples/single_shot_config.json \
  --model gpt-4o
```

### Example 2: Meta-Prompting (Generate a Prompt)

```bash
python3 cli.py prompt-engineer \
  --technique meta-prompting \
  --config examples/meta_prompting_config.json
```

### Example 3: With Evaluation Metrics

```bash
python3 cli.py prompt-engineer \
  --technique single-shot \
  --config examples/single_shot_config.json \
  --reference "Bonjour, passez une excellente journée!" \
  --keywords "Bonjour,journée,excellente"
```

### Example 4: Using Inline Parameters

```bash
python3 cli.py prompt-engineer \
  -t single-shot \
  -p '{"task_description": "Translate to Spanish", "example_input": "Hello", "example_output": "Hola", "actual_input": "Good morning"}' \
  -m gpt-4o
```

## View Available Commands

```bash
# See all CLI commands
python3 cli.py --help

# See prompt-engineer specific help
python3 cli.py prompt-engineer --help
```

## What You'll See

When you run a prompt engineering command, you'll see:

1. **Generated Prompt** - The optimized prompt created by the technique
2. **Model Output** - The response from the AI model
3. **Evaluation Report** - Metrics assessing the output quality (if enabled)
4. **Logs** - Experiment logged to `logs/prompt_engineering_runs.jsonl`

## Next Steps

- Read the full [Prompt Engineering Guide](./PROMPT_ENGINEERING_GUIDE.md)
- Explore the example configurations in `examples/`
- Create your own configuration files
- Experiment with different techniques and models
- Compare results across techniques

## Troubleshooting

**Issue**: Module not found errors
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: API key errors
- **Solution**: Set up your `.env` file with valid API keys

**Issue**: Need help with parameters
- **Solution**: Check the example config files in `examples/` directory

## Example Output

Here's what a successful run looks like:

```
                    Prompt Engineering Lab

Applying technique: single-shot
Using model: gpt-4o

╭─────────────── Generated Prompt ───────────────╮
│ Task: Translate English to French              │
│                                                 │
│ Example:                                        │
│ Input: Hello                                    │
│ Output: Bonjour                                 │
│                                                 │
│ Now, apply the same approach to the following: │
│ Input: Good morning                             │
│ Output:                                         │
╰─────────────────────────────────────────────────╯

Running prompt with model...

╭──────────────── Model Output ──────────────────╮
│ Bonjour                                         │
╰─────────────────────────────────────────────────╯

Latency: 1234.56ms

Evaluating output...

╭────────────── Evaluation Report ───────────────╮
│ BLEU Score: 0.8523                              │
│ Word Overlap: 92%                               │
│ Keyword Coverage: 100%                          │
╰─────────────────────────────────────────────────╯

Logging experiment...
Prompt engineering run logged successfully

✓ Prompt engineering experiment completed!
```

## Support

For detailed documentation, see:
- [README.md](./README.md) - Main documentation
- [PROMPT_ENGINEERING_GUIDE.md](./PROMPT_ENGINEERING_GUIDE.md) - Comprehensive guide
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Contribution guidelines
