# components/bottom_nav.py

import streamlit as st

def render_bottom_nav(config: dict):

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("➕ Nouvelle commande"):
            st.session_state.page = "commande"
            st.rerun()

    with col2:
        if st.button("📋 Liste commandes"):
            st.session_state.page = "liste"
            st.rerun()

    with col3:
        if st.button("🚪 Déconnexion"):
            st.session_state.authenticated = False
            st.session_state.page = "login"
            st.rerun()

    # JS SAFE (UNE FOIS)
    st.markdown("""
    <script>
        function styleButtons() {
            document.querySelectorAll('button').forEach(btn => {
                btn.style.borderRadius = '10px';
                btn.style.padding = '10px';
            });
        }
        window.addEventListener('load', styleButtons);
        setTimeout(styleButtons, 300);
    </script>
    """, unsafe_allow_html=True)