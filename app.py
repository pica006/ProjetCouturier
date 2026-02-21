"""
Application Streamlit optimisée - Gestion Couturier
Architecture MVC - Render SAFE - Même logique que app.py + beauté complète
================================================================================
Optimisations Render : bootstrap anti écran blanc, load_dotenv prioritaire.
Contenu identique à app.py (fonctionnel sur Render) avec tout le design.
"""
import os
import base64
import streamlit as st

# =====================
# BOOTSTRAP RENDER SAFE (anti écran blanc - affichage immédiat)
# =====================
st.set_page_config(
    page_title="Gestion Couturier",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)
_bootstrap_placeholder = st.empty()
with _bootstrap_placeholder:
    st.write("⏳ Initialisation de l'application...")

# Charger .env AVANT tout import de config (sinon DB_PASSWORD etc. restent vides)
from dotenv import load_dotenv
load_dotenv()

# Render : si DATABASE_URL est fourni (format postgres://...), le parser en variables
# pour que config.py fonctionne (DATABASE_HOST, DATABASE_NAME, etc.)
_database_url = os.getenv("DATABASE_URL", "").strip()
if _database_url and not os.getenv("DATABASE_HOST"):
    try:
        from urllib.parse import urlparse
        _parsed = urlparse(_database_url)
        if _parsed.scheme and "postgres" in _parsed.scheme:
            os.environ["DATABASE_HOST"] = _parsed.hostname or ""
            os.environ["DATABASE_PORT"] = str(_parsed.port or 5432)
            os.environ["DATABASE_NAME"] = (_parsed.path or "").lstrip("/") or ""
            os.environ["DATABASE_USER"] = _parsed.username or ""
            os.environ["DATABASE_PASSWORD"] = _parsed.password or ""
            os.environ["DATABASE_SSLMODE"] = "require"
    except Exception:
        pass

# Imports (même ordre que app.py)
from views.auth_view import afficher_page_connexion
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
from utils.bottom_nav import render_bottom_nav
from utils.permissions import est_super_admin
from models.database import DatabaseConnection, ChargesModel
from controllers.auth_controller import AuthController
from controllers.commande_controller import CommandeController
from config import APP_CONFIG, PAGE_BACKGROUND_IMAGES


# CSS personnalisé - Palette: Violet clair | Bleu turquoise | Beige (60% dominante)
# NOTE: L'erreur 'removeChild' est un bug connu de Streamlit
# Elle est bénigne et n'affecte pas le fonctionnement de l'application

# Image de fond pour la sidebar (assets/nav.png) - UNIQUEMENT sur la page de connexion
SIDEBAR_BG_PLAIN = "background: #FAFAFA !important;"
sidebar_bg_css_with_image = SIDEBAR_BG_PLAIN
try:
    project_root = os.path.dirname(__file__)
    nav_path = os.path.join(project_root, "assets", "nav.png")
    if os.path.exists(nav_path):
        with open(nav_path, "rb") as f:
            nav_b64 = base64.b64encode(f.read()).decode("utf-8")
        data_uri = f"data:image/png;base64,{nav_b64}"
        sidebar_bg_css_with_image = f"""
        background-image: url('{data_uri}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        """
except Exception:
    pass

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* ========================================================================
       PALETTE DE COULEURS - DESIGN PROFESSIONNEL 2025
       ======================================================================== */
    :root {
        /* Couleurs principales */
        --violet-clair: #B19CD9;
        --bleu-turquoise: #40E0D0;
        --beige: #FEFEFE;
        --beige-fonce: #FAFAFA;
        --beige-tres-fonce: #F5F5F5;
        
        /* Couleurs complémentaires */
        --blanc: #FFFFFF;
        --noir: #2C2C2C;
        --gris-clair: #F8F8F8;
        --gris-moyen: #E0E0E0;
        --gris-fonce: #6C6C6C;
        
        /* Dégradés */
        --gradient-primary: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%);
        --gradient-soft: linear-gradient(135deg, #F5F5DC 0%, #E8E8D3 100%);
        --gradient-accent: linear-gradient(135deg, #40E0D0 0%, #B19CD9 100%);
        
        /* Ombres */
        --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.15);
        
        /* Espacements */
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
    }
    
    /* ========================================================================
       FOND GLOBAL - BEIGE DOMINANT (60%)
       ======================================================================== */
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
    
    /* ========================================================================
       SIDEBAR - BEIGE FONCÉ (valeur par défaut, surchargée ensuite)
       ======================================================================== */
    [data-testid="stSidebar"] {
        border-right: 2px solid #F5F5F5;
    }
    
    /* ========================================================================
       BOUTONS - GRADIENT VIOLET-BLEU (PAS DE NOIR !)
       ======================================================================== */
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
    
    /* Boutons primaires - toujours violet-bleu (FORCER pour éviter le rouge) */
    button[kind="primary"],
    button[data-baseweb="button"][kind="primary"],
    button[data-baseweb="button"][data-testid="baseButton-primary"],
    .stButton > button[kind="primary"],
    div[data-testid="stButton"] > button[kind="primary"],
    button.st-emotion-cache-1[data-baseweb="button"][kind="primary"] {
        background: linear-gradient(135deg, #40E0D0 0%, #B19CD9 100%) !important;
        background-color: transparent !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    
    button[kind="primary"]:hover,
    button[kind="primary"]:active,
    button[kind="primary"]:focus,
    button[data-baseweb="button"][kind="primary"]:hover,
    button[data-baseweb="button"][kind="primary"]:active,
    button[data-baseweb="button"][kind="primary"]:focus {
        background: linear-gradient(135deg, #40E0D0 0%, #B19CD9 100%) !important;
        background-color: transparent !important;
        color: #FFFFFF !important;
    }
    
    /* Empêcher Streamlit de mettre du rouge ou du noir - TOUS les boutons */
    button[data-baseweb="button"],
    button[data-testid="baseButton"],
    .stButton > button,
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
        background-color: transparent !important;
        color: #FFFFFF !important;
    }
    
    button[data-baseweb="button"]:hover,
    button[data-baseweb="button"]:active,
    button[data-baseweb="button"]:focus,
    button[data-testid="baseButton"]:hover,
    button[data-testid="baseButton"]:active,
    button[data-testid="baseButton"]:focus {
        background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
        background-color: transparent !important;
        color: #FFFFFF !important;
    }
    
    /* Forcer le style sur les boutons de formulaire aussi */
    form button[data-baseweb="button"],
    form button[kind="primary"],
    form .stButton > button {
        background: linear-gradient(135deg, #40E0D0 0%, #B19CD9 100%) !important;
        background-color: transparent !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    
    form button[data-baseweb="button"]:hover,
    form button[kind="primary"]:hover {
        background: linear-gradient(135deg, #40E0D0 0%, #B19CD9 100%) !important;
        background-color: transparent !important;
        color: #FFFFFF !important;
    }
    
    /* FORCER LE DÉGRADÉ SUR TOUS LES BOUTONS (même les rouges de Streamlit) */
    button[data-baseweb="button"][style*="background"],
    button[data-baseweb="button"][style*="rgb"],
    button[data-baseweb="button"][style*="red"],
    button[data-baseweb="button"][style*="#ff"],
    button[data-baseweb="button"][style*="#FF"] {
        background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
        background-color: transparent !important;
        background-image: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
    }
    
    button[kind="primary"][style],
    button[data-baseweb="button"][kind="primary"][style] {
        background: linear-gradient(135deg, #40E0D0 0%, #B19CD9 100%) !important;
        background-color: transparent !important;
        background-image: linear-gradient(135deg, #40E0D0 0%, #B19CD9 100%) !important;
    }
    
    /* ========================================================================
       ONGLETS (TABS)
       ======================================================================== */
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
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #FEFEFE !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
        color: #FFFFFF !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .stTabs [aria-selected="true"]:hover,
    .stTabs [aria-selected="true"]:active,
    .stTabs [aria-selected="true"]:focus {
        background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
        color: #FFFFFF !important;
    }
    
    /* ========================================================================
       MÉTRIQUES
       ======================================================================== */
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
    
    /* ========================================================================
       FORMULAIRES
       ======================================================================== */
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
    
    /* ========================================================================
       TABLEAUX
       ======================================================================== */
    .stDataFrame {
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        background: var(--blanc);
    }
    
    .stDataFrame thead {
        background: var(--gradient-soft);
    }
    
    .stDataFrame th {
        background: var(--beige-fonce) !important;
        color: var(--noir) !important;
        font-weight: 600 !important;
    }
    
    /* ========================================================================
       TYPOGRAPHIE
       ======================================================================== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        color: var(--noir);
        font-weight: 600;
    }
    
    p, span, div {
        color: var(--noir);
    }
    
    /* ========================================================================
       ÉLÉMENTS CLIQUABLES - TOUJOURS VIOLET, JAMAIS NOIR
       ======================================================================== */
    a, a:visited, a:hover, a:active, a:focus {
        color: #B19CD9 !important;
    }
    
    [data-baseweb="button"] {
        background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
        color: #FFFFFF !important;
    }
    
    [data-baseweb="button"]:hover,
    [data-baseweb="button"]:active,
    [data-baseweb="button"]:focus {
        background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
        color: #FFFFFF !important;
    }
    
    [role="button"],
    [role="link"],
    [role="tab"] {
        color: #B19CD9 !important;
    }
    
    [role="button"]:hover,
    [role="link"]:hover,
    [role="tab"]:hover {
        color: #40E0D0 !important;
    }
    
    /* ========================================================================
       ALERTES
       ======================================================================== */
    .stAlert {
        border-radius: var(--radius-md);
        border-left: 4px solid;
    }
    
    /* ========================================================================
       SÉPARATEURS
       ======================================================================== */
    hr {
        border: none;
        border-top: 2px solid var(--beige-tres-fonce);
        margin: 2rem 0;
    }
    </style>
    
    <script>
    // Forcer le dégradé violet-bleu sur tous les boutons (SAUF la sidebar)
    function forceButtonColors() {
        var sidebar = document.querySelector('[data-testid="stSidebar"]');
        function isInSidebar(btn) { return sidebar && sidebar.contains(btn); }
        document.querySelectorAll('button[data-baseweb="button"]').forEach(btn => {
            if (isInSidebar(btn)) return;
            if (!btn.style.background || btn.style.background.includes('rgb') || btn.style.background.includes('#ff')) {
                btn.style.background = 'linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%)';
                btn.style.backgroundColor = 'transparent';
                btn.style.color = '#FFFFFF';
                btn.style.border = 'none';
            }
        });
        document.querySelectorAll('button[kind="primary"], button[data-baseweb="button"][kind="primary"]').forEach(btn => {
            if (isInSidebar(btn)) return;
            btn.style.background = 'linear-gradient(135deg, #40E0D0 0%, #B19CD9 100%)';
            btn.style.backgroundColor = 'transparent';
            btn.style.color = '#FFFFFF';
            btn.style.border = 'none';
        });
    }
    forceButtonColors();
    window.addEventListener('load', forceButtonColors);
    setTimeout(forceButtonColors, 100);
    setTimeout(forceButtonColors, 500);
    const observer = new MutationObserver(forceButtonColors);
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
""", unsafe_allow_html=True)

# Surcharge du fond de la sidebar + harmonisation des boutons (palette atelier couture)
def _sidebar_styles_css(sidebar_bg_css):
    return f"""
    <style>
    [data-testid="stSidebar"] {{
        {sidebar_bg_css}
    }}
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
        background: transparent !important;
    }}

    /* BOUTONS SIDEBAR - Palette pastel harmonisée */
    [data-testid="stSidebar"] .stButton > button {{
        background: linear-gradient(180deg, rgba(246, 239, 232, 0.9) 0%, rgba(143, 186, 217, 0.88) 50%, rgba(154, 143, 216, 0.87) 100%) !important;
        background-color: transparent !important;
        color: #3B2F4A !important;
        border: 1px solid rgba(59, 47, 74, 0.12) !important;
        border-radius: 12px !important;
        padding: 0.7rem 1rem !important;
        font-weight: 500 !important;
        opacity: 0.88 !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 1px 3px rgba(59, 47, 74, 0.08) !important;
        filter: saturate(0.92);
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        opacity: 0.92 !important;
        background: linear-gradient(175deg, rgba(246, 239, 232, 0.95) 0%, rgba(143, 186, 217, 0.9) 45%, rgba(154, 143, 216, 0.9) 100%) !important;
        box-shadow: 0 2px 8px rgba(59, 47, 74, 0.12) !important;
        border-color: rgba(59, 47, 74, 0.18) !important;
    }}
    [data-testid="stSidebar"] .stButton > button:active,
    [data-testid="stSidebar"] .stButton > button:focus {{
        outline: none !important;
        border-color: rgba(59, 47, 74, 0.2) !important;
    }}
    [data-testid="stSidebar"] .stButton > button.sidebar-btn-active {{
        background: linear-gradient(175deg, rgba(246, 239, 232, 0.98) 0%, rgba(143, 186, 217, 0.92) 40%, rgba(154, 143, 216, 0.92) 100%) !important;
        color: #3B2F4A !important;
        opacity: 0.95 !important;
        box-shadow: 0 3px 12px rgba(59, 47, 74, 0.15) !important;
        border: 1px solid rgba(59, 47, 74, 0.22) !important;
    }}
    [data-testid="stSidebar"] .stButton > button,
    [data-testid="stSidebar"] .stButton > button span {{
        color: #3B2F4A !important;
    }}
    [data-testid="stSidebar"] .stMarkdown h3 {{
        color: #3B2F4A !important;
    }}
    [data-testid="stSidebar"] .stSuccess, [data-testid="stSidebar"] .stInfo {{
        background: rgba(246, 239, 232, 0.85) !important;
        color: #3B2F4A !important;
        border-color: rgba(107, 100, 122, 0.3) !important;
    }}
    </style>
    <script>
    (function() {{
        var pageToLabel = {{
            'super_admin_dashboard': 'Dashboard Super Admin',
            'dashboard': 'Tableau de bord',
            'nouvelle_commande': 'Nouvelle commande',
            'liste_commandes': 'Mes commandes',
            'comptabilite': 'Comptabilité',
            'charges': 'Mes charges',
            'fermer_commandes': 'Fermer mes commandes',
            'calendrier': 'Modèles & Calendrier',
            'administration': 'Administration'
        }};
        function markSidebarActive() {{
            var el = document.querySelector('#sidebar-current-page');
            if (!el) return;
            var page = el.getAttribute('data-page');
            var label = pageToLabel[page];
            if (!label) return;
            var sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (!sidebar) return;
            sidebar.querySelectorAll('.stButton > button').forEach(function(btn) {{
                btn.classList.remove('sidebar-btn-active');
                if (btn.textContent.indexOf(label) !== -1) btn.classList.add('sidebar-btn-active');
            }});
        }}
        markSidebarActive();
        if (document.readyState !== 'complete') window.addEventListener('load', markSidebarActive);
        setTimeout(markSidebarActive, 150);
        setTimeout(markSidebarActive, 500);
    }})();
    </script>
    """


def get_page_background_html(page_id):
    """Retourne le HTML pour l'image de fond de la zone principale selon la page."""
    import json
    image_name = PAGE_BACKGROUND_IMAGES.get(page_id)
    if not image_name:
        return ""
    project_root = os.path.dirname(__file__)
    img_path = os.path.join(project_root, "assets", image_name)
    if not os.path.exists(img_path):
        return ""
    try:
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(image_name)[1].lower()
        mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
        data_uri = f"data:{mime};base64,{b64}"
        data_uri_js = json.dumps(data_uri)
        data_uri_css = data_uri.replace("'", "\\'")

        logo_html = ""
        logo_path = os.path.join(project_root, "assets", "logoBon.png")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f_logo:
                logo_b64 = base64.b64encode(f_logo.read()).decode("utf-8")
            logo_html = f'<div style="position:fixed;top:1rem;left:1rem;z-index:99999;width:110px;height:auto;background:rgba(255,255,255,0.95);padding:6px;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.15);"><img src="data:image/png;base64,{logo_b64}" alt="Logo" style="width:100%;height:auto;display:block;"></div>'

        return f"""
    {logo_html}
    <style id="page-bg-style">
    body .main, section.main, [data-testid="stAppViewContainer"] > div > section, section:has(div.block-container) {{
        position: relative !important;
        min-height: 100vh !important;
        background: #FAFAFA !important;
    }}
    body .main::before, section.main::before, [data-testid="stAppViewContainer"] > div > section::before, section:has(div.block-container)::before {{
        content: '' !important;
        position: absolute !important;
        inset: 0 !important;
        z-index: -2 !important;
        background-image: url('{data_uri_css}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        filter: blur(14px) !important;
        opacity: 0.75 !important;
    }}
    body .main::after, section.main::after, [data-testid="stAppViewContainer"] > div > section::after, section:has(div.block-container)::after {{
        content: '' !important;
        position: absolute !important;
        inset: 0 !important;
        z-index: -1 !important;
        background: rgba(255, 255, 255, 0.72) !important;
    }}
    body .main .block-container, .main .block-container {{
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 12px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
        box-shadow: 0 2px 14px rgba(0, 0, 0, 0.05) !important;
    }}
    </style>
    <script>
    (function() {{
        var dataUri = {data_uri_js};
        function applyBg() {{
            var main = document.querySelector(".main");
            if (main && !main.querySelector('.page-bg-blur')) {{
                var blur = document.createElement('div');
                blur.className = 'page-bg-blur';
                blur.style.cssText = 'position:absolute;inset:0;z-index:-2;background-image:url(' + dataUri + ');background-size:cover;background-position:center;filter:blur(14px);opacity:0.75;';
                main.insertBefore(blur, main.firstChild);
                var veil = document.createElement('div');
                veil.className = 'page-bg-veil';
                veil.style.cssText = 'position:absolute;inset:0;z-index:-1;background:rgba(255,255,255,0.72);';
                main.insertBefore(veil, main.firstChild);
            }}
        }}
        applyBg();
        if (document.readyState !== "complete") window.addEventListener("load", applyBg);
        setTimeout(applyBg, 100);
        setTimeout(applyBg, 500);
    }})();
    </script>
    """
    except Exception:
        return ""


def initialiser_session_state():
    """Initialise toutes les variables de session Streamlit."""
    if 'db_connection' not in st.session_state:
        st.session_state.db_connection = None
    if 'authentifie' not in st.session_state:
        st.session_state.authentifie = False
    if 'couturier_data' not in st.session_state:
        st.session_state.couturier_data = None
    if 'page' not in st.session_state:
        st.session_state.page = 'connexion'
    if 'db_type' not in st.session_state:
        st.session_state.db_type = None


def afficher_sidebar():
    """Affiche la barre latérale avec navigation"""
    with st.sidebar:
        if st.session_state.authentifie:
            current_page = st.session_state.get("page", "connexion")
            st.markdown(
                f'<div id="sidebar-current-page" data-page="{current_page}" style="display:none;"></div>',
                unsafe_allow_html=True,
            )
            st.success(f"**Connecté:** {st.session_state.couturier_data['prenom']} {st.session_state.couturier_data['nom']}")
            role_display = st.session_state.couturier_data.get('role', 'employe')
            st.info(f"**Code:** {st.session_state.couturier_data['code_couturier']} | **Rôle:** {role_display}")
            st.markdown("---")
            
            if est_super_admin():
                st.markdown("### 🔧 SUPER ADMINISTRATION")
                if st.button("📊 Dashboard Super Admin", width='stretch'):
                    st.session_state.page = 'super_admin_dashboard'
                    st.rerun()
                st.markdown("---")
                st.markdown("### 📋 Navigation")
            else:
                st.markdown("### 📋 Navigation")
            
            if st.button("📊 Tableau de bord", width='stretch'):
                st.session_state.page = 'dashboard'
                st.rerun()
            if st.button("➕ Nouvelle commande", width='stretch'):
                st.session_state.page = 'nouvelle_commande'
                st.rerun()
            if st.button("📜 Mes commandes", width='stretch'):
                st.session_state.page = 'liste_commandes'
                st.rerun()
            if st.button("💰 Comptabilité", width='stretch'):
                st.session_state.page = 'comptabilite'
                st.rerun()
            if st.button("📄 Mes charges", width='stretch'):
                st.session_state.page = 'charges'
                st.rerun()
            if st.button("🔒 Fermer mes commandes", width='stretch'):
                st.session_state.page = 'fermer_commandes'
                st.rerun()
            if st.button("📋 Modèles & Calendrier", width='stretch'):
                st.session_state.page = 'calendrier'
                st.rerun()
            
            if est_admin(st.session_state.couturier_data) and not est_super_admin():
                st.markdown("---")
                st.markdown("### 👑 Administration")
                if st.button("👑 Administration", width='stretch'):
                    st.session_state.page = 'administration'
                    st.rerun()
            
            st.markdown("---")
            if st.button("🚪 Déconnexion", width='stretch', key="btn_deconnexion"):
                try:
                    if st.session_state.get('db_connection'):
                        try:
                            st.session_state.db_connection.disconnect()
                        except Exception:
                            pass
                    keys_to_keep = ['db_connection', 'db_type']
                    for key in list(st.session_state.keys()):
                        if key not in keys_to_keep:
                            try:
                                del st.session_state[key]
                            except Exception:
                                pass
                    st.session_state.authentifie = False
                    st.session_state.couturier_data = None
                    st.session_state.page = 'connexion'
                except Exception:
                    st.session_state.authentifie = False
                    st.session_state.couturier_data = None
                    st.session_state.page = 'connexion'
                st.rerun()
        else:
            st.markdown("<div style='height: 100vh;'></div>", unsafe_allow_html=True)


def main():
    """Fonction principale de l'application"""
    _bootstrap_placeholder.empty()  # Masquer le message d'init une fois le contenu prêt
    initialiser_session_state()
    
    sidebar_bg_css = sidebar_bg_css_with_image if not st.session_state.authentifie else SIDEBAR_BG_PLAIN
    st.markdown(_sidebar_styles_css(sidebar_bg_css), unsafe_allow_html=True)
    
    afficher_sidebar()
    
    if not st.session_state.authentifie:
        afficher_page_connexion()
    else:
        page_bg_html = get_page_background_html(st.session_state.page)
        if page_bg_html:
            st.markdown(page_bg_html, unsafe_allow_html=True)

        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logoBon.png")
        if os.path.exists(logo_path):
            try:
                from PIL import Image
                logo_img = Image.open(logo_path)
                c1, c2 = st.columns([0.2, 0.8])
                with c1:
                    st.image(logo_img, width=100)
            except Exception:
                c1, c2 = st.columns([0.2, 0.8])
                with c1:
                    st.image(logo_path, width=100)

        if st.session_state.page == 'super_admin_dashboard':
            if est_super_admin():
                afficher_dashboard_super_admin()
            else:
                st.error("❌ Accès refusé. Cette page est réservée au Super Administrateur.")
                st.session_state.page = 'dashboard'
                st.rerun()
        elif st.session_state.page == 'nouvelle_commande':
            afficher_page_commande()
        elif st.session_state.page == 'liste_commandes':
            afficher_page_liste_commandes()
        elif st.session_state.page == 'comptabilite':
            afficher_page_comptabilite()
        elif st.session_state.page == 'charges':
            afficher_page_mes_charges()
        elif st.session_state.page == 'fermer_commandes':
            afficher_page_fermer_commandes()
        elif st.session_state.page == 'calendrier':
            afficher_page_calendrier(onglet_admin=False)
        elif st.session_state.page == 'dashboard':
            afficher_page_dashboard()
        elif st.session_state.page == 'administration':
            if est_admin(st.session_state.couturier_data):
                afficher_page_administration()
            else:
                st.error("❌ Accès refusé. Cette page est réservée aux administrateurs.")
                st.session_state.page = 'dashboard'
                st.rerun()
        else:
            if est_super_admin():
                st.session_state.page = 'super_admin_dashboard'
            else:
                st.session_state.page = 'dashboard'
            st.rerun()

    render_bottom_nav({
        "app_name": APP_CONFIG.get("name", ""),
        "app_subtitle": APP_CONFIG.get("subtitle", "")
    })


if __name__ == "__main__":
    main()
