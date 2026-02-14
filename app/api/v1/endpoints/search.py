from fastapi import APIRouter, Depends, Query
from app.models.search import SearchResponse
from app.services.nlp.query_parser import query_parser
from app.services.nlp.embedding import embedding_service
from app.services.search.elastic_service import elastic_service
from app.services.search.faiss_service import faiss_service
from app.services.search.ranker import ranker
from app.services.mongo_service import mongo_service
from app.core.logging import logger
import time

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
async def search_products(q: str = Query(..., min_length=1), limit: int = 10):
    start_time = time.time()
    
    # 1. Parse Query
    clean_query, filters = query_parser.parse(q)
    logger.info(f"Original: '{q}' -> Clean: '{clean_query}', Filters: {filters}")

    # 2. Generate Embedding
    query_vector = embedding_service.generate_embedding(clean_query)

    # 3. Parallel Search (Synchronous calls for POC simplicity)
    # Elasticsearch
    es_results = elastic_service.search(clean_query, filters=filters, limit=limit*2)
    es_ids = {hit['_id']: hit for hit in es_results}

    # FAISS
    faiss_results = faiss_service.search(query_vector, k=limit*2)
    faiss_ids = [res['id'] for res in faiss_results]

    # 4. Fetch Product Details
    all_ids = list(set(list(es_ids.keys()) + faiss_ids))
    products = mongo_service.get_products(all_ids)
    products_map = {p['id']: p for p in products}

    # 5. Hybrid Ranking
    # Prepare inputs for ranker
    # We need to pass the raw ES hits and FAISS results to the ranker
    ranked_results = ranker.rank(
        semantic_results=faiss_results,
        keyword_results=es_results,
        products_map=products_map
    )

    # Slice to limit
    final_results = ranked_results[:limit]
    
    execution_time = (time.time() - start_time) * 1000

    return {
        "results": final_results,
        "total": len(final_results),
        "execution_time_ms": execution_time
    }
