import streamlit as st
import requests
import json
import io
from PyPDF2 import PdfReader

# Backend URL
# BACKEND_URL = "http://127.0.0.1:8000"  # local testing
BACKEND_URL = "https://ai-interviewer-backend-s6ca.onrender.com" # when deployed on render take the url from there

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

    col1, col2, col3 = st.columns([1, 1, 3])

    with col1:
        if current_q > 0:
            if st.button("Previous"):
                st.session_state.answers[current_q] = st.session_state.answer_input
                st.session_state.current_q -= 1
                st.session_state.answer_input = st.session_state.answers[st.session_state.current_q]
                st.rerun()

    with col2:
        if current_q < total_q - 1:
            if st.button("Next"):
                st.session_state.answers[current_q] = st.session_state.answer_input
                st.session_state.current_q += 1
                st.session_state.answer_input = ""  # clear input for next question
                st.rerun()
        else:
            if st.button("Submit Interview"):
                st.session_state.answers[current_q] = st.session_state.answer_input
                qa_pairs = [
                    {"question": q, "answer": a}
                    for q, a in zip(st.session_state.questions, st.session_state.answers)
                ]
                with st.spinner("Evaluating your interview..."):
                    try:
                        res = requests.post(f"{BACKEND_URL}/evaluate/", json={"qa_pairs": qa_pairs})
                    except Exception as e:
                        st.error(f"Backend request failed: {e}")
                        st.stop()

                    if res.status_code == 200:
                        result = res.json().get("score", "No result received")
                        st.session_state.final_result = result
                        st.session_state.completed = True
                        st.session_state.answer_input = ""
                        st.rerun()
                    else:
                        st.error(f"Error: {res.status_code} - {res.text}")

# Step 4: Show Final Evaluation
if st.session_state.completed:
    st.success("Interview completed successfully!")
    st.subheader("Interview Evaluation Summary")
    st.write(st.session_state.final_result)

    if st.button("Restart Interview"):
        for key in ["questions", "answers", "current_q", "completed", "final_result", "answer_input"]:
            st.session_state.pop(key, None)
        st.rerun()
