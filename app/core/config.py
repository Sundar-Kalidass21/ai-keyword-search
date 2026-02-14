from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Hybrid Product Search POC"
    API_V1_STR: str = "/api/v1"
    
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGO_DB: str = "product_search"
    
    # Model parameters
    MODEL_NAME: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384

    class Config:
        env_file = ".env"

settings = Settings()
