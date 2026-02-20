"""
Service d'authentification - logique DB hors des vues.
Connexion et création de tables uniquement à l'action utilisateur (submit login).
"""

from typing import Optional, Tuple, Dict, Any


def authenticate(code: str, password: str) -> Tuple[bool, Optional[Dict], str, Optional[Any]]:
    from database import get_db
    db = get_db()
    if not db or not db.is_connected():
        return False, None, "Connexion base de données indisponible.", None
    _ensure_tables(db)
    from controllers.auth_controller import AuthController
    succes, donnees, message = AuthController(db).authentifier(code, password)
    return succes, donnees, message, db if succes else None


def _ensure_tables(db):
    from controllers.auth_controller import AuthController
    from controllers.commande_controller import CommandeController
    from models.database import ChargesModel
    AuthController(db).initialiser_tables()
    CommandeController(db).initialiser_tables()
    ChargesModel(db).creer_tables()
