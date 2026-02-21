# app3.py
"""
Application Streamlit principale - Gestion Couturier
Fusion : beauté (app2) + fonctionnalité Render (app)
"""

import os
import base64
import streamlit as st

# =====================
# BOOTSTRAP VISUEL (ANTI ÉCRAN BLANC)
# =====================
st.set_page_config(
    page_title="Gestion Couturier",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)
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
from config import PAGE_BACKGROUND_IMAGES

# =====================
# HELPERS BEAUTÉ (safe - os.path.exists + try/except)
# =====================
def _get_sidebar_bg_css(use_image: bool) -> str:
    """Fond sidebar : image nav.png si dispo, sinon beige. Ne crash jamais."""
    if not use_image:
        return "background: #FAFAFA !important;"
    try:
        project_root = os.path.dirname(os.path.abspath(__file__))
        nav_path = os.path.join(project_root, "assets", "nav.png")
        if os.path.exists(nav_path):
            with open(nav_path, "rb") as f:
                nav_b64 = base64.b64encode(f.read()).decode("utf-8")
            return f"""
                background-image: url('data:image/png;base64,{nav_b64}') !important;
                background-size: cover !important;
                background-position: center !important;
                background-repeat: no-repeat !important;
            """
    except Exception:
        pass
    return "background: #FAFAFA !important;"


def _get_page_background_html(page_id: str) -> str:
    """Image de fond par page (floue) + logo coin. Retourne '' si fichiers absents. Ne crash jamais."""
    page_to_config = {
        "commande": "nouvelle_commande", "nouvelle_commande": "nouvelle_commande",
        "liste": "liste_commandes", "liste_commandes": "liste_commandes",
        "admin": "administration", "super_admin": "super_admin_dashboard",
        "dashboard": "dashboard", "comptabilite": "comptabilite",
        "charges": "charges", "fermer_commandes": "fermer_commandes", "calendrier": "calendrier",
    }
    config_key = page_to_config.get(page_id, page_id)
    image_name = PAGE_BACKGROUND_IMAGES.get(config_key)
    logo_html = ""
    try:
        project_root = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(project_root, "assets", "logoBon.png")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f_logo:
                logo_b64 = base64.b64encode(f_logo.read()).decode("utf-8")
            logo_html = f'<div style="position:fixed;top:1rem;left:1rem;z-index:99999;width:100px;height:auto;background:rgba(255,255,255,0.95);padding:6px;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.15);"><img src="data:image/png;base64,{logo_b64}" alt="Logo" style="width:100%;height:auto;display:block;"></div>'
    except Exception:
        pass
    if not image_name:
        return logo_html
    try:
        project_root = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(project_root, "assets", image_name)
        if not os.path.exists(img_path):
            return logo_html
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(image_name)[1].lower()
        mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
        data_uri = f"data:{mime};base64,{b64}"
        data_uri_css = data_uri.replace("'", "\\'")
        return f"""
        {logo_html}
        <style id="page-bg-style">
        body .main, section.main {{ position: relative !important; min-height: 100vh !important; }}
        body .main::before, section.main::before {{
            content: '' !important;
            position: absolute !important;
            inset: 0 !important;
            z-index: -2 !important;
            background-image: url('{data_uri_css}') !important;
            background-size: cover !important;
            background-position: center !important;
            filter: blur(14px) !important;
            opacity: 0.75 !important;
        }}
        body .main::after, section.main::after {{
            content: '' !important;
            position: absolute !important;
            inset: 0 !important;
            z-index: -1 !important;
            background: rgba(255, 255, 255, 0.72) !important;
        }}
        body .main .block-container, .main .block-container {{
            background: rgba(255, 255, 255, 0.98) !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 14px rgba(0, 0, 0, 0.05) !important;
        }}
        </style>
        """
    except Exception:
        return logo_html


def _sidebar_styles_css(sidebar_bg_css: str) -> str:
    """Styles sidebar (palette pastel). CSS pur, pas de JS."""
    return f"""
    <style>
    [data-testid="stSidebar"] {{
        {sidebar_bg_css}
    }}
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
        background: transparent !important;
    }}
    [data-testid="stSidebar"] .stButton > button {{
        background: linear-gradient(180deg, rgba(246, 239, 232, 0.9) 0%, rgba(143, 186, 217, 0.88) 50%, rgba(154, 143, 216, 0.87) 100%) !important;
        background-color: transparent !important;
        color: #3B2F4A !important;
        border: 1px solid rgba(59, 47, 74, 0.12) !important;
        border-radius: 12px !important;
        padding: 0.7rem 1rem !important;
        font-weight: 500 !important;
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        background: linear-gradient(175deg, rgba(246, 239, 232, 0.95) 0%, rgba(143, 186, 217, 0.9) 45%, rgba(154, 143, 216, 0.9) 100%) !important;
        box-shadow: 0 2px 8px rgba(59, 47, 74, 0.12) !important;
    }}
    </style>
    """


# =====================
# STYLES CSS (BEAUTÉ app2 - SANS JS pour éviter crash Render)
# =====================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    :root {
        --violet-clair: #B19CD9;
        --bleu-turquoise: #40E0D0;
        --beige: #FEFEFE;
        --beige-fonce: #FAFAFA;
        --beige-tres-fonce: #F5F5F5;
        --blanc: #FFFFFF;
        --noir: #2C2C2C;
        --gris-clair: #F8F8F8;
        --gris-moyen: #E0E0E0;
        --gris-fonce: #6C6C6C;
        --gradient-primary: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%);
        --gradient-soft: linear-gradient(135deg, #F5F5DC 0%, #E8E8D3 100%);
        --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.1);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
    }
    
    .stApp {
        background: #FEFEFE !important;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    .main .block-container {
        background: #FEFEFE !important;
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    [data-testid="stSidebar"] {
        border-right: 2px solid #F5F5F5;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
        color: #FFFFFF !important;
        transform: translateY(-2px);
        box-shadow: var(--shadow-md) !important;
        opacity: 0.9;
    }
    
    .stButton > button:active,
    .stButton > button:focus {
        background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        outline: none !important;
    }
    
    button[kind="primary"],
    button[data-baseweb="button"][kind="primary"],
    .stButton > button[kind="primary"],
    form button[data-baseweb="button"],
    form button[kind="primary"],
    form .stButton > button {
        background: linear-gradient(135deg, #40E0D0 0%, #B19CD9 100%) !important;
        background-color: transparent !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    
    button[data-baseweb="button"],
    .stButton > button,
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
        background-color: transparent !important;
        color: #FFFFFF !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #FAFAFA;
        padding: 0.5rem;
        border-radius: var(--radius-md);
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.75rem 1.5rem !important;
        color: var(--noir) !important;
        font-weight: 500 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
        color: #FFFFFF !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--noir);
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: var(--gris-fonce);
        font-weight: 500;
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background: var(--blanc) !important;
        border: 2px solid #F5F5F5 !important;
        border-radius: var(--radius-sm) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #B19CD9 !important;
        box-shadow: 0 0 0 3px rgba(177, 156, 217, 0.1) !important;
        outline: none !important;
    }
    
    .stDataFrame {
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        background: var(--blanc);
    }
    
    .stDataFrame th {
        background: var(--beige-fonce) !important;
        color: var(--noir) !important;
        font-weight: 600 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        color: var(--noir);
        font-weight: 600;
    }
    
    a, a:visited, a:hover, a:active, a:focus {
        color: #B19CD9 !important;
    }
    
    .stAlert {
        border-radius: var(--radius-md);
        border-left: 4px solid;
    }
    
    hr {
        border: none;
        border-top: 2px solid var(--beige-tres-fonce);
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# =====================
# ROUTER PRINCIPAL
# =====================
def main():
    # --- Sidebar : fond image (login) ou beige (authentifié)
    use_sidebar_image = not st.session_state.authenticated
    sidebar_bg = _get_sidebar_bg_css(use_sidebar_image)
    st.markdown(_sidebar_styles_css(sidebar_bg), unsafe_allow_html=True)

    if not st.session_state.authenticated:
        afficher_page_connexion()
        return

    # --- Pages authentifiées : fond par page + logo
    page = st.session_state.page
    page_bg_html = _get_page_background_html(page)
    if page_bg_html:
        st.markdown(page_bg_html, unsafe_allow_html=True)

    # --- Pages internes
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

    # --- Navigation : boutons + footer (image / infos entreprise)
    render_bottom_nav({})
    render_nav_footer({
        "app_name": "Gestion Couturier",
        "app_subtitle": "Pilotage intelligent"
    })


# =====================
# RUN
# =====================
main()
