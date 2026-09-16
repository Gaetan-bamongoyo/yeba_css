"""CSS Mission : Le site détruit — TechNova (10 missions cumulatives)."""

TECHNOVA_SITE_HTML = "\n<header class=\"site-header\" id=\"header\">\n  <div class=\"header-inner\">\n    <a class=\"logo\" href=\"#accueil\">TechNova</a>\n    <nav class=\"nav\" id=\"nav\">\n      <a href=\"#accueil\">Accueil</a>\n      <a href=\"#services\">Services</a>\n      <a href=\"#apropos\">À propos</a>\n      <a href=\"#contact\">Contact</a>\n    </nav>\n  </div>\n</header>\n\n<main>\n  <section class=\"hero\" id=\"accueil\">\n    <div class=\"hero-content\">\n      <h1 class=\"hero-title\">Des solutions numériques qui accélèrent votre croissance</h1>\n      <p class=\"hero-text\">\n        TechNova conçoit des expériences web, mobiles et cloud pour les entreprises\n        qui veulent avancer plus vite, avec plus de clarté.\n      </p>\n      <a class=\"btn btn-primary\" href=\"#contact\">Demander une démo</a>\n    </div>\n    <div class=\"hero-media\">\n      <img class=\"hero-image\" src=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='520' height='360' viewBox='0 0 520 360'%3E%3Crect width='520' height='360' rx='24' fill='%23DBEAFE'/%3E%3Ccircle cx='160' cy='150' r='58' fill='%232563EB' opacity='.85'/%3E%3Crect x='250' y='110' width='180' height='24' rx='8' fill='%231E3A8A'/%3E%3Crect x='250' y='150' width='140' height='16' rx='6' fill='%2360A5FA'/%3E%3Crect x='250' y='180' width='160' height='16' rx='6' fill='%2393C5FD'/%3E%3C/svg%3E\" alt=\"Illustration TechNova\">\n    </div>\n  </section>\n\n  <section class=\"services\" id=\"services\">\n    <h2 class=\"section-title\">Nos services</h2>\n    <p class=\"section-lead\">Trois expertises pour accompagner votre transformation digitale.</p>\n    <div class=\"services-grid\">\n      <article class=\"service-card\">\n        <h3>Développement Web</h3>\n        <p>Sites et plateformes performants, pensés pour la conversion et la clarté.</p>\n      </article>\n      <article class=\"service-card\">\n        <h3>Applications mobiles</h3>\n        <p>Expériences natives et hybrides centrées sur l’usage réel de vos équipes.</p>\n      </article>\n      <article class=\"service-card\">\n        <h3>Solutions Cloud</h3>\n        <p>Infrastructure scalable, sécurisée et maintenable pour vos produits numériques.</p>\n      </article>\n    </div>\n  </section>\n\n  <section class=\"about\" id=\"apropos\">\n    <div class=\"about-media\">\n      <img class=\"about-image\" src=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='420' height='320' viewBox='0 0 420 320'%3E%3Crect width='420' height='320' rx='20' fill='%23E2E8F0'/%3E%3Crect x='40' y='50' width='340' height='40' rx='8' fill='%232563EB'/%3E%3Crect x='40' y='110' width='220' height='18' rx='6' fill='%2394A3B8'/%3E%3Crect x='40' y='145' width='280' height='18' rx='6' fill='%23CBD5E1'/%3E%3Crect x='40' y='200' width='90' height='60' rx='10' fill='%230F172A'/%3E%3Crect x='150' y='200' width='90' height='60' rx='10' fill='%232563EB'/%3E%3Crect x='260' y='200' width='90' height='60' rx='10' fill='%231E293B'/%3E%3C/svg%3E\" alt=\"Équipe TechNova\">\n    </div>\n    <div class=\"about-content\">\n      <h2 class=\"section-title\">À propos de TechNova</h2>\n      <p class=\"about-text\">\n        Depuis plusieurs années, nous aidons les organisations à construire des produits\n        numériques fiables. Notre méthode combine design, ingénierie et accompagnement produit.\n      </p>\n      <div class=\"stats\">\n        <div class=\"stat\"><strong>120+</strong><span>projets livrés</span></div>\n        <div class=\"stat\"><strong>45</strong><span>experts</span></div>\n        <div class=\"stat\"><strong>98%</strong><span>clients satisfaits</span></div>\n      </div>\n    </div>\n  </section>\n\n  <section class=\"contact\" id=\"contact\">\n    <h2 class=\"section-title\">Contact</h2>\n    <div class=\"contact-layout\">\n      <div class=\"contact-info\">\n        <p><strong>Email :</strong> hello@technova.example</p>\n        <p><strong>Téléphone :</strong> +243 800 000 000</p>\n        <p><strong>Adresse :</strong> Kinshasa, RDC</p>\n      </div>\n      <form class=\"contact-form\" action=\"#\" method=\"post\" onsubmit=\"return false;\">\n        <label>Nom<input type=\"text\" name=\"name\" placeholder=\"Votre nom\"></label>\n        <label>Email<input type=\"email\" name=\"email\" placeholder=\"vous@exemple.com\"></label>\n        <label>Message<textarea name=\"message\" rows=\"4\" placeholder=\"Votre besoin\"></textarea></label>\n        <button class=\"btn btn-primary\" type=\"submit\">Envoyer</button>\n      </form>\n    </div>\n  </section>\n</main>\n\n<footer class=\"site-footer\" id=\"footer\">\n  <div class=\"footer-inner\">\n    <a class=\"logo footer-logo\" href=\"#accueil\">TechNova</a>\n    <nav class=\"footer-nav\">\n      <a href=\"#services\">Services</a>\n      <a href=\"#apropos\">À propos</a>\n      <a href=\"#contact\">Contact</a>\n    </nav>\n    <p class=\"copyright\">© 2026 TechNova. Tous droits réservés.</p>\n  </div>\n</footer>\n"

TECHNOVA_REFERENCE_CSS = "*, *::before, *::after { box-sizing: border-box; }\nhtml, body { margin: 0; padding: 0; }\nbody {\n  font-family: Arial, Helvetica, sans-serif;\n  background: #F8FAFC;\n  color: #1E293B;\n  line-height: 1.6;\n}\na { color: inherit; text-decoration: none; }\nimg { max-width: 100%; height: auto; display: block; }\n.site-header, .site-footer { background: #0F172A; color: #F8FAFC; }\n.header-inner, .footer-inner {\n  max-width: 1100px; margin: 0 auto; padding: 1rem 1.5rem;\n  display: flex; align-items: center; justify-content: space-between; gap: 1rem;\n}\n.logo { font-weight: 700; font-size: 1.25rem; letter-spacing: 0.02em; color: #fff; }\n.nav, .footer-nav { display: flex; gap: 1.25rem; flex-wrap: wrap; }\n.nav a, .footer-nav a { color: #CBD5E1; transition: color 0.2s ease; }\n.nav a:hover, .footer-nav a:hover { color: #fff; }\n.hero, .services, .about, .contact {\n  max-width: 1100px; margin: 0 auto; padding: 3rem 1.5rem;\n}\n.hero {\n  display: flex; align-items: center; justify-content: space-between; gap: 2.5rem;\n}\n.hero-content { flex: 1; }\n.hero-media { flex: 1; }\n.hero-title { font-size: 2.25rem; line-height: 1.2; margin: 0 0 1rem; color: #0F172A; }\n.hero-text { color: #64748B; margin: 0 0 1.5rem; }\n.btn {\n  display: inline-block; border: none; cursor: pointer;\n  padding: 0.75rem 1.25rem; border-radius: 0.5rem; font-weight: 600;\n  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;\n}\n.btn-primary {\n  background: #2563EB; color: #fff;\n  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);\n}\n.btn-primary:hover { background: #1D4ED8; transform: translateY(-1px); }\n.section-title { margin: 0 0 0.5rem; font-size: 1.75rem; color: #0F172A; }\n.section-lead, .about-text { color: #64748B; margin: 0 0 1.5rem; }\n.services-grid {\n  display: flex; gap: 1.25rem; align-items: stretch;\n}\n.service-card {\n  flex: 1; background: #fff; border-radius: 12px; padding: 1.25rem;\n  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);\n  transition: transform 0.2s ease, box-shadow 0.2s ease;\n}\n.service-card:hover {\n  transform: translateY(-4px);\n  box-shadow: 0 16px 32px rgba(15, 23, 42, 0.12);\n}\n.service-card h3 { margin-top: 0; color: #0F172A; }\n.about {\n  display: flex; gap: 2rem; align-items: center;\n}\n.about-media, .about-content { flex: 1; }\n.stats { display: flex; gap: 1rem; }\n.stat {\n  flex: 1; background: #EFF6FF; border-radius: 10px; padding: 0.9rem;\n  text-align: center;\n}\n.stat strong { display: block; font-size: 1.4rem; color: #2563EB; }\n.stat span { color: #64748B; font-size: 0.85rem; }\n.contact-layout { display: flex; gap: 2rem; }\n.contact-info, .contact-form { flex: 1; }\n.contact-form label { display: block; margin-bottom: 0.85rem; font-weight: 600; }\n.contact-form input, .contact-form textarea {\n  width: 100%; margin-top: 0.35rem; padding: 0.65rem 0.75rem;\n  border: 1px solid #CBD5E1; border-radius: 8px; font: inherit;\n}\n.copyright { margin: 0; color: #94A3B8; font-size: 0.9rem; }\n@media (max-width: 768px) {\n  .header-inner, .footer-inner { flex-direction: column; align-items: flex-start; }\n  .hero, .about, .contact-layout, .services-grid, .stats { flex-direction: column; }\n  .hero-title { font-size: 1.75rem; }\n}"

LEVELS = [
    {
        "title": "Mission 01 — La charte graphique",
        "difficulty": "Débutant",
        "scene": "Brief client",
        "objective": "Nous avons retrouvé la charte graphique du client. TechNova veut une identité moderne.\n\nCHARTE :\n• Couleur principale : #2563EB\n• Couleur foncée : #0F172A\n• Arrière-plan clair : #F8FAFC\n• Texte principal : #1E293B\n• Texte secondaire : #64748B\n• Police sans-serif (Arial ou équivalent)\n• box-sizing border-box pour éviter les problèmes de dimensions\n\nRestaurez les styles généraux de la page.",
        "starter_code": "/* TechNova — feuille de style à reconstruire */\n\n",
        "target_styles": {
            "validation": [
                {
                    "type": "computed",
                    "selector": "body",
                    "prop": "background-color",
                    "rgb": [
                        248,
                        250,
                        252
                    ]
                },
                {
                    "type": "computed",
                    "selector": "body",
                    "prop": "color",
                    "rgb": [
                        30,
                        41,
                        59
                    ]
                },
                {
                    "type": "font_sans",
                    "selector": "body"
                },
                {
                    "type": "box_border_box"
                }
            ],
            "hints": [
                "Commencez par soigner l’apparence globale du document (fond, texte, police).",
                "Le modèle de boîte influence toutes les largeurs : pensez à border-box.",
                "Travaillez sur body et, si besoin, sur * ou html pour box-sizing."
            ]
        }
    },
    {
        "title": "Mission 02 — Le menu est cassé",
        "difficulty": "Débutant",
        "scene": "Header",
        "objective": "Le client trouve que le menu ressemble encore à une liste HTML.\n\nIl souhaite : TechNova à gauche, et Accueil | Services | À propos | Contact à droite, alignés sur une seule ligne.",
        "starter_code": "",
        "target_styles": {
            "validation": [
                {
                    "type": "display_flex",
                    "selector": ".header-inner"
                },
                {
                    "type": "row_layout",
                    "selector": ".header-inner",
                    "child_a": ".logo",
                    "child_b": ".nav"
                },
                {
                    "type": "display_flex",
                    "selector": ".nav"
                }
            ],
            "hints": [
                "Il existe un système CSS pour organiser plusieurs éléments sur un même axe.",
                "Regardez du côté de Flexbox sur le conteneur du header.",
                "display:flex avec une répartition gauche/droite (space-between) est une piste solide."
            ]
        }
    },
    {
        "title": "Mission 03 — Le Hero",
        "difficulty": "Débutant",
        "scene": "Section Hero",
        "objective": "La maquette prévoit : à gauche le titre, le texte et le bouton ; à droite l’illustration. Les deux parties doivent être alignées et occuper l’espace disponible.",
        "starter_code": "",
        "target_styles": {
            "validation": [
                {
                    "type": "display_flex_or_grid",
                    "selector": ".hero"
                },
                {
                    "type": "side_by_side",
                    "selector": ".hero",
                    "child_a": ".hero-content",
                    "child_b": ".hero-media"
                }
            ],
            "hints": [
                "Le Hero contient deux zones à placer côte à côte.",
                "Flexbox (ou Grid) peut partager l’espace entre contenu et image.",
                "Sur .hero, un display flexible avec align-items aide beaucoup."
            ]
        }
    },
    {
        "title": "Mission 04 — Tout est collé",
        "difficulty": "Intermédiaire",
        "scene": "Espacements",
        "objective": "La structure apparaît, mais tout est trop serré. Donnez de l’air aux titres, paragraphes, boutons et sections — sans toucher au HTML.",
        "starter_code": "",
        "target_styles": {
            "validation": [
                {
                    "type": "min_padding",
                    "selector": ".hero",
                    "min": 24
                },
                {
                    "type": "min_padding",
                    "selector": ".services",
                    "min": 24
                },
                {
                    "type": "min_padding",
                    "selector": ".about",
                    "min": 24
                }
            ],
            "hints": [
                "Distinguez l’espace intérieur (padding) de l’espace extérieur (margin).",
                "Les sections (.hero, .services, .about, .contact) ont besoin de padding.",
                "Un max-width centré améliore aussi la lecture sur grand écran."
            ]
        }
    },
    {
        "title": "Mission 05 — Services en cartes",
        "difficulty": "Intermédiaire",
        "scene": "Services",
        "objective": "Les trois services ne doivent plus ressembler à de simples paragraphes. Chaque service devient une carte. Sur grand écran, les trois cartes apparaissent sur une même ligne, avec coins arrondis, fond et légère ombre.",
        "starter_code": "",
        "target_styles": {
            "validation": [
                {
                    "type": "cards_row",
                    "selector": ".services-grid",
                    "card": ".service-card",
                    "count": 3
                },
                {
                    "type": "min_radius",
                    "selector": ".service-card",
                    "min": 8
                },
                {
                    "type": "has_shadow",
                    "selector": ".service-card"
                },
                {
                    "type": "min_padding",
                    "selector": ".service-card",
                    "min": 12
                }
            ],
            "hints": [
                "Le conteneur .services-grid doit organiser les trois cartes.",
                "Chaque .service-card peut avoir padding, border-radius et box-shadow.",
                "Flexbox ou Grid permettent d’aligner les cartes horizontalement."
            ]
        }
    },
    {
        "title": "Mission 06 — Le site doit réagir",
        "difficulty": "Intermédiaire",
        "scene": "Interactions",
        "objective": "Le client trouve le site trop statique. Au survol d’un bouton, d’une carte de service ou d’un lien important, une réaction visuelle légère et professionnelle doit apparaître.",
        "starter_code": "",
        "target_styles": {
            "validation": [
                {
                    "type": "css_source",
                    "pattern": ":hover"
                },
                {
                    "type": "css_source",
                    "pattern": "transition"
                }
            ],
            "hints": [
                "CSS permet de changer l’apparence au passage de la souris.",
                "La pseudo-classe :hover est faite pour ça.",
                "Ajoutez aussi une transition pour un effet fluide, pas brutal."
            ]
        }
    },
    {
        "title": "Mission 07 — Problème d’images",
        "difficulty": "Intermédiaire",
        "scene": "⚠ Designer",
        "objective": "⚠ PROBLÈME SIGNALÉ PAR LE DESIGNER\n\nCertaines images débordent et déforment la page. Elles doivent rester dans leur conteneur tout en gardant une belle apparence.",
        "starter_code": "",
        "target_styles": {
            "validation": [
                {
                    "type": "img_contained",
                    "selector": "img"
                }
            ],
            "hints": [
                "Une image trop large peut forcer un débordement horizontal.",
                "Limitez la largeur des images par rapport à leur parent.",
                "max-width: 100% (et height: auto) est une solution classique."
            ]
        }
    },
    {
        "title": "Mission 08 — Catastrophe sur mobile",
        "difficulty": "Avancé",
        "scene": "⚠ 30 min",
        "objective": "⚠ 30 MINUTES AVANT LA PRÉSENTATION\n\nSur téléphone, menu, Hero et cartes cassent. Rendez le site utilisable sur mobile sans modifier le HTML.",
        "starter_code": "",
        "target_styles": {
            "validation": [
                {
                    "type": "css_source",
                    "pattern": "@media"
                },
                {
                    "type": "mobile_stack",
                    "width": 390
                }
            ],
            "hints": [
                "Le même CSS ne doit pas forcément s’appliquer à toutes les largeurs d’écran.",
                "CSS peut appliquer des règles seulement quand l’écran devient petit.",
                "Regardez du côté de @media et de flex-direction: column."
            ]
        }
    },
    {
        "title": "Mission 09 — Les finitions",
        "difficulty": "Avancé",
        "scene": "15 min",
        "objective": "15 MINUTES AVANT LA PRÉSENTATION\n\nComparez avec la maquette mentale du client : hiérarchie des titres, boutons, footer, couleurs cohérentes, lisibilité. Le site doit sembler terminé.",
        "starter_code": "",
        "target_styles": {
            "validation": [
                {
                    "type": "computed",
                    "selector": ".site-header",
                    "prop": "background-color",
                    "rgb": [
                        15,
                        23,
                        42
                    ]
                },
                {
                    "type": "computed",
                    "selector": ".site-footer",
                    "prop": "background-color",
                    "rgb": [
                        15,
                        23,
                        42
                    ]
                },
                {
                    "type": "computed",
                    "selector": ".btn-primary",
                    "prop": "background-color",
                    "rgb": [
                        37,
                        99,
                        235
                    ]
                },
                {
                    "type": "display_flex_or_grid",
                    "selector": ".contact-layout"
                }
            ],
            "hints": [
                "Le header et le footer sombres renforcent l’identité TechNova.",
                "Le bouton principal doit utiliser la couleur de marque.",
                "Vérifiez aussi la section contact et le footer."
            ]
        }
    },
    {
        "title": "Mission 10 — Livraison client",
        "difficulty": "Expert",
        "scene": "5 min",
        "objective": "5 MINUTES AVANT LA PRÉSENTATION\n\nDernière vérification : site stylisé, cohérent, lisible, responsive, fidèle à la maquette, utilisable sur ordinateur et mobile. Finalisez votre feuille de style.",
        "starter_code": "",
        "target_styles": {
            "validation": [
                {
                    "type": "computed",
                    "selector": "body",
                    "prop": "background-color",
                    "rgb": [
                        248,
                        250,
                        252
                    ]
                },
                {
                    "type": "display_flex",
                    "selector": ".header-inner"
                },
                {
                    "type": "side_by_side",
                    "selector": ".hero",
                    "child_a": ".hero-content",
                    "child_b": ".hero-media"
                },
                {
                    "type": "cards_row",
                    "selector": ".services-grid",
                    "card": ".service-card",
                    "count": 3
                },
                {
                    "type": "img_contained",
                    "selector": "img"
                },
                {
                    "type": "css_source",
                    "pattern": ":hover"
                },
                {
                    "type": "css_source",
                    "pattern": "@media"
                },
                {
                    "type": "mobile_stack",
                    "width": 390
                },
                {
                    "type": "computed",
                    "selector": ".btn-primary",
                    "prop": "background-color",
                    "rgb": [
                        37,
                        99,
                        235
                    ]
                }
            ],
            "hints": [
                "Reprenez toute la checklist : charte, header, hero, cartes, images, mobile.",
                "Si un point manque, relisez les missions précédentes.",
                "Le CSS cumulatif doit contenir à la fois le desktop et le @media mobile."
            ]
        }
    }
]
