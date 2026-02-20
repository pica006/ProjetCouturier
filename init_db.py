"""
Initialisation base de données - exécuté UNE SEULE FOIS au démarrage.
"""

import streamlit as st


@st.cache_resource
def init_db():
    db = _get_db()
    if db:
        _create_tables(db)
    return db


def _get_db():
    from database import get_db
    return get_db()


def _create_tables(db):
    from controllers.auth_controller import AuthController
    from controllers.commande_controller import CommandeController
    from models.database import ChargesModel
    AuthController(db).initialiser_tables()
    CommandeController(db).initialiser_tables()
    ChargesModel(db).creer_tables()
