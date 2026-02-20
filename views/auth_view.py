"""
Vue d'authentification - formulaire uniquement.
Affiche le formulaire, récupère les inputs, appelle authenticate().
Aucune logique DB, aucune création de tables.
"""

import base64
import mimetypes
import os
import streamlit as st
from config import APP_CONFIG, BRANDING
from utils.bottom_nav import load_site_content


def _get_lux_vars_style():
    return f"""
    <style>
    :root {{
        --lux-primary: {BRANDING.get('primary', '#C9A227')};
        --lux-secondary: {BRANDING.get('secondary', '#0E0B08')};
        --lux-accent: {BRANDING.get('accent', '#F5EFE6')};
        --lux-text-dark: {BRANDING.get('text_dark', '#1A140F')};
        --lux-text-light: {BRANDING.get('text_light', '#F2ECE3')};
    }}
    </style>
"""


@st.cache_data(show_spinner=False)
def _load_wallpaper_data_uri(wallpaper_path: str):
    if not wallpaper_path:
        return None
    project_root = os.path.dirname(os.path.dirname(__file__))
    image_path = os.path.join(project_root, wallpaper_path)
    if not os.path.exists(image_path):
        return None
    try:
        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")
        mime = mimetypes.guess_type(image_path)[0] or "image/png"
        return f"data:{mime};base64,{img_b64}"
    except Exception:
        return None


HIDE_ST_STYLE = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stButton > button {
    background: linear-gradient(135deg, #B19CD9 0%, #40E0D0 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
}
.login-scope .login-card {
    background: var(--lux-accent);
    border-radius: 22px;
    padding: 2.8rem;
    box-shadow: 0 16px 32px rgba(0, 0, 0, 0.18);
    max-width: 560px;
    margin: 0 auto;
}
.login-scope .login-muted { color: rgba(26, 20, 15, 0.7); font-size: 1.2rem; }
.login-scope .login-support { margin-top: 1.2rem; padding-top: 1rem; border-top: 1px solid rgba(201, 162, 39, 0.2); }
</style>
"""


def afficher_page_connexion():
    st.markdown(_get_lux_vars_style(), unsafe_allow_html=True)
    st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)
    content = load_site_content()
    wallpaper_path = APP_CONFIG.get("wallpaper_url")
    data_uri = _load_wallpaper_data_uri(wallpaper_path) if wallpaper_path else None
    if data_uri:
        st.markdown(f"""
            <style>
            .stApp {{ background-image: url("{data_uri}") !important; background-size: cover !important;
                background-position: center !important; min-height: 100vh; }}
            .main .block-container {{ background: transparent !important; }}
            </style>
        """, unsafe_allow_html=True)
    st.markdown('<div class="login-scope">', unsafe_allow_html=True)
    _, form_col, _ = st.columns([1, 1.3, 1], gap="large")
    with form_col:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("### Connexion sécurisée")
        st.markdown(
            "<div class='login-muted'>Accédez à votre atelier et gérez vos commandes.</div>",
            unsafe_allow_html=True,
        )
        with st.form("auth_form", clear_on_submit=False):
            st.markdown("#### 🔑 Identifiants de connexion")
            code_couturier = st.text_input("Code Couturier *", placeholder="Ex: COUT001", key="code_input")
            password_input = st.text_input("Mot de passe *", type="password", placeholder="Entrez votre mot de passe", key="password_input")
            submit_auth = st.form_submit_button("🔓 Se connecter", type="primary")
            if submit_auth:
                if not code_couturier:
                    st.error("⚠️ Veuillez entrer votre code utilisateur")
                elif not password_input:
                    st.error("⚠️ Veuillez entrer votre mot de passe")
                else:
                    with st.spinner("Vérification..."):
                        from services.auth_service import authenticate
                        succes, donnees, message = authenticate(code_couturier.strip(), password_input)
                        if succes:
                            st.session_state.authenticated = True
                            st.session_state.user = donnees
                            role_n = str(donnees.get("role", "")).upper().strip()
                            st.session_state.page = "super_admin_dashboard" if role_n == "SUPER_ADMIN" else "nouvelle_commande"
                            st.success(f"✅ {message}")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
        support_text = content.get("support_text", "")
        if support_text:
            st.markdown(f'<div class="login-support">{support_text}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
