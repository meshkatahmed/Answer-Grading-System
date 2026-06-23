# prompt_template.py

"""Prompt template used for grading.
Placeholders:
- {scale}: Grading scale description (e.g., "0-10").
- {question}: The question text.
- {reference}: The reference answer.
- {candidate}: The candidate's answer.
"""

PROMPT = """You are an expert grader. Grading scale: {scale}.
Question: {question}
Reference answer: {reference}
Candidate answer: {candidate}
Provide a numeric score (as a number) and a brief justification.
"""
