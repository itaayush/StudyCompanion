# 📚 StudyCompanion — AI-Powered PDF Learning Engine

StudyCompanion is a **Retrieval-Augmented Generation (RAG)** system that transforms any PDF into an intelligent AI tutor. Upload documents, ask questions, and receive contextual answers with exact page citations.

## ✨ Features

- **📄 Smart Document Indexing**: Upload PDFs and instantly create a searchable vector database
- **🤖 AI-Powered Responses**: Get accurate answers grounded in your document's content
- **📍 Page Citations**: Every answer includes exact page references
- **⚡ Lightning-Fast Retrieval**: Semantic search powered by vector embeddings
- **🎨 Modern UI**: Clean, intuitive interface with gradient cyan theme

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI (Python) |
| **Vector Database** | Chroma DB (local persistence) |
| **Embeddings** | Google Generative AI (Gemini Embedding) |
| **LLM** | Google Generative AI (Gemini 3.6 Flash) |
| **Text Processing** | LangChain, PyPDF |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |

## 📋 Project Structure

```
StudyCompanion/
├── index.html              # Modern responsive UI
├── style.css               # Cyan gradient theme
├── script.js               # Frontend API client
├── main.py                 # FastAPI server
├── indexingpipe.py         # PDF indexing pipeline
├── retrivepipeline.py      # Query & response pipeline
├── requirements.txt        # Python dependencies
└── chroma_db/              # Local vector database
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Cloud API key (for Gemini embeddings & LLM)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file with your Google API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

### 3. Start the Backend Server

```bash
python main.py
```

The API will run at `http://127.0.0.1:8000`

### 4. Start the Frontend Server

Open a new terminal and run:

```bash
python -m http.server 5500
```

You'll see in the console:
```
Serving at http://127.0.0.1:5500/
```

Open your browser and navigate to: **http://127.0.0.1:5500/**

## 📖 How It Works

### Indexing Pipeline
1. Upload a PDF via the frontend
2. System extracts pages and chunks text
3. Chunks are embedded using Gemini embeddings
4. Vectors are stored in local Chroma database
5. Collection becomes "active" for queries

### Query Pipeline
1. User asks a question
2. Question is embedded and searched against the document
3. Top-4 relevant chunks are retrieved
4. Context + question sent to Gemini LLM
5. AI generates grounded answer with page citations

## 🔌 API Endpoints

### `POST /upload-pdf`

Upload and index a PDF document.

**Request:**
- Form field: `file` (PDF file)

**Response:**
```json
{
  "status": "success",
  "message": "'MyDocument.pdf' has been indexed successfully.",
  "collection": "mydocument"
}
```

### `POST /chat`

Ask a question about the indexed document.

**Request:**
- Form field: `question` (string)

**Response:**
```json
{
  "status": "success",
  "answer": "The answer to your question based on the document...",
  "pages": ["5", "12", "15"]
}
```

## ⚙️ Configuration

### Model Settings
- **Embedding Model**: `models/gemini-embedding-001`
- **LLM**: `gemini-3.6-flash`
- **Temperature**: 0.2 (for consistent, factual responses)

### Chunking Strategy
- Chunk Size: 1000 characters
- Chunk Overlap: 400 characters
- Retrieval: Top-4 most relevant chunks

### CORS Settings
- Enabled for all origins (`"*"`)
- Production: Restrict to your domain

## 📝 Example Usage

1. **Upload a PDF**: Click "Upload PDF" and select any technical document
2. **Ask Questions**: Type "What is X?" in the query box
3. **View Results**: Get instant answers with page references

## 🐛 Troubleshooting

### "RESOURCE_EXHAUSTED" Error
- Google API quota exceeded
- Solution: Wait 1 hour or request quota increase in [Google Cloud Console](https://console.cloud.google.com)

### "No document indexed yet"
- No PDF has been uploaded
- Solution: Upload a PDF first via the upload section

### API Connection Error
- Backend server not running
- Solution: Ensure `python main.py` is running on port 8000

## 🛠️ Development

### Local Testing
```bash
# Terminal 1: Backend API
python main.py

# Terminal 2: Frontend Server
python -m http.server 5500
```

### View Logs
- Frontend: Check browser console (F12 → Console tab)
- Backend: Check terminal where `python main.py` is running

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve StudyCompanion.

---

**Transform your PDFs into intelligent learning companions today!** 🎓✨
