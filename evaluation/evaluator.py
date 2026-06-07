def list_to_text(items):
    if not items:
        return ""
    return " ".join(items).lower()


def validate_output_strcture(output_json, test_case):
    required_keys = test_case.get("required_output_keys", [])
    missing_keys = []

    for key in required_keys:
        if key not in output_json:
            missing_keys.append(key)

    structure_valid = len(missing_keys) == 0

    return{
    "structure_valid": structure_valid, 
    "missing_keys": missing_keys
    }

def evaluate_retreived_content(retrieved_content, test_case):
    expected_skills = test_case.get("expected_matching_skills", [])
    for chunk in retrieved_content:
        retrieved_text =chunk.get("chunk_text","") + " "
    retrieved_text = retrieved_text.lower()

    found_skills = []
    missing_skills = []
    for skill in expected_skills:
        if skill.lower() in retrieved_text:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    total = len(expected_skills)
    score = len(found_skills)/total if total > 0 else 0
    return {
        "retrieval_score": score,
        "found_skills": found_skills,   
        "missing_skills": missing_skills
    }

def evaluate_matching_skills(output_json, test_case):
    expected_skills = test_case.get("expected_matching_skills", [])
    actual_matching_skills = output_json.get("matching_skills", [])
    actual_text = list_to_text(actual_matching_skills) # so that string matching is simpler and not exact list by list match which may miss some matches due to formatting or extra info in the skill names
    found_skills = []
    missing_skills = []
    for skill in expected_skills:
        if skill.lower() in actual_text:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    total = len(expected_skills)
    score = len(found_skills)/total if total > 0 else 0
    return {
        "matching_skills_score": score,
        "found_skills": found_skills,   
        "missing_skills": missing_skills
    }

def evaluate_missing_skills(output_json, test_case):
    expected_skills = test_case.get("expected_missing_skills", [])
    actual_missing_skills = output_json.get("missing_skills", [])
    actual_text = list_to_text(actual_missing_skills) # so that string matching is simpler and not exact list by list match which may miss some matches due to formatting or extra info in the skill names
    found_skills = []
    missing_skills = []
    for skill in expected_skills:
        if skill.lower() in actual_text:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    total = len(expected_skills)
    score = len(found_skills)/total if total > 0 else 0
    return {
        "missing_skills_score": score,
        "found_skills": found_skills,   
        "missing_skills": missing_skills
    }

def check_false_claims(output_json, test_case):
    """
    Check whether model claims skills that should not be claimed as experience.
    Only checks matching_skills, not missing_skills.
    """
    must_not_claim = test_case.get("must_not_claim_as_experience", [])
    actual_matching_skills = output_json.get("matching_skills", [])

    actual_text = list_to_text(actual_matching_skills)

    false_claims = []

    for skill in must_not_claim:
        if skill.lower() in actual_text:
            false_claims.append(skill)

    return {
        "false_claims_detected": len(false_claims) > 0,
        "false_claims": false_claims,
    }

def run_all_evaluations(output_json, retrieved_content, test_case):
    return {
        "case_id": test_case.get("case_id",""),
        "structure": validate_output_strcture(output_json, test_case),
        "retrieval": evaluate_retreived_content(retrieved_content, test_case),
        "matching_skills": evaluate_matching_skills(output_json, test_case),    
        "missing_skills": evaluate_missing_skills(output_json, test_case),
        "false_claims": check_false_claims(output_json, test_case)
    }