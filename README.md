# Partie Crawler

Un simple **crawler Python** qui explore les pages d'un site web en suivant les règles de `robots.txt` et en priorisant certaines pages. Le crawler extrait des informations (titre, premier paragraphe et liens internes), les stocke dans un fichier `data.json` et s'arrête après avoir visité 50 pages.

## Fonctionnalités
- Vérifie si le crawler est autorisé à accéder à une URL en lisant le fichier `robots.txt`.
- Explore les pages en suivant les liens internes, avec une priorité pour les pages contenant le mot-clé "product".
- Extrait le titre, le premier paragraphe et les liens internes de chaque page.
- Sauvegarde les données extraites dans un fichier `data.json`.
- S'arrête après avoir exploré 50 pages.
  
## Prérequis
Le projet nécessite Python 3.x ainsi que les bibliothèques suivantes:
 - beautifulsoup4 version 4.12.3
 - urllib3 version 2.0.7


# Partie indexation

Cette partie permet de générer, sauvegarder et charger des index à partir de données JSONL concernant des produits. Les index sont utilisés pour organiser et accéder rapidement à des informations sur les produits, telles que leurs titres, descriptions, avis, caractéristiques et position des termes dans les textes. Ce système d'indexation est basé sur des fichiers JSON, chacun représentant un type d'index pour les produits.

## Structure des Index

Les index générés sont sauvegardés dans des fichiers JSON distincts. Chaque type d'index représente un aspect spécifique des données des produits. Voici la structure détaillée de chaque index :

1. **Inverted Index - Title (inverted_index_title.json)**:
   - **Objectif** : Permet de rechercher des produits par leurs titres.
   - **Structure** : Un dictionnaire où chaque clé est un mot (token) et chaque valeur est une liste d'URLs des produits contenant ce mot.
   - **Exemple** :
     ```json
     {
       "product": ["https://web-scraping.dev/products/10?variant=blue-5", "https://web-scraping.dev/products/15?variant=red-10"],
       "blue": ["https://web-scraping.dev/products/10?variant=blue-5"],
       "shoes": ["https://web-scraping.dev/products/5?variant=black-3"]
     }
     ```

2. **Inverted Index - Description (inverted_index_description.json)**:
   - **Objectif** : Permet de rechercher des produits par leurs descriptions.
   - **Structure** : Un dictionnaire similaire à celui du titre, mais pour les mots dans la description des produits.
   - **Exemple** :
     ```json
     {
       "comfortable": ["https://web-scraping.dev/products/10?variant=blue-5"],
       "premium": ["https://web-scraping.dev/products/15?variant=red-10"]
     }
     ```

3. **Index des Avis (index_review.json)**:
   - **Objectif** : Permet de récupérer des informations agrégées sur les avis des produits.
   - **Structure** : Un dictionnaire où chaque clé est l'URL d'un produit et la valeur contient les informations suivantes :
     - `mean` : la note moyenne des avis.
     - `total` : le nombre total d'avis.
     - `last_rating` : la dernière note donnée.
   - **Exemple** :
     ```json
     {
       "https://web-scraping.dev/products/10?variant=blue-5": {
         "mean": 4.5,
         "total": 10,
         "last_rating": 5
       }
     }
     ```

4. **Inverted Index - Caractéristiques (inverted_index_features.json)**:
   - **Objectif** : Permet de rechercher des produits en fonction de certaines caractéristiques spécifiques (par exemple, marque, origine, etc.).
   - **Structure** : Un dictionnaire où chaque clé est une caractéristique (par exemple, `brand` ou `made in`) et la valeur est un autre dictionnaire qui associe des mots (tokens) à des URLs de produits.
   - **Exemple** :
     ```json
     {
       "brand": {
         "nike": ["https://web-scraping.dev/products/10?variant=blue-5"],
         "adidas": ["https://web-scraping.dev/products/15?variant=red-10"]
       },
       "made in": {
         "usa": ["https://web-scraping.dev/products/5?variant=black-3"]
       }
     }
     ```

5. **Inverted Index - Position (inverted_index_position.json)**:
   - **Objectif** : Permet de rechercher des mots dans le titre et la description d'un produit tout en conservant la position des mots.
   - **Structure** : Un dictionnaire où chaque clé est un mot (token) et chaque valeur est une liste de tuples contenant l'URL du produit et la position du mot dans le texte (position commence à 1).
   - **Exemple** :
     ```json
     {
       "blue": [
         ["https://web-scraping.dev/products/10?variant=blue-5", 2]
       ],
       "comfortable": [
         ["https://web-scraping.dev/products/10?variant=blue-5", 3]
       ]
     }
     ```

## Choix Techniques

### Langage et Bibliothèques

- **Python** : Le projet est développé en Python pour sa simplicité, sa flexibilité et son large écosystème de bibliothèques pour le traitement de données et la manipulation de fichiers JSON.
  
- **NLTK** : La bibliothèque NLTK (Natural Language Toolkit) est utilisée pour traiter et filtrer les mots (tokens) dans les textes. Elle permet d'exclure les mots vides (stopwords) dans les titres, descriptions et caractéristiques des produits.
  - **Méthode** : La méthode `tokenize` utilise `nltk.corpus.stopwords` pour filtrer les mots vides et obtenir des tokens significatifs.

### Structures de données

- **JSONL** : Les données des produits sont stockées dans un fichier JSONL (JSON Lines), où chaque ligne est un objet JSON représentant un produit. Cela permet de traiter facilement des grandes quantités de données ligne par ligne.

- **Index Inversé** : Les index sont construits à l'aide de la méthode classique de l'index inversé, où chaque mot (ou token) est associé à une liste de documents (produits) contenant ce mot.

- **Dictionnaires pour les Index** : Chaque index est représenté sous forme de dictionnaire (clé-valeur) pour permettre des recherches rapides et efficaces. Les clés sont les tokens (mots) et les valeurs sont des listes d'URLs ou d'autres informations pertinentes (comme les avis ou les positions).

### Sauvegarde et Chargement des Index

- **Fichiers JSON** : Les index sont sauvegardés sous forme de fichiers JSON. Chaque type d'index (par exemple, `inverted_index_title`) est sauvegardé dans un fichier distinct.
  
- **Gestion des erreurs** : Si un fichier d'index est introuvable lors du chargement, un message d'erreur est affiché, mais le programme continue sans planter.

### Fonctionnalités supplémentaires

- **Extraction d'ID et de variante d'URL** : La méthode `return_id_var` permet d'extraire l'ID du produit et la variante d'une URL donnée.
  
- **Gestion des clés manquantes** : Lors de la génération de l'index des caractéristiques (`build_inverted_index_features`), le programme gère les cas où certaines clés (par exemple, "brand") sont manquantes dans les données du produit, en les ignorant ou en affichant un avertissement.

## Utilisation

### Générer et sauvegarder les index

Exécute la fonction `generate_and_save_indexes('products.jsonl')` pour générer et sauvegarder tous les index dans des fichiers JSON.

```python
generate_and_save_indexes('products.jsonl')
``` 


# Partie moteur de recherche

## Description
Cette partie implémente un moteur de recherche de produits basé sur l'algorithme BM25, combiné à des pondérations spécifiques pour améliorer la pertinence des résultats. L'objectif est de fournir une recherche efficace en tenant compte du titre, de la description et des avis des produits.

## Fonctionnalités
- **Tokenisation et suppression des stopwords** : Nettoyage des requêtes utilisateur pour une recherche plus efficace.
- **Prise en compte des synonymes** : Expansion de la requête pour améliorer la recherche.
- **Recherche exacte et pondérée** : Utilisation des index inversés pour retrouver les documents contenant les mots-clés.
- **Calcul du score BM25** : Classement des produits selon la pertinence de la requête.
- **Utilisation des avis des utilisateurs** : Intégration des notes moyennes et du nombre d'avis pour départager les produits.

## Structure du Code
- `Requests` : Classe principale qui gère le traitement des requêtes et le classement des résultats.
- `compute_bm25_scores` : Calcul du score BM25 en fonction de la position des mots-clés dans les documents.
- `rank_products_bm25` : Classement final en combinant les scores BM25 et les avis clients.
- `test_requests` : Fonction permettant de tester le moteur de recherche sur un ensemble de requêtes prédéfinies.

## Pondération des éléments
Les poids utilisés dans l'algorithme permettent d'obtenir de bons résultats :
- **Titre (poids : 2.0)** : Impact fort, car les mots-clés les plus importants sont souvent présents dans le titre du produit.
- **Description (poids : 1.0)** : Impact moindre que le titre, mais permet d'inclure des mots-clés importants qui ne figurent pas dans le titre.
- **Avis clients** : Utilisés pour départager les produits ayant un score similaire afin de mettre en avant les produits les mieux notés. Ce critère ne doit pas avoir un poids trop élevé sinon certains produits bien notés mais moins pertinents pourraient être mis en avant.

## Fichiers d'index et de données
- `index_json/` : Dossier contenant les index JSON des titres, descriptions et avis clients.
- `products.jsonl` : Fichier JSONL contenant les informations des produits.
- `request_results.json` : Résultats des recherches enregistrés après exécution de `test_requests`.

## Utilisation
1. Placer les fichiers d'index dans `index_json/`.
2. Exécuter `test_requests()` pour générer les résultats de recherche.
3. Consulter les résultats dans `request_results.json`.




