import pandas as pd
import numpy as np
import argparse
import os
import sys
from pathlib import Path
from utils import parse_score
from llama3_1_client import get_score as get_score_llama


def benchmark_dataset(input_path: str, output_path: str, model: str = "llama3.1") -> float:
    df = pd.read_excel(input_path)

    expected_columns = [
        "Question",
        "Grading Scale",
        "Reference Answer",
        "Reference Grade",
        "Candidate Answer",
        "Candidate Grade",
    ]
    missing = [col for col in expected_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    ai_grades = []
    raw_responses = []
    errors = []

    for idx, row in df.iterrows():
        question = str(row["Question"])
        grading_scale = str(row["Grading Scale"])
        reference_answer = str(row["Reference Answer"])
        reference_grade = row["Reference Grade"]
        candidate_answer = str(row["Candidate Answer"])

        try:
            result = get_score_llama(grading_scale, question, reference_answer, candidate_answer, reference_grade)
            score = parse_score(result)
            ai_grades.append(score)
            raw_responses.append(result)
        except Exception as exc:
            errors.append((idx, exc))
            ai_grades.append(np.nan)
            raw_responses.append(str(exc))

    df["AI Grade"] = ai_grades
    df["LLM Raw Response"] = raw_responses

    mse = np.nan
    if len(df) > 0:
        valid = df["AI Grade"].notna() & df["Candidate Grade"].notna()
        if valid.any():
            squared_errors = (df.loc[valid, "AI Grade"].astype(float) - df.loc[valid, "Candidate Grade"].astype(float)) ** 2
            mse = float(squared_errors.mean())

    df.to_excel(output_path, index=False)

    if errors:
        error_lines = "\n".join([f"row {idx}: {exc}" for idx, exc in errors[:10]])
        print(f"Warning: {len(errors)} rows failed during grading. First errors:\n{error_lines}")

    return mse


def main(argv=None):
    parser = argparse.ArgumentParser(description="Benchmark the answer grading system on a dataset.")
    parser.add_argument("--input", default="dataset.xlsx", help="Path to the input dataset XLSX file.")
    parser.add_argument("--output", default="dataset_with_ai_grade.xlsx", help="Path to write the output dataset.")
    parser.add_argument("--model", choices=["llama3.1"], default="llama3.1", help="LLM model to use.")
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    try:
        mse = benchmark_dataset(str(input_path), str(args.output), model=args.model)
        print(f"Benchmark complete. Output written to: {args.output}")
        print(f"Mean squared error: {mse}")
    except Exception as exc:
        print(f"Error during benchmark: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
