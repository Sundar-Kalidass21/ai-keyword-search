# Hybrid AI Product Search POC

A production-level Proof of Concept for an AI-powered hybrid search engine. This system combines **Elasticsearch** (keyword search), **FAISS** (semantic vector search), and **Hybrid Ranking** to deliver highly relevant product search results.

## 🚀 Features
- **Hybrid Search**: Merges keyword-based BM25 scores with semantic cosine similarity.
- **Semantic Understanding**: Uses `sentence-transformers` to understand user intent beyond keywords.
- **Filter Extraction**: Automatically parses queries like "under 50k" or "laptop" into structured filters.
- **Explanation**: Returns reasoning for search rankings (e.g., "Matched semantic meaning", "High rating").
- **Scalable Architecture**: Built with FastAPI, Docker, and Hexagonal Architecture principles.

## 🏗 Architecture
- **Backend API**: FastAPI (Python 3.11)
- **Keyword Search**: Elasticsearch 8.x
- **Vector Search**: FAISS (Facebook AI Similarity Search)
- **Metadata Store**: MongoDB
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`

## 🛠 Prerequisites
- **Docker** & **Docker Compose**
- **Python 3.11+**

## ⚡ Quick Start

### 1. Start Infrastructure
Launch Elasticsearch and MongoDB containers:
```bash
docker-compose up -d elasticsearch mongodb
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Ingest Data
Load sample products, generate embeddings, and index data:
```bash
# Windows (PowerShell)
$env:PYTHONPATH="."; python app/services/ingestion.py

# Linux/Mac
export PYTHONPATH=.; python app/services/ingestion.py
```

### 4. Run the API
Start the FastAPI server:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
The API will be available at [http://localhost:8000](http://localhost:8000).

## 📖 API Documentation
Interactive Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### Search Endpoint
`GET /api/v1/search`

**Parameters:**
- `q`: Search query (e.g., "noise cancelling headphones")
- `limit`: Number of results (default: 10)

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/search?q=laptop&limit=5"
```

**Example Response:**
```json
{
  "results": [
    {
      "product": {
        "title": "Dell XPS 13",
        "price": 120000,
        ...
      },
      "score": 0.85,
      "explanation": [
        "Semantic match (0.78)",
        "Keyword match (0.92)",
        "High rating (4.5)"
      ]
    }
  ],
  "execution_time_ms": 45.2
}
```

## 📂 Project Structure
```
hybrid_search/
├── app/
│   ├── api/            # API Endpoints
│   ├── core/           # Config & Logging
│   ├── models/         # Pydantic Models
│   ├── services/       # Business Logic
│   │   ├── nlp/        # Embeddings & Query Parsing
│   │   ├── search/     # ES, FAISS, Ranking Adapters
│   │   └── ingestion.py
│   └── main.py
├── data/               # Data storage (CSV, FAISS index)
├── docker/             # Dockerfiles
└── docker-compose.yml
```
