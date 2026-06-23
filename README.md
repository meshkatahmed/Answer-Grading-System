# Answer Grading System

A simple Python command‑line tool that grades a candidate's answer against a reference answer using the Gemini LLM.

## Features
- Department‑wise question/answer banks stored as Python modules.
- Prompt template with placeholders for grading scale, question, reference answer, and candidate answer.
- Uses the Gemini API (`google-generativeai`).
- CLI interface built with `argparse` and `rich` for pretty output.

## Prerequisites
- Python 3.9+ installed.
- Gemini API key set in the environment variable `GEMINI_API_KEY`.
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Usage
```bash
python main.py --department example --question-index 0 --candidate "Your answer here"
```
- `--department` : name of the department bank (module under `banks/`).
- `--question-index` : zero‑based index of the question to grade.
- `--candidate` : the candidate's answer text.
- `--scale` (optional) : grading scale, default `0-10`.

The tool will print the numeric score and the LLM's justification.

## Adding New Departments
Create a new file under `banks/`, e.g., `banks/math.py`:
```python
questions = ["What is 2+2?", "Define derivative."]
answers   = ["4", "The derivative of a function ..."]
```
Then run the CLI with `--department math`.

## Environment Variable
```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```
On Windows:
```cmd
set GEMINI_API_KEY=YOUR_API_KEY
```

## License
MIT License
