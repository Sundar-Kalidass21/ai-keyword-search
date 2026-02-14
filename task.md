# Hybrid Product Search POC

## 1. Project Setup & Architecture
- [x] Initialize project structure and environment
- [x] Create `docker-compose.yml` for Elasticsearch, MongoDB
- [x] Create `requirements.txt` and install dependencies
- [x] Set up `app/core/config.py` (Settings management)

## 2. Infrastructure & Models
- [x] Implement Pydantic models for Product and Search
- [x] Implement MongoDB connection and service
- [x] Implement Elasticsearch connection and service
- [x] Implement FAISS service for vector storage
- [x] Implement Embedding service (SentenceTransformer)

## 3. Ingestion Pipeline
- [x] Create sample product data (CSV)
- [x] Implement Product Ingestion Script
    - [x] Load from CSV
    - [x] Generate Embeddings
    - [x] Index to MongoDB (Metadata)
    - [x] Index to Elasticsearch (Keyword)
    - [x] Index to FAISS (Vectors)

## 4. Search & Ranking Logic
- [x] Implement Query Understanding Module
    - [x] Text cleaning
    - [x] Filter extraction (price, category)
- [x] Implement Hybrid Search
    - [x] Elasticsearch query builder
    - [x] FAISS similarity search
- [x] Implement Ranking Service
    - [x] Combine scores (Semantic + Keyword + Rating + Price)
    - [x] Generate explanations

## 5. API Development
- [x] Create FastAPI app and Search Endpoint
- [x] Implement dependency injection
- [x] Add logging/middleware

## 6. Dockerization & Final Polish
- [x] Create Dockerfile for FastAPI app
- [x] Verify `docker-compose` full stack
- [x] Documentation (Basic usage)
