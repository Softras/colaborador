import streamlit as st
import re
from datetime import date
from database import DatabaseManager

# Inicializar o gerenciador de banco de dados
db = DatabaseManager()

def validar_cep(cep):
    """Valida formato do CEP"""
    return re.match(r'^\d{5}-?\d{3}$', cep) is not None

def validar_telefone(telefone):
    """Valida formato do telefone"""
    telefone_limpo = re.sub(r'[^\d]', '', telefone)
    return len(telefone_limpo) >= 10

# Título da página
st.markdown("# 📝 Cadastro de Colaboradores")
st.markdown("---")

# Formulário de cadastro
with st.form("form_colaborador"):
    st.subheader("🆕 Novo Colaborador")
    
    # Primeira linha
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nome_completo = st.text_input(
            "Nome completo *", 
            placeholder="Digite o nome completo",
            help="Campo obrigatório"
        )
    
    with col2:
        cidade = st.text_input("Cidade", placeholder="Digite a cidade")
    
    with col3:
        telefone = st.text_input(
            "Telefone", 
            placeholder="(11) 99999-9999",
            help="Mínimo 10 dígitos"
        )
    
    # Segunda linha
    col4, col5, col6 = st.columns(3)
    
    with col4:
        endereco = st.text_input("Endereço", placeholder="Digite o endereço completo")
    
    with col5:
        estados_brasil = [
            "", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
            "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", 
            "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ]
        estado = st.selectbox("Estado (UF)", estados_brasil)
    
    with col6:
        data_nascimento = st.date_input(
            "Data de nascimento",
            value=None,
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            help="Selecione a data de nascimento"
        )
    
    # Terceira linha
    col7, col8, col9 = st.columns(3)
    
    with col7:
        bairro = st.text_input("Bairro", placeholder="Digite o bairro")
    
    with col8:
        cep = st.text_input(
            "CEP", 
            placeholder="12345-678",
            help="Formato: 12345-678"
        )
    
    with col9:
        cargos_comuns = [
            "", "Analista", "Desenvolvedor", "Gerente", "Coordenador", 
            "Assistente", "Diretor", "Supervisor", "Técnico", "Estagiário",
            "Consultor", "Especialista", "Outro"
        ]
        cargo = st.selectbox("Cargo", cargos_comuns)
    
    # Espaço antes do botão
    st.markdown("---")
    
    # Botões
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        submitted = st.form_submit_button(
            "💾 Salvar Cadastro", 
            use_container_width=True,
            type="primary"
        )
    
    if submitted:
        # Validações
        erros = []
        
        if not nome_completo.strip():
            erros.append("Nome completo é obrigatório")
        
        if cep and not validar_cep(cep):
            erros.append("CEP deve ter o formato 12345-678")
        
        if telefone and not validar_telefone(telefone):
            erros.append("Telefone deve ter pelo menos 10 dígitos")
        
        if erros:
            for erro in erros:
                st.error(f"❌ {erro}")
        else:
            try:
                # Preparar dados para inserção
                dados = (
                    nome_completo.strip(),
                    endereco.strip() if endereco else None,
                    bairro.strip() if bairro else None,
                    cidade.strip() if cidade else None,
                    estado if estado else None,
                    cep.strip() if cep else None,
                    telefone.strip() if telefone else None,
                    data_nascimento,
                    cargo if cargo else None
                )
                
                # Inserir no banco de dados
                id_colaborador = db.inserir_colaborador(dados)
                
                st.success(f"✅ Colaborador cadastrado com sucesso! ID: {id_colaborador}")
                st.balloons()
                
                # Limpar formulário após sucesso
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erro ao cadastrar colaborador: {e}")

# Estatísticas rápidas
st.markdown("---")
st.subheader("📊 Estatísticas Rápidas")

try:
    stats = db.obter_estatisticas()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Colaboradores", stats['total_colaboradores'])
    
    with col2:
        st.metric("Cidades Cadastradas", stats['total_cidades'])
    
    with col3:
        st.metric("Estados Representados", stats['total_estados'])
    
    with col4:
        st.metric("Cargos Diferentes", stats['total_cargos'])
    
except Exception as e:
    st.error(f"Erro ao carregar estatísticas: {e}")

# Dicas de uso
with st.expander("💡 Dicas de Preenchimento"):
    st.markdown("""
    **Campos obrigatórios:**
    - ✅ Nome completo: Obrigatório para cadastro
    
    **Formatos aceitos:**
    - 📞 Telefone: (11) 99999-9999 ou 11999999999
    - 📍 CEP: 12345-678 ou 12345678
    - 📅 Data: Use o seletor de data
    
    **Dicas:**
    - Preencha o máximo de campos possível para facilitar futuras consultas
    - Use o cargo mais específico disponível na lista
    - Verifique os dados antes de salvar
    """)