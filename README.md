# Nayekola

Plateforme d'apprentissage par le jeu. Le premier parcours enseigne **CSS Flexbox**.

## Principe

- **Django** sert les pages, le catalogue et la sauvegarde de progression
- **HTML / CSS / JavaScript** gèrent tout le gameplay dans le navigateur
- Au chargement d'un jeu, **tout le pack de niveaux** est envoyé une seule fois
- Pendant la partie : **aucune requête** pour valider un niveau
- La progression est écrite dans `localStorage`, puis synchronisée de temps en temps

## Structure

```text
config/                 # settings, urls
catalog/                # jeux, niveaux, seed
progress/               # progression session / utilisateur
templates/              # pages HTML
static/
  css/style.css
  js/games/flexbox/     # moteur + sync locale
```

## Installation

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_flexbox
python manage.py runserver
```

Ouvrir [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

- Accueil / catalogue : `/`
- Jeu Flexbox : `/jeux/css-flexbox/`
- Admin : `/admin/` (après `createsuperuser`)

## Sync progression

| Moment | Comportement |
|---|---|
| En jeu | `localStorage` immédiat |
| ~1,2 s après un succès | `POST /api/progress/css-flexbox/` |
| Onglet caché / retour online | nouvelle tentative de sync |

## Étendre

1. Ajouter des niveaux via l'admin ou `catalog/data/flexbox_levels.py` + `seed_flexbox`
2. Plus tard : nouveau jeu = nouveau slug + moteur JS dédié, même shell plateforme
