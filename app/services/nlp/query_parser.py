import re
from typing import Dict, Any, Tuple

class QueryParser:
    def parse(self, query: str) -> Tuple[str, Dict[str, Any]]:
        filters = {}
        clean_query = query.lower()

        # Extract price "under X"
        price_match = re.search(r"under (\d+)(k?)", clean_query)
        if price_match:
            amount = int(price_match.group(1))
            if price_match.group(2) == 'k':
                amount *= 1000
            filters['price_max'] = amount
            clean_query = query.replace(price_match.group(0), "").strip()

        # Simple category extraction (Hardcoded for POC, ideal is NER)
        categories = ["laptop", "phone", "headphones", "watch", "camera"]
        for cat in categories:
            if cat in clean_query:
                filters['category'] = cat
                # We might keep the category in query for semantic match or remove it
                # For now, let's keep it to ensure relevance
        
        return clean_query, filters

query_parser = QueryParser()
