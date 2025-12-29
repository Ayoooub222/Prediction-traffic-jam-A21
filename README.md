# Prédiction de trafic (A21)

Ce projet utilise du machine learning (via un modèle de regression) pour prédire les embouteillages.

## Contenu
* `ML_emb.ipynb` : Analyse des données et entraînement du modèle (1er commit à 11 000 lignes de données).
* `Scrapping_api_mel_github.py.py` : Script pour récupérer les données de trafic.

## Technologies
* Python
* Pandas/ Numpy / Matplotlib/ Scikit-learn
* Framework API : FastAPI
* Docker

# Mise en place du script de scrapping

* Sur le site https://developer.tomtom.com/  créez votre compte puis récupérez votre APi dans votre espace personnel.
* L'API se trouve juste en dessous de key.
![alt text](image.png)
* Mettre l'API dans la variable API_KEY (mettre son API en str --> "fd3i.....ThEJ33"  par exemple).
* (Optionnel) Choisir un chemin où le fichier CSV va s'enregistrer.
* Choisir des points venant de https://www.coordonnees-gps.fr/ et nommez les dans lea liste de dictionnaire "POINTS_A_SURVEILLER" puis rentrez leurs coordonnées respectives.
* Ex : {"nom": "Point A_1 - Vrai Point Inser1 vers D ", 
        "lat": 50.431664, 
        "lon": 2.931068}

## Condition

* Le script de scrapping doit tourner environ 2 semaines pour que ce dernier rencontre un maximum d'évenement (matin/soir , semaine/week-end , accident , vacances(optionnel))
* (Optionnel) Prévoir une plannification de tâches

# Run via Docker/FastAPI

* Clonez le projet via "git clone https://github.com/Ayoooub222/Prediction-traffic-jam-A21.git"  cd Prediction-traffic-jam-A21
* Installez DockerDestop
* Ouvrez un terminal
* Copiez collez le chemin des fichiers télechargés
* Tapez "docker build -t (donner un nom à l'image) ."
* Puis "docker run -p 8000:80 (le nom de l'image)"
* Ouvrez la page "http://localhost:8000/docs" sur votre navigateur

## Exemple d'utilisation 

* jour : 0 (Lundi) à 6 (Dimanche) (ex: 5)
* heure : 0 à 23
* nom_point : Choisissez un point dans la liste (ex: Point A_1 - Inser1 vers D)
* vitesse_precedente : 100  (facultatif)
* est_ferie : 0 (Non) ou 1 (Oui) (facultatif)