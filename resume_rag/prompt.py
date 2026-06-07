def build_resume_analysis_prompt(
    job_description: str,
    retrieved_context: str,
) -> str:
    return f"""
You are an expert AI career advisor.

Your task is to compare a candidate's resume against a job description using only the provided resume context.

Job Description:
{job_description}

Relevant Resume Sections:
{retrieved_context}

Return ONLY a valid JSON object with exactly these keys:

{{
	"alignment_summary": "string",
	"matching_skills": ["string"],
	"missing_skills": ["string"],
	"missing_skills_explanation": "string",
	"bullet_improvements": ["string"],
	"impact_suggestions": ["string"],
	"evidence_used": ["string"]
}}

Rules:
- Use only the provided resume context.
- Do not invent experience that is not present in the resume context.
- matching_skills must include skills from the job description that are supported by the resume context.
- missing_skills must include skills from the job description that are not clearly supported by the resume context.
- missing_skills_explanation should briefly explain the most important gaps.
- bullet_improvements should suggest honest improvements based only on the resume context.
- impact_suggestions should suggest how the candidate can present existing experience more effectively.
- evidence_used should list specific chunks and keywords from the chunks used for the analysis.
- All list fields must always be lists, even if empty.
- Do not use null values.
"""
