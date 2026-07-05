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
1. Compare the candidate's answer with the reference answer in terms of content accuracy, completeness, clarity, and relevance to the question.
2. Use the reference grade ({reference_grade}) as an anchor point, but grade relative to the reference answer quality rather than in isolation.
   - If the candidate's answer is semantically similar to the reference answer with minor differences, grade it close to the reference grade ({reference_grade}).
   - If the candidate's answer is substantially better than the reference answer, assign a HIGHER grade than the reference grade ({reference_grade}).
   - If the candidate's answer is worse, incomplete, or contains inaccuracies, assign a LOWER grade than the reference grade ({reference_grade}).
   - If the candidate's answer is completely irrelevant, misleading, or factually incorrect, assign 0.
3. Do not over-penalize for wording differences when the meaning is correct. Synonyms, alternative examples, or different but valid structures should be treated as correct when they preserve the core idea.
4. If the candidate adds extra information that is not in the reference answer, fact-check it. Relevant and factually correct extra information can raise the grade; incorrect, unsupported, or misleading information should lower it. Reward or penalize multiple extra points proportionally.
5. Judge the answer in the context of the department and domain (for example IT, HR, Compliance, Marketing, or other RMG-sector topics). Domain-specific correctness, policy relevance, and business appropriateness matter.
6. If the answer is partially correct but incomplete, assign an intermediate grade rather than an all-or-nothing score.
7. Penalize hallucinations, unsupported claims, and contradictions, especially in compliance, policy, procedural, or regulatory questions.
8. For blank, vague, or refusal-style answers such as "I don't know" or a single word that does not address the question, assign a very low score unless the question explicitly allows such a response.
9. For coding questions, award full or near-full credit when the code is correct, clean, and meets the requirements. Give partial credit for partially correct solutions and penalize logic errors, missing edge cases, syntax errors, or unsafe behavior.
10. For multi-part questions, evaluate each important part. Missing one major required component should reduce the grade even if the rest is correct.
11. Keep the score within the stated grading scale. Clamp the final grade to the minimum and maximum values of the scale.
12. Do not reward verbosity alone; clarity, correctness, and relevance should matter more than length.
13. Follow grading examples provided below for guidance.

**GRADING EXAMPLES:**
Example 1:
- Question: "What is FastAPI?"
- Grading scale: "0-10"
- Reference answer: "FastAPI is a backend framework."
- Reference grade: 8
- Candidate answer: "FastAPI is a backend framework built on top of Python."
- Candidate grade: 10
- Explanation: The candidate's answer covers the facts in the reference answer, so they will get the same grade as the reference answer. Additionally, the candidate's answer provides extra information about FastAPI being built on top of Python, which is factually correct and adds value. Therefore, the candidate's answer gets rewarded and the grade is clamped to the maximum grade in the scale.

Example 2:
- Question: "What is FastAPI?"
- Grading scale: "0-10"
- Reference answer: "FastAPI is a backend framework."
- Reference grade: 8
- Candidate answer: "FastAPI is a backend framework built on top of Java."
- Candidate grade: 4
- Explanation: The candidate's answer covers the main facts in the reference answer, but adds factually incorrect information. This should be penalized, so the score is reduced below the reference grade.

Example 3:
- Question: "What is FastAPI?"
- Grading scale: "0-10"
- Reference answer: "FastAPI is a backend framework."
- Reference grade: 8
- Candidate answer: "FastAPI is using System Design."
- Candidate grade: 0
- Explanation: The candidate's answer is irrelevant and factually incorrect, so it should receive 0.

Example 4:
- Question: "Write a Python function that takes a list of numbers as input and returns the average."
- Grading scale: "0-10"
- Reference answer: 
      def average(numbers):
          return sum(numbers) / len(numbers) if numbers else 0
- Reference grade: 10
- Candidate answer: 
      def mean(nums):
          sum = 0
          count = 0
          for n in nums:
              sum += n
              count += 1
          return sum / count
- Candidate grade: 6
- Explanation: The candidate's answer implements the core idea but uses a different function name. Though it is functionally reasonable, it is verbose and does not cover the case of an empty list, so it should be penalized but still receive partial credit.

Example 5:
- Question: "What is a RAG system?"
- Grading scale: "0-10"
- Reference answer: "A RAG system retrieves relevant documents from a knowledge base and uses them to improve LLM responses."
- Reference grade: 8
- Candidate answer: "It retrieves documents and uses them to ground the model answer."
- Candidate grade: 8
- Explanation: The candidate answer conveys the same core meaning with different wording. Because it is semantically correct and complete, it should receive a grade close to the reference grade rather than being penalized for wording differences.

Respond without markdown in below format:
Grade:
Short Explanation:

"""
