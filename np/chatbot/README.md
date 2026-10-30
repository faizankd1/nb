# 📄 Offline Document Intelligence Chatbot

An AI-powered, local-only document chatbot. Upload documents and ask questions grounded in their contents. Built using **FastAPI, Streamlit, ChromaDB, SQLite, and Ollama**, it supports offline inference and persistent local storage.

## 🚀 Features

- **Offline AI:** Run language models locally using Ollama.
- **Multi-Format Support:** Process PDFs, Word documents, spreadsheets, images, presentations, and more.
- **Grounded RAG Chat:** Generate answers from relevant document content; unrelated questions return a clear no-relevant-information response.
- **Hybrid Retrieval & Verification:** Combine semantic and exact-term matching, then verify that each draft answer is supported by the retrieved evidence.
- **Visible Citations:** Show the filenames and source locations used for every answer.
- **Persistent Storage:** Preserve uploaded files, extracted text, metadata, and embeddings across restarts.
- **Multi-Question Support:** Answer each explicitly separated question in one message.
- **Background Processing:** Process documents asynchronously using an ingestion queue.
- **OCR Support:** Extract text from scanned documents and images using Tesseract.
- **Duplicate Detection:** Identify duplicate uploads using SHA-256 hashing.
- **Recovery Mechanism:** Recover interrupted ingestion operations.
- **Explicit Deletion:** Documents are not automatically deleted as temporary cache.

## 🏗️ Architecture

```text
Streamlit UI
     |
     v
FastAPI Backend
     |
     +---- Document Ingestion
     |          |
     |          +---- Text Extraction / OCR
     |          +---- Chunking
     |          +---- Ollama Embeddings
     |          +---- ChromaDB Indexing
     |
     +---- RAG Chat
                |
                +---- Local Document Retrieval
                +---- Ollama LLM
                +---- Grounded Answers

Persistent Storage:
├── data/uploads/     - Original documents
├── data/extracted/   - Extracted text
├── data/chroma_db/   - Vector embeddings
├── data/metadata/    - SQLite database
└── data/logs/        - Application logs
```

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| FastAPI | Backend API |
| Streamlit | User interface |
| ChromaDB | Vector storage |
| SQLite | Metadata and job tracking |
| Ollama | Local LLM and embeddings |
| Tesseract OCR | Scanned document extraction |

## ⚙️ Installation

**Prerequisites:** Python 3.11+, Ollama, and Tesseract OCR if scanned-document processing is required.

### 1. Clone the Repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd offline_document_chatbot
```

### 2. Create a Virtual Environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Install Local AI Models

```powershell
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

### 4. Configure Environment Variables

```powershell
Copy-Item .env.example .env
```

Configure the settings in `.env`. Never commit this file to GitHub. The application is deliberately local-only and has no login or network-facing authentication layer.

### 5. Start the Backend

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 6. Start the Frontend

Open another terminal:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app/ui/streamlit_app.py --server.address 127.0.0.1 --server.port 8501
```

**Access the application:** http://127.0.0.1:8501

**API documentation:** http://127.0.0.1:8000/docs

## 🔐 Data Persistence & Security

- Uploaded documents and indexed data are stored permanently until explicitly deleted.
- This build is single-user and intended for one local computer.
- Keep services bound to `127.0.0.1`; do not expose them to a network without adding proper authentication and authorization.
- Runtime data is stored in the configurable `data/` directory.
- Back up the complete data directory regularly.
- Keep services bound to `127.0.0.1` for local-only access.
- Verify authentication and user isolation before network deployment.

**Important:** Persistent storage does not replace backups. RAG reduces unsupported answers but cannot guarantee that every response is correct.

Answer verification performs one additional local model call for supported answers. Set `VERIFY_ANSWERS=false` in `.env` if faster responses are more important than this extra guardrail.

Exact-term matching uses a local SQLite FTS5 index. It is especially useful for dates, names, invoice numbers, IDs, and values in tabular documents; it remains fully offline.

## 📂 Supported Formats

PDF, DOCX, TXT, Markdown, logs, HTML, RTF, ODT, JPG, JPEG, PNG, TIFF, BMP, WEBP, XLSX, XLSM, CSV, ODS, PPTX, JSON, XML, YAML, and EML.

OCR requires Tesseract. Legacy XLS and PPT files may require conversion.

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check application status |
| POST | `/documents/upload` | Upload documents |
| GET | `/documents` | List documents |
| DELETE | `/documents/{document_id}` | Delete a document |
| POST | `/chat` | Ask document-based questions |
| POST | `/admin/reconcile` | Recover incomplete operations |
| GET | `/admin/recovery-events` | View recovery events |

Refer to the running API documentation for actual request schemas and available routes.

## 📌 Key Objectives

- Keep AI processing local.
- Preserve documents and embeddings across restarts.
- Abstain instead of guessing when uploaded documents do not support an answer.
- Improve ingestion performance through background processing.
- Generate answers grounded in uploaded documents.

