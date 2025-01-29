import urllib.request 
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse
import time
import json
import os



def fetch_page(url, headers=None):
    """
    Envoie une requête HTTP GET et retourne l'objet BeautifulSoup si la requête réussit.
    """
    try:
        response = urllib.request.urlopen(url)
        if response.status == 200:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            return soup
        else:
            print(f"Erreur HTTP: {response.status}")
            return None
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return None



def get_internal_links(soup, base_url):
    """
    Extrait tous les liens internes à partir d'un objet BeautifulSoup.
    """
    links = set()
    for link in soup.find_all("a", href=True):
        href = link["href"]
        parsed_url = urlparse(href)
        base_parsed_url = urlparse(base_url)
        if parsed_url.netloc == base_parsed_url.netloc:
            links.add(href)
    return list(links)



def polite_request(url, delay=10):
    """
    Vérifie robots.txt avant de scraper et attend un délai entre les requêtes.
    """
    if can_fetch(url):
        time.sleep(delay)  # Attente avant la requête
        return fetch_page(url)
    else:
        print(f"Accès interdit par robots.txt : {url}")
        return None



def save_data(data, filename="data/data.json"):
    """
    Sauvegarde les données collectées dans un fichier JSON.
    """
    try:
        # Charge le fichier si il existe déjà
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        # Ajoute les nouvelles données
        existing_data.append(data)

        # Sauvegarde dans le fichier JSON
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)

        print(f"Données enregistrées dans {filename}")

    except Exception as e:
        print(f"Erreur lors de l'enregistrement des données : {e}")



def can_fetch(url, user_agent="*"):
    """
    Vérifie si le crawler est autorisé à accéder à une URL en lisant robots.txt.
    """
    try:
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)

    except Exception as e:
        print(f"Erreur lors de la lecture de robots.txt : {e}")
        return False  # Par défaut, on évite de scraper si on ne peut pas vérifier



def html_parse(soup, url):
    """Parse le htlm"""
    title = soup.title.string if soup.title else "Titre non trouvé"
    paragraphs = soup.find_all("p")
    first_paragraph = paragraphs[0].get_text(strip=True) if paragraphs else "Aucun paragraphe trouvé"
    internal_links = get_internal_links(soup, url)
    return {'title': title, 'first_paragraph': first_paragraph, 'internal_links': internal_links}



def add_link(url, to_visit, visited, priority=1):
    """Fonction pour ajouter un lien à la queue avec priorité"""
    if url not in visited:
        to_visit.put((priority, url))