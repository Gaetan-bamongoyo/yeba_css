from django.core.management.base import BaseCommand

from catalog.data.css_registry import CSS_MISSIONS, get_css_mission_pack
from catalog.data.css_technova import LEVELS as TECHNOVA_LEVELS
from catalog.data.flexbox_levels import FLEXBOX_LEVELS
from catalog.data.sql_registry import SQL_MISSIONS, get_sql_mission_pack
from catalog.models import Game, Level


class Command(BaseCommand):
    help = (
        "Initialise le catalogue : hub CSS (Flexbox + Le site détruit), "
        "hub SQL, et carte Python (bientôt)."
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Seed Nayekola"))
        self._seed_css_hub()
        self._seed_sql()
        self._seed_python_card()
        self.stdout.write(self.style.SUCCESS("Seed terminé."))

    def _seed_css_hub(self):
        """Catégorie CSS — Missions (Flexbox + TechNova / Le site détruit)."""
        Game.objects.filter(slug__in=["css-flexbox", "css-technova"]).update(is_active=False)

        game, created = Game.objects.update_or_create(
            slug="css",
            defaults={
                "title": "CSS — Missions",
                "short_description": (
                    "Missions CSS : Flexbox, reconstruction de site et plus encore."
                ),
                "description": (
                    "Choisis une mission CSS et progresse étape par étape "
                    "en reconstruisant de vraies interfaces."
                ),
                "is_active": True,
                "order": 1,
            },
        )
        game.levels.all().delete()

        order = 0
        total_levels = 0
        mission_summaries = []

        for mission_meta in CSS_MISSIONS:
            if not mission_meta.get("is_playable"):
                mission_summaries.append(f"  · {mission_meta['title']} (bientôt)")
                continue

            pack = get_css_mission_pack(mission_meta["slug"])
            if not pack:
                mission_summaries.append(f"  · {mission_meta['title']} (pack manquant)")
                continue

            mission_level_count = 0
            for payload in pack["levels"]:
                target = dict(payload.get("target") or {})
                target["mission"] = mission_meta["slug"]
                if payload.get("hints"):
                    target["hints"] = payload["hints"]
                Level.objects.create(
                    game=game,
                    order=order,
                    title=payload["title"],
                    difficulty=payload["difficulty"],
                    scene=payload.get("scene", ""),
                    objective=payload.get("objective", ""),
                    hint=payload.get("hint", ""),
                    item_count=payload.get("itemCount", 1),
                    target_styles=target,
                    starter_code=payload.get("starterCode", ""),
                    is_active=True,
                )
                order += 1
                total_levels += 1
                mission_level_count += 1

            mission_summaries.append(
                f"  · {mission_meta['title']} "
                f"(/jeux/css/mission/{mission_meta['slug']}/) — "
                f"{mission_level_count} niveaux"
            )

        action = "créée" if created else "mise à jour"
        self.stdout.write(
            self.style.SUCCESS(
                f"CSS hub '{game.title}' {action} "
                f"({total_levels} niveaux, {len(CSS_MISSIONS)} missions)."
            )
        )
        for line in mission_summaries:
            self.stdout.write(line)

        self._seed_legacy_flexbox_inactive()
        self._seed_legacy_technova_inactive()

    def _seed_legacy_flexbox_inactive(self):
        """Conserve le slug legacy (redirigé vers le hub CSS)."""
        game, _ = Game.objects.update_or_create(
            slug="css-flexbox",
            defaults={
                "title": "CSS Flexbox",
                "short_description": "Énigmes Flexbox (intégré au hub CSS).",
                "description": "Redirigé vers /jeux/css/mission/flexbox/",
                "is_active": False,
                "order": 90,
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
        self.stdout.write(
            f"  · Legacy css-flexbox inactif ({len(FLEXBOX_LEVELS)} niveaux conservés)."
        )

    def _seed_legacy_technova_inactive(self):
        """Conserve le slug legacy TechNova (redirigé vers le hub CSS)."""
        game, _ = Game.objects.update_or_create(
            slug="css-technova",
            defaults={
                "title": "CSS Mission : Le site détruit",
                "short_description": "TechNova (intégré au hub CSS).",
                "description": "Redirigé vers /jeux/css/mission/le-site-detruit/",
                "is_active": False,
                "order": 91,
            },
        )
        for index, payload in enumerate(TECHNOVA_LEVELS):
            hints = (payload.get("target_styles") or {}).get("hints") or []
            Level.objects.update_or_create(
                game=game,
                order=index,
                defaults={
                    "title": payload["title"],
                    "difficulty": payload["difficulty"],
                    "scene": payload.get("scene", ""),
                    "objective": payload["objective"],
                    "hint": hints[0] if hints else payload.get("hint", ""),
                    "item_count": 1,
                    "target_styles": payload["target_styles"],
                    "starter_code": payload.get("starter_code") or "",
                    "is_active": True,
                },
            )
        self.stdout.write(
            f"  · Legacy css-technova inactif ({len(TECHNOVA_LEVELS)} niveaux conservés)."
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
                f"SQL hub '{game.title}' {action} "
                f"({total_levels} niveaux, {len(SQL_MISSIONS)} missions)."
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
