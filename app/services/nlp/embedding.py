from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.core.logging import logger

class EmbeddingService:
    def __init__(self):
        logger.info(f"Loading SentenceTransformer model: {settings.MODEL_NAME}")
        self.model = SentenceTransformer(settings.MODEL_NAME)
        logger.info("Model loaded successfully")

    def generate_embedding(self, text: str):
        return self.model.encode(text).tolist()

    def generate_embeddings(self, texts: list):
        return self.model.encode(texts).tolist()

embedding_service = EmbeddingService()
