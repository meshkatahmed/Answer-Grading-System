# main.py
"""Command-line interface for the Answer Grading system.

Usage example:
    python main.py --dept math --question 0 \
        --candidate "My answer" --scale "0-10"
"""

import argparse
import sys
from utils import load_bank, parse_score
from gemini_client import get_score

def grade_question(department: str, q_index: int, candidate: str, scale: str):
    questions, answers = load_bank(department)
    if q_index < 0 or q_index >= len(questions):
        raise IndexError(f"Question index {q_index} out of range for department '{department}'.")
    question = questions[q_index]
    reference = answers[q_index]
    raw_response = get_score(scale, question, reference, candidate)
    score = parse_score(raw_response)
    return {
        "department": department,
        "question_index": q_index,
        "question": question,
        "candidate_answer": candidate,
        "reference_answer": reference,
        "raw_response": raw_response,
        "score": score,
    }

def main(argv=None):
    parser = argparse.ArgumentParser(description="Answer Grading CLI using Gemini LLM")
    parser.add_argument("--dept", required=True, help="Department name (matches bank module)")
    parser.add_argument("--question", type=int, required=True, help="Index of the question in the bank (0‑based)")
    parser.add_argument("--candidate", required=True, help="Candidate answer text")
    parser.add_argument("--scale", default="0-10", help="Grading scale description")
    args = parser.parse_args(argv)
    try:
        result = grade_question(args.dept, args.question, args.candidate, args.scale)
        print("Score:", result["score"])
        print("Raw LLM response:\n", result["raw_response"])
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
