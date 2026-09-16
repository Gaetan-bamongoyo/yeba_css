"""Registre central des missions CSS."""

from catalog.data import css_technova
from catalog.data.flexbox_levels import FLEXBOX_LEVELS


def _level_to_pack(level, index):
    hints = level.get("hints") or []
    target = level.get("target_styles") or {}
    if not hints and isinstance(target, dict):
        hints = target.get("hints") or []
    hint = level.get("hint") or (hints[0] if hints else "")
    return {
        "id": index,
        "order": index,
        "title": level["title"],
        "difficulty": level["difficulty"],
        "scene": level.get("scene", ""),
        "objective": level.get("objective", ""),
        "hint": hint,
        "hints": hints,
        "itemCount": level.get("item_count", 1),
        "target": target,
        "starterCode": level.get("starter_code", ""),
    }


CSS_MISSIONS = [
    {
        "slug": "flexbox",
        "title": "Le site fantôme",
        "kicker": "Mission 01 — Flexbox",
        "short_description": (
            "Nayekola est figé. Chaque énigme rallume un fragment "
            "de l’interface grâce au CSS Flexbox."
        ),
        "difficulty": "Débutant → Avancé",
        "is_playable": True,
        "cover_image": "img/games/css-flexbox.svg",
        "order": 1,
        "progress_slug": "css-mission-flexbox",
        "progress_aliases": ["css-flexbox"],
        "stability_label": "Stabilité du site",
        "engine": "flexbox",
        "template": "games/flexbox.html",
        "level_count": len(FLEXBOX_LEVELS),
    },
    {
        "slug": "le-site-detruit",
        "title": "Le site détruit",
        "kicker": "Mission 02 — TechNova",
        "short_description": (
            "Le CSS de TechNova a disparu. Reconstruis progressivement "
            "toute l’apparence du site avant la présentation client."
        ),
        "difficulty": "Débutant → Expert",
        "is_playable": True,
        "cover_image": "img/games/css-technova.svg",
        "order": 2,
        "progress_slug": "css-mission-technova",
        "progress_aliases": ["css-technova"],
        "stability_label": "Restauration du site",
        "engine": "technova",
        "template": "games/technova.html",
        "level_count": len(css_technova.LEVELS),
    },
]

_MISSION_LEVELS = {
    "flexbox": FLEXBOX_LEVELS,
    "le-site-detruit": css_technova.LEVELS,
}


def get_css_mission(mission_slug):
    for mission in CSS_MISSIONS:
        if mission["slug"] == mission_slug:
            return mission
    return None


def get_css_mission_pack(mission_slug):
    meta = get_css_mission(mission_slug)
    raw_levels = _MISSION_LEVELS.get(mission_slug)
    if not meta or raw_levels is None:
        return None

    levels = [_level_to_pack(level, index) for index, level in enumerate(raw_levels)]
    pack = {
        **meta,
        "level_count": len(levels),
        "levels": levels,
    }
    if meta.get("engine") == "technova":
        pack["site_html"] = css_technova.TECHNOVA_SITE_HTML
        pack["reference_css"] = css_technova.TECHNOVA_REFERENCE_CSS
    return pack


def playable_mission_level_count():
    return sum(
        mission.get("level_count", 0)
        for mission in CSS_MISSIONS
        if mission.get("is_playable")
    )


def playable_mission_count():
    return sum(1 for mission in CSS_MISSIONS if mission.get("is_playable"))
