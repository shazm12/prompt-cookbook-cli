import json
import os
from groq import Groq
from dotenv import load_dotenv
from models.prompt_log import PromptLogger
import time

load_dotenv()


task_file_mapper ={
    "summarization": "prompts/summarization.json",
    "coding": "prompts/coding.json"
}


def get_prompt_by_type(task, type, input):
    with open(task_file_mapper[task], "r") as f:
        prompts = json.load(f)
        prompt = next((p for p in prompts if p["type"] == type), None)
        if prompt is None:
            raise ValueError(f"Prompt type {type} not found for task {task}")
        prompt["prompt"] = prompt["prompt"].format(input=input)
        return prompt

def run_prompt(prompt, model):
    inferences = run_groq_inference(prompt, model)
    return inferences



def run_groq_inference(prompt, model):
    start_time = time.time()
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    completion = groq_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_completion_tokens=8192,
        stream=False        
    )
    end_time = time.time()
    
    if completion.choices[0].message.content is not None:
        return completion.choices[0].message.content, calculate_latency(start_time, end_time)
    else:
        raise ValueError("No response from the model")


def calculate_latency(start_time, end_time):
    return (end_time - start_time) * 1000



def create_prompt_log(command, name, prompt, task, type, input, model, output, latency, status):
    prompt_log = PromptLogger(
        command=command,
        name=name,
        prompt=prompt,
        task=task,
        type=type,
        input=input,
        model=model,
        output=output,
        latency_ms=latency,
        status=status
    )
    return prompt_log


def log_prompt_run(prompt_log):
    status = "success"
    try:
        with open("logs/prompt_runs.jsonl", "a", encoding="utf-8") as f:
            f.write(prompt_log.model_dump_json() + "\n")
        return status, "Prompt run logged successfully"
    except Exception as e:
        status = "error"
        return status, e