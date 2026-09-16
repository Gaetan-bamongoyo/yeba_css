"""Mission SQL : Sauver l'année académique."""

DATASET = {
    "etudiants": [
        {"id": 1, "matricule": "ETU-001", "nom": "Kabongo", "postnom": "Mukendi", "prenom": "Jean", "sexe": "M"},
        {"id": 2, "matricule": "ETU-002", "nom": "Ilunga", "postnom": "Bahati", "prenom": "Marie", "sexe": "F"},
        {"id": 3, "matricule": "ETU-003", "nom": "Tshilombo", "postnom": "Kasongo", "prenom": "Paul", "sexe": "M"},
        {"id": 4, "matricule": "ETU-004", "nom": "Mbuyi", "postnom": "Nzuzi", "prenom": "Grace", "sexe": "F"},
        {"id": 5, "matricule": "ETU-005", "nom": "Bahati", "postnom": "Lumumba", "prenom": "David", "sexe": "M"},
        {"id": 6, "matricule": "ETU-006", "nom": "Nzuzi", "postnom": "Mutombo", "prenom": "Clara", "sexe": "F"},
        {"id": 7, "matricule": "ETU-007", "nom": "Kasongo", "postnom": "Mukendi", "prenom": "Kevin", "sexe": "M"},
        {"id": 8, "matricule": "ETU-008", "nom": "Lumumba", "postnom": "Ilunga", "prenom": "Sarah", "sexe": "F"},
        {"id": 9, "matricule": "ETU-009", "nom": "Mutombo", "postnom": "Tshilombo", "prenom": "Joel", "sexe": "M"},
        {"id": 10, "matricule": "ETU-010", "nom": "Mukendi", "postnom": "Mbuyi", "prenom": "Alice", "sexe": "F"},
        {"id": 11, "matricule": "ETU-011", "nom": "Tshisekedi", "postnom": "Kabila", "prenom": "Pierre", "sexe": "M"},
        {"id": 12, "matricule": "ETU-012", "nom": "Ilunga", "postnom": "Mbuyi", "prenom": "Sophie", "sexe": "F"},
        {"id": 13, "matricule": "ETU-013", "nom": "Bahati", "postnom": "Nzuzi", "prenom": "Marc", "sexe": "M"},
        {"id": 14, "matricule": "ETU-014", "nom": "Mukendi", "postnom": "Kasongo", "prenom": "Nina", "sexe": "F"},
        {"id": 15, "matricule": "ETU-015", "nom": "Kasongo", "postnom": "Bahati", "prenom": "Eric", "sexe": "M"},
    ],
    "filieres": [
        {"id": 1, "nom": "Informatique"},
        {"id": 2, "nom": "Droit"},
        {"id": 3, "nom": "Medecine"},
    ],
    "inscriptions": [
        {"id": 1, "etudiant_id": 1, "filiere_id": 1, "promotion": "L2", "annee_academique": "2025-2026"},
        {"id": 2, "etudiant_id": 2, "filiere_id": 1, "promotion": "L2", "annee_academique": "2025-2026"},
        {"id": 3, "etudiant_id": 3, "filiere_id": 2, "promotion": "L1", "annee_academique": "2025-2026"},
        {"id": 4, "etudiant_id": 4, "filiere_id": 1, "promotion": "L2", "annee_academique": "2025-2026"},
        {"id": 5, "etudiant_id": 5, "filiere_id": 2, "promotion": "L1", "annee_academique": "2025-2026"},
        {"id": 6, "etudiant_id": 6, "filiere_id": 3, "promotion": "L3", "annee_academique": "2025-2026"},
        {"id": 7, "etudiant_id": 7, "filiere_id": 1, "promotion": "L2", "annee_academique": "2025-2026"},
        {"id": 8, "etudiant_id": 8, "filiere_id": 2, "promotion": "L1", "annee_academique": "2025-2026"},
        {"id": 9, "etudiant_id": 9, "filiere_id": 3, "promotion": "L3", "annee_academique": "2025-2026"},
        {"id": 10, "etudiant_id": 10, "filiere_id": 1, "promotion": "L2", "annee_academique": "2025-2026"},
        {"id": 11, "etudiant_id": 11, "filiere_id": 2, "promotion": "L1", "annee_academique": "2024-2025"},
        {"id": 12, "etudiant_id": 12, "filiere_id": 1, "promotion": "L2", "annee_academique": "2025-2026"},
        {"id": 13, "etudiant_id": 13, "filiere_id": 2, "promotion": "L1", "annee_academique": "2025-2026"},
        {"id": 14, "etudiant_id": 14, "filiere_id": 3, "promotion": "L3", "annee_academique": "2025-2026"},
        {"id": 15, "etudiant_id": 15, "filiere_id": 3, "promotion": "L3", "annee_academique": "2025-2026"},
    ],
    "cours": [
        {"id": 1, "intitule": "Algorithmique", "credits": 4},
        {"id": 2, "intitule": "Base de donnees", "credits": 3},
        {"id": 3, "intitule": "Droit civil", "credits": 4},
        {"id": 4, "intitule": "Anatomie", "credits": 5},
        {"id": 5, "intitule": "Reseaux", "credits": 3},
        {"id": 6, "intitule": "Ethique", "credits": 2},
    ],
    "notes": [
        {"id": 1, "inscription_id": 1, "cours_id": 1, "note": 10},
        {"id": 2, "inscription_id": 1, "cours_id": 2, "note": 11},
        {"id": 3, "inscription_id": 1, "cours_id": 5, "note": 10},
        {"id": 4, "inscription_id": 1, "cours_id": 6, "note": 12},
        {"id": 5, "inscription_id": 2, "cours_id": 1, "note": 10},
        {"id": 6, "inscription_id": 2, "cours_id": 2, "note": 10},
        {"id": 7, "inscription_id": 2, "cours_id": 5, "note": 10},
        {"id": 8, "inscription_id": 2, "cours_id": 6, "note": 10},
        {"id": 9, "inscription_id": 3, "cours_id": 3, "note": 12},
        {"id": 10, "inscription_id": 3, "cours_id": 6, "note": 11},
        {"id": 11, "inscription_id": 3, "cours_id": 1, "note": 13},
        {"id": 12, "inscription_id": 3, "cours_id": 2, "note": 12},
        {"id": 13, "inscription_id": 4, "cours_id": 1, "note": 12},
        {"id": 14, "inscription_id": 4, "cours_id": 2, "note": 14},
        {"id": 15, "inscription_id": 4, "cours_id": 5, "note": 11},
        {"id": 16, "inscription_id": 4, "cours_id": 6, "note": 13},
        {"id": 17, "inscription_id": 5, "cours_id": 3, "note": 11},
        {"id": 18, "inscription_id": 5, "cours_id": 6, "note": 12},
        {"id": 19, "inscription_id": 5, "cours_id": 1, "note": 13},
        {"id": 20, "inscription_id": 5, "cours_id": 2, "note": 11},
        {"id": 21, "inscription_id": 6, "cours_id": 4, "note": 10},
        {"id": 22, "inscription_id": 6, "cours_id": 6, "note": 11},
        {"id": 23, "inscription_id": 6, "cours_id": 1, "note": 12},
        {"id": 24, "inscription_id": 6, "cours_id": 2, "note": 10},
        {"id": 25, "inscription_id": 7, "cours_id": 1, "note": 7},
        {"id": 26, "inscription_id": 7, "cours_id": 2, "note": 8},
        {"id": 27, "inscription_id": 7, "cours_id": 5, "note": 9},
        {"id": 28, "inscription_id": 7, "cours_id": 6, "note": 8},
        {"id": 29, "inscription_id": 8, "cours_id": 3, "note": 12},
        {"id": 30, "inscription_id": 8, "cours_id": 6, "note": 3},
        {"id": 31, "inscription_id": 8, "cours_id": 1, "note": 14},
        {"id": 32, "inscription_id": 8, "cours_id": 2, "note": 13},
        {"id": 33, "inscription_id": 9, "cours_id": 4, "note": 12},
        {"id": 34, "inscription_id": 9, "cours_id": 6, "note": 11},
        {"id": 35, "inscription_id": 9, "cours_id": 1, "note": 13},
        {"id": 36, "inscription_id": 9, "cours_id": 2, "note": 12},
        {"id": 37, "inscription_id": 10, "cours_id": 1, "note": 15},
        {"id": 38, "inscription_id": 10, "cours_id": 2, "note": 16},
        {"id": 39, "inscription_id": 10, "cours_id": 5, "note": 14},
        {"id": 40, "inscription_id": 10, "cours_id": 6, "note": 15},
        {"id": 41, "inscription_id": 11, "cours_id": 3, "note": 11},
        {"id": 42, "inscription_id": 11, "cours_id": 6, "note": 10},
        {"id": 43, "inscription_id": 12, "cours_id": 1, "note": 11},
        {"id": 44, "inscription_id": 12, "cours_id": 2, "note": 4},
        {"id": 45, "inscription_id": 12, "cours_id": 5, "note": 12},
        {"id": 46, "inscription_id": 12, "cours_id": 6, "note": 13},
        {"id": 47, "inscription_id": 13, "cours_id": 3, "note": 10},
        {"id": 48, "inscription_id": 13, "cours_id": 6, "note": 11},
        {"id": 49, "inscription_id": 13, "cours_id": 1, "note": 10},
        {"id": 50, "inscription_id": 13, "cours_id": 2, "note": 11},
        {"id": 51, "inscription_id": 14, "cours_id": 4, "note": 6},
        {"id": 52, "inscription_id": 14, "cours_id": 6, "note": 7},
        {"id": 53, "inscription_id": 14, "cours_id": 1, "note": 8},
        {"id": 54, "inscription_id": 14, "cours_id": 2, "note": 9},
        {"id": 55, "inscription_id": 15, "cours_id": 4, "note": 11},
        {"id": 56, "inscription_id": 15, "cours_id": 6, "note": 12},
        {"id": 57, "inscription_id": 15, "cours_id": 1, "note": 11},
        {"id": 58, "inscription_id": 15, "cours_id": 2, "note": 12},
    ],
    "paiements": [
        {"id": 1, "inscription_id": 1, "montant": 500, "date_paiement": "2025-10-01"},
        {"id": 2, "inscription_id": 2, "montant": 500, "date_paiement": "2025-10-02"},
        {"id": 3, "inscription_id": 3, "montant": 500, "date_paiement": "2025-10-03"},
        {"id": 4, "inscription_id": 4, "montant": 300, "date_paiement": "2025-10-04"},
        {"id": 5, "inscription_id": 4, "montant": 250, "date_paiement": "2025-11-10"},
        {"id": 6, "inscription_id": 5, "montant": 200, "date_paiement": "2025-10-05"},
        {"id": 7, "inscription_id": 5, "montant": 200, "date_paiement": "2025-11-05"},
        {"id": 8, "inscription_id": 5, "montant": 200, "date_paiement": "2025-12-01"},
        {"id": 9, "inscription_id": 6, "montant": 500, "date_paiement": "2025-10-06"},
        {"id": 10, "inscription_id": 7, "montant": 500, "date_paiement": "2025-10-07"},
        {"id": 11, "inscription_id": 8, "montant": 500, "date_paiement": "2025-10-08"},
        {"id": 12, "inscription_id": 9, "montant": 150, "date_paiement": "2025-10-09"},
        {"id": 13, "inscription_id": 9, "montant": 150, "date_paiement": "2025-11-09"},
        {"id": 14, "inscription_id": 10, "montant": 500, "date_paiement": "2025-10-10"},
        {"id": 15, "inscription_id": 11, "montant": 500, "date_paiement": "2024-10-01"},
        {"id": 16, "inscription_id": 12, "montant": 500, "date_paiement": "2025-10-11"},
        {"id": 17, "inscription_id": 13, "montant": 300, "date_paiement": "2025-10-12"},
        {"id": 18, "inscription_id": 13, "montant": 200, "date_paiement": "2025-11-12"},
        {"id": 19, "inscription_id": 14, "montant": 500, "date_paiement": "2025-10-13"},
        {"id": 20, "inscription_id": 15, "montant": 250, "date_paiement": "2025-10-14"},
        {"id": 21, "inscription_id": 15, "montant": 250, "date_paiement": "2025-11-14"},
    ],
}

# Liste officielle finale (9 étudiants admissibles, tri filière puis moyenne desc)
FINAL_OFFICIAL_LIST = [
    {
        "matricule": "ETU-003",
        "nom_complet": "Tshilombo Kasongo Paul",
        "filiere": "Droit",
        "promotion": "L1",
        "moyenne": 12,
        "total_paye": 500,
    },
    {
        "matricule": "ETU-005",
        "nom_complet": "Bahati Lumumba David",
        "filiere": "Droit",
        "promotion": "L1",
        "moyenne": 11.75,
        "total_paye": 600,
    },
    {
        "matricule": "ETU-013",
        "nom_complet": "Bahati Nzuzi Marc",
        "filiere": "Droit",
        "promotion": "L1",
        "moyenne": 10.5,
        "total_paye": 500,
    },
    {
        "matricule": "ETU-010",
        "nom_complet": "Mukendi Mbuyi Alice",
        "filiere": "Informatique",
        "promotion": "L2",
        "moyenne": 15,
        "total_paye": 500,
    },
    {
        "matricule": "ETU-004",
        "nom_complet": "Mbuyi Nzuzi Grace",
        "filiere": "Informatique",
        "promotion": "L2",
        "moyenne": 12.5,
        "total_paye": 550,
    },
    {
        "matricule": "ETU-001",
        "nom_complet": "Kabongo Mukendi Jean",
        "filiere": "Informatique",
        "promotion": "L2",
        "moyenne": 10.75,
        "total_paye": 500,
    },
    {
        "matricule": "ETU-002",
        "nom_complet": "Ilunga Bahati Marie",
        "filiere": "Informatique",
        "promotion": "L2",
        "moyenne": 10,
        "total_paye": 500,
    },
    {
        "matricule": "ETU-015",
        "nom_complet": "Kasongo Bahati Eric",
        "filiere": "Medecine",
        "promotion": "L3",
        "moyenne": 11.5,
        "total_paye": 500,
    },
    {
        "matricule": "ETU-006",
        "nom_complet": "Nzuzi Mutombo Clara",
        "filiere": "Medecine",
        "promotion": "L3",
        "moyenne": 10.75,
        "total_paye": 500,
    },
]

LEVELS = [
    {
        "title": "Mission 01 — Vérification du système",
        "difficulty": "Débutant",
        "scene": "Rectorat — 14h00",
        "objective": (
            "Le système de délibération vient de tomber en panne. "
            "Avant toute opération, le Rectorat doit s'assurer que les données "
            "des étudiants sont toujours présentes. "
            "Déterminez combien d'étudiants sont enregistrés dans la base."
        ),
        "hints": [
            "Il faut compter toutes les fiches présentes dans le registre des étudiants.",
            "Une seule valeur numérique doit être retournée.",
            "Pensez à une fonction d'agrégation sur la table etudiants.",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["etudiants"],
            "validation": {
                "type": "contains_row",
                "match": {"total": 15},
                "numeric_tolerance": 0.01,
            },
        },
    },
    {
        "title": "Mission 02 — Retrouver les étudiants concernés",
        "difficulty": "Débutant",
        "scene": "Registre académique",
        "objective": (
            "Bonne nouvelle : les données sont toujours présentes. "
            "Mais la base contient aussi les dossiers des années précédentes. "
            "Travaillez uniquement sur les étudiants inscrits en 2025-2026. "
            "Retrouvez-les."
        ),
        "hints": [
            "Les inscriptions indiquent l'année académique de chaque dossier.",
            "Reliez les inscriptions aux étudiants pour obtenir leurs informations.",
            "Filtrez sur l'année 2025-2026 dans la table inscriptions.",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["etudiants", "inscriptions"],
            "validation": {"type": "row_count", "count": 14},
        },
    },
    {
        "title": "Mission 03 — Construire l'identité académique",
        "difficulty": "Intermédiaire",
        "scene": "Secrétariat académique",
        "objective": (
            "Pour préparer la délibération, le secrétariat a besoin pour chaque "
            "étudiant concerné de : son matricule, son nom complet, sa filière "
            "et sa promotion. Ces informations sont réparties dans plusieurs "
            "parties de la base."
        ),
        "hints": [
            "Le nom complet combine plusieurs colonnes de la fiche étudiant.",
            "La filière n'est pas sur la fiche étudiant : cherchez la table dédiée.",
            "Croisez etudiants, inscriptions et filieres pour l'année 2025-2026.",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["etudiants", "inscriptions", "filieres"],
            "validation": {"type": "row_count", "count": 14},
        },
    },
    {
        "title": "Mission 04 — Calculer les résultats",
        "difficulty": "Intermédiaire",
        "scene": "Jury académique",
        "objective": (
            "Nous avons retrouvé toutes les notes. "
            "Connaissez la moyenne générale de chaque étudiant inscrit en 2025-2026."
        ),
        "hints": [
            "Les notes sont liées à une inscription, pas directement à l'étudiant.",
            "Reliez notes → inscriptions → etudiants, puis calculez une moyenne par étudiant.",
            "Regardez du côté de AVG() et GROUP BY après le JOIN.",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["etudiants", "inscriptions", "notes"],
            "validation": {
                "type": "contains_row",
                "match": {"matricule": "ETU-004", "moyenne": 12.5},
                "numeric_tolerance": 0.05,
            },
        },
    },
    {
        "title": "Mission 05 — Première sélection",
        "difficulty": "Intermédiaire",
        "scene": "Jury académique",
        "objective": (
            "Selon le règlement académique, un étudiant doit obtenir une moyenne "
            "générale d'au moins 10/20 pour passer en classe supérieure. "
            "Retirez de la liste les étudiants qui ne remplissent pas cette condition."
        ),
        "hints": [
            "Vous devez filtrer sur un résultat calculé, pas sur une colonne brute.",
            "Calculez d'abord la moyenne par étudiant pour 2025-2026.",
            "Seuls les étudiants avec moyenne >= 10 doivent rester.",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["etudiants", "inscriptions", "notes"],
            "validation": {"type": "row_count", "count": 12},
        },
    },
    {
        "title": "Mission 06 — ALERTE : note éliminatoire",
        "difficulty": "Avancé",
        "scene": "15h20 — Jury",
        "objective_html": (
            "<p class=\"sql-story-alert\">⚠ ALERTE — NOUVELLE INFORMATION DU JURY</p>"
            "<p>Ne transmettez surtout pas encore cette liste au Recteur.</p>"
            "<p>Nous venons de retrouver une disposition importante du règlement : "
            "même lorsqu'un étudiant possède une moyenne générale supérieure ou "
            "égale à 10/20, il ne peut pas passer s'il possède au moins une note "
            "inférieure à 5/20.</p>"
            "<p>Revérifiez tous les dossiers et retirez les étudiants concernés.</p>"
        ),
        "hints": [
            "Certains étudiants ont une bonne moyenne mais une note très basse.",
            "Cherchez ceux qui possèdent au moins une note strictement inférieure à 5.",
            "NOT EXISTS, NOT IN ou MIN(note) >= 5 sont des pistes possibles.",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["etudiants", "inscriptions", "filieres", "notes"],
            "validation": {"type": "row_count", "count": 10},
        },
    },
    {
        "title": "Mission 07 — Contrôle financier",
        "difficulty": "Avancé",
        "scene": "Service financier",
        "objective": (
            "La vérification académique est terminée. "
            "Le Rectorat exige que l'étudiant soit en ordre financièrement. "
            "Pour apparaître sur la liste finale, chaque étudiant doit avoir "
            "payé au moins 500 $. "
            "Attention : les frais peuvent avoir été payés en plusieurs tranches. "
            "Vérifiez la situation financière de chaque candidat encore en lice."
        ),
        "hints": [
            "Les paiements sont liés à une inscription ; plusieurs tranches sont possibles.",
            "Additionnez les montants par inscription pour obtenir le total payé.",
            "JOIN paiements → inscriptions, puis SUM() avec GROUP BY.",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["etudiants", "inscriptions", "filieres", "notes", "paiements"],
            "validation": {
                "type": "contains_row",
                "match": {"matricule": "ETU-005", "total_paye": 600},
                "numeric_tolerance": 0.01,
            },
        },
    },
    {
        "title": "Mission 08 — Liste provisoire",
        "difficulty": "Avancé",
        "scene": "15h35 — Rectorat",
        "objective": (
            "Nous avons maintenant toutes les informations nécessaires. "
            "Construisez la liste provisoire des étudiants qui remplissent "
            "simultanément toutes les conditions connues. "
            "Affichez : matricule, nom complet, filière, promotion, moyenne, total payé."
        ),
        "hints": [
            "Combinez inscription 2025-2026, moyenne >= 10, aucune note < 5, total >= 500.",
            "Vous pouvez utiliser des sous-requêtes ou plusieurs JOIN.",
            "Ne filtrez que les étudiants encore admissibles sur tous les critères.",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["etudiants", "inscriptions", "filieres", "notes", "paiements"],
            "validation": {
                "type": "result_set",
                "rows": FINAL_OFFICIAL_LIST,
                "numeric_tolerance": 0.05,
            },
        },
    },
    {
        "title": "Mission 09 — Dernière demande du Recteur",
        "difficulty": "Expert",
        "scene": "15h45 — Recteur",
        "objective_html": (
            "<p class=\"sql-story-time\">15:45</p>"
            "<p>La publication approche. Organisez la liste par filière. "
            "Dans chaque filière, les étudiants ayant les meilleures moyennes "
            "doivent apparaître en premier.</p>"
        ),
        "hints": [
            "Reprenez votre liste provisoire et imposez un ordre.",
            "Classez d'abord par filière, puis par moyenne décroissante.",
            "ORDER BY filiere, moyenne DESC",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["etudiants", "inscriptions", "filieres", "notes", "paiements"],
            "validation": {
                "type": "ordered_result",
                "rows": FINAL_OFFICIAL_LIST,
                "numeric_tolerance": 0.05,
            },
        },
    },
    {
        "title": "Mission 10 — MISSION FINALE",
        "difficulty": "Expert",
        "scene": "15h55 — URGENT",
        "objective_html": (
            "<p class=\"sql-story-time sql-story-time--urgent\">15:55 — URGENT</p>"
            "<p>Excellent travail. Mais nous ne pouvons pas refaire manuellement "
            "toutes ces opérations chaque année.</p>"
            "<p>Construisez <strong>une seule requête SQL</strong> capable de produire "
            "directement la liste officielle à partir de la base de données. "
            "Vous avez cinq minutes avant la publication.</p>"
            "<p>La liste doit contenir : matricule, nom complet, filière, promotion, "
            "moyenne, total payé — avec le même classement que demandé par le Recteur.</p>"
        ),
        "hints": [
            "Regroupez toute la logique dans une seule requête.",
            "2025-2026, moyenne >= 10, aucune note < 5, total payé >= 500.",
            "JOIN + GROUP BY + HAVING + sous-requête + ORDER BY filiere, moyenne DESC",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["etudiants", "inscriptions", "filieres", "notes", "paiements", "cours"],
            "validation": {
                "type": "ordered_result",
                "rows": FINAL_OFFICIAL_LIST,
                "numeric_tolerance": 0.05,
            },
        },
    },
]
