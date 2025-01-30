from index import index as Index

def generate_and_save_indexes(file_path='products.jsonl'):
    index_instance = Index(file_path)

    print("Génération des index...")
    inverted_index_title = index_instance.build_inverted_index_title()
    inverted_index_description = index_instance.build_inverted_index_description()
    index_review = index_instance.build_index_review()
    inverted_index_features = index_instance.build_inverted_index_features()
    inverted_index_position = index_instance.build_inverted_index_position()

    print("Sauvegarde des index...")
    index_instance.save_indexes()

def load_indexes():
    index_instance = Index()
    
    print("Chargement des index...")
    indexes = index_instance.load_indexes()
    return indexes

def main():
    generate_and_save_indexes('products.jsonl')
    
    loaded_indexes = load_indexes()
    
    print("\nIndex chargés :")
    for name, index in loaded_indexes.items():
        print(f"{name}: {index}")

    index_instance = Index('products.jsonl') 
    print("\nPremier élément du fichier 'products.jsonl':")
    print(index_instance.parse_jsonl('products.jsonl')[0])

    url = "https://web-scraping.dev/products/10?variant=blue-5"
    print("\nTest de return_id_var avec l'URL :")
    print(index_instance.return_id_var(url))

if __name__ == "__main__":
    main()
