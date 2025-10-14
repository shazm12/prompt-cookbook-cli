"""
Prompt Engineering Techniques Module

This module implements various prompt engineering techniques:
- Single-shot prompting: Providing one example to guide the model
- Meta-prompting: Using prompts to generate or improve other prompts
"""

from typing import Dict, Any, Optional, Tuple
import json


class PromptEngineeringTechniques:
    """Base class for prompt engineering techniques"""

    @staticmethod
    def single_shot_prompting(
        task_description: str,
        example_input: str,
        example_output: str,
        actual_input: str,
    ) -> str:
        """
        Single-shot prompting: Provide one example to guide the model's response.

        Args:
            task_description: Description of the task to perform
            example_input: Example input for the task
            example_output: Expected output for the example input
            actual_input: The actual input to process

        Returns:
            Formatted prompt with single-shot example
        """
        prompt = f"""Task: {task_description}

Example:
Input: {example_input}
Output: {example_output}

Now, apply the same approach to the following:
Input: {actual_input}
Output:"""
        return prompt

    @staticmethod
    def meta_prompting(
        goal: str,
        context: Optional[str] = None,
        constraints: Optional[str] = None,
        output_format: Optional[str] = None,
    ) -> str:
        """
        Meta-prompting: Generate an optimized prompt for a specific task.

        Args:
            goal: The main objective of the prompt
            context: Additional context or background information
            constraints: Any constraints or requirements
            output_format: Desired format for the output

        Returns:
            Meta-prompt that can be used to generate or improve prompts
        """
        meta_prompt_parts = [
            "You are an expert prompt engineer. Generate an optimized prompt for the following task:",
            f"\nGoal: {goal}",
        ]

        if context:
            meta_prompt_parts.append(f"\nContext: {context}")

        if constraints:
            meta_prompt_parts.append(f"\nConstraints: {constraints}")

        if output_format:
            meta_prompt_parts.append(f"\nDesired Output Format: {output_format}")

        meta_prompt_parts.append(
            "\n\nGenerate a clear, effective prompt that will help achieve this goal. "
            "The prompt should be specific, actionable, and optimized for LLM understanding."
        )

        return "".join(meta_prompt_parts)

    @staticmethod
    def chain_of_thought_prompting(task: str, input_text: str) -> str:
        """
        Chain-of-thought prompting: Encourage step-by-step reasoning.

        Args:
            task: Description of the task
            input_text: The input to process

        Returns:
            Prompt that encourages step-by-step reasoning
        """
        prompt = f"""Task: {task}

Input: {input_text}

Please solve this step by step:
1. First, analyze the input and identify key components
2. Then, apply the necessary reasoning or transformations
3. Finally, provide the output with your reasoning

Let's work through this systematically:"""
        return prompt

    @staticmethod
    def few_shot_prompting(
        task_description: str,
        examples: list[Dict[str, str]],
        actual_input: str,
    ) -> str:
        """
        Few-shot prompting: Provide multiple examples to guide the model.

        Args:
            task_description: Description of the task
            examples: List of dicts with 'input' and 'output' keys
            actual_input: The actual input to process

        Returns:
            Formatted prompt with multiple examples
        """
        prompt_parts = [f"Task: {task_description}\n"]

        for i, example in enumerate(examples, 1):
            prompt_parts.append(f"\nExample {i}:")
            prompt_parts.append(f"\nInput: {example['input']}")
            prompt_parts.append(f"\nOutput: {example['output']}\n")

        prompt_parts.append(f"\nNow, apply the same approach to the following:")
        prompt_parts.append(f"\nInput: {actual_input}")
        prompt_parts.append("\nOutput:")

        return "".join(prompt_parts)


def apply_technique(
    technique: str, params: Dict[str, Any]
) -> Tuple[str, Dict[str, Any]]:
    """
    Apply a specific prompt engineering technique.

    Args:
        technique: Name of the technique to apply
        params: Parameters required for the technique

    Returns:
        Tuple of (generated_prompt, metadata)

    Raises:
        ValueError: If technique is not supported or params are invalid
    """
    techniques = PromptEngineeringTechniques()

    if technique == "single-shot":
        required_params = [
            "task_description",
            "example_input",
            "example_output",
            "actual_input",
        ]
        if not all(param in params for param in required_params):
            raise ValueError(
                f"Single-shot prompting requires: {', '.join(required_params)}"
            )

        prompt = techniques.single_shot_prompting(
            task_description=params["task_description"],
            example_input=params["example_input"],
            example_output=params["example_output"],
            actual_input=params["actual_input"],
        )

        metadata = {
            "technique": "single-shot",
            "task_description": params["task_description"],
            "has_example": True,
        }

    elif technique == "meta-prompting":
        if "goal" not in params:
            raise ValueError("Meta-prompting requires 'goal' parameter")

        prompt = techniques.meta_prompting(
            goal=params["goal"],
            context=params.get("context"),
            constraints=params.get("constraints"),
            output_format=params.get("output_format"),
        )

        metadata = {
            "technique": "meta-prompting",
            "goal": params["goal"],
            "has_context": "context" in params,
            "has_constraints": "constraints" in params,
        }

    elif technique == "chain-of-thought":
        required_params = ["task", "input_text"]
        if not all(param in params for param in required_params):
            raise ValueError(
                f"Chain-of-thought prompting requires: {', '.join(required_params)}"
            )

        prompt = techniques.chain_of_thought_prompting(
            task=params["task"], input_text=params["input_text"]
        )

        metadata = {"technique": "chain-of-thought", "task": params["task"]}

    elif technique == "few-shot":
        required_params = ["task_description", "examples", "actual_input"]
        if not all(param in params for param in required_params):
            raise ValueError(
                f"Few-shot prompting requires: {', '.join(required_params)}"
            )

        prompt = techniques.few_shot_prompting(
            task_description=params["task_description"],
            examples=params["examples"],
            actual_input=params["actual_input"],
        )

        metadata = {
            "technique": "few-shot",
            "task_description": params["task_description"],
            "num_examples": len(params["examples"]),
        }

    else:
        raise ValueError(
            f"Unsupported technique: {technique}. "
            f"Supported techniques: single-shot, meta-prompting, chain-of-thought, few-shot"
        )

    return prompt, metadata


def load_technique_config(config_file: str) -> Dict[str, Any]:
    """
    Load technique configuration from a JSON file.

    Args:
        config_file: Path to the configuration file

    Returns:
        Configuration dictionary
    """
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in configuration file: {config_file}")
