var levels = [
    {
        title: "Niveau 1 : Centrer horizontalement",
        difficulty: "Debutant",
        objective: "Utilisez <code class=\"inline-code\">justify-content</code> pour placer le carre au centre horizontalement.",
        target: {
            justifyContent: "center",
            alignItems: "flex-start"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 2 : Centrer verticalement",
        difficulty: "Debutant",
        objective: "Utilisez <code class=\"inline-code\">align-items</code> pour placer le carre au centre verticalement.",
        target: {
            justifyContent: "flex-start",
            alignItems: "center"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 3 : Centrer completement",
        difficulty: "Debutant",
        objective: "Combinez <code class=\"inline-code\">justify-content</code> et <code class=\"inline-code\">align-items</code> pour centrer le carre.",
        target: {
            justifyContent: "center",
            alignItems: "center"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 4 : Aller a droite",
        difficulty: "Intermediaire",
        objective: "Placez le carre sur la droite avec <code class=\"inline-code\">justify-content</code>.",
        target: {
            justifyContent: "flex-end",
            alignItems: "flex-start"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 5 : Bas droite",
        difficulty: "Intermediaire",
        objective: "Placez le carre en bas a droite en combinant les deux axes.",
        target: {
            justifyContent: "flex-end",
            alignItems: "flex-end"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 6 : Axe inverse",
        difficulty: "Avance",
        objective: "Utilisez <code class=\"inline-code\">flex-direction: column</code>, puis centrez le carre.",
        target: {
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center"
        },
        starterCode: "#container {\n  display: flex;\n  flex-direction: column;\n}"
    },
    {
        title: "Niveau 7 : Direction colonne",
        difficulty: "Avance",
        objective: "Avec <code class=\"inline-code\">flex-direction: column</code>, placez le carre en bas a gauche.",
        target: {
            flexDirection: "column",
            justifyContent: "flex-end",
            alignItems: "flex-start"
        },
        starterCode: "#container {\n  display: flex;\n  flex-direction: column;\n}"
    },
    {
        title: "Niveau 8 : Defi final",
        difficulty: "Expert",
        objective: "Placez le carre au centre bas. Observez bien l'axe horizontal et vertical.",
        target: {
            justifyContent: "center",
            alignItems: "flex-end"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 9 : Deux carres au centre",
        difficulty: "Intermediaire",
        objective: "Centrez deux carres ensemble au milieu de la zone.",
        itemCount: 2,
        target: {
            justifyContent: "center",
            alignItems: "center"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 10 : Deux carres a droite",
        difficulty: "Intermediaire",
        objective: "Placez les deux carres au centre vertical, colles a droite.",
        itemCount: 2,
        target: {
            justifyContent: "flex-end",
            alignItems: "center"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 11 : Trois carres espaces",
        difficulty: "Avance",
        objective: "Utilisez <code class=\"inline-code\">space-between</code> pour repartir trois carres sur toute la largeur.",
        itemCount: 3,
        target: {
            justifyContent: "space-between",
            alignItems: "center"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 12 : Trois carres autour du centre",
        difficulty: "Avance",
        objective: "Utilisez <code class=\"inline-code\">space-around</code> et centrez les carres verticalement.",
        itemCount: 3,
        target: {
            justifyContent: "space-around",
            alignItems: "center"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 13 : Trois carres equilibres",
        difficulty: "Avance",
        objective: "Utilisez <code class=\"inline-code\">space-evenly</code> pour repartir trois carres avec des espaces egaux.",
        itemCount: 3,
        target: {
            justifyContent: "space-evenly",
            alignItems: "center"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 14 : Colonne centree",
        difficulty: "Avance",
        objective: "Passez en colonne et centrez trois carres au milieu.",
        itemCount: 3,
        target: {
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 15 : Colonne en bas",
        difficulty: "Avance",
        objective: "Passez en colonne, puis placez les trois carres en bas au centre.",
        itemCount: 3,
        target: {
            flexDirection: "column",
            justifyContent: "flex-end",
            alignItems: "center"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 16 : Synthese colonne",
        difficulty: "Expert",
        objective: "Combinez <code class=\"inline-code\">flex-direction</code>, <code class=\"inline-code\">justify-content</code> et <code class=\"inline-code\">align-items</code> pour repartir trois carres en colonne.",
        itemCount: 3,
        target: {
            flexDirection: "column",
            justifyContent: "space-between",
            alignItems: "center"
        },
        starterCode: "#container {\n  display: flex;\n  flex-direction: column;\n}"
    },
    {
        title: "Niveau 17 : Synthese espace",
        difficulty: "Expert",
        objective: "Combinez <code class=\"inline-code\">justify-content</code>, <code class=\"inline-code\">align-items</code> et <code class=\"inline-code\">gap</code> pour centrer trois carres avec un grand espace.",
        itemCount: 3,
        target: {
            justifyContent: "center",
            alignItems: "center",
            gap: "24px"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 18 : Synthese bas gauche",
        difficulty: "Expert",
        objective: "En colonne, combinez les deux axes et <code class=\"inline-code\">gap</code> pour placer trois carres en bas a gauche.",
        itemCount: 3,
        target: {
            flexDirection: "column",
            justifyContent: "flex-end",
            alignItems: "flex-start",
            gap: "18px"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 19 : Synthese repartition",
        difficulty: "Expert",
        objective: "Utilisez plusieurs notions ensemble pour repartir quatre carres a droite, au centre vertical, avec un ecart regulier.",
        itemCount: 4,
        target: {
            justifyContent: "flex-end",
            alignItems: "center",
            gap: "12px"
        },
        starterCode: "#container {\n  display: flex;\n}"
    },
    {
        title: "Niveau 20 : Synthese finale",
        difficulty: "Expert",
        objective: "Defi final : combinez <code class=\"inline-code\">display</code>, <code class=\"inline-code\">flex-direction</code>, <code class=\"inline-code\">justify-content</code>, <code class=\"inline-code\">align-items</code> et <code class=\"inline-code\">gap</code>.",
        itemCount: 4,
        target: {
            flexDirection: "column",
            justifyContent: "flex-end",
            alignItems: "flex-end",
            gap: "12px"
        },
        starterCode: "#container {\n}"
    },
    {
        title: "Niveau 21 : Flex wrap et flex-flow",
        difficulty: "Expert",
        objective: "Utilisez <code class=\"inline-code\">flex-flow</code> pour definir la direction et le retour a la ligne, puis centrez les lignes avec <code class=\"inline-code\">align-content</code>.",
        itemCount: 8,
        target: {
            flexFlow: "row wrap",
            justifyContent: "center",
            alignItems: "center",
            alignContent: "center",
            gap: "12px"
        },
        starterCode: "#container {\n  display: flex;\n}"
    }
];
