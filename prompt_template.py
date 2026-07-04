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
   - If the candidate's answer is completely irrelevant or factually incorrect, assign 0.
3. Ensure your grading is relative to the reference answer quality, not in isolation.
4. If the candidate's answer includes any extra information that is not present in the reference answer, fact check that information and if it is factually correct, assign a grade higher than the reference grade ({reference_grade}). If it is factually incorrect, penalize for that by negating marks.
   - If the candidate's answer adds two or more factually correct/incorrect extra information, reward/penalize with extra marks proportianally.

**GRADING EXAMPLES:**
Example 1:
- Reference answer: "FastAPI is a backend framework."
- Reference grade: 8
- Candidate answer: "FastAPI is a backend framework built on top of Python."
- Candidate grade: 10
- Explanation: The candidate's answer covers the facts in the reference answer, so they will get the same grade as the reference answer.
   Additionally, the candidate's answer provides extra information about FastAPI being built on top of Python, which is factually correct and adds value to the answer. 
   Therefore, the candidate's answer will get rewarded with half the score for one fact in the reference answer. 
   But if we add half the score for one fact in the reference answer, the candidate's grade will exceed the grading scale.
   So, it is clamped to the maximum grade in the scale.

Example 2:
- Reference answer: "FastAPI is a backend framework."
- Reference grade: 8
- Candidate answer: "FastAPI is a backend framework built on top of Java."
- Candidate grade: 4
- Explanation: The candidate's answer covers the facts in the reference answer, so they will get the same grade as the reference answer.
   Additionally, the candidate's answer provides extra information about FastAPI being built on top of Java, which is factually incorrect. 
   Therefore, the candidate's answer will get penalized with half the score for one fact in the reference answer. 
   So, if we deduct half the score for one fact in the reference answer, the candidate's grade will be reference grade - half the score for one fact.
   So, the grade will be 8 - 4 = 4.
   
Example 3:
- Reference answer: "FastAPI is a backend framework."
- Reference grade: 8
- Candidate answer: "FastAPI is using System Design."
- Candidate grade: 0
- Explanation: The candidate's answer does not cover the facts in the reference answer, and it is completely irrelevant.
   Additionally, the candidate's answer talks about system design, that is factually incorrect about FastAPI.
   As it does not cover the facts in the reference answer and is completely irrelevant, the candidate's answer will get a grade of 0.

Provide a numeric score and step by step reasoning and math behind your grading."""
