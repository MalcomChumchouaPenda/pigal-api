# pigal-api
PIGAL api template based on Flask to develop academic services

## Présentation
Ce template permet de devolopper des services utilisables sur des sites ou portails PIGAL pour des etablissements universitaires.


## Structure Générale du Projet
```
/pigal
│
├── app.py                     # Point d'entrée principal pour l'application Flask
├── requirements.txt           # Dépendances du projet
├── README.md                  # Documentation du projet
│
├── /services                  # Microservices Flask ou API
│   ├── /auth                  # Service d'authentification
│   ├── /courses               # Service de gestion des formations (Demo)
│
├── /core                      # Fonctions, paramètres, ressources et routes principales
├── /pages                     # Pages demo Flask ou UI
├── /tests                     # Tests unitaires et d'intégration
├── /migrations                # Fichiers de migration pour SQLAlchemy
```


## Structure du Core
Le dossier `core/` contient les fichiers et ressources essentielles pour le bon fonctionnement de l'application Flask.
```
/core
├── /static                # Ressources statiques globales (CSS, JS, images)
├── /templates             # Templates de base pour Flask
├── /store                 # Ressources dynamiques (fichiers temporaires, etc.)
├── config.py              # Configuration de l'application Flask
├── constants.py           # Contient les constantes globales
├── utils.py               # Fonctions utilitaires
```

## Structure des Tests
Le dossier `tests/` regroupe les tests unitaires et d'intégration pour garantir la fiabilité de l'application.
```
/tests
├── /data                  # Donnees pour les Tests unitaires
├── conftest.py            # Configuration de pytest (fixtures, etc.)
├── test_service_a.py      # Tests unitaires du service A
├── test_service_b.py      # Tests unitaires du service B
```


## Structure des Services
Le dossier `services/` contient les microservices gérant différentes fonctionnalités de l'application via des API REST.
```
/services
├── /auth                  # Gestion des utilisateurs
│   ├── defaults.py        # Generateurs des donnees par defaut de l'API Auth
│   ├── models.py          # Modèles de base de données pour Auth
│   ├── routes.py          # Routes de l'API Auth
│   ├── schemas.py         # Schemas externes de la base de données
│   ├── tasks.py           # Taches pour Auth
│
├── /courses               # API pour gérer les formations (demo)
│   ├── defaults.py        # Generateurs des donnees par defaut pour Formations
│   ├── models.py          # Modèles de base de données pour l'API Formations
│   ├── routes.py          # Routes de l'API Formations
│   ├── schemas.py         # Modèles de base de données pour Formations
│   ├── tasks.py           # Taches pour l'API Formations
```


## Installation et Lancement
1. Cloner le dépôt :
   ```bash
   git clone <repo_url>
   cd mon_projet
   ```
2. Créer et activer un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```
3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Lancer l'api :
   ```bash
   flask run
   ```


## Processus de migration de la base
Le processus normal de migration se déroule comme suit :

- Vous apportez des modifications à vos modèles dans votre code source Python.
- Vous exécutez ensuite `flask db migrate` pour générer une nouvelle migration de base de données pour ces changements.
- Enfin, vous appliquerez les modifications à la base de données en exécutant `flask db upgrade`.


## Contribution
Toute contribution est la bienvenue ! N'hésitez pas à proposer des améliorations via des issues ou des pull requests.

## Licence
Ce projet est sous licence MIT.
