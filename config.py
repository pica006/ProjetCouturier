"""
Configuration - constantes, dictionnaires, chemins statiques uniquement.
"""

APP_CONFIG = {
    "name": "An's Learning",
    "subtitle": "Système de gestion d'atelier",
    "logo_path": "assets/logo",
    "wallpaper_url": "assets/background_dark.png",
}

PAGE_BACKGROUND_IMAGES = {
    "administration": "Admnistrateur.png",
    "super_admin_dashboard": "Admnistrateur.png",
    "nouvelle_commande": "commandes.png",
    "liste_commandes": "commandes.png",
    "dashboard": "TableauDeBord.png",
    "comptabilite": "Comptabilite.png",
    "charges": "Charges.png",
    "fermer_commandes": "commandes.png",
    "calendrier": "commandes.png",
}

BRANDING = {
    "primary": "#C9A227",
    "secondary": "#0E0B08",
    "accent": "#F5EFE6",
    "text_dark": "#1A140F",
    "text_light": "#F2ECE3",
}

COMPANY_INFO = {
    "name": "An's Learning",
    "address": "Douala - Kotto",
    "manager": "Sango Justin",
    "phone": "698192507",
    "email": "andresgroup63@gmail.com",
}

MODELES = {
    "adulte": {
        "homme": [
            "Costume 3 pièces",
            "Costume 2 pièces",
            "Pantalon classique",
            "Chemise sur mesure",
            "Veste",
            "Boubou",
            "Caftan",
            "Gandoura",
        ],
        "femme": [
            "Robe de soirée",
            "Robe cocktail",
            "Tailleur jupe",
            "Tailleur pantalon",
            "Robe traditionnelle",
            "Caftan",
            "Boubou",
            "Ensemble pagne",
        ],
    },
    "enfant": {
        "garcon": [
            "Costume enfant",
            "Pantalon",
            "Chemise",
            "Ensemble traditionnel",
            "Boubou enfant",
        ],
        "fille": [
            "Robe de cérémonie",
            "Robe casual",
            "Ensemble jupe",
            "Robe traditionnelle",
            "Boubou enfant",
        ],
    },
}

MESURES = {
    "Costume 3 pièces": [
        "Tour de cou", "Largeur épaules", "Tour de poitrine", "Tour de taille",
        "Tour de hanches", "Longueur dos", "Longueur manche", "Tour de bras",
        "Longueur pantalon", "Entrejambe", "Largeur pantalon (cuisse)",
    ],
    "Costume 2 pièces": [
        "Tour de cou", "Largeur épaules", "Tour de poitrine", "Tour de taille",
        "Tour de hanches", "Longueur dos", "Longueur manche", "Tour de bras",
        "Longueur pantalon", "Entrejambe", "Largeur pantalon (cuisse)",
    ],
    "Pantalon classique": [
        "Tour de taille", "Tour de hanches", "Longueur pantalon",
        "Entrejambe", "Largeur pantalon (cuisse)", "Largeur pantalon (bas)",
    ],
    "Chemise sur mesure": [
        "Tour de cou", "Largeur épaules", "Tour de poitrine", "Tour de taille",
        "Longueur dos", "Longueur manche", "Tour de bras", "Longueur chemise",
    ],
    "Veste": [
        "Tour de cou", "Largeur épaules", "Tour de poitrine", "Tour de taille",
        "Longueur dos", "Longueur manche", "Tour de bras", "Longueur veste",
    ],
    "Boubou": [
        "Tour de cou", "Largeur épaules", "Tour de poitrine", "Tour de taille",
        "Longueur dos", "Longueur manche", "Longueur boubou", "Largeur bas",
    ],
    "Caftan": [
        "Tour de cou", "Largeur épaules", "Tour de poitrine", "Tour de taille",
        "Tour de hanches", "Longueur dos", "Longueur manche", "Longueur caftan",
        "Largeur bas",
    ],
    "Gandoura": [
        "Tour de cou", "Largeur épaules", "Tour de poitrine", "Tour de taille",
        "Longueur dos", "Longueur manche", "Longueur gandoura", "Largeur bas",
    ],
    "Robe de soirée": [
        "Tour de cou", "Largeur épaules", "Tour de poitrine", "Tour de taille",
        "Tour de hanches", "Longueur dos", "Longueur manche", "Tour de bras",
        "Longueur robe", "Hauteur poitrine",
    ],
    "Robe cocktail": [
        "Tour de cou", "Largeur épaules", "Tour de poitrine", "Tour de taille",
        "Tour de hanches", "Longueur dos", "Longueur manche", "Tour de bras",
        "Longueur robe", "Hauteur poitrine",
    ],
    "Tailleur jupe": [
        "Tour de cou", "Largeur épaules", "Tour de poitrine", "Tour de taille",
        "Tour de hanches", "Longueur dos", "Longueur manche", "Tour de bras",
        "Longueur jupe", "Hauteur poitrine",
    ],
    "Tailleur pantalon": [
        "Tour de cou", "Largeur épaules", "Tour de poitrine", "Tour de taille",
        "Tour de hanches", "Longueur dos", "Longueur manche", "Tour de bras",
        "Longueur pantalon", "Entrejambe", "Hauteur poitrine",
    ],
    "Robe traditionnelle": [
        "Tour de cou", "Largeur épaules", "Tour de poitrine", "Tour de taille",
        "Tour de hanches", "Longueur dos", "Longueur manche", "Longueur robe",
        "Largeur bas",
    ],
    "Ensemble pagne": [
        "Tour de cou", "Largeur épaules", "Tour de poitrine", "Tour de taille",
        "Tour de hanches", "Longueur dos", "Longueur manche", "Longueur pagne",
        "Largeur bas",
    ],
    "Costume enfant": [
        "Tour de cou", "Tour de poitrine", "Tour de taille", "Longueur dos",
        "Longueur manche", "Longueur pantalon", "Entrejambe",
    ],
    "Pantalon": [
        "Tour de taille", "Tour de hanches", "Longueur pantalon",
        "Entrejambe", "Largeur pantalon (cuisse)",
    ],
    "Chemise": [
        "Tour de cou", "Tour de poitrine", "Tour de taille", "Longueur dos",
        "Longueur manche", "Longueur chemise",
    ],
    "Ensemble traditionnel": [
        "Tour de cou", "Tour de poitrine", "Tour de taille", "Longueur dos",
        "Longueur manche", "Longueur ensemble", "Largeur bas",
    ],
    "Boubou enfant": [
        "Tour de cou", "Tour de poitrine", "Tour de taille", "Longueur dos",
        "Longueur manche", "Longueur boubou", "Largeur bas",
    ],
    "Robe de cérémonie": [
        "Tour de cou", "Tour de poitrine", "Tour de taille", "Tour de hanches",
        "Longueur dos", "Longueur manche", "Longueur robe",
    ],
    "Robe casual": [
        "Tour de cou", "Tour de poitrine", "Tour de taille", "Tour de hanches",
        "Longueur dos", "Longueur manche", "Longueur robe",
    ],
    "Ensemble jupe": [
        "Tour de cou", "Tour de poitrine", "Tour de taille", "Tour de hanches",
        "Longueur dos", "Longueur manche", "Longueur jupe",
    ],
}

EMAIL_CONFIG = {
    "enabled": True,
    "host": "smtp.gmail.com",
    "port": 587,
    "user": "",
    "password": "",
    "from_email": "",
    "use_tls": True,
    "use_ssl": False,
}

PDF_STORAGE_PATH = "/tmp/pdfs"
CHARGES_STORAGE_PATH = "/tmp/charges_docs"
