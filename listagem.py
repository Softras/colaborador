import streamlit as st
import pandas as pd
from database import DatabaseManager
import re
from datetime import date

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
st.markdown("# 📋 Gerenciar Colaboradores")
st.markdown("*Listar, editar e excluir cadastros*")
st.markdown("---")

# Buscar dados
df = db.listar_colaboradores()

if df.empty:
    st.info("ℹ️ Nenhum colaborador cadastrado ainda.")
    st.markdown("### 🚀 Comece cadastrando seu primeiro colaborador!")
    if st.button("➕ Ir para Cadastro", type="primary"):
        st.switch_page("cadastro.py")
else:
    # Abas para organizar funcionalidades
    tab1, tab2, tab3 = st.tabs(["📋 Listagem", "✏️ Editar", "📊 Estatísticas"])
    
    with tab1:
        st.subheader("🔍 Filtros")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_nome = st.text_input("🔍 Filtrar por nome:", placeholder="Digite parte do nome")
        
        with col2:
            cargos_disponivel = [""] + sorted(df['cargo'].dropna().unique().tolist())
            filtro_cargo = st.selectbox("🔍 Filtrar por cargo:", cargos_disponivel)
        
        with col3:
            estados_disponivel = [""] + sorted(df['estado'].dropna().unique().tolist())
            filtro_estado = st.selectbox("🔍 Filtrar por estado:", estados_disponivel)
        
        # Aplicar filtros
        df_filtrado = df.copy()
        
        if filtro_nome:
            df_filtrado = df_filtrado[df_filtrado['nome_completo'].str.contains(filtro_nome, case=False, na=False)]
        
        if filtro_cargo:
            df_filtrado = df_filtrado[df_filtrado['cargo'] == filtro_cargo]
        
        if filtro_estado:
            df_filtrado = df_filtrado[df_filtrado['estado'] == filtro_estado]
        
        # Mostrar estatísticas dos filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Colaboradores", len(df))
        with col2:
            st.metric("Resultados da Busca", len(df_filtrado))
        with col3:
            if not df['cargo'].isna().all() and len(df) > 0:
                cargo_mais_comum = df['cargo'].value_counts().index[0]
                st.metric("Cargo Mais Comum", cargo_mais_comum)
        
        st.markdown("---")
        
        # Exibir tabela
        if not df_filtrado.empty:
            # Preparar dados para exibição
            df_display = df_filtrado[[
                'id', 'nome_completo', 'cidade', 'estado', 'telefone', 
                'cargo', 'data_nascimento', 'data_cadastro'
            ]].copy()
            
            # Renomear colunas
            df_display.columns = [
                'ID', 'Nome Completo', 'Cidade', 'UF', 'Telefone', 
                'Cargo', 'Nascimento', 'Cadastrado em'
            ]
            
            # Formatar datas
            if 'Cadastrado em' in df_display.columns:
                df_display['Cadastrado em'] = pd.to_datetime(df_display['Cadastrado em']).dt.strftime('%d/%m/%Y %H:%M')
            
            if 'Nascimento' in df_display.columns:
                df_display['Nascimento'] = pd.to_datetime(df_display['Nascimento'], errors='coerce').dt.strftime('%d/%m/%Y')
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # Exportar dados
            if st.button("📥 Exportar para CSV"):
                csv = df_display.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name='colaboradores.csv',
                    mime='text/csv'
                )
        else:
            st.warning("⚠️ Nenhum colaborador encontrado com os filtros aplicados.")
    
    with tab2:
        st.subheader("✏️ Editar Colaborador")
        
        # Seleção do colaborador para editar
        colaboradores_opcoes = [""] + [f"{row['id']} - {row['nome_completo']}" for _, row in df.iterrows()]
        colaborador_selecionado = st.selectbox(
            "Selecione o colaborador para editar:",
            colaboradores_opcoes
        )
        
        if colaborador_selecionado:
            id_colaborador = int(colaborador_selecionado.split(" - ")[0])
            
            # Buscar dados do colaborador
            colaborador_data = db.buscar_colaborador_por_id(id_colaborador)
            
            if colaborador_data:
                # Formulário de edição
                with st.form("form_editar"):
                    st.write(f"**Editando:** {colaborador_data[1]}")
                    
                    # Primeira linha
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        nome_completo = st.text_input(
                            "Nome completo *", 
                            value=colaborador_data[1] or "",
                            placeholder="Digite o nome completo"
                        )
                    
                    with col2:
                        cidade = st.text_input(
                            "Cidade", 
                            value=colaborador_data[4] or "",
                            placeholder="Digite a cidade"
                        )
                    
                    with col3:
                        telefone = st.text_input(
                            "Telefone", 
                            value=colaborador_data[7] or "",
                            placeholder="(11) 99999-9999"
                        )
                    
                    # Segunda linha
                    col4, col5, col6 = st.columns(3)
                    
                    with col4:
                        endereco = st.text_input(
                            "Endereço", 
                            value=colaborador_data[2] or "",
                            placeholder="Digite o endereço"
                        )
                    
                    with col5:
                        estados_brasil = [
                            "", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
                            "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", 
                            "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
                        ]
                        estado_atual = colaborador_data[5] or ""
                        estado_index = estados_brasil.index(estado_atual) if estado_atual in estados_brasil else 0
                        estado = st.selectbox("Estado (UF)", estados_brasil, index=estado_index)
                    
                    with col6:
                        data_nascimento_atual = None
                        if colaborador_data[8]:
                            try:
                                data_nascimento_atual = pd.to_datetime(colaborador_data[8]).date()
                            except:
                                data_nascimento_atual = None
                        
                        data_nascimento = st.date_input(
                            "Data de nascimento",
                            value=data_nascimento_atual,
                            min_value=date(1900, 1, 1),
                            max_value=date.today()
                        )
                    
                    # Terceira linha
                    col7, col8, col9 = st.columns(3)
                    
                    with col7:
                        bairro = st.text_input(
                            "Bairro", 
                            value=colaborador_data[3] or "",
                            placeholder="Digite o bairro"
                        )
                    
                    with col8:
                        cep = st.text_input(
                            "CEP", 
                            value=colaborador_data[6] or "",
                            placeholder="12345-678"
                        )
                    
                    with col9:
                        cargos_comuns = [
                            "", "Analista", "Desenvolvedor", "Gerente", "Coordenador", 
                            "Assistente", "Diretor", "Supervisor", "Técnico", "Estagiário",
                            "Consultor", "Especialista", "Outro"
                        ]
                        cargo_atual = colaborador_data[9] or ""
                        cargo_index = cargos_comuns.index(cargo_atual) if cargo_atual in cargos_comuns else 0
                        cargo = st.selectbox("Cargo", cargos_comuns, index=cargo_index)
                    
                    # Botões
                    col_btn1, col_btn2, col_btn3 = st.columns(3)
                    
                    with col_btn1:
                        submitted_update = st.form_submit_button("💾 Atualizar", type="primary")
                    
                    with col_btn2:
                        submitted_delete = st.form_submit_button("🗑️ Excluir", type="secondary")
                    
                    if submitted_update:
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
                                # Preparar dados para atualização
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
                                
                                # Atualizar no banco de dados
                                if db.atualizar_colaborador(id_colaborador, dados):
                                    st.success("✅ Colaborador atualizado com sucesso!")
                                    st.rerun()
                                else:
                                    st.error("❌ Erro ao atualizar colaborador")
                                    
                            except Exception as e:
                                st.error(f"❌ Erro ao atualizar colaborador: {e}")
                    
                    if submitted_delete:
                        if st.session_state.get('confirm_delete') != id_colaborador:
                            st.session_state.confirm_delete = id_colaborador
                            st.warning("⚠️ Clique novamente para confirmar a exclusão")
                        else:
                            try:
                                if db.excluir_colaborador(id_colaborador):
                                    st.success("✅ Colaborador excluído com sucesso!")
                                    if 'confirm_delete' in st.session_state:
                                        del st.session_state.confirm_delete
                                    st.rerun()
                                else:
                                    st.error("❌ Erro ao excluir colaborador")
                            except Exception as e:
                                st.error(f"❌ Erro ao excluir colaborador: {e}")
    
    with tab3:
        st.subheader("📊 Estatísticas Detalhadas")
        
        # Métricas gerais
        stats = db.obter_estatisticas()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Colaboradores", stats['total_colaboradores'])
        
        with col2:
            st.metric("Cidades Diferentes", stats['total_cidades'])
        
        with col3:
            st.metric("Estados Diferentes", stats['total_estados'])
        
        with col4:
            st.metric("Cargos Diferentes", stats['total_cargos'])
        
        # Informações adicionais
        col5, col6 = st.columns(2)
        
        with col5:
            st.info(f"**Cargo mais comum:** {stats['cargo_mais_comum']}")
        
        with col6:
            st.info(f"**Estado mais representado:** {stats['estado_mais_comum']}")
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição por cargo
            if not df['cargo'].isna().all() and len(df) > 0:
                st.subheader("Distribuição por Cargo")
                cargo_counts = df['cargo'].value_counts()
                st.bar_chart(cargo_counts)
        
        with col2:
            # Distribuição por estado
            if not df['estado'].isna().all() and len(df) > 0:
                st.subheader("Distribuição por Estado")
                estado_counts = df['estado'].value_counts()
                st.bar_chart(estado_counts)
        
        # Cadastros por período
        if len(df) > 0:
            st.subheader("Cadastros por Período")
            df_time = df.copy()
            df_time['data_cadastro'] = pd.to_datetime(df_time['data_cadastro'])
            df_time['mes_cadastro'] = df_time['data_cadastro'].dt.to_period('M')
            cadastros_por_mes = df_time['mes_cadastro'].value_counts().sort_index()
            st.line_chart(cadastros_por_mes)