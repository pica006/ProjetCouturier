# app3.py
"""
Application Streamlit principale - Gestion Couturier
Fusion : beauté (app2) + fonctionnalité Render (app)
VERSION MINIMALE - uniquement CSS statique, pas de DOM dynamique
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
# STYLES CSS (statique uniquement - pas de @import, pas de ::before/::after)
# Évite les conflits DOM qui crashent sur Render
# =====================
st.markdown("""
<style>
.stApp { background: #FEFEFE !important; }
.main .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px; }
[data-testid="stSidebar"] { border-right: 2px solid #F5F5F5; }
.stButton > button {
    background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 500 !important;
}
.stButton > button:hover { opacity: 0.9; }
form button[data-baseweb="button"], form .stButton > button {
    background: linear-gradient(135deg, #40E0D0 0%, #B19CD9 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
}
.stTabs [data-baseweb="tab-list"] { background: #FAFAFA; padding: 0.5rem; border-radius: 12px; margin-bottom: 1rem; }
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
    color: #FFFFFF !important;
}
[data-testid="stMetricValue"] { font-size: 2rem; font-weight: 700; color: #2C2C2C; }
.stTextInput > div > div > input, .stNumberInput > div > div > input {
    border: 2px solid #F5F5F5 !important;
    border-radius: 8px !important;
}
.stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus {
    border-color: #B19CD9 !important;
}
.stDataFrame { border-radius: 12px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.stDataFrame th { background: #FAFAFA !important; color: #2C2C2C !important; font-weight: 600 !important; }
h1, h2, h3 { color: #2C2C2C; font-weight: 600; }
a { color: #B19CD9 !important; }
.stAlert { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# =====================
# ROUTER PRINCIPAL (identique à app.py)
# =====================
def main():

    if not st.session_state.authenticated:
        afficher_page_connexion()
        return

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
