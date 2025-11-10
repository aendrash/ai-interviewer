AI Interviewer – RAG-Based AI Engineer Interview Assistant
An AI-powered interactive interview platform that evaluates candidates for AI/ML Engineer roles using their resume context, a RAG knowledge base, and LLM intelligence.

Reads and understands the candidate’s resume

Generates 10 dynamic technical questions based on it

Takes answers one-by-one

Evaluates responses and gives a final score with feedback

Architecture Overview
text
ai_interviewer/
│
├── backend/                # FastAPI backend (RAG engine)
│   ├── main.py             # Core API (question generation + scoring)
│   ├── data/               # Knowledge base (ML/DL/AI text files)
│   ├── faiss_index.pkl     # Auto-created FAISS vector DB
│   ├── requirements.txt    # Backend dependencies
│   ├── .env                # OpenAI key (excluded from git)
│
└── frontend/               # Streamlit Cloud app (user interface)
    ├── app.py              # Streamlit UI logic
    ├── requirements.txt    # Frontend dependencies
Tech Stack
LLM API: OpenAI GPT-4o-mini

Vector Store: FAISS (in-memory RAG)

Backend API: FastAPI

Frontend UI: Streamlit

Deployment: Render (Backend) + Streamlit Cloud (Frontend)

Language: Python 3.10+

Features
Upload resume (PDF/TXT)

Resume context extraction (via RAG)

Auto-generated 10 technical questions

One-by-one interview flow

AI evaluation and feedback (score 0–100)

Progress bar and restart option

Cloud deployable (free-tier ready)

Installation (Local Setup)
Clone the Repository

text
git clone https://github.com/yourusername/ai_interviewer.git
cd ai_interviewer
Install Backend Dependencies

text
cd backend
pip install -r requirements.txt
Add Environment Variables

Create a .env file inside /backend:

text
OPENAI_API_KEY=sk-your-openai-key-here
Do not commit this file to GitHub.

Run Backend Server

text
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
Test locally at: http://127.0.0.1:8000/docs

Run Frontend (Streamlit)

text
cd ../frontend
pip install -r requirements.txt
streamlit run app.py
App will open at: http://localhost:8501

Backend Requirements Example (backend/requirements.txt)
text
fastapi
uvicorn
faiss-cpu
openai
python-dotenv
numpy
pydantic
Frontend Requirements Example (frontend/requirements.txt)
text
streamlit
requests
PyPDF2
Deployment Guide
Step 1: Deploy Backend on Render
Go to Render

Create a new Web Service

Connect your backend GitHub repo

Set the start command:

text
uvicorn main:app --host 0.0.0.0 --port 10000
Add the environment variable:

text
OPENAI_API_KEY=sk-your-openai-key
Port: 10000

Click Deploy

After deployment, note your API URL:
https://ai-interviewer-backend.onrender.com

Test at: https://ai-interviewer-backend.onrender.com/docs

Step 2: Deploy Frontend on Streamlit Cloud
Go to Streamlit Cloud

Sign in with GitHub

Select your frontend repo

Set the main file to: app.py

Add your dependencies (frontend/requirements.txt)

Click Deploy

Step 3: Connect Backend to Frontend
In your frontend/app.py, update:

python
BACKEND_URL = "https://ai-interviewer-backend.onrender.com"
Push the change to GitHub — Streamlit redeploys automatically.

Testing Your App (Live)
Visit your Streamlit URL (e.g. https://aendra-ai-interviewer.streamlit.app)

Upload your resume (PDF/TXT)

Click Start Interview

Answer questions sequentially

Submit and view AI-generated evaluation

Folder Summary
Folder/File	Description
backend/main.py	FastAPI app with RAG and scoring
backend/data/	ML/DL/AI .txt files for context
backend/faiss_index.pkl	Auto-created FAISS index
frontend/app.py	Streamlit interview interface
frontend/requirements.txt	Streamlit dependencies
.env	Your OpenAI API key (local only)
Example Backend .env
text
OPENAI_API_KEY=sk-your-key-here
Add .env to your .gitignore:

text
.env
__pycache__/
*.pkl
Example API Endpoints
Generate Questions

POST /generate_questions/
FormData: resume (file)
Response:

json
{"questions": ["What is overfitting?", "..."]}
Evaluate Answers

POST /evaluate/
Body:

json
{"qa_pairs": [{"question": "...", "answer": "..."}]}
Response:

json
{"score": "Score: 85/100\nSummary: Strong understanding..."}
Future Enhancements
Add authentication for admin/interviewer roles

Store past interviews in a DB (MongoDB/Firebase)

Add difficulty selector (easy / medium / hard)

Add voice-based interview (speech-to-text)

Fine-tune custom LLM on AI engineering interviews

Author
Aendra Shukla
AI Engineer | ML Researcher | Full-Stack Developer
Lucknow, India
Email: shuklaaendra123@gmail.com
