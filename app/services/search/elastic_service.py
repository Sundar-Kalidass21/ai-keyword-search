from elasticsearch import Elasticsearch
from app.core.config import settings
from app.core.logging import logger

class ElasticService:
    def __init__(self):
        self.es = Elasticsearch(settings.ELASTICSEARCH_URL)
        self.index_name = "products"
        self._create_index()

    def _create_index(self):
        if not self.es.indices.exists(index=self.index_name):
            analysis_settings = {
                "settings": {
                    "analysis": {
                        "analyzer": {
                            "ngram_analyzer": {
                                "tokenizer": "ngram_tokenizer",
                                "filter": ["lowercase"]
                            }
                        },
                        "tokenizer": {
                            "ngram_tokenizer": {
                                "type": "ngram",
                                "min_gram": 3,
                                "max_gram": 3,
                                "token_chars": ["letter", "digit"]
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "title": {"type": "text", "analyzer": "standard"},
                        "description": {"type": "text", "analyzer": "standard"},
                        "brand": {"type": "keyword"},
                        "category": {"type": "keyword"},
                        "price": {"type": "float"},
                        "rating": {"type": "float"}
                    }
                }
            }
            self.es.indices.create(index=self.index_name, body=analysis_settings)
            logger.info("Created Elasticsearch index")

    def index_product(self, product_data: dict):
        self.es.index(index=self.index_name, id=product_data["id"], document=product_data)

    def search(self, query: str, filters: dict = None, limit: int = 10):
        must = [{"multi_match": {"query": query, "fields": ["title^3", "description"]}}]
        
        filter_clauses = []
        if filters:
            for key, value in filters.items():
                if key == "price_max":
                    filter_clauses.append({"range": {"price": {"lte": value}}})
                elif key == "price_min":
                    filter_clauses.append({"range": {"price": {"gte": value}}})
                else:
                    filter_clauses.append({"term": {key: value}})

        body = {
            "query": {
                "bool": {
                    "must": must,
                    "filter": filter_clauses
                }
            },
            "size": limit
        }
        
        response = self.es.search(index=self.index_name, body=body)
        return response['hits']['hits']

elastic_service = ElasticService()
