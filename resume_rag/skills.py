SKILLS = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "nlp",
    "computer vision",
    "kubernetes",
    "docker",
    "aws",
    "azure",
    "fastapi",
    "flask",
    "react",
    "data analysis",
    "pandas",
    "numpy",
    "transformers",
    "llm",
    "statistics",
    "scikit-learn",
    "ci/cd",
    "git",
]


def extract_skills(text):
    text = text.lower()
    return list({skill for skill in SKILLS if skill in text})
