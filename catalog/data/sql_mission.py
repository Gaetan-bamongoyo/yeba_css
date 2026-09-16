"""Compatibilité : exports SQL historiques."""

from catalog.data.sql_enfant_retrouve import DATASET as SQL_DATASET
from catalog.data.sql_enfant_retrouve import LEVELS as SQL_LEVELS
from catalog.data.sql_registry import SQL_MISSIONS, get_sql_mission, get_sql_mission_pack

__all__ = [
    "SQL_DATASET",
    "SQL_LEVELS",
    "SQL_MISSIONS",
    "get_sql_mission",
    "get_sql_mission_pack",
]
