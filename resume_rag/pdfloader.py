import fitz


def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_pdf_path(file_path: str) -> str:
    doc = fitz.open(file_path)

    text = ""
    for page in doc:
        text += page.get_text()

    return text.strip()