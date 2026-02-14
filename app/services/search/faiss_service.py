import faiss
import numpy as np
import pickle
import os
from app.core.config import settings
from app.core.logging import logger

class FaissService:
    def __init__(self):
        self.dimension = settings.EMBEDDING_DIM
        self.index = faiss.IndexFlatL2(self.dimension)
        self.product_ids = []
        self.index_file = "data/faiss_index.bin"
        self.ids_file = "data/product_ids.pkl"
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_file) and os.path.exists(self.ids_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.ids_file, "rb") as f:
                self.product_ids = pickle.load(f)
            logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors")
        else:
            logger.info("Initialized new FAISS index")

    def save_index(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.ids_file, "wb") as f:
            pickle.dump(self.product_ids, f)
        logger.info("Saved FAISS index to disk")

    def add_vectors(self, embeddings: list, ids: list):
        vectors = np.array(embeddings).astype('float32')
        self.index.add(vectors)
        self.product_ids.extend(ids)
        self.save_index()

    def search(self, vector: list, k: int = 10):
        query_vector = np.array([vector]).astype('float32')
        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.product_ids):
                results.append({
                    "id": self.product_ids[idx],
                    "score": float(1 / (1 + distances[0][i])) # Convert distance to similarity score
                })
        return results

faiss_service = FaissService()
