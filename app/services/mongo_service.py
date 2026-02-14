from pymongo import MongoClient
from app.core.config import settings
from app.core.logging import logger

class MongoService:
    def __init__(self):
        try:
            self.client = MongoClient(settings.MONGODB_URL)
            self.db = self.client[settings.MONGO_DB]
            self.products = self.db.products
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def insert_product(self, product_data: dict):
        # Update if exists, otherwise insert
        return self.products.update_one(
            {"id": product_data["id"]}, 
            {"$set": product_data}, 
            upsert=True
        )

    def get_product(self, product_id: str):
        return self.products.find_one({"id": product_id}, {"_id": 0})
    
    def get_products(self, product_ids: list):
        return list(self.products.find({"id": {"$in": product_ids}}, {"_id": 0}))

mongo_service = MongoService()
