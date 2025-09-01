# BCT AI Agent 🧠

An intelligent AI assistant specialized in Central Bank of Tunisia (BCT) regulations and laws. This project implements a Retrieval-Augmented Generation (RAG) system that provides accurate, source-referenced answers from official BCT documents.

## Features

- **🔍 Intelligent Document Search**: Semantic search through BCT regulations and laws
- **🤖 AI-Powered Responses**: Context-aware answers using Llama 3
- **📚 Source Attribution**: Direct links to official BCT documents with page references
- **🔐 Secure Authentication**: Google OAuth 2.0 integration
- **🌐 Multilingual Support**: Handles both French and Arabic documents
- **📱 Modern Interface**: Responsive Vue.js frontend with glassmorphism design
- **⚡ Real-time Processing**: Fast document retrieval and answer generation

## Architecture

### Backend Stack
- **FastAPI**: High-performance API framework
- **Haystack**: Document indexing and retrieval pipeline
- **Elasticsearch**: Vector database for semantic search
- **Llama 3**: Large language model via Ollama
- **OAuth 2.0**: Google authentication

### Frontend Stack
- **Vue.js**: Progressive JavaScript framework
- **Modern CSS**: Glassmorphism design with responsive layout
- **Session Management**: Secure user authentication flow

### Document Processing
- **PyMuPDF**: PDF text extraction
- **Tesseract OCR**: Image-to-text conversion for scanned documents
- **Sentence Transformers**: Multilingual embeddings (E5-Large)
- **Semantic Chunking**: Context-aware document segmentation

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- Elasticsearch 7.x+
- Tesseract OCR
- Poppler (for PDF processing)
- Ollama with Llama 3 model

### Backend Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd bct-ai-agent
```

2. **Install Python dependencies**
```bash
pip install fastapi uvicorn haystack-ai elasticsearch sentence-transformers
pip install PyMuPDF pytesseract requests python-magic pdf2image
pip install beautifulsoup4 langdetect nltk pillow tqdm authlib
pip install python-dotenv python-multipart
```

3. **Install Tesseract OCR**
- Windows: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
- Update path in `indexing.py`: `pytesseract.pytesseract.tesseract_cmd`

4. **Install Poppler**
- Windows: Download from [Poppler releases](https://github.com/oschwartz10612/poppler-windows/releases)
- Update path in `indexing.py`: `poppler_path`

5. **Setup Elasticsearch**
```bash
# Using Docker
docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.17.0
```

6. **Install and run Ollama**
```bash
# Install Ollama from https://ollama.ai
ollama pull llama3
```

7. **Environment Configuration**
Create `.env` file:
```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### Frontend Setup

1. **Install Node.js dependencies**
```bash
cd frontend  # or your Vue.js directory
npm install vue@next
```

2. **Configure development server**
Update Vue.js dev server to run on port 8081

## Usage

### 1. Index BCT Documents
```bash
python indexing.py
```
This will:
- Scrape PDF documents from BCT official website
- Extract text using OCR when necessary
- Apply semantic chunking for better retrieval
- Store embeddings in Elasticsearch

### 2. Start the Backend
```bash
uvicorn main:app --reload --port 8000
```

### 3. Start the Frontend
```bash
npm run dev  # or your Vue.js start command
```

### 4. Access the Application
- Open `http://localhost:8081`
- Click "Se connecter avec Google"
- Ask questions about BCT regulations

## API Endpoints

### Authentication
- `GET /login` - Initiate Google OAuth flow
- `GET /auth/callback` - Handle OAuth callback
- `GET /api/user` - Get current user info
- `GET /logout` - Logout user

### Question Answering
- `POST /ask` - Submit question and get AI response
  ```json
  {
    "query": "Quelles sont les réglementations sur les changes?"
  }
  ```

## Project Structure

```
AI_AGENT_BCT/
├── backend/
│   ├── __pycache__/         # Python cache files
│   ├── app/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── indexing.py      # Document collection and indexing
│   │   ├── main.py          # FastAPI application
│   │   ├── reset_index.py   # Index reset utilities
│   │   ├── search.py        # Haystack search components
│   │   └── test.py          # Testing utilities
│   ├── venv/               # Python virtual environment
│   ├── data/               # Data storage
│   ├── temp_pdfs/          # Temporary PDF storage
│   ├── auth.py             # OAuth authentication
│   ├── in_req.py           # Requirements processing
│   ├── indexed_pdfs.txt    # Indexed documents tracking
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── node_modules/       # Node.js dependencies
│   ├── public/             # Static assets
│   ├── src/
│   │   ├── assets/         # Vue.js assets
│   │   ├── components/     # Vue components
│   │   └── App.vue         # Main Vue application
│   ├── main.js             # Vue.js entry point
│   ├── .browserslistrc     # Browser compatibility
│   ├── .gitignore          # Git ignore rules
│   ├── babel.config.js     # Babel configuration
│   ├── jsconfig.json       # JavaScript configuration
│   ├── package-lock.json   # Dependency lock file
│   ├── package.json        # Node.js dependencies
│   └── vue.config.js       # Vue.js configuration
├── .gitignore              # Root git ignore
└── README.md               # Project documentation
```

## Key Components

### Document Processing Pipeline
1. **PDF Collection**: Automatic scraping from BCT website
2. **Text Extraction**: Direct PDF text + OCR fallback
3. **Language Detection**: French/Arabic document handling
4. **Semantic Chunking**: Context-preserving text segmentation
5. **Vector Embedding**: Multilingual E5-Large model

### Search & Retrieval
1. **Embedding Search**: Initial semantic retrieval (top-k)
2. **Reranking**: Cross-encoder refinement for relevance
3. **Answer Generation**: Llama 3 with context injection
4. **Source Linking**: Direct BCT document references

## Configuration

### Elasticsearch Settings
- **Host**: localhost:9200
- **Index**: bct
- **Embedding Dimension**: 1024

### Models Used
- **Embedding**: `intfloat/multilingual-e5-large`
- **Reranker**: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- **LLM**: Llama 3 via Ollama

## Security Features

- OAuth 2.0 authentication with Google
- Session-based user management
- CORS protection
- Secure credential handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Acknowledgments

- Banque Centrale de Tunisie for providing official documentation
- Haystack team for the retrieval framework
- Meta for Llama 3 model
- Google for authentication services

