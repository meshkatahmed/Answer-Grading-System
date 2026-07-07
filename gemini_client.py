# gemini_client.py
"""Simple wrapper around google-generativeai for the grading prompt.
Requires the environment variable GEMINI_API_KEY to be set.
"""
import os
from google import genai  # Updated import for new SDK
from prompt_templates.prompt_template import PROMPT

def get_score(scale: str, question: str, reference: str, candidate: str, reference_grade: int) -> str:
    """Build the prompt and call Gemini, returning the raw response string.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY environment variable not set.")
    # Initialize the GenAI client with the API key
    client = genai.Client(api_key=api_key)
    # Choose a suitable model (e.g., Gemini 1.5 Flash)
    model_name = "gemini-2.5-flash"
    prompt = PROMPT.format(scale=scale, question=question, reference=reference, reference_grade=reference_grade, candidate=candidate)
    # Generate content using the client
    response = client.models.generate_content(model=model_name, contents=prompt)
    return response.text
