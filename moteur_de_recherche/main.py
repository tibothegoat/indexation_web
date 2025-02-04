import os
import json
from requests import Requests

def test_requests():
    product_requests = [
        "Box of Chocolate Candy",
        "Chocolate",
        "Candy",
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

    folder_path = 'index_json/'
    results_dict = {}

    for request in product_requests:
        req = Requests(request, folder_path=folder_path)
        req.load_indexes()
        req.parse_jsonl("products.jsonl")
        req.tokenize_request()
        req.add_synonyms()

        number_of_documents = req.number_of_filtered_doc()[0]
        number_of_filtered_documents = req.number_of_filtered_doc()[1]
        ranked_products = req.rank_products_bm25()
        
        documents = [
            {
                "title": product[2],
                "url": product[0],
                "description": product[3],
                "ranking_score": product[1]
            } for product in ranked_products
        ]
        
        results_dict[request] = {
            "documents": documents,
            "total_documents": number_of_documents,
            "filtered_documents": number_of_filtered_documents
        }

    with open("request_results.json", "w", encoding="utf-8") as json_file:
        json.dump(results_dict, json_file, indent=4, ensure_ascii=False)
    
    print("Les résultats ont été enregistrés dans request_results.json")

if __name__ == "__main__":
    test_requests()
