import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Sistema de Colaboradores",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
personalizado = "estilos.md"
st.markdown(personalizado, unsafe_allow_html=True)

# Páginas do sistema
pages = {
    "Menu": [
        st.Page("cadastro.py", title="Cadastro de colaboradores"),
        st.Page("listagem.py", title="Listar/Atualizar/Excluir cadastros")
    ],
    "Sistema": [
        st.Page("sobre.py", title="Sobre o Sistema")
    ]
}

# Navegação no topo
pg = st.navigation(pages, position="top")
pg.run()