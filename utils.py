import json

task_file_mapper ={
    "summarization": "prompts/summarization.json",
    "coding": "prompts/coding.json"
}


def get_prompt_by_type(task, type):
    with open(task_file_mapper[task], "r") as f:
        prompts = json.load(f)
        prompt = next((p for p in prompts if p["type"] == type), None)
        return prompt

