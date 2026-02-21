# app.py
"""
Application Streamlit principale - Gestion Couturier
Architecture MVC - Render SAFE
"""

import os
import streamlit as st

# =====================
# BOOTSTRAP VISUEL (ANTI ÉCRAN BLANC)
# =====================
st.set_page_config(page_title="Gestion Couturier", layout="wide")
st.write("⏳ Initialisation de l'application...")

# =====================
# ENV
# =====================
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if not DATABASE_URL:
    st.warning("⚠️ DATABASE_URL non détectée. Mode limité activé.")

# =====================
# SESSION STATE SAFE
# =====================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# =====================
# IMPORTS (APRÈS INIT)
# =====================
from views.auth_view import afficher_page_connexion
from views.commande_view import afficher_page_commande
from views.liste_view import afficher_liste_commandes
from components.bottom_nav import render_bottom_nav

# =====================
# ROUTER PRINCIPAL
# =====================
def main():

    if not st.session_state.authenticated:
        afficher_page_connexion()
        return

    # --- Pages internes
    if st.session_state.page == "commande":
        afficher_page_commande()
    elif st.session_state.page == "liste":
        afficher_liste_commandes()
    else:
        afficher_page_commande()

    # --- Navigation UNIQUEMENT SI AUTH
    render_bottom_nav({
        "app_name": "Gestion Couturier",
        "app_subtitle": "Pilotage intelligent"
    })


# =====================
# RUN
# =====================
main()