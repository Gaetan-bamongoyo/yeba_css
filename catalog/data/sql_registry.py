"""Registre central des missions SQL."""

from catalog.data import sql_annee_academique, sql_enfant_retrouve


def _level_to_pack(level, index):
    hints = level.get("hints") or []
    hint = level.get("hint") or (hints[0] if hints else "")
    return {
        "id": index,
        "order": index,
        "title": level["title"],
        "difficulty": level["difficulty"],
        "scene": level.get("scene", ""),
        "objective": level.get("objective", ""),
        "objectiveHtml": level.get("objective_html", ""),
        "hint": hint,
        "hints": hints,
        "itemCount": 1,
        "target": level.get("target_styles", {}),
        "starterCode": level.get("starter_code", ""),
        "successMessage": level.get("success_message", ""),
    }


def _mission_entry(meta, module):
    levels = [_level_to_pack(level, index) for index, level in enumerate(module.LEVELS)]
    return {
        **meta,
        "level_count": len(levels),
        "dataset": module.DATASET,
        "levels": levels,
        "victory": meta.get("victory") or {},
    }


SQL_MISSIONS = [
    {
        "slug": "enfant-retrouve",
        "title": "L'enfant retrouvé",
        "kicker": "Enquête 01",
        "short_description": (
            "Un enfant a été retrouvé sans papiers. "
            "Interroge les registres pour identifier son parent."
        ),
        "difficulty": "Débutant → Expert",
        "is_playable": True,
        "cover_image": "img/games/sql.svg",
        "order": 1,
        "progress_slug": "sql-mission-enfant-retrouve",
        "stability_label": "Enquête",
        "victory": {
            "kicker": "Enquête close",
            "title": "Bravo ! Le parent est retrouvé",
            "text": (
                "Grace Mwamba a été identifiée comme parent d'Amina. "
                "Tu as mené l'enquête SQL jusqu'au bout."
            ),
            "note": "Prochaine mission : Python arrive bientôt.",
        },
    },
    {
        "slug": "annee-academique",
        "title": "Sauver l'année académique",
        "kicker": "Mission SQL",
        "short_description": (
            "Le système de délibération est en panne. "
            "Reconstruis avant 16 h 00 la liste officielle des étudiants admissibles."
        ),
        "difficulty": "Débutant → Expert",
        "is_playable": True,
        "cover_image": "img/games/sql-annee-academique.svg",
        "order": 2,
        "progress_slug": "sql-mission-annee-academique",
        "stability_label": "Délibération",
        "victory": {
            "kicker": "Mission accomplie",
            "title": "La liste officielle est reconstruite",
            "text": (
                "Le système de délibération reste indisponible, mais grâce à votre "
                "maîtrise de SQL, le Rectorat peut publier les résultats à temps."
            ),
            "note": "SQL MISSION — TERMINÉE",
        },
    },
]

_MISSION_MODULES = {
    "enfant-retrouve": sql_enfant_retrouve,
    "annee-academique": sql_annee_academique,
}


def get_sql_mission(mission_slug):
    for mission in SQL_MISSIONS:
        if mission["slug"] == mission_slug:
            return mission
    return None


def get_sql_mission_pack(mission_slug):
    meta = get_sql_mission(mission_slug)
    module = _MISSION_MODULES.get(mission_slug)
    if not meta or not module:
        return None
    return _mission_entry(meta, module)


def playable_mission_level_count():
    return sum(
        len(_MISSION_MODULES[m["slug"]].LEVELS)
        for m in SQL_MISSIONS
        if m.get("is_playable") and m["slug"] in _MISSION_MODULES
    )
