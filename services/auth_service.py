"""
Service d'authentification - logique DB hors des vues.
"""

from typing import Optional, Tuple, Dict


def authenticate(code: str, password: str) -> Tuple[bool, Optional[Dict], str]:
    from database import get_db
    db = get_db()
    if not db or not db.is_connected():
        return False, None, "Connexion base de données indisponible."
    from controllers.auth_controller import AuthController
    return AuthController(db).authentifier(code, password)
