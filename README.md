# indexation_web

Un simple **crawler Python** qui explore les pages d'un site web en suivant les règles de `robots.txt` et en priorisant certaines pages. Le crawler extrait des informations (titre, premier paragraphe et liens internes), les stocke dans un fichier `data.json` et s'arrête après avoir visité 50 pages.

## Fonctionnalités
- Vérifie si le crawler est autorisé à accéder à une URL en lisant le fichier `robots.txt`.
- Explore les pages en suivant les liens internes, avec une priorité pour les pages contenant le mot-clé "product".
- Extrait le titre, le premier paragraphe et les liens internes de chaque page.
- Sauvegarde les données extraites dans un fichier `data.json`.
- S'arrête après avoir exploré 50 pages.
  
## Prérequis
Le projet nécessite Python 3.x ainsi que les bibliothèques suivantes.

