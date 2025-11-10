
# backend/main.py

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import numpy as np
import faiss, os, json
from typing import List
import pickle
from dotenv import load_dotenv

# ----------------------------------------
# FastAPI Setup
# ----------------------------------------
app = FastAPI(title="AI Interview Backend")

# Allow frontend (Streamlit) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------
# OpenAI Client
# ----------------------------------------
# Best practice: use env var in production, keep key out of code

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if not os.getenv("OPENAI_API_KEY"):
    print("OpenAI API key not found in environment!")
else:
    print("OpenAI API key loaded successfully.")


# ----------------------------------------
# Config
# ----------------------------------------
DATA_FOLDER = "data"
VECTOR_DB_PATH = "faiss_index.pkl"
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

# ----------------------------------------
# Embedding + Vector DB
# ----------------------------------------
def embed_texts(texts):
    """Generate embeddings for a list of texts."""
    res = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [r.embedding for r in res.data]


def build_vector_db():
    """Build FAISS vector index from data folder."""
    if not os.path.exists(DATA_FOLDER):
        raise FileNotFoundError(f"Data folder not found: {DATA_FOLDER}")

    txt_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".txt")]
    if not txt_files:
        raise FileNotFoundError("No .txt files found in data folder.")

    docs = []
    for file in txt_files:
        path = os.path.join(DATA_FOLDER, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                print(f"Skipping empty file: {file}")
                continue
            docs.append(content)
            print(f"Loaded: {file} ({len(content)} chars)")

    embeddings = embed_texts(docs)
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    with open(VECTOR_DB_PATH, "wb") as f:
        pickle.dump((index, docs), f)

    print("FAISS vector DB built successfully.")


# ----------------------------------------
# Load or Build Vector DB
# ----------------------------------------
if not os.path.exists(VECTOR_DB_PATH):
    print("No vector index found. Building one now...")
    build_vector_db()

with open(VECTOR_DB_PATH, "rb") as f:
    index, docs = pickle.load(f)
print("Vector DB loaded.")


# ----------------------------------------
# Helper Functions
# ----------------------------------------
def retrieve_context(query: str, k=3):
    query_emb = np.array(embed_texts([query])[0]).astype("float32").reshape(1, -1)
    _, I = index.search(query_emb, k)
    selected = [docs[i] for i in I[0] if i < len(docs)]
    return "\n\n---\n\n".join(selected) if selected else "No relevant context found."


def generate_question(resume_text: str, asked: list):
    """Generate one diverse interview question."""
    context = retrieve_context(resume_text)
    prompt = f"""
You are an AI interviewer for AI Engineer candidates.

Resume:
{resume_text[:2500]}

Relevant context:
{context}

Already asked questions:
{json.dumps(asked)}

Generate ONE new technical interview question.
Vary difficulty (easy/medium/hard) and cover different areas
(ML, DL, NLP, AI concepts, math, system design).
Avoid repeating topics.
"""
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "system", "content": prompt}],
        max_tokens=150,
        temperature=0.7,  # more creative variety
    )
    raw = resp.choices[0].message.content.strip()

    # Clean unwanted info before returning
    cleaned = raw.split("Expected Answer:")[0]
    cleaned = cleaned.replace("New Technical Interview Question", "")
    cleaned = cleaned.replace("Question:", "").strip()

    return cleaned


def score_answers(qa_pairs: List[dict]):
    """Evaluate answers and return encouraging feedback."""
    prompt = f"""
You are an AI interview evaluator.
Evaluate the following AI Engineer interview based on clarity, correctness, and technical understanding.

Rules:
- Give a numeric score (0-100).
- Highlight positives even if the answers are weak.
- Provide 3-5 short, constructive feedback points.
- End with a one-line recommendation (e.g. "Strong candidate", "Needs improvement", etc.)

Interview transcript:
{json.dumps(qa_pairs, indent=2, ensure_ascii=False)}
"""

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "system", "content": prompt}],
        max_tokens=400,
        temperature=0.3,  # low randomness for consistency
    )
    return resp.choices[0].message.content.strip()


# ----------------------------------------
# API Models
# ----------------------------------------
class QARequest(BaseModel):
    qa_pairs: List[dict]


# ----------------------------------------
# API Endpoints
# ----------------------------------------
@app.post("/generate_questions/")
async def generate_questions(resume: UploadFile, difficulty: str = "mixed"):
    """Generate 10 interview questions from resume."""
    text = (await resume.read()).decode("utf-8", errors="ignore")
    questions = []
    for i in range(10):
        q = generate_question(text + f"\nDifficulty: {difficulty}", questions)
        questions.append(q)
    return {"questions": questions}


@app.post("/evaluate/")
async def evaluate_answers(data: QARequest):
    """Evaluate candidate answers and return feedback."""
    result = score_answers(data.qa_pairs)
    return {"score": result}
