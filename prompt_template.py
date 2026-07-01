# prompt_template.py

"""Prompt template used for grading.
Placeholders:
- {scale}: Grading scale description (e.g., "0-10").
- {question}: The question text.
- {reference}: The reference answer.
- {reference_grade}: The grade assigned to the reference answer.
- {candidate}: The candidate's answer.
"""

PROMPT = """You are an expert grader evaluating candidate answers. Your task is to grade the candidate's answer on the scale: {scale}.

**GRADING REFERENCE:**
- Reference answer: {reference}
- Reference grade: {reference_grade}

**CANDIDATE ANSWER TO GRADE:**
- Question: {question}
- Candidate answer: {candidate}

**GRADING INSTRUCTIONS:**
1. Compare the candidate's answer with the reference answer in terms of content accuracy, completeness, and clarity.
2. Use the reference grade ({reference_grade}) as an anchor point:
   - If the candidate's answer is semantically similar to the reference answer with minor differences (same concepts, similar depth, correct understanding), grade it close to the reference grade ({reference_grade}).
   - If the candidate's answer is substantially better than the reference answer (more comprehensive, clearer explanation, additional relevant insights, or better examples), assign a HIGHER grade than the reference grade ({reference_grade}).
   - If the candidate's answer is worse (missing key concepts, less clear, or contains inaccuracies), assign a LOWER grade than the reference grade ({reference_grade}).
3. Ensure your grading is relative to the reference answer quality, not in isolation.

Provide a numeric score (within the {scale} range) and a brief justification (2-3 sentences)."""
