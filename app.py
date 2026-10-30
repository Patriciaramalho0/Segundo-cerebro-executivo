import streamlit as st
import plotly.express as px
import pandas as pd

# 1. Configuração da página
st.set_page_config(
    page_title="Segundo Cérebro Executivo",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .css-1d3 Sterling { background-color: #0f172a; }
</style>
""", unsafe_allow_html=True)

# 2. Gestão de Estado da Sessão
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 3. Tela de Acesso Direto
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #0f172a;'>🧠 Segundo Cérebro</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b;'>Plataforma Autônoma Executiva & Vendas</p>", unsafe_allow_html=True)
        
        st.info("💡 **Acesso Executivo:** Clique abaixo para acessar sua central de comando.")
        if st.button("🚀 Entrar no Meu Segundo Cérebro", use_container_width=True, type="primary"):
            st.session_state.authenticated = True
            st.session_state.user = {"email": "patriciateixeira816@gmail.com"}
            st.rerun()
    st.stop()

# 4. Navegação Principal e Sidebar
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

# 5. Módulos do Aplicativo
if modulo == "📊 Dashboard Geral":
    st.title("📊 Painel Executivo")
    st.markdown("Visão consolidada da sua rotina, finanças e metas.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Propostas Fechadas", "R$ 120.000", "+12%")
    col2.metric("Meta Diária Caminhada", "5.0 km", "Concluído")
    col3.metric("Livros em Leitura", "2 Obras", "Em andamento")
    col4.metric("Status Geral", "100% Ativo", "Nuvem")

elif modulo == "💼 CRM & Vendas":
    st.title("💼 CRM & Prospecção High Ticket")
    st.write("Gestão de leads, diagnósticos e fechamento de contratos.")
    
    df_leads = pd.DataFrame({
        "Cliente": ["Mentoria AURA", "Laboratório Mulher Segura", "Consultoria Individual"],
        "Etapa": ["Proposta Enviada", "Diagnóstico", "Fechado"],
        "Valor": ["R$ 15.000", "R$ 8.000", "R$ 120.000"]
    })
    st.dataframe(df_leads, use_container_width=True)

elif modulo == "💰 Finanças":
    st.title("💰 Controle Financeiro")
    st.write("Visão financeira unificada.")
    st.metric("Saldo do Mês", "R$ 45.200,00", "+8.5%")

elif modulo == "🏋️ Saúde & Rotina":
    st.title("🏋️ Metas de Saúde & Bem-estar")
    st.checkbox("Caminhada diária de 5km", value=True)
    st.checkbox("Treino Ritbox / Pular Corda", value=True)

elif modulo == "📚 Estudos & Livros":
    st.title("📚 Biblioteca & Estudos")
    st.write("Livros em estudo:")
    st.markdown("- *Os Segredos da Mente Milionária*")
    st.markdown("- *O Homem Mais Rico da Babilônia*")
    st.markdown("- *Como Fazer Amigos e Influenciar Pessoas*")

elif modulo == "🤖 Assistente IA":
    st.title("🤖 Assistente de IA")
    st.text_input("Digite um comando ou dúvida sobre vendas/estratégia:")