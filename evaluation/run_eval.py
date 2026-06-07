import os
from openai import OpenAI
import json
from resume_rag.rag_utils import create_vector_store, retrieve
from resume_rag.pdfloader import extract_text_from_pdf_path
from resume_rag.llm_analyzer import analyze_resume_match
from evaluation.evaluator import run_all_evaluations
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

CHUNK_SIZE = 1000
OVERLAP = 150
TOP_K = 5
LLM_MODEL = "gpt-4o-mini"
TEMPERATURE = 0.3
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_sample_test(test_case_path):
    with open(test_case_path, "r", encoding="utf-8") as file:
        test_cases = json.load(file)
    return test_cases

def main():
    test_case_path = Path("evaluation/test_cases.json")
    test_cases = load_sample_test(test_case_path)
    for test_case in test_cases:
        resume_path = test_case["resume_file"]
        job_description = test_case["job_description"]
        resume_text = extract_text_from_pdf_path(resume_path)
        index, chunks = create_vector_store(
                resume_text,
                chunk_size=CHUNK_SIZE,
                overlap=OVERLAP,
            )
        retrieved_chunks = retrieve(
                query=job_description,
                index=index,
                chunks=chunks,
                k=TOP_K,
            )
        output_json = analyze_resume_match(
                client=client,
                job_description=job_description,
                retrieved_chunks=retrieved_chunks,
                model=LLM_MODEL,
                temperature=TEMPERATURE,
        )
        print(f"Output for {test_case['case_id']}:")
        eval_res = run_all_evaluations(output_json = output_json, retrieved_content = retrieved_chunks, test_case = test_case)
        print(json.dumps(eval_res, indent=2))
              
if __name__ == "__main__":
    main()





