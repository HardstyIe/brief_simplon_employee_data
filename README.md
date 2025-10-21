# Brief Simplon — Gestion des salaires employés (Collections)

Projet d'initiation IA/Data pour calculer, afficher et exporter les salaires mensuels des employés par branche.

## Aperçu
Le script principal est `app.py`. Il charge les données JSON, calcule les salaires mensuels (avec prise en compte des heures supplémentaires), exporte un CSV et peut afficher un tableau interactif avec Streamlit.

Fonctions principales :
- `load_json` : charge les fichiers JSON.
- `calc_monthly_salary` : calcule les salaires mensuels et génère les statistiques et les lignes CSV.
- `export_salaries_to_csv` : exporte les résultats dans `salaries_export.csv`.
- `show_data_tabs` : affiche les données et statistiques dans une interface Streamlit.

## Structure du projet
- `app.py` — code principal et fonctions utilitaires.
- `lib/data/employe_data.json` — données réelles.
- `lib/data/employe_data_test.json` — jeu de données de test.
- `salaries_export.csv` — exemple d'export généré.
- `requirement.txt` — dépendances.
- `LICENSE` — licence MIT.

## Prérequis
- Python 3.8+
- Installer les dépendances :
```sh
pip install -r requirement.txt
```

## Exécution
1. Interface Streamlit (recommandé) :
```sh
streamlit run app.py
```
2. Script console (génère le CSV et Affiche l'output console) :
```sh
python app.py
```
Le CSV exporté par défaut est `salaries_export.csv`.

## Données
- Utiliser le jeu de test : `lib/data/employe_data_test.json`
- Pour utiliser d'autres données, modifiez l'appel à `load_json` dans `app.py` ou remplacez le fichier JSON ciblé.

## Résultats & Statistiques
- `calc_monthly_salary` retourne :
  - lignes CSV prêtes à l'export,
  - statistiques par branche,
  - statistiques globales (min / max / moyenne).

## Tests
- Vérifier le comportement avec `lib/data/employe_data_test.json`.

## Licence
Ce projet est sous licence MIT — voir `LICENSE`.

## Contribution
Issues et PR bienvenues. Respecter la structure de données JSON lors de l'ajout ou modification des entrées.
