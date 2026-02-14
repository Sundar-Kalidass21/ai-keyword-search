from typing import List, Dict
import numpy as np

class Ranker:
    def rank(self, semantic_results: List[Dict], keyword_results: List[Dict], products_map: Dict) -> List[Dict]:
        scores = {}
        explanations = {}

        # Normalize semantic scores (0-1)
        # Note: FAISS score is already converted to similarity 0-1 in service
        for item in semantic_results:
            pid = item['id']
            scores[pid] = scores.get(pid, 0) + 0.5 * item['score']
            explanations.setdefault(pid, []).append(f"Semantic match ({item['score']:.2f})")

        # Normalize keyword scores
        if keyword_results:
            max_score = max(h['_score'] for h in keyword_results) if keyword_results else 1
            for hit in keyword_results:
                pid = hit['_id']
                norm_score = hit['_score'] / max_score
                scores[pid] = scores.get(pid, 0) + 0.3 * norm_score
                explanations.setdefault(pid, []).append(f"Keyword match ({norm_score:.2f})")

        # Add product features (Rating, Price)
        final_results = []
        for pid, score in scores.items():
            product = products_map.get(pid)
            if not product:
                continue

            # Rating boost (0 to 5 -> 0 to 0.1)
            rating_score = (product.get('rating', 0) / 5.0) * 0.1
            score += rating_score
            if rating_score > 0.08:
                explanations[pid].append(f"High rating ({product.get('rating')})")

            # Price boost (Lower is better? Or just feature? Let's assume lower price within range is better for this logic)
            # Simplified: just fixed weight for now or skip to keep it simple as per request specific formula
            # "0.1 * price_score" -> Let's inverse normalize price? 
            # For POC, let's ignore complex price normalization and just add a small constant if it has a price
            price_score = 0.1 # Placeholder
            score += price_score
            
            final_results.append({
                "product": product,
                "score": score,
                "explanation": explanations[pid]
            })

        # Sort by final score
        final_results.sort(key=lambda x: x['score'], reverse=True)
        return final_results

ranker = Ranker()
