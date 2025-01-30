import json
from urllib.parse import urlparse, parse_qs
from nltk.corpus import stopwords
from nltk import download

class index:
    def __init__(self, file_path='products.jsonl'):
        self.data = []
        if file_path:
            self.data = self.parse_jsonl(file_path)

    def parse_jsonl(self, file_path):
        """Reads a JSONL file and returns a list of dictionaries.

        Args:
            file_path (str): Path to the JSONL file
        
        Returns:
            list: A list of JSON objects
        """
        data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Erreur de décodage JSON sur la ligne: {line.strip()}\nErreur: {e}")
        return data
    
    @staticmethod
    def return_id_var(url):
        """Extracts the product ID and variant from a given URL.

        Args:
            url (str): Product URL
        
        Returns:
            dict: A dictionary with 'id' and 'variant', or None if the URL is invalid
        """
        if url == "https://web-scraping.dev/products":
            return {"id": 0, "variant": None}
        parsed_url = urlparse(url)
        
        if parsed_url.netloc != "web-scraping.dev" or not parsed_url.path.startswith("/products/"):
            return None
        
        path_parts = parsed_url.path.split('/')
        if not path_parts[2].isdigit():
            return None
        
        product_id = path_parts[2]
        variant = parse_qs(parsed_url.query).get('variant', [None])[0]
        
        return {"id": int(product_id), "variant": variant}

    @staticmethod
    def tokenize(text):
        """Tokenizes and filters stopwords from text.

            Args:
                char (char): char

            Returns:
                list: list of filtered tokens
            """
        download('stopwords')
        stop_words = set(stopwords.words('english'))
        tokens = text.split()
        return [token for token in tokens if token.lower() not in stop_words]
    
    def build_inverted_index_title(self):
        """
        Builds an inverted index for product title.
        
        Returns:
            dict: An inverted index mapping tokens to document IDs.
        """
        inverted_index = {}
        
        for i in range(len(self.data)):
            char = self.data[i]['title']
            filtered_tokens = self.tokenize(char)
            url = self.data[i]['url']
            for token in filtered_tokens:
                if token not in inverted_index:
                    inverted_index[token] = []
                inverted_index[token].append(url)
        return inverted_index
    

    def build_inverted_index_description(self):
        """
        Builds an inverted index for product description.
        
        Returns:
            dict: An inverted index mapping tokens to document IDs.
        """
        inverted_index = {}
        
        for i in range(len(self.data)):
            char = self.data[i]['description']
            filtered_tokens = self.tokenize(char)
            url = self.data[i]['url']
            for token in filtered_tokens:
                if token not in inverted_index:
                    inverted_index[token] = []
                inverted_index[token].append(url)
        return inverted_index
    
    
    def build_index_review(self):
        """
        Builds an index for reviews.
        
        Returns:
            dict: An index for reviews for each product.
        """
        index = {}
        
        for i in range(len(self.data)):
            mean = 0
            total = len(self.data[i]['product_reviews'])
            last_rating = 0
            for j in range(total):
                mean += self.data[i]['product_reviews'][j]['rating'] / total
                if j == total - 1:
                    last_rating = self.data[i]['product_reviews'][j]['rating']
            index[self.data[i]['url']] = {'mean': mean, 'total': total, 'last_rating': last_rating}

        return index
    
    def build_inverted_index_features(self, list_features=['brand', 'made in']):
        """
        Builds an inverted index for product features.

        Args:
            list_features (list): List of product features.
        
        Returns:
            dict: An inverted index mapping tokens to document IDs.
        """
        indexes = {}

        for k in range(len(list_features)):
            inverted_index = {}

            for i in range(len(self.data)):
                feature = list_features[k]

                # Vérifier si la clé existe dans 'product_features'
                if feature in self.data[i]['product_features']:
                    char = self.data[i]['product_features'][feature]
                    filtered_tokens = self.tokenize(char)
                    url = self.data[i]['url']

                    for token in filtered_tokens:
                        if token not in inverted_index:
                            inverted_index[token] = []
                        inverted_index[token].append(url)
                else:
                    # Si la clé n'existe pas, afficher un message (optionnel) ou ignorer
                    print(f"Clé '{feature}' introuvable pour l'élément {self.data[i]['url']}")

            indexes[feature] = inverted_index

        return indexes

    
    
    def build_inverted_index_position(self):
        """
        Builds an inverted index for product title and description.
        
        Returns:
            dict: An inverted index mapping tokens to document IDs and its position.
        """
        inverted_index = {}
        

        for i in range(len(self.data)):

            char = self.data[i]['title']
            filtered_tokens = self.tokenize(char)
            url = self.data[i]['url']

            for position, token in enumerate(filtered_tokens):
                if token not in inverted_index:
                    inverted_index[token] = []
                inverted_index[token].append((url, position + 1))


            char = self.data[i]['description']
            filtered_tokens = self.tokenize(char)
            url = self.data[i]['url']

            for position, token in enumerate(filtered_tokens):
                if token not in inverted_index:
                    inverted_index[token] = []
                inverted_index[token].append((url, position + 1))


        return inverted_index


    def save_indexes(self):
        """Saves each index to a separate JSON file."""
        indexes = {
            "inverted_index_title": self.build_inverted_index_title(),
            "inverted_index_description": self.build_inverted_index_description(),
            "index_review": self.build_index_review(),
            "inverted_index_features": self.build_inverted_index_features(),
            "inverted_index_position": self.build_inverted_index_position()
        }
        
        for name, index in indexes.items():
            with open(f"{name}.json", "w", encoding="utf-8") as f:
                json.dump(index, f, ensure_ascii=False, indent=4)
    
    def load_indexes(self):
        """Loads each saved index from JSON files."""
        indexes = {}
        for name in ["inverted_index_title", "inverted_index_description", "index_review", "inverted_index_features", "inverted_index_position"]:
            try:
                with open(f"{name}.json", "r", encoding="utf-8") as f:
                    indexes[name] = json.load(f)
            except FileNotFoundError:
                print(f"Fichier {name}.json introuvable.")
        return indexes
