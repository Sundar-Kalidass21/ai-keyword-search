# Hybrid Product Search System POC - Implementation Plan

## Goal Description
Build a production-ready POC for an AI-powered hybrid product search engine. This system will combine keyword search (Elasticsearch) with semantic search (FAISS + Sentence Transformers) and use a custom ranking algorithm to serve the best results.

## Architecture

We will follow a clean **Hexagonal/Clean Architecture** inspired structure, separating core domain logic, infrastructure adapters, and API interfaces.

### Tech Stack
- **Framework**: FastAPI
- **Language**: Python 3.11
- **Database (Metadata)**: MongoDB
- **Search Engine (Keyword)**: Elasticsearch
- **Vector Store (Semantic)**: FAISS (In-memory/Flat for POC, persistance via pickling or disk write)
- **ML Model**: `sentence-transformers/all-MiniLM-L6-v2` (Lightweight, good for POC)
- **Containerization**: Docker & Docker Compose

### Folder Structure
```
hybrid_search_poc/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   └── endpoints/
│   │   │       └── search.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── models/           # Pydantic models (Domain entities)
│   │   ├── product.py
│   │   └── search.py
│   ├── services/
│   │   ├── ingestion.py
│   │   ├── nlp/
│   │   │   ├── embedding.py
│   │   │   └── query_parser.py
│   │   ├── search/
│   │   │   ├── elastic_adapter.py
│   │   │   ├── faiss_adapter.py
│   │   │   ├── mongo_adapter.py
│   │   │   └── ranker.py
│   └── main.py
├── data/
│   └── products.csv
├── docker/
│   └── app.Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

## Proposed Changes

### 1. Infrastructure Setup
- **`docker-compose.yml`**: Define services for Elasticsearch (single node), MongoDB, and the FastAPI app.
- **`requirements.txt`**: `fastapi`, `uvicorn`, `elasticsearch`, `pymongo`, `faiss-cpu`, `sentence-transformers`, `numpy`, `pandas`, `pydantic-settings`.

### 2. Core Modules & Services

#### `app/models/`
- **`product.py`**:
    - `Product` (id, title, description, price, rating, brand, category)
- **`search.py`**:
    - `SearchResponse` (product, score, explanation)

#### `app/services/mongo_service.py`
- Handles storing and retrieving product metadata.

#### `app/services/search/elastic_service.py`
- Connects to ES.
- Creates index with fuzzy search capabilities.
- Executes keyword search.

#### `app/services/search/faiss_service.py`
- Manages FAISS index.
- Adds vectors.
- Searches vectors.
- **Note**: For POC, we will rebuild the index on startup or provide a save/load mechanism.

#### `app/services/nlp/embedding.py`
- Wraps `SentenceTransformer` to generate embeddings.

#### `app/services/nlp/query_parser.py`
- Extracts filters (e.g., "under 50k" -> price < 50000).
- Cleans query for ES/Vector search.

#### `app/services/search/ranker.py`
- Implements the hybrid scoring formula:
  `final_score = 0.5 * semantic + 0.3 * elastic + 0.1 * rating + 0.1 * price`
- Generates explanations.

### 3. Ingestion Pipeline
- **`app/services/ingestion.py`**:
    - Reads CSV.
    - Generates embeddings.
    - Pushes to MongoDB, ES, and FAISS.

### 4. API Layer
- **`app/main.py`**: App entry point.
- **`app/api/v1/endpoints/search.py`**: `GET /search` endpoint.

## Verification Plan

### Automated Verification
- We will write a simple test script `test_search.py` to hit the API (running locally or in docker) and verify the structure of the response and that results are returned.

### Manual Verification
- Verify Docker containers come up healthy.
- Check logs for ingestion success.
- Perform sample queries via `curl` or docs UI:
    - "iphone under 1000" (check filter extraction)
    - "laptop" (check hybrid results)
