"""
========================================
CONNEXION POSTGRESQL RENDER-SAFE (database.py)
========================================

Utilise UNIQUEMENT la variable d'environnement DATABASE_URL.
Une seule connexion partagée via st.cache_resource.
Aucune connexion au top-level, aucune reconnexion à chaque rerun.
"""

import os
from urllib.parse import urlparse

import streamlit as st

def _parse_database_url(url: str) -> dict:
    """
    Parse DATABASE_URL (format postgresql://user:pass@host:port/dbname)
    Retourne un dict compatible avec DatabaseConnection.
    """
    if not url or not url.strip():
        return {}
    # Render peut fournir postgres:// ou postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    try:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        ssl_default = "prefer" if host in ("localhost", "127.0.0.1") else "require"
        return {
            "host": host,
            "port": parsed.port or 5432,
            "database": (parsed.path or "/").lstrip("/") or "",
            "user": parsed.username or "",
            "password": parsed.password or "",
            "sslmode": os.getenv("DATABASE_SSLMODE", ssl_default),
        }
    except Exception:
        return {}


@st.cache_resource
def get_db():
    """
    Connexion PostgreSQL partagée via st.cache_resource.
    Appelée uniquement quand nécessaire (pas au top-level).
    Retourne DatabaseConnection ou None si DATABASE_URL manquant.
    """
    url = os.getenv("DATABASE_URL")
    if not url or not url.strip():
        return None
    config = _parse_database_url(url)
    if not all([config.get("host"), config.get("database"), config.get("user")]):
        return None
    try:
        from models.database import DatabaseConnection
        db = DatabaseConnection("postgresql", config)
        if db.connect():
            return db
    except Exception:
        pass
    return None


