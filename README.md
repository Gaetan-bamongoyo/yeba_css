# Nayekola

Plateforme d'apprentissage par le jeu : **CSS** et **SQL** (Python bientôt).

## Principe

- **Django** sert les pages, le catalogue et la sauvegarde de progression
- **HTML / CSS / JavaScript** gèrent le gameplay dans le navigateur
- Au chargement d'un jeu, **tout le pack de niveaux** est envoyé une seule fois
- Pendant la partie : **aucune requête** pour valider un niveau
- La progression est écrite dans `localStorage`, puis synchronisée de temps en temps

## Structure

```text
config/                 # settings, urls
catalog/                # jeux, niveaux, seed, données missions
progress/               # progression session / utilisateur
templates/              # pages HTML
static/
  css/style.css
  js/games/flexbox/     # moteur Flexbox + sync
  js/games/technova/    # moteur CSS Mission TechNova
  js/games/sql/         # moteur SQL
```

## Installation

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_flexbox
python manage.py runserver
```

`seed_flexbox` initialise **tout le catalogue** :

- hub **CSS** (Flexbox + Le site détruit / TechNova)
- hub **SQL**
- carte **Python** (bientôt)

Ouvrir [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

- Accueil : `/`
- Missions CSS : `/jeux/css/`
  - Flexbox : `/jeux/css/mission/flexbox/`
  - Le site détruit : `/jeux/css/mission/le-site-detruit/`
- Missions SQL : `/jeux/sql/`
- Admin : `/admin/` (après `createsuperuser`)

## Sync progression

| Moment | Comportement |
|---|---|
| En jeu | `localStorage` immédiat |
| ~1,2 s après un succès | `POST /api/progress/<slug>/` (quand sync activée) |
| Onglet caché / retour online | nouvelle tentative de sync |

## Étendre

1. **CSS** : ajouter une entrée dans `catalog/data/css_registry.py` + données de niveaux, puis `seed_flexbox`
2. **SQL** : ajouter une mission dans `catalog/data/sql_registry.py` + module de données, puis `seed_flexbox`
3. Flexbox seul : `catalog/data/flexbox_levels.py`
4. TechNova : `catalog/data/css_technova.py`
