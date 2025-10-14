# Contributing to Prompt Engineering Features

Thank you for your interest in contributing to the Prompt Engineering features of the Prompt Cookbook CLI! This guide will help you get started.

## Quick Links

- [Main Contributing Guide](./CONTRIBUTING.md)
- [Prompt Engineering Guide](./PROMPT_ENGINEERING_GUIDE.md)
- [Implementation Summary](./IMPLEMENTATION_SUMMARY.md)

## Areas for Contribution

### 1. New Prompt Engineering Techniques

We currently support:
- Single-shot prompting
- Meta-prompting
- Chain-of-thought prompting
- Few-shot prompting

**Ideas for new techniques:**
- Zero-shot prompting
- Role-based prompting
- Instruction-following optimization
- Self-consistency prompting
- Tree-of-thought prompting
- Prompt chaining
- Retrieval-augmented prompting

**How to add a new technique:**

1. Add the technique method to `PromptEngineeringTechniques` class in `prompt_engineering.py`:

```python
@staticmethod
def your_technique_name(param1: str, param2: str) -> str:
    """
    Description of your technique.
    
    Args:
        param1: Description
        param2: Description
        
    Returns:
        Formatted prompt
    """
    prompt = f"Your prompt template using {param1} and {param2}"
    return prompt
```

2. Add handling in the `apply_technique()` function:

```python
elif technique == "your-technique-name":
    required_params = ["param1", "param2"]
    if not all(param in params for param in required_params):
        raise ValueError(f"Your technique requires: {', '.join(required_params)}")
    
    prompt = techniques.your_technique_name(
        param1=params["param1"],
        param2=params["param2"]
    )
    
    metadata = {
        "technique": "your-technique-name",
        "param1": params["param1"]
    }
```

3. Update the CLI command choices in `cli.py`:

```python
type=click.Choice([
    "single-shot", 
    "meta-prompting", 
    "chain-of-thought", 
    "few-shot",
    "your-technique-name"  # Add here
], case_sensitive=False)
```

4. Create an example config file in `examples/your_technique_config.json`

5. Add tests in `test_prompt_engineering.py`

6. Update documentation in `PROMPT_ENGINEERING_GUIDE.md`

### 2. New Evaluation Metrics

Current metrics:
- BLEU score
- Word overlap
- Length metrics
- Keyword presence

**Ideas for new metrics:**
- Semantic similarity using embeddings
- Perplexity scores
- Coherence metrics
- Task-specific metrics (e.g., code correctness, factual accuracy)
- Readability scores
- Toxicity/safety checks

**How to add a new metric:**

1. Add method to `EvaluationMetrics` class in `evaluation.py`:

```python
@staticmethod
def calculate_your_metric(candidate: str, reference: str) -> float:
    """
    Calculate your custom metric.
    
    Args:
        candidate: Generated output
        reference: Reference text
        
    Returns:
        Metric score
    """
    # Your implementation
    return score
```

2. Update `evaluate_output()` function to include your metric:

```python
if "your_metric" in metrics:
    results["your_metric"] = evaluator.calculate_your_metric(
        candidate, reference
    )
```

3. Update `generate_evaluation_report()` to display your metric

4. Add tests for your metric

5. Document in `PROMPT_ENGINEERING_GUIDE.md`

### 3. Example Configurations

**What makes a good example:**
- Real-world use case
- Clear, well-commented parameters
- Demonstrates best practices
- Includes expected output (as comment)

**Example template:**

```json
{
  "_comment": "Brief description of what this example demonstrates",
  "task_description": "Clear task description",
  "example_input": "Representative input",
  "example_output": "Expected output",
  "actual_input": "Input to process",
  "_expected_result": "What you expect to get (for documentation)"
}
```

**Suggested domains:**
- Code generation/review
- Data extraction
- Creative writing
- Technical documentation
- Customer support
- Educational content
- Scientific analysis

### 4. Documentation Improvements

**Areas needing documentation:**
- More use case examples
- Comparison guides (when to use which technique)
- Performance benchmarks
- Integration guides
- Video tutorials
- Blog posts

**Documentation standards:**
- Clear, concise language
- Code examples that work
- Screenshots where helpful
- Links to relevant resources

### 5. Testing

**What we need:**
- Unit tests for new techniques
- Integration tests for CLI commands
- Performance tests
- Edge case handling
- Error message validation

**Testing template:**

```python
def test_your_feature():
    """Test description"""
    print("=" * 60)
    print("Testing Your Feature")
    print("=" * 60)
    
    # Setup
    params = {...}
    
    # Execute
    result = your_function(params)
    
    # Verify
    assert result is not None
    print("\n✓ Test passed!\n")
```

### 6. Performance Optimization

**Areas for optimization:**
- BLEU score calculation for long texts
- Batch processing support
- Caching mechanisms
- Parallel evaluation
- Memory efficiency

### 7. UI/UX Improvements

**Ideas:**
- Interactive mode for parameter input
- Progress bars for long operations
- Better error messages
- Color schemes
- Export formats (PDF, HTML)
- Comparison visualizations

## Contribution Workflow

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add tests
   - Update documentation

4. **Test your changes**
   ```bash
   python3 test_prompt_engineering.py
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: Your feature description"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style Guidelines

### Python Code
- Follow PEP 8
- Use type hints
- Write docstrings for all functions
- Keep functions focused and small
- Use meaningful variable names

### Example:
```python
def calculate_metric(
    candidate: str, 
    reference: str, 
    threshold: float = 0.5
) -> Dict[str, Any]:
    """
    Calculate a custom evaluation metric.
    
    Args:
        candidate: The generated text to evaluate
        reference: The reference text for comparison
        threshold: Minimum score threshold (default: 0.5)
        
    Returns:
        Dictionary containing metric results
        
    Raises:
        ValueError: If inputs are empty
    """
    if not candidate or not reference:
        raise ValueError("Inputs cannot be empty")
    
    # Implementation
    score = compute_score(candidate, reference)
    
    return {
        "score": score,
        "passed": score >= threshold
    }
```

### JSON Configurations
- Use clear, descriptive keys
- Include comments (as `_comment` keys)
- Format consistently (2-space indent)
- Validate JSON syntax

### Documentation
- Use Markdown formatting
- Include code examples
- Add table of contents for long docs
- Link to related resources

## Testing Requirements

All contributions should include:

1. **Unit tests** for new functions
2. **Integration tests** for CLI commands
3. **Example configurations** that work
4. **Documentation** updates

Run tests before submitting:
```bash
python3 test_prompt_engineering.py
```

## Review Process

1. Automated tests must pass
2. Code review by maintainers
3. Documentation review
4. Testing on different platforms
5. Merge when approved

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Ideas**: Open a GitHub Issue with "enhancement" label
- **Urgent**: Tag maintainers in your PR

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Thank You!

Every contribution, no matter how small, helps make this tool better for everyone. We appreciate your time and effort!

---

**Happy Contributing! 🚀**
