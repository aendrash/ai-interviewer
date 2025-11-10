import streamlit as st
import requests
import json
import io
from PyPDF2 import PdfReader

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"  # local testing
# BACKEND_URL = "https://ai-interviewer-backend.onrender.com" # when deployed on render take the url from there

# App Title
st.title("AI Engineer Interview Assistant")
st.caption("An AI-powered interactive interview simulator")

# Safe session state init
for key, default in {
    "questions": [],
    "answers": [],
    "current_q": 0,
    "completed": False,
    "final_result": None,
    "answer_input": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Step 1: Upload Resume
st.subheader("Upload Your Resume")
resume_file = st.file_uploader("Upload your resume (TXT or PDF)", type=["txt", "pdf"])
resume_text = ""

if resume_file:
    if resume_file.type == "application/pdf":
        try:
            pdf_reader = PdfReader(io.BytesIO(resume_file.read()))
            pages = [page.extract_text() for page in pdf_reader.pages]
            resume_text = "\n".join(p for p in pages if p)
            st.success(f"PDF extracted successfully ({len(pages)} pages).")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
    else:
        try:
            resume_text = resume_file.read().decode("utf-8")
        except UnicodeDecodeError:
            resume_text = resume_file.read().decode("latin-1")
        st.success("Text file uploaded successfully!")

    st.text_area("Resume Preview (first 2000 chars)", resume_text[:2000], height=200)

# Step 2: Generate Questions
if resume_text and st.button("Start Interview"):
    with st.spinner("Generating interview questions..."):
        files = {"resume": ("resume.txt", resume_text.encode("utf-8"), "text/plain")}
        try:
            res = requests.post(f"{BACKEND_URL}/generate_questions/", files=files)
        except Exception as e:
            st.error(f"Backend request failed: {e}")
            st.stop()

        if res.status_code == 200:
            raw_questions = res.json().get("questions", [])

            # Clean and simplify questions
            cleaned_questions = []
            for q in raw_questions:
                q = q.split("Expected Answer:")[0]
                q = q.replace("New Technical Interview Question", "")
                q = q.replace("Question:", "")
                q = q.strip()
                cleaned_questions.append(q)

            if not cleaned_questions:
                st.warning("No questions returned. Please check backend logs.")
            else:
                st.session_state.questions = cleaned_questions
                st.session_state.current_q = 0
                st.session_state.answers = ["" for _ in cleaned_questions]
                st.session_state.answer_input = ""
                st.success("Interview started! Let's begin.")
                st.rerun()
        else:
            st.error(f"Error: {res.status_code} - {res.text}")

# Step 3: Sequential Question Flow
if st.session_state.questions:
    questions = st.session_state.questions
    current_q = st.session_state.current_q
    total_q = len(questions)

    # Progress bar
    st.progress((current_q + 1) / total_q)
    st.markdown(f"### Question {current_q + 1} of {total_q}")
    st.markdown(f"**{questions[current_q]}**")

    # Text input box with placeholder
    st.session_state.answer_input = st.text_area(
        "Your Answer:",
        value=st.session_state.answer_input,
        height=150,
        key=f"answer_box_{current_q}",
        placeholder="Type your answer here..."
    )

    col1, col2, col3 = st.columns([1,]()
