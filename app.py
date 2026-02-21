# app3.py
"""
Gestion Couturier - Version STABLE
"""

import os
import streamlit as st

# =====================
# BOOTSTRAP (identique app.py - PAS de placeholder)
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

if "db" not in st.session_state:
    from database import get_db
    st.session_state.db = get_db()

# =====================
# IMPORTS (APRÈS INIT)
# =====================
from views.auth_view import afficher_page_connexion
from components.bottom_nav import render_bottom_nav
from views.commande_view import afficher_page_commande
from views.liste_view import afficher_page_liste_commandes
from views.comptabilite_view import afficher_page_comptabilite
from views.dashboard_view import afficher_page_dashboard
from views.mes_charges_view import afficher_page_mes_charges
from views.admin_view import afficher_page_administration
from views.fermer_commandes_view import afficher_page_fermer_commandes
from views.calendrier_view import afficher_page_calendrier
from views.super_admin_dashboard import afficher_dashboard_super_admin
from utils.role_utils import est_admin
from utils.bottom_nav import render_bottom_nav as render_nav_footer
from utils.permissions import est_super_admin

# =====================
# CSS sidebar : boutons gradient violet-bleu (comme image 2)
# =====================
st.markdown("""
<style>
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    width: 100% !important;
    text-align: left !important;
}
</style>
""", unsafe_allow_html=True)

# =====================
# ROUTER
# =====================
def main():
    if not st.session_state.authenticated:
        # Sidebar : image nav.png si dispo (remplace le bandeau bleu)
        nav_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "nav.png")
        if os.path.exists(nav_path):
            with st.sidebar:
                st.image(nav_path, width=300)
        afficher_page_connexion()
        return

    # --- Sidebar : navigation (comme image 2)
    with st.sidebar:
        st.markdown("### 📋 Navigation")
        if st.button("📊 Tableau de bord", key="sb_dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
        if st.button("➕ Nouvelle commande", key="sb_commande"):
            st.session_state.page = "commande"
            st.rerun()
        if st.button("📋 Mes commandes", key="sb_liste"):
            st.session_state.page = "liste"
            st.rerun()
        if st.button("💰 Comptabilité", key="sb_compta"):
            st.session_state.page = "comptabilite"
            st.rerun()
        if st.button("📄 Mes frais", key="sb_charges"):
            st.session_state.page = "charges"
            st.rerun()
        if st.button("🔒 Fermer mes commandes", key="sb_fermer"):
            st.session_state.page = "fermer_commandes"
            st.rerun()
        if st.button("📅 Modèles & Calendrier", key="sb_calendrier"):
            st.session_state.page = "calendrier"
            st.rerun()
        if est_admin(st.session_state.get("user") or st.session_state.get("couturier_data") or {}):
            st.markdown("---")
            st.markdown("### 👑 Administration")
            if st.button("👑 Administration", key="sb_admin"):
                st.session_state.page = "admin"
                st.rerun()
        st.markdown("---")
        if st.button("🚪 Déconnexion", key="sb_deco"):
            st.session_state.authenticated = False
            st.session_state.page = "login"
            st.rerun()

    page = st.session_state.page
    if page in ("commande", "nouvelle_commande"):
        afficher_page_commande()
    elif page in ("liste", "liste_commandes"):
        afficher_page_liste_commandes()
    elif page == "dashboard":
        afficher_page_dashboard()
    elif page == "comptabilite":
        afficher_page_comptabilite()
    elif page == "charges":
        afficher_page_mes_charges()
    elif page == "fermer_commandes":
        afficher_page_fermer_commandes()
    elif page == "calendrier":
        afficher_page_calendrier()
    elif page == "admin":
        afficher_page_administration()
    elif page == "super_admin":
        afficher_dashboard_super_admin()
    else:
        afficher_page_commande()

    render_bottom_nav({})
    render_nav_footer({
        "app_name": "Gestion Couturier",
        "app_subtitle": "Pilotage intelligent"
    })


main()
