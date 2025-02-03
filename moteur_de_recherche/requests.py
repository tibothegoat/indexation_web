import os
import json
import math
from nltk.corpus import stopwords
from nltk import download
import copy


class Requests:
    def __init__(self, request, folder_path='index_json/'):
        self.request = request
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

        expanded_list = list(set(self.tokens_request + expanded_list))
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

        if not self.verify_all_tokens(request_type):
            return []

        file = f"{request_type}_index"
        if len(self.tokens_request) == 0:
            return []
        list_sites = list(self.indexes[file][self.tokens_request[0]])
        if len(list_sites) == 0:
            return []
        list_sites_final = copy.deepcopy(list_sites)

        for k in range(len(self.tokens_request)):
            for i in range(len(list_sites)):
                if list_sites[i] not in self.indexes[file][self.tokens_request[k]] and list_sites[i] in list_sites_final:
                    list_sites_final.remove(list_sites[i])

        return list_sites_final
    
    @staticmethod
    def idf(term, inverted_index, N):
        df = len(inverted_index.get(term, {}))
        return math.log(1 + (N - df + 0.5) / (df + 0.5)) if df > 0 else 0

    
    def compute_bm25_scores(self, index):
        """Calculates the BM25 score for each document in a given index, considering token position"""
        k1, b = 1.5, 0.75
        doc_lengths = {}
        for token, dico_url in index.items():
            for url in dico_url.keys():
                if url not in doc_lengths.keys():
                    doc_lengths[url] = len(dico_url[url])
                else:
                    doc_lengths[url] += len(dico_url[url])
        N = len(doc_lengths)
        avg_doc_length = sum(doc_lengths.values()) / N if N > 0 else 1

        inverted_index = {}
        for token, dico_url in index.items():
            dico_url_int = copy.deepcopy(dico_url)
            inverted_index[token] = dico_url_int
            for url in dico_url_int.keys():
                inverted_index[token][url] = len(inverted_index[token][url])
                
        scores = {}
        for doc_id in doc_lengths.keys():
            score = 0
            doc_length = doc_lengths.get(doc_id, 0)
            for term in self.tokens_request:
                if term in inverted_index and doc_id in inverted_index[term]:
                    tf = inverted_index[term][doc_id]
                    term_idf = self.idf(term, inverted_index, N)
                    num = tf * (k1 + 1)
                    denom = tf + k1 * (1 - b + b * (doc_length / avg_doc_length))
                    bm25_term_score = term_idf * (num / denom)

                    position_boost = 1
                    dico_url = index[term]
                    if doc_id in dico_url.keys():
                        first_position = index[term][doc_id][0]  
                        position_boost = 1 + (1 / (1 + math.log(first_position + 1)))

                    score += bm25_term_score * position_boost 

            scores[doc_id] = score
        return scores


    def rank_products_bm25(self):
        """Classifies products by combining BM25, reviews, and exact matches"""
        weights = {'title': 2.0, 'description': 1.0}
        scores = {}

        for request_type, weight in weights.items():
            file = f"{request_type}_index"
            index = self.indexes.get(file, {})
            bm25_scores = self.compute_bm25_scores(index)
            for url, score in bm25_scores.items():
                scores[url] = scores.get(url, 0) + score * weight

                if url in self.exact_match(request_type):
                    scores[url] += 3 
        
        reviews_index = self.indexes.get('reviews_index', {})
        for url, base_score in scores.items():
            if url in reviews_index:
                mean = reviews_index[url].get("mean_mark", 0)
                total_reviews = reviews_index[url].get("total_reviews", 0)
                last = reviews_index[url].get("last_rating", 0)
                review_score = (mean * total_reviews + last) * math.log(1 + total_reviews) / (total_reviews + 1)
                scores[url] += review_score
            
        list_ranked = [(url, base_score) for url, base_score in scores.items()]
        list_ranked.sort(key=lambda x: x[1], reverse = True)
        return list_ranked
