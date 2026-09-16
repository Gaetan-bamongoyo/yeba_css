"""Mission SQL : L'enfant retrouvé."""

DATASET = {
    "enfants": [
        {"id": 1, "prenom": "Amina", "age": 7, "ville": "Kinshasa", "quartier": "Gombe"},
        {"id": 2, "prenom": "Kevin", "age": 9, "ville": "Kinshasa", "quartier": "Lemba"},
        {"id": 3, "prenom": "Sarah", "age": 6, "ville": "Lubumbashi", "quartier": "Kenya"},
        {"id": 4, "prenom": "Joel", "age": 8, "ville": "Kinshasa", "quartier": "Ngaliema"},
        {"id": 5, "prenom": "Maya", "age": 5, "ville": "Goma", "quartier": "Himbi"},
    ],
    "personnes": [
        {"id": 10, "nom": "Mwamba", "prenom": "Grace", "age": 34, "ville": "Kinshasa", "quartier": "Gombe", "telephone": "+243810000101"},
        {"id": 11, "nom": "Kabila", "prenom": "Paul", "age": 41, "ville": "Kinshasa", "quartier": "Lemba", "telephone": "+243810000102"},
        {"id": 12, "nom": "Ilunga", "prenom": "Marie", "age": 29, "ville": "Lubumbashi", "quartier": "Kenya", "telephone": "+243810000103"},
        {"id": 13, "nom": "Tshisekedi", "prenom": "Alice", "age": 37, "ville": "Kinshasa", "quartier": "Ngaliema", "telephone": "+243810000104"},
        {"id": 14, "nom": "Bahati", "prenom": "Jean", "age": 45, "ville": "Kinshasa", "quartier": "Gombe", "telephone": "+243810000105"},
        {"id": 15, "nom": "Nzuzi", "prenom": "Clara", "age": 31, "ville": "Goma", "quartier": "Himbi", "telephone": "+243810000106"},
        {"id": 16, "nom": "Mbuyi", "prenom": "David", "age": 38, "ville": "Kinshasa", "quartier": "Gombe", "telephone": "+243810000107"},
    ],
    "liens_familiaux": [
        {"parent_id": 10, "enfant_id": 1, "type_lien": "parent"},
        {"parent_id": 14, "enfant_id": 1, "type_lien": "oncle"},
        {"parent_id": 11, "enfant_id": 2, "type_lien": "parent"},
        {"parent_id": 12, "enfant_id": 3, "type_lien": "parent"},
        {"parent_id": 13, "enfant_id": 4, "type_lien": "parent"},
        {"parent_id": 15, "enfant_id": 5, "type_lien": "parent"},
        {"parent_id": 16, "enfant_id": 1, "type_lien": "voisin"},
    ],
    "signalements": [
        {"id": 1, "enfant_id": 1, "lieu": "Marché de Gombe", "temoin": "vendeuse de fruits"},
        {"id": 2, "enfant_id": 2, "lieu": "École de Lemba", "temoin": "enseignant"},
        {"id": 3, "enfant_id": 4, "lieu": "Parc Ngaliema", "temoin": "gardien"},
    ],
}

LEVELS = [
    {
        "title": "Énigme 01 — Une voix dans le registre",
        "difficulty": "Débutant",
        "scene": "Fichier central",
        "objective": (
            "On ne connaît d'elle qu'un prénom murmuré : Amina. "
            "Explore le registre des enfants et isole sa fiche."
        ),
        "hints": [
            "Commence par lire la table `enfants`, puis filtre sur le prénom.",
            "Un SELECT avec WHERE sur la colonne `prenom` suffit.",
            "SELECT * FROM enfants WHERE prenom = 'Amina'",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["enfants"],
            "validation": {
                "type": "contains_row",
                "match": {"prenom": "Amina", "id": 1},
            },
        },
    },
    {
        "title": "Énigme 02 — Ceux du même horizon",
        "difficulty": "Débutant",
        "scene": "Filtre géographique",
        "objective": (
            "Sa fiche révèle une ville. "
            "Liste tous les enfants enregistrés dans la même ville qu'elle — "
            "sans te fier à ta mémoire : déduis-la de ce que tu as déjà trouvé."
        ),
        "hints": [
            "Regarde la colonne `ville` d'Amina, puis refais un SELECT avec un WHERE.",
            "Kinshasa regroupe plusieurs enfants dans ce registre.",
            "SELECT * FROM enfants WHERE ville = 'Kinshasa'",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["enfants"],
            "validation": {"type": "row_count", "count": 3},
        },
    },
    {
        "title": "Énigme 03 — L'endroit du signalement",
        "difficulty": "Débutant",
        "scene": "Signalements",
        "objective": (
            "Quelqu'un a signalé sa disparition. "
            "Dans les signalements, retrouve celui qui correspond à Amina "
            "en te servant de l'identifiant découvert dans sa fiche."
        ),
        "hints": [
            "La table `signalements` contient une colonne qui pointe vers l'enfant.",
            "Relie l'id d'Amina à la colonne qui référence l'enfant.",
            "SELECT * FROM signalements WHERE enfant_id = 1",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["enfants", "signalements"],
            "validation": {
                "type": "contains_row",
                "match": {"enfant_id": 1, "lieu": "Marché de Gombe"},
            },
        },
    },
    {
        "title": "Énigme 04 — Les voisins du quartier",
        "difficulty": "Intermédiaire",
        "scene": "Annuaire",
        "objective": (
            "Le lieu du signalement (ou le quartier sur sa fiche) indique où chercher. "
            "Liste les personnes qui vivent dans ce même quartier."
        ),
        "hints": [
            "Ouvre `personnes` et filtre sur `quartier`.",
            "Le quartier est déjà visible dans tes résultats précédents.",
            "SELECT * FROM personnes WHERE quartier = 'Gombe'",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["enfants", "signalements", "personnes"],
            "validation": {"type": "row_count", "count": 3},
        },
    },
    {
        "title": "Énigme 05 — Trop de pistes ?",
        "difficulty": "Intermédiaire",
        "scene": "Analyse",
        "objective": (
            "Avant d'aller plus loin, mesure le terrain : "
            "combien de personnes vivent dans ce quartier ? "
            "Une seule valeur, nommée `total`."
        ),
        "hints": [
            "Il te faut une seule valeur numérique pour ce quartier.",
            "COUNT(*) avec un alias `total` répond à la question.",
            "SELECT COUNT(*) AS total FROM personnes WHERE quartier = 'Gombe'",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["enfants", "signalements", "personnes"],
            "validation": {"type": "contains_row", "match": {"total": 3}},
        },
    },
    {
        "title": "Énigme 06 — Des noms autour d'elle",
        "difficulty": "Intermédiaire",
        "scene": "Relations",
        "objective": (
            "Des adultes sont reliés à Amina dans `liens_familiaux`. "
            "Relie cette table aux personnes pour afficher "
            "leur nom, prénom et le type de lien — pour Amina seulement."
        ),
        "hints": [
            "Il te faut croiser `liens_familiaux` et `personnes`.",
            "Un JOIN entre les deux tables permet de relier parent et enfant.",
            "JOIN liens_familiaux et personnes, filtre enfant_id = 1",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["enfants", "signalements", "personnes", "liens_familiaux"],
            "validation": {"type": "row_count", "count": 3},
        },
    },
    {
        "title": "Énigme 07 — Le vrai lien du sang",
        "difficulty": "Avancé",
        "scene": "Filtre familial",
        "objective": (
            "Parmi ces liens, certains ne sont pas des parents. "
            "Garde uniquement le lien parental, "
            "et montre nom, prénom et téléphone."
        ),
        "hints": [
            "Observe les valeurs possibles dans `type_lien`.",
            "Seul le lien `parent` correspond au parent recherché.",
            "Filtre type_lien = 'parent' en plus du JOIN",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["enfants", "signalements", "personnes", "liens_familiaux"],
            "validation": {
                "type": "contains_row",
                "match": {"nom": "Mwamba", "prenom": "Grace"},
            },
        },
    },
    {
        "title": "Énigme 08 — La plus proche en âge",
        "difficulty": "Avancé",
        "scene": "Priorisation",
        "objective": (
            "Dans le quartier d'Amina, classe les personnes de la plus jeune à la plus âgée. "
            "La première ligne doit être la plus jeune."
        ),
        "hints": [
            "Filtre le quartier, puis impose un ordre sur l'âge.",
            "ORDER BY age ASC place la plus jeune en premier.",
            "WHERE quartier = 'Gombe' ORDER BY age ASC",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["enfants", "signalements", "personnes", "liens_familiaux"],
            "validation": {
                "type": "first_row",
                "match": {"prenom": "Grace", "nom": "Mwamba"},
            },
        },
    },
    {
        "title": "Énigme 09 — Même toit, même quartier",
        "difficulty": "Avancé",
        "scene": "Recoupement",
        "objective": (
            "Le parent recherché partage le quartier de l'enfant. "
            "Croise enfants, liens et personnes pour n'afficher "
            "que ce parent-là (nom, prénom, téléphone)."
        ),
        "hints": [
            "JOIN les trois tables, filtre le type parent.",
            "Compare les quartiers enfant/personne.",
            "JOIN enfants, liens_familiaux, personnes — type parent + même quartier",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["enfants", "signalements", "personnes", "liens_familiaux"],
            "validation": {
                "type": "contains_row",
                "match": {"nom": "Mwamba", "telephone": "+243810000101"},
            },
        },
    },
    {
        "title": "Énigme 10 — Le rapport de clôture",
        "difficulty": "Expert",
        "scene": "Clôture",
        "objective": (
            "Clos l'enquête : une seule ligne avec "
            "le nom et le prénom du parent, son téléphone, "
            "et le prénom de l'enfant sous l'alias `enfant`."
        ),
        "hints": [
            "Reprends ton JOIN final et sélectionne exactement quatre colonnes.",
            "Un alias permet de renommer la colonne enfant.",
            "SELECT nom, prenom, telephone, prenom AS enfant …",
        ],
        "starter_code": "",
        "target_styles": {
            "tables": ["enfants", "signalements", "personnes", "liens_familiaux"],
            "validation": {
                "type": "exact_result",
                "rows": [
                    {
                        "nom": "Mwamba",
                        "prenom": "Grace",
                        "telephone": "+243810000101",
                        "enfant": "Amina",
                    }
                ],
            },
        },
    },
]
