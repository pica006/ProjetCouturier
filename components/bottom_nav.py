# components/bottom_nav.py

import streamlit as st
import os


def render_bottom_nav(config: dict):
    """Affiche la barre de navigation avec boutons et logo."""
    st.markdown("---")

    # Logo / image en haut de la nav (si disponible)
    try:
        from config import APP_CONFIG
        logo_base = APP_CONFIG.get("logo_path", "assets/logo")
        logo_shown = False
        for candidate in [
            f"{logo_base}.png", f"{logo_base}.jpg", f"{logo_base}.jpeg",
            os.path.join(logo_base, "logo.png"), os.path.join(logo_base, "Logo.png"),
        ]:
            if os.path.exists(candidate):
                col_logo, _ = st.columns([1, 5])
                with col_logo:
                    st.image(candidate, width=100)
                logo_shown = True
                break
        if not logo_shown:
            st.markdown("")  # Espacement
    except Exception:
        pass

    # Boutons de navigation
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        if st.button("📊 Tableau de bord", use_container_width=True, key="nav_dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

    with col2:
        if st.button("➕ Nouvelle commande", use_container_width=True, key="nav_commande"):
            st.session_state.page = "commande"
            st.rerun()

    with col3:
        if st.button("📋 Liste commandes", use_container_width=True, key="nav_liste"):
            st.session_state.page = "liste"
            st.rerun()

    with col4:
        if st.button("💰 Comptabilité", use_container_width=True, key="nav_compta"):
            st.session_state.page = "comptabilite"
            st.rerun()

    with col5:
        if st.button("📄 Mes charges", use_container_width=True, key="nav_charges"):
            st.session_state.page = "charges"
            st.rerun()

    with col6:
        if st.button("🚪 Déconnexion", use_container_width=True, key="nav_deco"):
            st.session_state.authenticated = False
            st.session_state.page = "login"
            st.rerun()
