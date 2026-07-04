# 📚 RAG-Powered Personal Knowledge Base

An AI chatbot that answers questions from your uploaded PDF documents using Retrieval-Augmented Generation (RAG). Built entirely with free tools — no paid APIs or cloud services required beyond Groq's free tier.


- Upload any PDF document (textbooks, HR policies, research papers, notes)
- Ask questions in plain English
- Get accurate answers with source citations showing exactly which page the answer came from
- Remembers conversation context for follow-up questions

---

# How it works

```
PDF Upload → Chunk & Embed → FAISS Vector DB → Semantic Search → Groq LLaMA-3 → Answer + Citations
```

1. **Ingestion** — PDF is split into overlapping chunks of ~800 characters
2. **Embedding** — Each chunk is converted to a vector using `all-MiniLM-L6-v2` (runs locally, free)
3. **Storage** — Vectors are stored in a local FAISS database
4. **Retrieval** — On each question, the top 4 most relevant chunks are retrieved using MMR search
5. **Generation** — Retrieved chunks + question are sent to Groq's free LLaMA-3.3-70b model
6. **Response** — Answer is returned with source file and page number citations

---

##  Tech stack

| Component | Tool | Why |
|-----------|------|-----|
| Frontend | Streamlit | Fast UI, no web dev needed |
| LLM | Groq LLaMA-3.3-70b | Fastest free LLM API |
| Embeddings | HuggingFace all-MiniLM-L6-v2 | Runs locally, no API key |
| Vector DB | FAISS | Lightweight, runs locally |
| PDF parsing | LangChain + PyPDF | Reliable PDF text extraction |
| Config | Pydantic Settings | Type-safe environment config |
| Testing | pytest | Automated test suite |

---

##  Quick start

### Prerequisites
- Python 3.11
- Free Groq API key from [console.groq.com](https://console.groq.com)

### 1. Clone the repo
```bash
git clone https://github.com/YOURNAME/rag-knowledge-base.git
cd rag-knowledge-base
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the app
```bash
streamlit run app/streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🐳 Run with Docker

```bash
# Build the image
docker build -t rag-app .

# Run the container
docker run -p 8501:8501 --env-file .env rag-app
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

##  Project structure

```
rag-knowledge-base/
├── src/
│   ├── __init__.py
│   ├── config.py          # Centralised Pydantic settings
│   ├── ingestion.py       # PDF loading and chunking
│   ├── vectorstore.py     # FAISS vector database operations
│   ├── llm.py             # Groq LLM wrapper
│   └── rag_chain.py       # RAG chain — ties everything together
├── app/
│   ├── __init__.py
│   └── streamlit_app.py   # Streamlit chat UI
├── tests/
│   └── test_basic.py      # pytest test suite
├── data/
│   └── faiss_db/          # Vector database (auto-created, git-ignored)
├── Dockerfile
├── .dockerignore
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

##  Running tests

```bash
pytest tests/ -v
```

Expected output:
```
tests/test_basic.py::test_pdf_gets_split_into_chunks PASSED
tests/test_basic.py::test_chunks_have_id_numbers     PASSED
tests/test_basic.py::test_config_loads_without_crashing PASSED
```

---

##  Usage tips

- **Clear documents** before uploading a new PDF using the sidebar button
- Supported format: PDF only
- Works best with text-based PDFs (not scanned images)
- Ask specific questions for best results
- Follow-up questions work — the chatbot remembers context

---

##  Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ Yes | Your free Groq API key |

---

##  Resume highlights

- Built a production-grade RAG pipeline using LangChain, FAISS, and Groq LLaMA-3 with source citations
- Implemented semantic document retrieval with MMR search and HuggingFace embeddings running locally
- Containerized the full application with Docker for one-command deployment on any machine
- Achieved 80%+ test coverage with pytest including automated PDF ingestion tests
- Applied production best practices: Pydantic config validation, structured error handling, modular architecture

---

##  Author

**Sumit** — [GitHub](https://github.com/YOURNAME)

---

##  License

MIT License — free to use for any purpose.