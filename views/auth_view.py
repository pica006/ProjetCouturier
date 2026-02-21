# views/auth_view.py

import streamlit as st

def load_site_content():
    """
    Chargement de contenu statique (safe)
    """
    try:
        return {
            "title": "Connexion",
            "subtitle": "Accès sécurisé"
        }
    except Exception:
        return {}

def afficher_page_connexion():

    content = load_site_content()

    st.markdown("## 🔐 Connexion")
    st.caption(content.get("subtitle", ""))

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter")

        if submit:
            if username and password:
                # 👉 LOGIQUE AUTH SIMPLE (à remplacer plus tard)
                st.session_state.authenticated = True
                st.session_state.page = "commande"
                st.success("Connexion réussie")
                st.rerun()
            else:
                st.error("Veuillez remplir tous les champs")