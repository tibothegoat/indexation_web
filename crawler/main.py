import queue
import os
from utils import polite_request, save_data, html_parse, add_link, can_fetch



def crawl_website(start_url, max_pages=50):
    """
    Explore un site web en suivant les liens internes et en priorisant les pages produit.
    """
    filename = "data/data.json"
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Le fichier {filename} a été supprimé.")
    
    visited = set()  # URLs déjà visitées
    to_visit = queue.PriorityQueue()  # File d'attente avec priorité
    
    # Ajouter la première URL
    add_link(start_url, to_visit, visited, priority=0)

    while not to_visit.empty() and len(visited) < max_pages:
        _, url = to_visit.get()  # Récupère l'URL avec la plus haute priorité

        if url not in visited and can_fetch(url):

            print(f"Exploration : {url}")

            # Récupérer et analyser la page
            soup = polite_request(url)
            if not soup:
                continue  # Passe à la page suivante si erreur

            html_parsed = html_parse(soup, start_url)
            html_parsed['url'] = url

            # Stocker les données
            save_data(html_parsed)

            # Marquer l'URL comme visitée
            visited.add(url)

            # Ajouter les liens internes à explorer
            internal_links = html_parsed['internal_links']
            for link in internal_links:
                priority = 0 if "produit" in link.lower() else 1  # Priorise les pages produit
                add_link(link, to_visit, visited, priority)

    print("Exploration terminée !")

# Lancer le crawler
if __name__ == "__main__":
    start_url = "https://web-scraping.dev/products"  # Remplace par l'URL du site cible
    crawl_website(start_url)
