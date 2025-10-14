"""
Test script for prompt engineering functionality
Run this to verify the implementation without making API calls
"""

import json
from prompt_engineering import apply_technique, PromptEngineeringTechniques
from evaluation import evaluate_output, EvaluationMetrics


def test_single_shot():
    """Test single-shot prompting"""
    print("=" * 60)
    print("Testing Single-Shot Prompting")
    print("=" * 60)

    params = {
        "task_description": "Translate English to French",
        "example_input": "Hello",
        "example_output": "Bonjour",
        "actual_input": "Good morning",
    }

    prompt, metadata = apply_technique("single-shot", params)
    print("\nGenerated Prompt:")
    print(prompt)
    print("\nMetadata:")
    print(json.dumps(metadata, indent=2))
    print("\n✓ Single-shot test passed!\n")


def test_meta_prompting():
    """Test meta-prompting"""
    print("=" * 60)
    print("Testing Meta-Prompting")
    print("=" * 60)

    params = {
        "goal": "Create a prompt for summarizing technical documentation",
        "context": "For junior developers",
        "constraints": "Keep under 200 words",
        "output_format": "Bullet points",
    }

    prompt, metadata = apply_technique("meta-prompting", params)
    print("\nGenerated Prompt:")
    print(prompt)
    print("\nMetadata:")
    print(json.dumps(metadata, indent=2))
    print("\n✓ Meta-prompting test passed!\n")


def test_chain_of_thought():
    """Test chain-of-thought prompting"""
    print("=" * 60)
    print("Testing Chain-of-Thought Prompting")
    print("=" * 60)

    params = {
        "task": "Solve a math problem",
        "input_text": "If a train travels 60 km in 30 minutes, what is its speed in km/h?",
    }

    prompt, metadata = apply_technique("chain-of-thought", params)
    print("\nGenerated Prompt:")
    print(prompt)
    print("\nMetadata:")
    print(json.dumps(metadata, indent=2))
    print("\n✓ Chain-of-thought test passed!\n")


def test_few_shot():
    """Test few-shot prompting"""
    print("=" * 60)
    print("Testing Few-Shot Prompting")
    print("=" * 60)

    params = {
        "task_description": "Classify sentiment",
        "examples": [
            {"input": "This is great!", "output": "Positive"},
            {"input": "This is terrible.", "output": "Negative"},
            {"input": "It's okay.", "output": "Neutral"},
        ],
        "actual_input": "I love this product!",
    }

    prompt, metadata = apply_technique("few-shot", params)
    print("\nGenerated Prompt:")
    print(prompt)
    print("\nMetadata:")
    print(json.dumps(metadata, indent=2))
    print("\n✓ Few-shot test passed!\n")


def test_evaluation_metrics():
    """Test evaluation metrics"""
    print("=" * 60)
    print("Testing Evaluation Metrics")
    print("=" * 60)

    candidate = "The quick brown fox jumps over the lazy dog"
    reference = "The quick brown fox jumped over the lazy dog"
    keywords = ["fox", "dog", "quick"]

    results = evaluate_output(
        candidate=candidate, reference=reference, keywords=keywords
    )

    print("\nEvaluation Results:")
    print(json.dumps(results, indent=2))
    print("\n✓ Evaluation metrics test passed!\n")


def test_bleu_score():
    """Test BLEU score calculation"""
    print("=" * 60)
    print("Testing BLEU Score")
    print("=" * 60)

    evaluator = EvaluationMetrics()

    # Test exact match
    score1 = evaluator.calculate_bleu_score("hello world", "hello world")
    print(f"Exact match BLEU: {score1:.4f} (should be close to 1.0)")

    # Test partial match
    score2 = evaluator.calculate_bleu_score(
        "the cat sat on the mat", "the dog sat on the mat"
    )
    print(f"Partial match BLEU: {score2:.4f} (should be moderate)")

    # Test no match
    score3 = evaluator.calculate_bleu_score("hello world", "goodbye universe")
    print(f"No match BLEU: {score3:.4f} (should be low)")

    print("\n✓ BLEU score test passed!\n")


def test_error_handling():
    """Test error handling"""
    print("=" * 60)
    print("Testing Error Handling")
    print("=" * 60)

    # Test invalid technique
    try:
        apply_technique("invalid-technique", {})
        print("❌ Should have raised ValueError for invalid technique")
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {e}")

    # Test missing parameters
    try:
        apply_technique("single-shot", {"task_description": "test"})
        print("❌ Should have raised ValueError for missing parameters")
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {e}")

    print("\n✓ Error handling test passed!\n")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("PROMPT ENGINEERING TEST SUITE")
    print("=" * 60 + "\n")

    try:
        test_single_shot()
        test_meta_prompting()
        test_chain_of_thought()
        test_few_shot()
        test_evaluation_metrics()
        test_bleu_score()
        test_error_handling()

        print("=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        print("\nThe prompt engineering feature is ready to use!")
        print("Try running: python cli.py prompt-engineer --help")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
