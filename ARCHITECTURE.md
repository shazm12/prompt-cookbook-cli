# Prompt Engineering Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI Interface                            │
│                         (cli.py)                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ├─── prompt-engineer command
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌─────────────────┐            ┌──────────────────┐
│ Prompt          │            │  Evaluation      │
│ Engineering     │            │  Metrics         │
│ Module          │            │  Module          │
│                 │            │                  │
│ - Single-shot   │            │ - BLEU Score     │
│ - Meta-prompt   │            │ - Word Overlap   │
│ - Chain-of-     │            │ - Length Metrics │
│   thought       │            │ - Keyword Check  │
│ - Few-shot      │            │                  │
└────────┬────────┘            └────────┬─────────┘
         │                              │
         │                              │
         ▼                              ▼
┌─────────────────────────────────────────────────────────┐
│                    AI Model Provider                     │
│                  (OpenAI / Groq)                        │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    Logging System                        │
│            (logs/prompt_engineering_runs.jsonl)         │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Input Flow

```
User Command
    │
    ├─ Technique Selection (--technique)
    ├─ Parameters (--config or --params)
    ├─ Model Selection (--model)
    ├─ Evaluation Options (--reference, --keywords)
    │
    ▼
Parameter Validation
    │
    ├─ Check required parameters
    ├─ Validate JSON format
    ├─ Verify technique exists
    │
    ▼
Technique Application
    │
    ├─ Load technique class
    ├─ Generate optimized prompt
    ├─ Create metadata
    │
    ▼
Model Execution
    │
    ├─ Send prompt to AI model
    ├─ Track latency
    ├─ Capture response
    │
    ▼
Evaluation (if enabled)
    │
    ├─ Calculate metrics
    ├─ Compare with reference
    ├─ Check keywords
    ├─ Generate report
    │
    ▼
Logging & Display
    │
    ├─ Save to JSONL
    ├─ Display results
    └─ Show evaluation report
```

## Module Architecture

### prompt_engineering.py

```
PromptEngineeringTechniques (Class)
│
├─ single_shot_prompting()
│  └─ Returns: Formatted prompt with 1 example
│
├─ meta_prompting()
│  └─ Returns: Prompt for generating prompts
│
├─ chain_of_thought_prompting()
│  └─ Returns: Prompt encouraging reasoning
│
└─ few_shot_prompting()
   └─ Returns: Formatted prompt with N examples

apply_technique() (Function)
│
├─ Validates parameters
├─ Calls appropriate technique method
├─ Generates metadata
└─ Returns: (prompt, metadata)

load_technique_config() (Function)
└─ Loads JSON configuration files
```

### evaluation.py

```
EvaluationMetrics (Class)
│
├─ calculate_bleu_score()
│  └─ N-gram precision measurement
│
├─ calculate_word_overlap()
│  └─ Set intersection ratio
│
├─ calculate_length_metrics()
│  └─ Word count comparison
│
├─ calculate_keyword_presence()
│  └─ Keyword coverage analysis
│
└─ calculate_sentence_count()
   └─ Sentence structure analysis

evaluate_output() (Function)
│
├─ Runs selected metrics
├─ Aggregates results
└─ Returns: Evaluation dictionary

compare_techniques() (Function)
└─ Compares multiple technique results

generate_evaluation_report() (Function)
└─ Creates human-readable report
```

### cli.py - prompt_engineer command

```
@cli.command()
│
├─ Parse arguments
│  ├─ --technique (required)
│  ├─ --config (optional)
│  ├─ --params (optional)
│  ├─ --model (default: gpt-3.5-turbo)
│  ├─ --reference (optional)
│  ├─ --keywords (optional)
│  └─ --evaluate (default: True)
│
├─ Load parameters
│  ├─ From config file, OR
│  └─ From inline JSON
│
├─ Apply technique
│  └─ Call apply_technique()
│
├─ Run prompt
│  └─ Call run_prompt()
│
├─ Evaluate (if enabled)
│  ├─ Call evaluate_output()
│  └─ Generate report
│
└─ Log experiment
   └─ Save to JSONL
```

## Data Models

### PromptEngineeringLog

```python
{
    "timestamp": "ISO 8601 datetime",
    "technique": "single-shot | meta-prompting | chain-of-thought | few-shot",
    "prompt": "Generated prompt text",
    "model": "Model identifier",
    "output": "Model response",
    "latency_ms": 1234.56,
    "status": "success | error",
    "metadata": {
        "technique": "...",
        "has_example": true,
        ...
    },
    "evaluation_metrics": {
        "bleu_score": 0.85,
        "word_overlap": 0.92,
        ...
    },
    "reference_text": "Optional reference",
    "keywords": ["keyword1", "keyword2"]
}
```

## Configuration Schema

### Single-Shot Config
```json
{
  "task_description": "string (required)",
  "example_input": "string (required)",
  "example_output": "string (required)",
  "actual_input": "string (required)"
}
```

### Meta-Prompting Config
```json
{
  "goal": "string (required)",
  "context": "string (optional)",
  "constraints": "string (optional)",
  "output_format": "string (optional)"
}
```

### Chain-of-Thought Config
```json
{
  "task": "string (required)",
  "input_text": "string (required)"
}
```

### Few-Shot Config
```json
{
  "task_description": "string (required)",
  "examples": [
    {
      "input": "string",
      "output": "string"
    }
  ],
  "actual_input": "string (required)"
}
```

## Error Handling

```
User Input
    │
    ▼
┌─────────────────┐
│ Validation      │
│ - JSON format   │
│ - Required params│
│ - Technique name│
└────┬────────────┘
     │
     ├─ Valid ──────────────────────────────┐
     │                                       │
     └─ Invalid ──> Error Message ──> Exit  │
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │ Technique Apply │
                                    └────┬────────────┘
                                         │
                                         ├─ Success ──────────────┐
                                         │                         │
                                         └─ Error ──> Log ──> Exit │
                                                                   │
                                                                   ▼
                                                          ┌─────────────────┐
                                                          │ Model Execution │
                                                          └────┬────────────┘
                                                               │
                                                               ├─ Success ──> Continue
                                                               │
                                                               └─ Error ──> Log ──> Display
```

## Performance Considerations

### Optimization Points

1. **BLEU Score Calculation**
   - Complexity: O(n*m) where n=candidate length, m=reference length
   - Optimization: Cache n-grams for repeated calculations

2. **Model API Calls**
   - Latency: 500ms - 5000ms depending on model
   - Optimization: Async execution for batch processing

3. **Evaluation Metrics**
   - Complexity: O(n) for most metrics
   - Optimization: Parallel metric calculation

4. **Logging**
   - I/O operation: ~1-10ms
   - Optimization: Async file writes

## Extension Points

### Adding New Techniques

1. Implement method in `PromptEngineeringTechniques`
2. Add case in `apply_technique()`
3. Update CLI choices
4. Create example config
5. Add tests
6. Update docs

### Adding New Metrics

1. Implement method in `EvaluationMetrics`
2. Add to `evaluate_output()`
3. Update report generation
4. Add tests
5. Update docs

### Adding New Models

1. Add to `constants.py`
2. Implement inference function in `utils.py`
3. Update model selection logic
4. Test with all techniques

## Security Considerations

1. **Input Validation**
   - JSON parsing with error handling
   - Parameter type checking
   - File path validation

2. **API Key Management**
   - Environment variables only
   - Never logged or displayed
   - Secure storage recommendations

3. **Output Sanitization**
   - No code execution from model outputs
   - Safe file writing
   - Path traversal prevention

## Testing Strategy

```
Unit Tests
├─ Technique generation
├─ Metric calculation
├─ Parameter validation
└─ Error handling

Integration Tests
├─ CLI command execution
├─ Config file loading
└─ End-to-end workflows

Performance Tests
├─ Large input handling
├─ Batch processing
└─ Memory usage
```

## Deployment Considerations

1. **Dependencies**
   - Python 3.8+
   - Required packages in requirements.txt
   - API keys for providers

2. **Environment Setup**
   - Virtual environment recommended
   - .env file for configuration
   - Log directory creation

3. **Monitoring**
   - JSONL logs for analysis
   - Latency tracking
   - Error rate monitoring

## Future Architecture Enhancements

1. **Plugin System**
   - Dynamic technique loading
   - Custom metric plugins
   - Provider plugins

2. **Caching Layer**
   - Prompt caching
   - Result caching
   - Evaluation caching

3. **Web Interface**
   - REST API
   - Web dashboard
   - Real-time monitoring

4. **Database Integration**
   - Structured storage
   - Query capabilities
   - Analytics support
