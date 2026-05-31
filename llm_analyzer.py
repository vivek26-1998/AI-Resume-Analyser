from openai import OpenAI
import json
from prompt import build_resume_analysis_prompt
def format_retrieved_context(retrieved_chunks: list[dict]) -> str:
    context_parts = []

    for chunk in retrieved_chunks:
        chunk_text = f"[Chunk {chunk['chunk_id']}]\n{chunk['chunk_text']}"
        context_parts.append(chunk_text)
    
    return "\n\n".join(context_parts)

def analyze_resume_match(
    client: OpenAI,
    job_description: str,
    retrieved_chunks: list[dict],
    model: str = "gpt-4o-mini",
    temperature: float = 0.3,
) -> dict:
    """
    Analyze resume-job alignment using the retrieved resume chunks.
    """
    retrieved_context = format_retrieved_context(retrieved_chunks)

    prompt = build_resume_analysis_prompt(
        job_description=job_description,
        retrieved_context=retrieved_context,
    )

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        response_format={"type": "json_object"},
    )

    output_text = response.choices[0].message.content

    return json.loads(output_text)