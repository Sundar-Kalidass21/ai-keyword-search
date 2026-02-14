import pandas as pd
from app.services.nlp.embedding import embedding_service
from app.services.mongo_service import mongo_service
from app.services.search.elastic_service import elastic_service
from app.services.search.faiss_service import faiss_service
from app.core.logging import logger

DATA_FILE = "data/products.csv"

def ingest_data():
    logger.info("Starting ingestion process...")
    try:
        df = pd.read_csv(DATA_FILE)
        
        embeddings = []
        product_ids = []

        total = len(df)
        for idx, row in df.iterrows():
            product = row.to_dict()
            product['id'] = str(product['id']) # Ensure ID is string
            
            # 1. MongoDB (Metadata)
            mongo_service.insert_product(product)
            
            # 2. Elasticsearch (Keyword)
            elastic_service.index_product(product)

            # 3. Generate Embedding (for FAISS)
            # Combine relevant fields for semantic meaning
            text_to_embed = f"{product['title']} {product['brand']} {product['description']}"
            vector = embedding_service.generate_embedding(text_to_embed)
            
            embeddings.append(vector)
            product_ids.append(product['id'])

            if idx % 10 == 0:
                logger.info(f"Processed {idx}/{total} products")

        # 4. FAISS (Vector)
        if embeddings:
            faiss_service.add_vectors(embeddings, product_ids)
        
        logger.info("Ingestion completed successfully!")

    except Exception as e:
        logger.error(f"Ingestion failed: {e}")

if __name__ == "__main__":
    ingest_data()
