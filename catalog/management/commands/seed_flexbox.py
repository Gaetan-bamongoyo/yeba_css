from django.core.management.base import BaseCommand

from catalog.data.flexbox_levels import FLEXBOX_LEVELS
from catalog.models import Game, Level

UPCOMING_GAMES = [
    {
        "slug": "python",
        "title": "Python",
        "short_description": "Découvrez les bases de Python à travers des défis interactifs.",
        "description": "Parcours Python à venir.",
        "order": 2,
    },
    {
        "slug": "sql",
        "title": "SQL",
        "short_description": "Apprenez à interroger des données avec des requêtes ludiques.",
        "description": "Parcours SQL à venir.",
        "order": 3,
    },
]


class Command(BaseCommand):
    help = "Crée le jeu CSS Flexbox et les cartes à venir (Python, SQL)."

    def handle(self, *args, **options):
        game, created = Game.objects.update_or_create(
            slug="css-flexbox",
            defaults={
                "title": "CSS Flexbox",
                "short_description": "Mission : préparer l'interface de Nayekola avant le lancement.",
                "description": (
                    "La plateforme ouvre demain. Range chaque panneau de l'interface "
                    "avec Flexbox : header, cartes, menus et catalogue. "
                    "Tout le parcours se charge en une fois."
                ),
                "is_active": True,
                "order": 1,
            },
        )

        for index, payload in enumerate(FLEXBOX_LEVELS):
            Level.objects.update_or_create(
                game=game,
                order=index,
                defaults={
                    "title": payload["title"],
                    "difficulty": payload["difficulty"],
                    "objective": payload["objective"],
                    "item_count": payload.get("item_count", 1),
                    "target_styles": payload["target_styles"],
                    "starter_code": payload["starter_code"],
                    "is_active": True,
                },
            )

        action = "créé" if created else "mis à jour"
        self.stdout.write(
            self.style.SUCCESS(
                f"Jeu '{game.title}' {action} avec {len(FLEXBOX_LEVELS)} niveaux."
            )
        )

        for item in UPCOMING_GAMES:
            upcoming, upcoming_created = Game.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "short_description": item["short_description"],
                    "description": item["description"],
                    "is_active": True,
                    "order": item["order"],
                },
            )
            status = "créé" if upcoming_created else "mis à jour"
            self.stdout.write(
                self.style.SUCCESS(f"Carte '{upcoming.title}' {status} (bientôt).")
            )
