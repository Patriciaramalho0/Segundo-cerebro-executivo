import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração Inicial da Página
st.set_page_config(
    page_title="Segundo Cérebro Executivo",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada para um design executivo moderno
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 2. Gestão de Estado (Sessão, Utilizadores e Dados)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "users_db" not in st.session_state:
    # Conta padrão inicial para facilitar o seu acesso imediato
    st.session_state.users_db = {"patriciateixeira816@gmail.com": "123456"}

if "leads_data" not in st.session_state:
    st.session_state.leads_data = pd.DataFrame({
        "Cliente": ["Mentoria AURA", "Laboratório Mulher Segura", "Consultoria Individual"],
        "Etapa": ["Proposta Enviada", "Diagnóstico Realizado", "Fechado"],
        "Valor (R$)": [15000.0, 8000.0, 120000.0]
    })

# 3. Tela de Autenticação (Login / Registo)
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #0f172a;'>🧠 Segundo Cérebro</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b;'>Plataforma Autônoma Executiva & Vendas</p>", unsafe_allow_html=True)
        
        tab_login, tab_register = st.tabs(["🔑 Entrar", "📝 Criar Conta"])
        
        with tab_login:
            login_email = st.text_input("E-mail", key="login_email")
            login_senha = st.text_input("Senha", type="password", key="login_senha")
            
            if st.button("🚀 Entrar na Plataforma", use_container_width=True, type="primary"):
                if login_email in st.session_state.users_db and st.session_state.users_db[login_email] == login_senha:
                    st.session_state.authenticated = True
                    st.session_state.user = {"email": login_email}
                    st.success("Login efetuado com sucesso!")
                    st.rerun()
                else:
                    st.error("E-mail ou senha inválidos. Verifique os dados.")
                    
        with tab_register:
            reg_email = st.text_input("Novo E-mail", key="reg_email")
            reg_senha = st.text_input("Nova Senha", type="password", key="reg_senha")
            
            if st.button("✨ Registar Conta", use_container_width=True):
                if reg_email and reg_senha:
                    if reg_email in st.session_state.users_db:
                        st.warning("Este e-mail já está registado.")
                    else:
                        st.session_state.users_db[reg_email] = reg_senha
                        st.success("Conta criada com sucesso! Vá na aba 'Entrar'.")
                else:
                    st.warning("Preencha todos os campos.")
    st.stop()

# 4. Navegação e Barra Lateral (Sidebar)
st.sidebar.title("🧠 Segundo Cérebro")
st.sidebar.caption("Gestão Executiva & Performance")

modulo = st.sidebar.radio(
    "Módulos Principais",
    ["📊 Dashboard Geral", "💼 CRM & Vendas", "💰 Finanças", "🏋️ Saúde & Rotina", "📚 Estudos & Livros", "🤖 Assistente IA"]
)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Sair"):
    st.session_state.authenticated = False
    st.rerun()

# 5. Módulos Funcionais da Aplicação
if modulo == "📊 Dashboard Geral":
    st.title("📊 Painel Executivo")
    st.markdown("Visão consolidada da sua rotina operacional, comercial e pessoal.")
    
    col1, col2, col3, col4 = st.columns(4)
    total_vendas = st.session_state.leads_data["Valor (R$)"].sum()
    col1.metric("Volume de Negóciados", f"R$ {total_vendas:,.2f}", "+12%")
    col2.metric("Meta Diária Caminhada", "5.0 km", "Concluído")
    col3.metric("Livros em Leitura", "3 Obras", "Em andamento")
    col4.metric("Status do Sistema", "100% Online", "Cloud")
    
    st.markdown("---")
    st.subheader("📈 Desempenho de Prospecção")
    fig = px.bar(st.session_state.leads_data, x="Cliente", y="Valor (R$)", color="Etapa", title="Contratos por Etapa do Funil")
    st.plotly_chart(fig, use_container_width=True)

elif modulo == "💼 CRM & Vendas":
    st.title("💼 CRM & Prospecção High Ticket")
    st.write("Gestão de diagnósticos, negociações e fechamento de contratos de alta conversão.")
    
    st.dataframe(st.session_state.leads_data, use_container_width=True)
    
    with st.expander("➕ Adicionar Novo Lead / Negócio"):
        novo_cliente = st.text_input("Nome do Cliente / Programa")
        nova_etapa = st.selectbox("Etapa do Funil", ["Prospecção", "Diagnóstico", "Proposta Enviada", "Fechado"])
        novo_valor = st.number_input("Valor do Contrato (R$)", min_value=0.0, step=500.0)
        
        if st.button("Registar Negócio"):
            novo_df = pd.DataFrame({"Cliente": [novo_cliente], "Etapa": [nova_etapa], "Valor (R$)": [novo_valor]})
            st.session_state.leads_data = pd.concat([st.session_state.leads_data, novo_df], ignore_index=True)
            st.success("Lead adicionado com sucesso!")
            st.rerun()

elif modulo == "💰 Finanças":
    st.title("💰 Controle Financeiro Executivo")
    st.write("Acompanhamento de fluxo de caixa e faturamento.")
    
    col1, col2 = st.columns(2)
    col1.metric("Faturamento Mensal", "R$ 45.200,00", "+8.5%")
    col2.metric("Despesas Operacionais", "R$ 4.150,00", "-2.1%")
    
    st.markdown("---")
    st.info("💡 Dica: Mantenha os registos de faturamento atualizados para otimizar a sua previsibilidade financeira.")

elif modulo == "🏋️ Saúde & Rotina":
    st.title("🏋️ Metas de Saúde & Bem-estar")
    st.write("Acompanhamento diário da sua rotina de alta performance:")
    
    st.checkbox("Caminhada diária de 5km", value=True)
    st.checkbox("Sessão de Pular Corda & Ritbox", value=True)
    st.checkbox("Manutenção da Sobriedade e Hidratação", value=True)
    
    st.success("Parabéns por manter o foco na sua energia física e mental!")

elif modulo == "📚 Estudos & Livros":
    st.title("📚 Biblioteca & Desenvolvimento Pessoal")
    st.write("Obras de referência em estudo:")
    st.markdown("- 📖 *Os Segredos da Mente Milionária*")
    st.markdown("- 📖 *O Homem Mais Rico da Babilônia*")
    st.markdown("- 📖 *Como Fazer Amigos e Influenciar Pessoas*")

elif modulo == "🤖 Assistente IA":
    st.title("🤖 Assistente Estratégico de IA")
    st.write("Tire dúvidas sobre abordagens comerciais, neurovendas ou planeamento.")
    
    pergunta = st.text_input("Digite o seu comando ou estratégia para análise:")
    if st.button("Analisar com IA"):
        if pergunta:
            st.info(f"Análise Estratégica para: '{pergunta}'")
            st.success("🤖 **Diretriz de IA:** Com base em metodologias consultivas e neurovendas, foque em aprofundar o diagnóstico das dores do cliente antes de apresentar a proposta de alto valor.")
        else:
            st.warning("Por favor, digite uma pergunta ou cenário.")