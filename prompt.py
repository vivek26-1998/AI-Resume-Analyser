def build_resume_analysis_prompt(
    job_description: str,
    retrieved_context: str,
) -> str:
    """
    Build the prompt for resume-job matching analysis.
    """
    return f"""
      You are an expert AI career advisor.

      Your task is to compare a candidate's resume against a job description using only the provided resume context.

      Job Description:
      {job_description}

      Relevant Resume Sections:
      {retrieved_context}

      Compare the resume against the job description.

      Return ONLY a valid JSON object with the following keys:

      - alignment_summary
      - missing_skills_explanation
      - bullet_improvements
      - impact_suggestions
      - evidence_used

      Rules:
      - Do not invent experience that is not present in the resume context.
      - If a skill is missing, clearly mention it.
      - Bullet improvements should be honest and based on the resume evidence.
      - evidence_used should list resume phrases or chunk references that support the analysis.
      """