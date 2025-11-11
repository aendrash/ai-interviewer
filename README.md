
# 🤖 AI Interviewer – RAG-Based AI Engineer Interview Assistant

An AI-powered interactive interview platform that evaluates candidates for AI/ML Engineer roles using their resume context, a RAG knowledge base, and LLM intelligence.

---

## 🎯 Core Capabilities
- Reads and understands the candidate’s resume
- Generates **10 dynamic technical questions** based on it
- Takes answers one-by-one in an interactive flow
- Evaluates responses and gives a **final score with feedback**

---

## 🧱 Architecture Overview
```
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
```

---

## 🧠 Tech Stack
| Component | Technology |
|------------|-------------|
| **LLM API** | OpenAI GPT-4o-mini |
| **Vector Store** | FAISS (in-memory RAG) |
| **Backend API** | FastAPI |
| **Frontend UI** | Streamlit |
| **Deployment** | Render (Backend) + Streamlit Cloud (Frontend) |
| **Language** | Python 3.10+ |

---

## 🌟 Features
- Resume upload (PDF/TXT)
- Context extraction via RAG
- Auto-generated 10 technical questions
- Sequential question flow
- AI-based evaluation & feedback (0–100 score)
- Restart and progress tracking
- Cloud deployable on free-tier

---

## ⚙️ Installation (Local Setup)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/ai_interviewer.git
cd ai_interviewer
```

### 2️⃣ Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3️⃣ Add Environment Variables
Create a `.env` file inside `/backend`:
```bash
OPENAI_API_KEY=sk-your-openai-key-here
```
🛑 **Do not commit this file** to GitHub.

### 4️⃣ Run Backend Server
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
Test locally at → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 5️⃣ Run Frontend (Streamlit)
```bash
cd ../frontend
pip install -r requirements.txt
streamlit run app.py
```
App will open at → [http://localhost:8501](http://localhost:8501)

---

## 🧩 Backend Requirements (`backend/requirements.txt`)
```
fastapi
uvicorn
faiss-cpu
openai
python-dotenv
python-multipart
numpy
pydantic
```

## 🎨 Frontend Requirements (`frontend/requirements.txt`)
```
streamlit
requests
PyPDF2
```

---

## 🚀 Deployment Guide

### Step 1️⃣ — Deploy Backend on Render
1. Go to [https://render.com](https://render.com)
2. Create a new **Web Service**
3. Connect your backend GitHub repo
4. Set start command:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 10000
   ```
5. Add environment variable:
   ```bash
   OPENAI_API_KEY=sk-your-openai-key
   ```
6. Click **Deploy**  
   After deployment, note your API URL:  
   👉 https://ai-interviewer-backend.onrender.com  
   Test it at `/docs` endpoint.

### Step 2️⃣ — Deploy Frontend on Streamlit Cloud
1. Go to [https://share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Select your **frontend repo**
4. Set main file: `app.py`
5. Add dependencies from `frontend/requirements.txt`
6. Click **Deploy**

### Step 3️⃣ — Connect Backend to Frontend
Edit in `frontend/app.py`:
```python
BACKEND_URL = "https://ai-interviewer-backend.onrender.com"
```
Push to GitHub → Streamlit redeploys automatically.

---

## 🧪 Testing Your App (Live)
Visit your Streamlit URL (e.g. [https://aendra-ai-interviewer.streamlit.app](https://aendra-ai-interviewer.streamlit.app))

- Upload your resume (PDF/TXT)
- Click “Start Interview”
- Answer questions sequentially
- Submit → View AI-generated evaluation

---

## 📂 Folder Summary
| File | Description |
|------|--------------|
| `backend/main.py` | FastAPI app with RAG + evaluation |
| `backend/data/` | ML/DL/AI text-based knowledge base |
| `backend/faiss_index.pkl` | Auto-generated FAISS index |
| `frontend/app.py` | Streamlit interview flow |
| `.env` | Local OpenAI key (excluded from repo) |

---

## 🔐 Example `.env`
```
OPENAI_API_KEY=sk-your-key-here
```

And add to `.gitignore`:
```
.env
__pycache__/
*.pkl
```

---

## 🧾 Example API Endpoints

### Generate Questions
`POST /generate_questions/`  
FormData: resume (file)

**Response:**
```json
{"questions": ["What is overfitting?", "..."]}
```

### Evaluate Answers
`POST /evaluate/`  
Body:
```json
{"qa_pairs": [{"question": "...", "answer": "..."}]}
```
**Response:**
```json
{"score": "Score: 85/100\nSummary: Strong understanding..."}
```

---

## 🚧 Future Enhancements
- Add authentication for interviewer/admin
- Store interviews in MongoDB / Firebase
- Add difficulty selector (easy / medium / hard)
- Voice-based interview (speech-to-text)
- Fine-tune custom LLM for interview domain

---

## 👤 Author
**Aendra Shukla**  
AI Engineer | ML Researcher | Full-Stack Developer  
📍 Lucknow, India  
📧 shuklaaendra123@gmail.com
