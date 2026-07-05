# llama3_1_client.py
"""Wrapper for locally hosted LLM via ollama.
Requires ollama to be running locally on http://localhost:11434
Model: llama3.1
"""
import requests
from prompt_template import PROMPT

def get_score(scale: str, question: str, reference: str, candidate: str, reference_grade: int) -> str:
    """Build the prompt and call ollama (llama3.1), returning the raw response string.
    """
    ollama_endpoint = "http://192.168.1.9:11434/api/generate"
    model_name = "llama3.1:8b"
    
    prompt = PROMPT.format(
        scale=scale,    
        question=question, 
        reference=reference, 
        reference_grade=reference_grade, 
        candidate=candidate
    )
    
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "temperature": 0,
        "verbose": False,
    }
    
    try:
        response = requests.post(ollama_endpoint, json=payload, timeout=240)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"Cannot connect to ollama at {ollama_endpoint}. Ensure ollama is running and accessible.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error calling ollama: {str(e)}")
