# 🏢 Sistema de Cadastro de Colaboradores

Sistema modular desenvolvido em **Streamlit** com banco de dados **SQLite3** para gerenciar cadastro de colaboradores com navegação organizada.

## 🗂 Estrutura do Projeto

```
Sistema-Colaboradores/
├── main.py              # Arquivo principal com navegação
├── database.py          # Gerenciador do banco SQLite3
├── cadastro.py          # Página de cadastro
├── listagem.py          # Página de gerenciamento
├── sobre.py             # Página de informações
├── requirements.txt     # Dependências
└── README.md           # Documentação
```

## 🚀 Como Executar

### 1. Instalar dependências
```bash
pip install streamlit pandas
```

### 2. Executar o sistema
```bash
streamlit run main.py
```

### 3. Acessar no navegador
O sistema estará disponível em: `http://localhost:8501`

## 🎨 Navegação do Sistema

O sistema utiliza **st.navigation** para organizar as páginas:

### 📁 Menu Principal
- **Cadastro de colaboradores** - Formulário de cadastro completo
- **Listar/Atualizar/Excluir cadastros** - Gerenciamento total dos dados

### ⚙️ Sistema
- **Sobre o Sistema** - Informações e documentação

## ✨ Funcionalidades por Página

### 📝 Cadastro (cadastro.py)
- Formulário responsivo em 3 colunas
- Validações em tempo real
- Campos obrigatórios e opcionais
- Estatísticas rápidas do sistema
- Dicas de preenchimento

### 📋 Listagem (listagem.py)
**Aba Listagem:**
- Filtros avançados (nome, cargo, estado)
- Tabela formatada com dados organizados
- Exportação para CSV
- Métricas de busca em tempo real

**Aba Editar:**
- Seleção do colaborador
- Formulário pré-preenchido
- Atualização com validações
- Exclusão com confirmação dupla

**Aba Estatísticas:**
- Métricas detalhadas
- Gráficos de distribuição
- Análise temporal de cadastros

### ℹ️ Sobre (sobre.py)
- Documentação completa do sistema
- Estatísticas em tempo real
- Informações técnicas
- Estrutura do banco de dados

## 🗃️ Banco de Dados (database.py)

### Classe DatabaseManager
- **create_table()** - Criação automática da tabela
- **inserir_colaborador()** - Inserção de novos registros
- **listar_colaboradores()** - Listagem completa
- **buscar_colaborador_por_id()** - Busca específica
- **atualizar_colaborador()** - Atualização de dados
- **excluir_colaborador()** - Remoção de registros
- **obter_estatisticas()** - Estatísticas do sistema

### Estrutura da Tabela
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

## 🛡️ Validações Implementadas

### Campos Obrigatórios
- ✅ **Nome completo**: Essencial para cadastro

### Formatos Validados
- 📞 **Telefone**: Mínimo 10 dígitos (regex)
- 📍 **CEP**: Formato brasileiro 12345-678 (regex)
- 📅 **Data nascimento**: Entre 1900 e data atual
- 🏳️ **Estado**: Lista oficial dos estados brasileiros

## 🎨 Interface e UX

### Tema Visual
- **Tema escuro** profissional
- **Layout responsivo** com colunas organizadas
- **Navegação superior** intuitiva
- **Ícones e emojis** para melhor identificação

### Feedback do Usuário
- **Mensagens de sucesso/erro** coloridas
- **Confirmações de exclusão** duplas
- **Progress feedback** em operações
- **Dicas contextuais** em campos

## 📈 Características Avançadas

### Modularidade
- **Separação clara** de responsabilidades
- **Reutilização** da classe DatabaseManager
- **Navegação centralizada** no arquivo principal
- **Manutenção facilitada** com arquivos independentes

### Performance
- **Lazy loading** de dados quando necessário
- **Cache de estatísticas** para melhor performance
- **Filtros eficientes** com pandas
- **Consultas otimizadas** ao SQLite

### Usabilidade
- **Filtros dinâmicos** em tempo real
- **Exportação de dados** em CSV
- **Navegação entre páginas** fluida
- **Responsividade** em diferentes telas

## 🔄 Fluxo de Uso Recomendado

1. **Acesso inicial** → main.py inicia o sistema
2. **Primeiro cadastro** → cadastro.py para criar registros
3. **Gerenciamento** → listagem.py para consultar/editar
4. **Documentação** → sobre.py para referência

## 🚀 Melhorias Futuras

### Funcionalidades
- Upload em lote via Excel/CSV
- Autenticação e controle de acesso
- API REST para integrações
- Backup/restore automático
- Logs de auditoria completos

### Técnicas
- Migration system para o banco
- Testes automatizados
- Docker containerization
- Deploy em cloud
- Monitoring e alertas

---

**💻 Desenvolvido com Streamlit e SQLite3**  
**🔗 MiniMax Agent - Outubro 2024**
