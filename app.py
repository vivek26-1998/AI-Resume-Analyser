import streamlit as st
from openai import OpenAI

from rag_utils import create_vector_store, retrieve
from pdfloader import extract_text_from_pdf
from llm_analyzer import analyze_resume_match
import traceback


CHUNK_SIZE = 800
OVERLAP = 100
TOP_K = 3
LLM_MODEL = "gpt-4o-mini"
TEMPERATURE = 0.3


st.set_page_config(layout="wide")
st.title("RAG-Powered Resume Intelligence System")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Enter job description")


if uploaded_file and job_description:
    try:
        with st.spinner("Extracting resume text..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            print(f"Extracted resume text length: {len(resume_text)} characters")

        with st.spinner("Creating vector store..."):
            index, chunks = create_vector_store(
                resume_text,
                chunk_size=CHUNK_SIZE,
                overlap=OVERLAP,
            )

        with st.spinner("Extracting relevant sections..."):
            retrieved_chunks = retrieve(
                query=job_description,
                index=index,
                chunks=chunks,
                k=TOP_K,
            )
            print(f"Retrieved chunks: {len(retrieved_chunks)}")
        with st.spinner("Analyzing resume match..."):
            output_json = analyze_resume_match(
                client=client,
                job_description=job_description,
                retrieved_chunks=retrieved_chunks,
                model=LLM_MODEL,
                temperature=TEMPERATURE,
            )
            print(f"LLM Output {output_json}")

        st.subheader("AI Analysis")

        st.write("**Alignment Summary:**")
        st.write(output_json.get("alignment_summary", "Not provided"))

        st.write("**Missing Skills Explanation:**")
        st.write(output_json.get("missing_skills_explanation", "Not provided"))

        st.write("**Bullet Improvements:**")
        for item in output_json.get("bullet_improvements", []):
            st.write(f"- {item}")

        st.write("**Impact Suggestions:**")
        for item in output_json.get("impact_suggestions", []):
            st.write(f"- {item}")

        st.write("**Evidence Used:**")
        for item in output_json.get("evidence_used", []):
            st.write(f"- {item}")

        with st.expander("Retrieved Resume Chunks"):
            for chunk in retrieved_chunks:
                st.write(f"**Chunk {chunk['chunk_id']}**")
                st.write(f"Distance: {chunk['distance']:.4f}")
                st.write(chunk["chunk_text"])

    except Exception as e:# for detailed error reporting
        st.error("Error processing output.")
        st.write(f"Exception type: {type(e).__name__}")
        st.write(f"Exception message: {e}")
        st.code(traceback.format_exc())