from django.core.management.base import BaseCommand

from catalog.data.flexbox_levels import FLEXBOX_LEVELS
from catalog.data.sql_registry import SQL_MISSIONS, get_sql_mission_pack
from catalog.models import Game, Level


class Command(BaseCommand):
    help = "Crée les jeux CSS Flexbox et SQL (missions du hub SQL)."

    def handle(self, *args, **options):
        self._seed_flexbox()
        self._seed_sql()
        self._seed_python_card()

    def _seed_flexbox(self):
        game, created = Game.objects.update_or_create(
            slug="css-flexbox",
            defaults={
                "title": "CSS Flexbox",
                "short_description": "Énigmes : réveille le site fantôme de Nayekola avec Flexbox.",
                "description": (
                    "Le site est figé. Chaque énigme te demande de remettre un fragment "
                    "d'interface à sa place grâce au CSS Flexbox."
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
                    "scene": payload.get("scene", ""),
                    "objective": payload["objective"],
                    "hint": payload.get("hint", ""),
                    "item_count": payload.get("item_count", 1),
                    "target_styles": payload["target_styles"],
                    "starter_code": payload["starter_code"],
                    "is_active": True,
                },
            )
        action = "créé" if created else "mis à jour"
        self.stdout.write(
            self.style.SUCCESS(f"Jeu '{game.title}' {action} ({len(FLEXBOX_LEVELS)} énigmes).")
        )

    def _seed_sql(self):
        game, created = Game.objects.update_or_create(
            slug="sql",
            defaults={
                "title": "SQL — Missions",
                "short_description": "Enquêtes SQL : résous des missions complètes étape par étape.",
                "description": (
                    "Choisis une mission SQL et reconstruis la vérité des données "
                    "avant la deadline."
                ),
                "is_active": True,
                "order": 2,
            },
        )
        game.levels.all().delete()
        order = 0
        total_levels = 0
        for mission_meta in SQL_MISSIONS:
            if not mission_meta.get("is_playable"):
                continue
            pack = get_sql_mission_pack(mission_meta["slug"])
            if not pack:
                continue
            for payload in pack["levels"]:
                target = dict(payload.get("target") or {})
                target["mission"] = mission_meta["slug"]
                Level.objects.create(
                    game=game,
                    order=order,
                    title=payload["title"],
                    difficulty=payload["difficulty"],
                    scene=payload.get("scene", ""),
                    objective=payload.get("objective") or payload.get("objectiveHtml", ""),
                    hint=payload.get("hint", ""),
                    item_count=1,
                    target_styles=target,
                    starter_code=payload.get("starterCode", ""),
                    is_active=True,
                )
                order += 1
                total_levels += 1
        action = "créé" if created else "mis à jour"
        self.stdout.write(
            self.style.SUCCESS(
                f"Jeu '{game.title}' {action} ({total_levels} niveaux, {len(SQL_MISSIONS)} missions)."
            )
        )

    def _seed_python_card(self):
        upcoming, created = Game.objects.update_or_create(
            slug="python",
            defaults={
                "title": "Python",
                "short_description": "Découvrez les bases de Python à travers des défis interactifs.",
                "description": "Parcours Python à venir.",
                "is_active": True,
                "order": 3,
            },
        )
        upcoming.levels.all().delete()
        status = "créée" if created else "mise à jour"
        self.stdout.write(self.style.SUCCESS(f"Carte '{upcoming.title}' {status} (bientôt)."))
