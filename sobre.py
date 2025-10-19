import streamlit as st
from datetime import datetime

# Título da página
st.markdown("# ℹ️ Sobre o Sistema")
st.markdown("---")

# Informações do sistema
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## 🏢 Sistema de Cadastro de Colaboradores
    
    Este sistema foi desenvolvido para facilitar o gerenciamento de informações 
    de colaboradores de forma simples e eficiente.
    
    ### ✨ Funcionalidades Principais:
    
    **📝 Cadastro de Colaboradores**
    - Formulário completo com validações
    - Campos obrigatórios e opcionais
    - Validação de CEP e telefone
    - Interface intuitiva e responsiva
    
    **📋 Gerenciamento Completo**
    - Listagem de todos os colaboradores
    - Filtros avançados por nome, cargo e estado
    - Edição de dados existentes
    - Exclusão de registros
    - Exportação para CSV
    
    **📊 Estatísticas e Relatórios**
    - Métricas gerais do sistema
    - Gráficos de distribuição
    - Análise temporal de cadastros
    - Informações consolidadas
    
    ### 🛡️ Segurança e Validações:
    
    - **Nome completo**: Campo obrigatório
    - **CEP**: Formato brasileiro (12345-678)
    - **Telefone**: Mínimo de 10 dígitos
    - **Data de nascimento**: Entre 1900 e data atual
    - **Estado**: Lista oficial dos estados brasileiros
    
    ### 🎨 Interface:
    
    - Tema escuro profissional
    - Layout responsivo
    - Navegação intuitiva
    - Feedback visual para ações
    - Ícones e emojis para melhor UX
    """)

with col2:
    st.markdown("""
    ### 🔧 Tecnologias Utilizadas:
    
    - **Frontend**: Streamlit
    - **Banco de Dados**: SQLite3
    - **Linguagem**: Python
    - **Validações**: Regex
    - **Visualizações**: Plotly/Streamlit
    
    ### 📊 Estatísticas do Sistema:
    """)
    
    # Importar e mostrar estatísticas em tempo real
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        stats = db.obter_estatisticas()
        
        st.metric("Colaboradores", stats['total_colaboradores'])
        st.metric("Cidades", stats['total_cidades'])
        st.metric("Estados", stats['total_estados'])
        st.metric("Cargos", stats['total_cargos'])
        
        if stats['cargo_mais_comum'] != 'N/A':
            st.info(f"**Cargo predominante:**\n{stats['cargo_mais_comum']}")
        
        if stats['estado_mais_comum'] != 'N/A':
            st.info(f"**Estado predominante:**\n{stats['estado_mais_comum']}")
            
    except Exception as e:
        st.error(f"Erro ao carregar estatísticas: {e}")

st.markdown("---")

# Informações técnicas
with st.expander("🔧 Informações Técnicas"):
    st.markdown("""
    ### 🗃️ Estrutura do Banco de Dados:
    
    ```sql
    CREATE TABLE colaboradores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT NOT NULL,
        endereco TEXT,
        bairro TEXT,
        cidade TEXT,
        estado TEXT,
        cep TEXT,
        telefone TEXT,
        data_nascimento DATE,
        cargo TEXT,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```
    
    ### 📁 Arquivos do Sistema:
    
    - `main.py` - Arquivo principal com navegação
    - `database.py` - Gerenciador do banco de dados
    - `cadastro.py` - Página de cadastro de colaboradores
    - `listagem.py` - Página de listagem e gerenciamento
    - `sobre.py` - Esta página de informações
    
    ### 🚀 Funcionalidades Futuras:
    
    - Upload em lote via arquivo Excel/CSV
    - Autenticação de usuários
    - API REST para integrações
    - Backup automático do banco
    - Logs de auditoria
    - Relatórios personalizados
    - Integração com API de CEP
    - Validação de CPF
    """)

# Rodapé
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col2:
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>📅 Sistema desenvolvido em outubro de 2024</p>
        <p>💻 Desenvolvido com ❤️ usando Streamlit</p>
        <p>🔗 MiniMax Agent</p>
    </div>
    """, unsafe_allow_html=True)