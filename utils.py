# utils.py
"""Utility helpers for the Answer Grading CLI.
- load_bank: dynamically import a department bank module and return questions/answers.
- parse_score: extract the first numeric score from Gemini's response.
"""
import importlib.util
import os
import re
from typing import List

def load_bank(department: str) -> List[List]:
    """Load the bank for a given department.

    The function expects a Python module at `banks/<department>.py` that defines
    a `bank` variable containing a list of [question, grading_scale, reference_answer, reference_grade].
    
    Returns: List of bank entries, where each entry is [question, grading_scale, reference_answer, reference_grade]
    """
    base_dir = os.path.dirname(__file__)
    module_path = os.path.join(base_dir, "banks", f"{department}.py")
    if not os.path.isfile(module_path):
        raise FileNotFoundError(f"Bank module for department '{department}' not found at {module_path}")
    spec = importlib.util.spec_from_file_location(department, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    bank = getattr(module, "bank", [])
    
    return bank


def parse_score(response: str) -> float:
    """Extract the grade awarded to the candidate from the LLM response.

    The parser prefers explicit grade labels such as "Candidate grade: 8",
    "**Grade:** 8", or "Grade: 8". If multiple grade-like labels appear,
    it uses the last one so that a final grading statement overrides earlier
    reasoning or examples. If no grade label is present, it falls back to the
    last numeric value in the response. Raises ValueError if no number is
    found.
    """
    grade_patterns = [
        r"\b(?:candidate\s+)?grade\b[^\d\n]*?([-+]?[0-9]*\.?[0-9]+)",
        r"\b(?:final\s+)?(?:score|marks?)\b[^\d\n]*?([-+]?[0-9]*\.?[0-9]+)",
        r"\*\*grade\*\*[:\s]*([-+]?[0-9]*\.?[0-9]+)",
    ]

    matches = []
    for pattern in grade_patterns:
        matches.extend(re.finditer(pattern, response, re.IGNORECASE))

    # Completely new for benchmarking:If the response is a model result dict, prefer the explicit score field.
    if isinstance(response, dict):
        if "score" in response:
            return float(response["score"])
        if "response" in response and isinstance(response["response"], str):
            response = response["response"]
        else:
            # Fallback to the raw dict string if no explicit score is present.
            response = str(response)

    if matches:
        last_match = matches[-1]
        return float(last_match.group(1))

    match = re.search(r"[-+]?[0-9]*\.?[0-9]+", response)
    if not match:
        raise ValueError("No numeric score found in LLM response")
    return float(match.group())
