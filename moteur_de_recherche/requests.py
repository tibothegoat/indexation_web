import os
import json


class Requests:
    def __init__(self, request, request_types=['title', 'description'], folder_path='index_json/'):
        self.request = request
        self.request_types = request_types
        self.folder_path = folder_path
        self.json_files = [f for f in os.listdir(self.folder_path) if f.endswith('.json')]
        self.indexes = {}
    

    def load_indexes(self):

        for json_file in self.json_files:
            file_path = os.path.join(self.folder_path, json_file)
            name = os.path.splitext(json_file)[0]
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.indexes[name] = json.load(f)
            except FileNotFoundError:
                print(f"Fichier {name}.json introuvable.")
        self.synonyms = self.indexes['origin_synonyms']
    

    @staticmethod
    def tokenize(text):
        """Tokenizes, normalizes and filters stopwords from text.

            Args:
                char (char): char

            Returns:
                list: list of filtered tokens
            """
        download('stopwords')
        stop_words = set(stopwords.words('english'))
        tokens = text.split()
        return [token.lower() for token in tokens if token.lower() not in stop_words]


    def tokenize_request(self):
        """Tokenizes request.
        """
        self.tokens_request = self.tokenize(self.request)
    

    def add_synonyms(self):
        """Add synonyms
        """
        expanded_list = []

        for key, synonyms in self.synonyms.items():
            synonym_group = synonyms + [key]
            for i in range(len(self.tokens_request)):
                if self.tokens_request[i] in synonym_group:
                    expanded_list += synonym_group

        expanded_list = list(set(expanded_list))
        self.tokens_request = expanded_list
    

    def verify_one_token(self, request_type):
        """Checks whether at least one element of the list is a dictionary key.
        
        Returns:
                bool
        """
        file = f"{request_type}_index"
        return any(key in self.indexes[file] for key in self.tokens_request)

    

    def verify_all_tokens(self, request_type):
        """Checks if all elements of the list is a dictionary key.
        
        Returns:
                bool
        """
        file = f"{request_type}_index"
        return all(key in self.indexes[file] for key in self.tokens_request)
    

    def exact_match(self, request_type):
        """Finds exact matches for the request in the index."""

        if not self.verify_all_tokens():
            return []

        file = f"{request_type}_index"
        list_sites = self.indexes[file][self.tokens_request[0]]
        list_sites_final = list_sites

        for k in range(len(self.tokens_request)):
            for i in range(len(list_sites)):
                if list_sites[i] not in self.indexes[file][self.tokens_request[k]] and list_sites[i] in list_sites_final:
                    list_sites_final.remove(list_sites[i])

        return list_sites_final


    def linear_scoring(self, weights = {'title': 2.0, 'description': 1.0}):
        """Computes a linear scoring function based on multiple factors."""
        
        scores = {}
        for request_type in self.request_types:
            file = f"{request_type}_index"
            index = self.indexes[file]
            for token in self.tokens_request:
                if token in index:
                    for key, url in index.items():
                        if url in score:
                            score[url] += 1 * weights[request_type]
                        else:
                            score[url] = 1 * weights[request_type]
        
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
