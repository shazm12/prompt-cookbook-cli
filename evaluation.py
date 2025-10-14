"""
Evaluation Metrics Module

This module provides evaluation metrics for prompt engineering outputs:
- BLEU score: Measures similarity to reference text
- Semantic similarity: Measures meaning similarity
- Length metrics: Compares output length characteristics
- Custom metrics: Task-specific evaluation
"""

from typing import Dict, Any, Optional, List
import re
from collections import Counter
import math


class EvaluationMetrics:
    """Evaluation metrics for prompt engineering outputs"""

    @staticmethod
    def calculate_bleu_score(
        candidate: str, reference: str, n_gram: int = 4
    ) -> float:
        """
        Calculate BLEU score between candidate and reference text.
        Simplified implementation for n-gram precision.

        Args:
            candidate: Generated output text
            reference: Reference/expected text
            n_gram: Maximum n-gram size (default: 4)

        Returns:
            BLEU score between 0 and 1
        """

        def get_ngrams(text: str, n: int) -> List[tuple]:
            words = text.lower().split()
            return [tuple(words[i : i + n]) for i in range(len(words) - n + 1)]

        candidate_words = candidate.lower().split()
        reference_words = reference.lower().split()

        if not candidate_words or not reference_words:
            return 0.0

        # Calculate precision for each n-gram size
        precisions = []
        for n in range(1, min(n_gram + 1, len(candidate_words) + 1)):
            candidate_ngrams = Counter(get_ngrams(candidate, n))
            reference_ngrams = Counter(get_ngrams(reference, n))

            if not candidate_ngrams:
                precisions.append(0.0)
                continue

            # Count matching n-grams
            matches = sum(
                min(candidate_ngrams[ngram], reference_ngrams[ngram])
                for ngram in candidate_ngrams
            )
            total = sum(candidate_ngrams.values())

            precisions.append(matches / total if total > 0 else 0.0)

        if not precisions or all(p == 0 for p in precisions):
            return 0.0

        # Geometric mean of precisions
        log_precisions = [
            math.log(p) if p > 0 else float("-inf") for p in precisions
        ]
        if any(p == float("-inf") for p in log_precisions):
            return 0.0

        geo_mean = math.exp(sum(log_precisions) / len(log_precisions))

        # Brevity penalty
        bp = (
            1.0
            if len(candidate_words) >= len(reference_words)
            else math.exp(1 - len(reference_words) / len(candidate_words))
        )

        return bp * geo_mean

    @staticmethod
    def calculate_word_overlap(candidate: str, reference: str) -> float:
        """
        Calculate word overlap ratio between candidate and reference.

        Args:
            candidate: Generated output text
            reference: Reference/expected text

        Returns:
            Overlap ratio between 0 and 1
        """
        candidate_words = set(candidate.lower().split())
        reference_words = set(reference.lower().split())

        if not reference_words:
            return 0.0

        overlap = len(candidate_words & reference_words)
        return overlap / len(reference_words)

    @staticmethod
    def calculate_length_metrics(candidate: str, reference: str) -> Dict[str, Any]:
        """
        Calculate length-based metrics.

        Args:
            candidate: Generated output text
            reference: Reference/expected text

        Returns:
            Dictionary with length metrics
        """
        candidate_words = candidate.split()
        reference_words = reference.split()

        return {
            "candidate_length": len(candidate_words),
            "reference_length": len(reference_words),
            "length_ratio": (
                len(candidate_words) / len(reference_words)
                if reference_words
                else 0.0
            ),
            "length_difference": abs(len(candidate_words) - len(reference_words)),
        }

    @staticmethod
    def calculate_keyword_presence(candidate: str, keywords: List[str]) -> Dict[str, Any]:
        """
        Check presence of important keywords in the output.

        Args:
            candidate: Generated output text
            keywords: List of important keywords to check

        Returns:
            Dictionary with keyword metrics
        """
        candidate_lower = candidate.lower()
        present_keywords = [kw for kw in keywords if kw.lower() in candidate_lower]

        return {
            "total_keywords": len(keywords),
            "present_keywords": len(present_keywords),
            "keyword_coverage": (
                len(present_keywords) / len(keywords) if keywords else 0.0
            ),
            "missing_keywords": [
                kw for kw in keywords if kw.lower() not in candidate_lower
            ],
        }

    @staticmethod
    def calculate_sentence_count(text: str) -> int:
        """
        Count number of sentences in text.

        Args:
            text: Input text

        Returns:
            Number of sentences
        """
        # Simple sentence splitting on common punctuation
        sentences = re.split(r"[.!?]+", text)
        return len([s for s in sentences if s.strip()])


def evaluate_output(
    candidate: str,
    reference: Optional[str] = None,
    keywords: Optional[List[str]] = None,
    metrics: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Evaluate generated output using multiple metrics.

    Args:
        candidate: Generated output text
        reference: Optional reference text for comparison
        keywords: Optional list of important keywords
        metrics: Optional list of specific metrics to calculate
                (default: all available metrics)

    Returns:
        Dictionary containing evaluation results
    """
    evaluator = EvaluationMetrics()
    results = {
        "candidate_stats": {
            "word_count": len(candidate.split()),
            "char_count": len(candidate),
            "sentence_count": evaluator.calculate_sentence_count(candidate),
        }
    }

    # If no specific metrics requested, use all
    if metrics is None:
        metrics = ["bleu", "word_overlap", "length", "keywords"]

    # Reference-based metrics
    if reference:
        if "bleu" in metrics:
            results["bleu_score"] = evaluator.calculate_bleu_score(
                candidate, reference
            )

        if "word_overlap" in metrics:
            results["word_overlap"] = evaluator.calculate_word_overlap(
                candidate, reference
            )

        if "length" in metrics:
            results["length_metrics"] = evaluator.calculate_length_metrics(
                candidate, reference
            )

    # Keyword-based metrics
    if keywords and "keywords" in metrics:
        results["keyword_metrics"] = evaluator.calculate_keyword_presence(
            candidate, keywords
        )

    return results


def compare_techniques(
    results: List[Dict[str, Any]], metric: str = "bleu_score"
) -> Dict[str, Any]:
    """
    Compare results from different prompt engineering techniques.

    Args:
        results: List of evaluation results from different techniques
        metric: Metric to use for comparison (default: bleu_score)

    Returns:
        Comparison summary
    """
    if not results:
        return {"error": "No results to compare"}

    # Extract metric values
    metric_values = []
    for i, result in enumerate(results):
        if metric in result:
            metric_values.append(
                {
                    "index": i,
                    "technique": result.get("technique", f"technique_{i}"),
                    "value": result[metric],
                }
            )

    if not metric_values:
        return {"error": f"Metric '{metric}' not found in results"}

    # Sort by metric value
    sorted_results = sorted(metric_values, key=lambda x: x["value"], reverse=True)

    return {
        "metric": metric,
        "best_technique": sorted_results[0]["technique"],
        "best_value": sorted_results[0]["value"],
        "rankings": sorted_results,
        "average": sum(r["value"] for r in metric_values) / len(metric_values),
    }


def generate_evaluation_report(
    technique: str,
    prompt: str,
    output: str,
    evaluation_results: Dict[str, Any],
) -> str:
    """
    Generate a human-readable evaluation report.

    Args:
        technique: Prompt engineering technique used
        prompt: The prompt that was used
        output: The generated output
        evaluation_results: Evaluation metrics results

    Returns:
        Formatted report string
    """
    report_lines = [
        "=" * 60,
        "PROMPT ENGINEERING EVALUATION REPORT",
        "=" * 60,
        f"\nTechnique: {technique}",
        f"\nPrompt Length: {len(prompt)} characters",
        f"Output Length: {len(output)} characters",
        "\n" + "-" * 60,
        "EVALUATION METRICS",
        "-" * 60,
    ]

    # Add candidate stats
    if "candidate_stats" in evaluation_results:
        stats = evaluation_results["candidate_stats"]
        report_lines.extend(
            [
                "\nOutput Statistics:",
                f"  - Word Count: {stats['word_count']}",
                f"  - Character Count: {stats['char_count']}",
                f"  - Sentence Count: {stats['sentence_count']}",
            ]
        )

    # Add BLEU score
    if "bleu_score" in evaluation_results:
        score = evaluation_results["bleu_score"]
        report_lines.extend(
            [
                f"\nBLEU Score: {score:.4f}",
                f"  Quality: {'Excellent' if score > 0.7 else 'Good' if score > 0.5 else 'Fair' if score > 0.3 else 'Poor'}",
            ]
        )

    # Add word overlap
    if "word_overlap" in evaluation_results:
        overlap = evaluation_results["word_overlap"]
        report_lines.append(f"\nWord Overlap: {overlap:.2%}")

    # Add length metrics
    if "length_metrics" in evaluation_results:
        length = evaluation_results["length_metrics"]
        report_lines.extend(
            [
                "\nLength Comparison:",
                f"  - Candidate: {length['candidate_length']} words",
                f"  - Reference: {length['reference_length']} words",
                f"  - Ratio: {length['length_ratio']:.2f}",
            ]
        )

    # Add keyword metrics
    if "keyword_metrics" in evaluation_results:
        kw = evaluation_results["keyword_metrics"]
        report_lines.extend(
            [
                "\nKeyword Analysis:",
                f"  - Coverage: {kw['keyword_coverage']:.2%} ({kw['present_keywords']}/{kw['total_keywords']})",
            ]
        )
        if kw["missing_keywords"]:
            report_lines.append(
                f"  - Missing: {', '.join(kw['missing_keywords'])}"
            )

    report_lines.append("\n" + "=" * 60)

    return "\n".join(report_lines)
