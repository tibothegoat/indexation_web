import os
import json
from requests import Requests

# Test des requêtes avec des produits spécifiques
def test_requests():
    # Liste des produits à tester
    product_requests = [
        "Box of Chocolate Candy",
        "Chocolate",
        "Candy"
        "Energy Potion",
        "Potion",
        "Energy",
        "Red Energy Potion",
        "Hiking Boots",
        "Boots",
        "Outdoor",
        "Boots for Outdoor",
        "Women's Sandals",
        "Sandals",
        "Running Shoes for Men",
        "Running Shoes",
        "Shoes for Men",
        "Shoes",
        "Kids' Sneakers",
        "Sneakers",
        "Classic Sneakers"
    ]
    product_requests = [
        "Box of Chocolate Candy"
    ]
    
    folder_path = 'index_json/' 
    for request in product_requests:
        
        req = Requests(request, folder_path=folder_path)
        
        req.load_indexes()

        req.tokenize_request()

        req.add_synonyms()

        print(f"Requête: {request}")
        
        request_types=['title', 'description']
        for request_type in request_types:
            results = req.exact_match(request_type)
            print(f"  Résultats pour {request_type} index: {results}")

        ranked_products = req.rank_products_bm25()[0:3]
        print(f"  Produits classés par score BM25: {ranked_products}\n")

if __name__ == "__main__":
    test_requests()
