# RAG Service - Retrieval-Augmented Generation for Clinical Assessment

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com/)

> **A microservice that enhances depression diagnostic assessments with retrieval-augmented generation using DSM-5 clinical documentation.**

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Service](#-running-the-service)
- [Data Ingestion](#-data-ingestion)
- [API Documentation](#-api-documentation)
- [Usage Examples](#-usage-examples)
- [Troubleshooting](#-troubleshooting)
- [Development](#-development)
- [Performance](#-performance)
- [Security](#-security)

---

## 🎯 Overview

The RAG (Retrieval-Augmented Generation) Service is a Python FastAPI microservice that provides AI-powered clinical insights by combining:

1. **Semantic Search**: Retrieves relevant DSM-5 documentation using vector similarity
2. **Large Language Models**: Uses OpenAI GPT-4 to generate contextual clinical assessments
3. **Vector Database**: ChromaDB stores and searches embedded clinical documentation

### Purpose

This service augments rule-based MDD diagnosis with:

- **Clinical Context**: Retrieves relevant DSM-5 criteria and guidelines
- **Treatment Recommendations**: Evidence-based intervention suggestions
- **Differential Diagnosis**: Helps distinguish between similar conditions
- **Clinical Insights**: AI-generated contextual information for clinicians

### Position in System Architecture

```
Backend (Port 3000) → RAG Service (Port 8001) → OpenAI GPT-4 API
                            ↓
                      ChromaDB Vector Store
                  (DSM-5 Embedded Documents)
```

---

## ✨ Features

- ✅ **OpenAI GPT-4o Integration**: State-of-the-art language understanding
- ✅ **Semantic Search**: Vector similarity search using OpenAI embeddings
- ✅ **ChromaDB Vector Store**: Persistent, efficient embeddings database
- ✅ **DSM-5 Knowledge Base**: Ingests and indexes clinical documentation
- ✅ **Configurable Retrieval**: Adjustable top-k results and minimum relevance scores
- ✅ **Async API**: FastAPI with async/await for high performance
- ✅ **Structured Outputs**: Type-safe responses with Pydantic schemas
- ✅ **Health Monitoring**: Comprehensive health check endpoint
- ✅ **Error Handling**: Graceful degradation and detailed error messages
- ✅ **CORS Support**: Configurable cross-origin resource sharing
- ✅ **Docker Ready**: Containerized for easy deployment

---

## 🏗 Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                       RAG SERVICE (Port 8001)                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    FastAPI Application                       │  │
│  │  • /health           • /rag/query                            │  │
│  │  • CORS Middleware    • Request Validation                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                     RAG Pipeline                             │  │
│  │  • Orchestrates retrieval and generation                     │  │
│  │  • Combines patient text + symptoms + context                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│           ↓                                    ↓                    │
│  ┌─────────────────────────┐      ┌──────────────────────────┐    │
│  │  Retrieval Service      │      │   LLM Service            │    │
│  │  • Query embeddings     │      │   • Prompt construction  │    │
│  │  • Vector similarity    │      │   • GPT-4 API calls      │    │
│  │  • Result ranking       │      │   • Response parsing     │    │
│  └─────────────────────────┘      └──────────────────────────┘    │
│           ↓                                    ↓                    │
│  ┌─────────────────────────┐      ┌──────────────────────────┐    │
│  │  Embedding Service      │      │   OpenAI API             │    │
│  │  • text-embedding-3     │      │   • gpt-4o               │    │
│  │  • 1536 dimensions      │      │   • Max 4096 tokens      │    │
│  └─────────────────────────┘      └──────────────────────────┘    │
│           ↓                                                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              ChromaDB Vector Database                        │  │
│  │  • Persistent storage at ./data/chroma_db                    │  │
│  │  • Collection: dsm5                                          │  │
│  │  • Stores: embeddings + text chunks + metadata              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component          | Technology                   | Purpose                         |
| ------------------ | ---------------------------- | ------------------------------- |
| **Web Framework**  | FastAPI 0.109                | Async REST API                  |
| **Server**         | Uvicorn with standard extras | ASGI server                     |
| **LLM**            | OpenAI GPT-4o                | Natural language generation     |
| **Embeddings**     | text-embedding-3-small       | Semantic vector representations |
| **Vector DB**      | ChromaDB 0.4.22+             | Similarity search               |
| **PDF Parsing**    | PyMuPDF (fitz) 1.23+         | DSM-5 document extraction       |
| **Validation**     | Pydantic 2.5                 | Schema validation               |
| **Token Counting** | tiktoken 0.5+                | LLM token usage tracking        |
| **Retry Logic**    | tenacity 8.2+                | Fault-tolerant API calls        |

---

## 📦 Prerequisites

### Required

- **Python**: 3.10 or higher
- **OpenAI API Key**: Valid OpenAI API key with GPT-4 access
- **Disk Space**: ~500MB for dependencies + ChromaDB data

### Recommended

- **RAM**: 2GB minimum (4GB recommended)
- **Network**: Stable internet connection for OpenAI API calls

---

## 🚀 Installation

### 1. Navigate to RAG Service Directory

```bash
cd rag-service
```

### 2. Create Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python -c "import fastapi, chromadb, openai; print('✅ All dependencies installed')"
```

**Expected Output**: `✅ All dependencies installed`

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `rag-service/` directory:

```env
# OpenAI Configuration (REQUIRED)
OPENAI_API_KEY=sk-proj-your-api-key-here
OPENAI_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536
MAX_COMPLETION_TOKENS=4096
TEMPERATURE=0.2

# Server Configuration
HOST=0.0.0.0
PORT=8001
LOG_LEVEL=info

# ChromaDB Configuration
CHROMA_PERSIST_DIR=./data/chroma_db
CHROMA_COLLECTION_NAME=dsm5

# Retrieval Configuration
RETRIEVAL_TOP_K=8
RETRIEVAL_MIN_SCORE=0.3

# Document Processing
CHUNK_SIZE=800
CHUNK_OVERLAP=150

# CORS
ENABLE_CORS=true
```

### Configuration Parameters

| Parameter                | Type   | Default                  | Description                                     |
| ------------------------ | ------ | ------------------------ | ----------------------------------------------- |
| `OPENAI_API_KEY`         | string | **(Required)**           | Your OpenAI API key                             |
| `OPENAI_MODEL`           | string | `gpt-4o`                 | OpenAI model to use                             |
| `EMBEDDING_MODEL`        | string | `text-embedding-3-small` | Embedding model for vectors                     |
| `EMBEDDING_DIMENSIONS`   | int    | `1536`                   | Dimension of embedding vectors                  |
| `MAX_COMPLETION_TOKENS`  | int    | `4096`                   | Max tokens in LLM response                      |
| `TEMPERATURE`            | float  | `0.2`                    | LLM temperature (0.0-2.0, lower = more focused) |
| `HOST`                   | string | `0.0.0.0`                | Server bind address                             |
| `PORT`                   | int    | `8001`                   | Server port                                     |
| `LOG_LEVEL`              | string | `info`                   | Logging level (debug/info/warning/error)        |
| `CHROMA_PERSIST_DIR`     | string | `./data/chroma_db`       | ChromaDB storage path                           |
| `CHROMA_COLLECTION_NAME` | string | `dsm5`                   | ChromaDB collection name                        |
| `RETRIEVAL_TOP_K`        | int    | `8`                      | Number of documents to retrieve                 |
| `RETRIEVAL_MIN_SCORE`    | float  | `0.3`                    | Minimum relevance score (0.0-1.0)               |
| `CHUNK_SIZE`             | int    | `800`                    | Characters per document chunk                   |
| `CHUNK_OVERLAP`          | int    | `150`                    | Overlap between chunks                          |
| `ENABLE_CORS`            | bool   | `true`                   | Enable CORS middleware                          |

---

## 🏃 Running the Service

### Development Mode

```bash
# Ensure virtual environment is activated
cd rag-service
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start the service
python -m app.main
```

**Output:**

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     RAG service started on 0.0.0.0:8001
INFO:     OpenAI model: gpt-4o
INFO:     Embedding model: text-embedding-3-small
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Production Mode (with Uvicorn)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 4
```

### Docker

```bash
# Build image
docker build -t rag-service .

# Run container
docker run -d \
  -p 8001:8001 \
  -e OPENAI_API_KEY=your-key-here \
  -v $(pwd)/data:/data \
  --name rag-service \
  rag-service
```

### Verify Service is Running

```bash
curl http://localhost:8001/health
```

**Expected Response:**

```json
{
  "status": "healthy",
  "service": "rag-service",
  "version": "1.0.0",
  "openai_model": "gpt-4o",
  "embedding_model": "text-embedding-3-small",
  "chromadb_status": "ready",
  "document_count": 245
}
```

---

## 📂 Data Ingestion

Before the RAG service can provide clinical insights, you must ingest DSM-5 documentation into ChromaDB.

### Prerequisites for Ingestion

- DSM-5-TR PDF file (obtain legally from APA or your institution)
- Adequate disk space (~100MB for processed data)
- OpenAI API key (for generating embeddings)

### Ingestion Script Usage

#### Basic Ingestion

```bash
cd rag-service
python scripts/ingest_pdf.py --pdf /path/to/DSM-5-TR.pdf
```

#### With Custom Options

```bash
python scripts/ingest_pdf.py \
  --pdf /path/to/DSM-5-TR.pdf \
  --collection dsm5 \
  --chunk-size 800 \
  --chunk-overlap 150 \
  --dry-run  # Preview without actually ingesting
```

### Ingestion Process

The script performs the following steps:

1. **Extract Text**: Parses PDF page by page using PyMuPDF
2. **Detect Structure**: Identifies disorder sections and headings
3. **Chunk Documents**: Splits text into semantic chunks with overlap
4. **Generate Embeddings**: Creates vector embeddings using OpenAI
5. **Store in ChromaDB**: Persists embeddings with metadata
6. **Verify**: Confirms successful ingestion

### Script Parameters

| Parameter         | Type   | Default        | Description                      |
| ----------------- | ------ | -------------- | -------------------------------- |
| `--pdf`           | string | **(Required)** | Path to DSM-5 PDF file           |
| `--collection`    | string | `dsm5`         | ChromaDB collection name         |
| `--chunk-size`    | int    | `800`          | Max characters per chunk         |
| `--chunk-overlap` | int    | `150`          | Character overlap between chunks |
| `--dry-run`       | flag   | `false`        | Preview without ingesting        |

### Example Output

```
Opening PDF: DSM-5-TR.pdf
Extracted text from 987 pages (out of 991 total)
Detected 45 disorder sections
Created 245 semantic chunks
Generating embeddings... [========================================] 245/245
Storing in ChromaDB collection: dsm5
✅ Successfully ingested 245 documents
   Total tokens: 186,420
   Estimated cost: $0.37
   Time elapsed: 3m 42s
```

### Verifying Ingestion

```bash
# Check service health to see document count
curl http://localhost:8001/health

# Test retrieval
curl -X POST http://localhost:8001/rag/query \
  -H "Content-Type: application/json" \
  -d '{"text": "What are the criteria for major depressive disorder?"}'
```

---

## 📚 API Documentation

### Interactive Documentation

Once the service is running, access interactive API documentation:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### Endpoints

#### 1. Health Check

**GET** `/health`

Returns service health status and configuration.

**Response:**

```json
{
  "status": "healthy",
  "service": "rag-service",
  "version": "1.0.0",
  "openai_model": "gpt-4o",
  "embedding_model": "text-embedding-3-small",
  "chromadb_status": "ready",
  "document_count": 245
}
```

#### 2. RAG Query

**POST** `/rag/query`

Performs retrieval-augmented generation for clinical assessment.

**Request Body:**

```json
{
  "text": "Patient has been feeling depressed for 3 weeks with loss of interest",
  "symptoms": [
    {
      "code": "A1",
      "name": "Depressed Mood",
      "confidence": 0.85,
      "evidence": "feeling depressed"
    },
    {
      "code": "A2",
      "name": "Anhedonia",
      "confidence": 0.9,
      "evidence": "loss of interest"
    }
  ],
  "metadata": {
    "patient_age": 35,
    "gender": "female",
    "duration_weeks": 3
  },
  "disorder_filter": "296"
}
```

**Request Schema:**

| Field             | Type          | Required | Description                              |
| ----------------- | ------------- | -------- | ---------------------------------------- |
| `text`            | string        | Yes      | Patient symptom description              |
| `symptoms`        | array[object] | No       | Pre-extracted symptoms from NLP service  |
| `metadata`        | object        | No       | Additional patient context               |
| `disorder_filter` | string        | No       | DSM-5 disorder code filter (e.g., "296") |

**Response:**

```json
{
  "success": true,
  "assessment": "Based on the clinical presentation, the patient meets DSM-5 criteria for Major Depressive Disorder...",
  "relevant_criteria": [
    "DSM-5 Criterion A: Five or more symptoms present...",
    "Duration criterion met with 3 weeks of symptoms..."
  ],
  "recommendations": [
    "Consider evidence-based psychotherapy (CBT or IPT)",
    "Assess need for antidepressant medication",
    "Rule out medical causes and substance-induced symptoms"
  ],
  "confidence": 0.88,
  "sources": [
    {
      "text": "Major Depressive Disorder diagnostic criteria...",
      "relevance_score": 0.92,
      "page": 165,
      "disorder": "Major Depressive Disorder"
    }
  ],
  "processing_time_ms": 2341
}
```

**Error Responses:**

- **503 Service Unavailable**: RAG pipeline not initialized

  ```json
  {
    "detail": "RAG service not fully initialized"
  }
  ```

- **400 Bad Request**: Invalid request format

  ```json
  {
    "detail": "Validation error: text field is required"
  }
  ```

- **500 Internal Server Error**: OpenAI API error or system failure
  ```json
  {
    "detail": "OpenAI API error: Rate limit exceeded"
  }
  ```

---

## 💡 Usage Examples

### Example 1: Basic Query

```bash
curl -X POST http://localhost:8001/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Patient reports feeling sad and hopeless for 4 weeks, with sleep problems and loss of appetite."
  }'
```

### Example 2: Query with Symptoms

```bash
curl -X POST http://localhost:8001/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Experiencing persistent sadness and fatigue",
    "symptoms": [
      {"code": "A1", "name": "Depressed Mood", "confidence": 0.9},
      {"code": "A6", "name": "Fatigue", "confidence": 0.85}
    ]
  }'
```

### Example 3: Python Client

```python
import requests

response = requests.post(
    "http://localhost:8001/rag/query",
    json={
        "text": "Patient shows symptoms of major depression",
        "symptoms": [
            {"code": "A1", "name": "Depressed Mood", "confidence": 0.9},
            {"code": "A2", "name": "Anhedonia", "confidence": 0.85}
        ],
        "metadata": {
            "patient_age": 42,
            "duration_weeks": 6
        }
    }
)

result = response.json()
print(f"Assessment: {result['assessment']}")
print(f"Confidence: {result['confidence']}")
```

### Example 4: JavaScript/Node.js Client

```javascript
const axios = require('axios');

const response = await axios.post('http://localhost:8001/rag/query', {
  text: 'Patient experiencing severe depression with suicidal thoughts',
  symptoms: [
    { code: 'A1', name: 'Depressed Mood', confidence: 0.95 },
    { code: 'A9', name: 'Suicidal Ideation', confidence: 0.88 },
  ],
});

console.log('Assessment:', response.data.assessment);
console.log('Recommendations:', response.data.recommendations);
```

---

## 🔧 Troubleshooting

### Issue 1: OpenAI API Key Not Found

**Error:**

```
OPENAI_API_KEY not set! RAG service will not function.
```

**Solution:**

1. Create `.env` file in `rag-service/` directory
2. Add: `OPENAI_API_KEY=sk-proj-your-key-here`
3. Restart the service

### Issue 2: ChromaDB Collection Empty

**Error:**

```
ChromaDB collection is empty! Run the ingestion script first.
```

**Solution:**

```bash
python scripts/ingest_pdf.py --pdf /path/to/DSM-5-TR.pdf
```

### Issue 3: Rate Limit Exceeded

**Error:**

```
OpenAI API error: Rate limit exceeded
```

**Solution:**

- Wait and retry (rate limits reset after time)
- Upgrade your OpenAI API plan for higher limits
- Implement request queuing in your application

### Issue 4: Out of Memory

**Error:**

```
MemoryError: Unable to allocate array
```

**Solution:**

- Reduce `CHUNK_SIZE` and `RETRIEVAL_TOP_K` in `.env`
- Increase system RAM
- Use a smaller embedding model dimension

### Issue 5: Slow Response Times

**Symptoms:** Queries take >5 seconds

**Solutions:**

1. **Reduce retrieval size**: Set `RETRIEVAL_TOP_K=3`
2. **Cache embeddings**: ChromaDB already does this
3. **Use faster model**: Switch to `gpt-4o-mini` (less accurate but faster)
4. **Check network**: Ensure stable connection to OpenAI

### Issue 6: Cannot Connect to Service

**Error:**

```
Connection refused at http://localhost:8001
```

**Solution:**

```bash
# Check if service is running
curl http://localhost:8001/health

# Check port is not in use
netstat -ano | findstr :8001  # Windows
lsof -i :8001                  # macOS/Linux

# Restart service with verbose logging
LOG_LEVEL=debug python -m app.main
```

---

## 🛠 Development

### Project Structure

```
rag-service/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py              # API endpoints
│   │   └── schemas.py             # Pydantic request/response models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── rag_pipeline.py        # Main RAG orchestration
│   │   ├── embedding_service.py   # OpenAI embeddings client
│   │   ├── retrieval_service.py   # ChromaDB vector search
│   │   └── llm_service.py         # OpenAI GPT-4 client
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── system_prompt.py       # LLM system instructions
│   │   └── query_templates.py     # Query formatting
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py            # Configuration management
│   └── utils/
│       ├── __init__.py
│       └── logger.py              # Logging setup
├── data/
│   └── chroma_db/                 # Persistent vector database
├── scripts/
│   └── ingest_pdf.py              # DSM-5 PDF ingestion
├── .env                           # Environment variables (create this)
├── .env.example                   # Environment template
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container image
└── README.md                      # This file
```

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

### Code Style

```bash
# Format code
black app/

# Lint
pylint app/

# Type checking
mypy app/
```

### Adding New Features

1. **Create feature branch**: `git checkout -b feature/new-feature`
2. **Implement changes** in appropriate service/module
3. **Add tests** in `tests/` directory
4. **Update documentation** in this README
5. **Submit pull request** with clear description

---

## ⚡ Performance

### Benchmarks

Typical performance on standard hardware:

| Operation            | Latency (p50) | Latency (p95) | Notes                    |
| -------------------- | ------------- | ------------- | ------------------------ |
| Health check         | 5ms           | 15ms          | No external calls        |
| Embedding generation | 150ms         | 300ms         | OpenAI API call          |
| Vector search        | 20ms          | 50ms          | ChromaDB local           |
| GPT-4 completion     | 2000ms        | 5000ms        | Depends on output length |
| **Full RAG query**   | **2500ms**    | **6000ms**    | End-to-end               |

### Optimization Tips

1. **Reduce retrieval documents**: Lower `RETRIEVAL_TOP_K` to 3-5
2. **Use smaller models**: `gpt-4o-mini` for faster responses
3. **Implement caching**: Cache common queries at application level
4. **Batch requests**: If possible, batch multiple assessments
5. **Optimize chunks**: Smaller chunks = faster retrieval, but less context

---

## 🔒 Security

### Best Practices

1. **API Key Protection**:
   - Never commit `.env` file to version control
   - Use environment variables in production
   - Rotate API keys regularly

2. **Access Control**:
   - Implement authentication middleware
   - Use API gateway for rate limiting
   - Restrict network access in production

3. **Data Privacy**:
   - Patient data is not persisted in ChromaDB
   - Logs are sanitized to remove PHI
   - OpenAI: Review their data usage policies

4. **CORS Configuration**:
   - Set specific allowed origins in production
   - Disable CORS if not needed

### HIPAA Considerations

- OpenAI: Requires Business Associate Agreement (BAA)
- ChromaDB storage: Ensure encrypted at rest
- Audit trails: Implement logging of all API calls
- Data retention: Configure appropriate retention policies

---

## 📞 Support

For issues specific to the RAG service:

- Check service logs: `docker logs rag-service` or console output
- Review OpenAI status: https://status.openai.com/
- Check ChromaDB documentation: https://docs.trychroma.com/

For general project support, see the [main README](../README.md).

---

## 📄 License

This service is part of the AI Psychologist project, licensed under the MIT License.

**OpenAI Usage**: Subject to [OpenAI Terms of Use](https://openai.com/policies/terms-of-use).

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Maintainer**: AI Psychologist Development Team
