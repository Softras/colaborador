# Classe do arquivo database.py
from database import DatabaseManager

from datetime import date
import streamlit as st
import re

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
with st.form("form_colaborador", clear_on_submit=True):
    st.subheader("🆕 Novo Colaborador")
    
    # Primeira linha
    col1, col2, col3 = st.columns(3)
    with col1:
        nome_completo = st.text_input("Nome completo *", placeholder="Digite o nome completo")
    with col2:
        cidade = st.text_input("Cidade", placeholder="Digite a cidade")
    with col3:
        telefone = st.text_input("Telefone", placeholder="(11) 99999-9999")

    # Segunda linha
    col4, col5, col6 = st.columns(3)
    with col4:
        endereco = st.text_input("Endereço", placeholder="Digite o endereço completo")
    with col5:
        estados_brasil = ["", "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG",
                          "PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]
        estado = st.selectbox("Estado (UF)", estados_brasil, index=0)
    with col6:
        data_nascimento = st.date_input("Data de nascimento", value=date.today(),
                                        min_value=date(1900,1,1), max_value=date.today())

    # Terceira linha
    col7, col8, col9 = st.columns(3)
    with col7:
        bairro = st.text_input("Bairro", placeholder="Digite o bairro")
    with col8:
        cep = st.text_input("CEP", placeholder="12345-678")
    with col9:
        cargos_comuns = ["", "Analista","Desenvolvedor","Gerente","Coordenador",
                         "Assistente","Diretor","Supervisor","Técnico","Estagiário",
                         "Consultor","Especialista","Outro"]
        cargo = st.selectbox("Cargo", cargos_comuns, index=0)

    # Botão de envio
    submitted = st.form_submit_button("💾 Salvar Cadastro")
    
    if submitted:
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
                id_colaborador = db.inserir_colaborador(dados)
                st.success(f"✅ Colaborador cadastrado com sucesso! ID: {id_colaborador}")
            except Exception as e:
                st.error(f"❌ Erro ao cadastrar colaborador: {e}")

# Estatísticas rápidas
st.markdown("---")
st.subheader("📊 Estatísticas Rápidas")
try:
    stats = db.obter_estatisticas()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Colaboradores", stats['total_colaboradores'])
    col2.metric("Cidades Cadastradas", stats['total_cidades'])
    col3.metric("Estados Representados", stats['total_estados'])
    col4.metric("Cargos Diferentes", stats['total_cargos'])
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
    - Se os campos não limparem automaticamente, pressione F5 para atualizar
    """)