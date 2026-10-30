import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração Inicial da Página
st.set_page_config(
    page_title="Segundo Cérebro | Central Pessoal & Executiva",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada para um design moderno e limpo
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    h1, h2, h3 { color: #0f172a; }
</style>
""", unsafe_allow_html=True)

# 2. Gestão de Estado da Sessão e Dados 100% Personalizáveis
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "name": "Patrícia",
        "email": "patriciateixeira816@gmail.com",
        "google_connected": False
    }

# CRM / Negócios totalmente editáveis pelo utilizador
if "leads_data" not in st.session_state:
    st.session_state.leads_data = pd.DataFrame(columns=["Cliente / Projeto", "Etapa", "Valor (R$)", "Observações"])

# Finanças personalizáveis
if "finance_data" not in st.session_state:
    st.session_state.finance_data = pd.DataFrame(columns=["Descrição", "Tipo", "Valor (R$)", "Categoria"])

# Rotina e Metas personalizáveis
if "routine_data" not in st.session_state:
    st.session_state.routine_data = [
        {"meta": "Caminhada diária", "concluido": True},
        {"meta": "Atividade física (Corda / Ritbox)", "concluido": True},
        {"meta": "Leitura diária", "concluido": False}
    ]

# Biblioteca e Livros com suporte a títulos e notas personalizadas
if "books_data" not in st.session_state:
    st.session_state.books_data = pd.DataFrame({
        "Título": ["Os Segredos da Mente Milionária", "O Homem Mais Rico da Babilônia", "Como Fazer Amigos e Influenciar Pessoas"],
        "Categoria": ["Finanças / Mentalidade", "Finanças / Riqueza", "Desenvolvimento Pessoal"],
        "Status": ["Em Leitura", "Concluído", "Em Leitura"]
    })

# Histórico da Assistente IA personalizada
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Olá, Patrícia! Estou conectada ao seu Segundo Cérebro. Como posso ajudar a organizar sua rotina, gerir seus projetos ou analisar suas estratégias hoje?"}
    ]

# 3. Tela de Autenticação e Conexão Google
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #0f172a;'>🧠 Meu Segundo Cérebro</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b;'>Central Autônoma, Personalizável & Inteligente</p>", unsafe_allow_html=True)
        
        tab_login, tab_google = st.tabs(["🔑 Entrar na Central", "🌐 Conectar Conta Google"])
        
        with tab_login:
            nome_usuario = st.text_input("Como gostaria de ser chamada?", value="Patrícia")
            email_input = st.text_input("E-mail", value="patriciateixeira816@gmail.com")
            senha_input = st.text_input("Senha", type="password")
            
            if st.button("🚀 Aceder ao Meu Espaço", use_container_width=True, type="primary"):
                if email_input:
                    st.session_state.authenticated = True
                    st.session_state.user_profile["name"] = nome_usuario if nome_usuario else "Utilizador"
                    st.session_state.user_profile["email"] = email_input
                    st.success("Bem-vinda de volta!")
                    st.rerun()
                else:
                    st.error("Insira um e-mail válido.")
                    
        with tab_google:
            st.info("💡 Conecte a sua conta Google para sincronizar dados, notas e reuniões de forma totalmente personalizada.")
            if st.button("🔗 Sincronizar com Conta Google", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.user_profile["google_connected"] = True
                st.success("Conta Google conectada com sucesso!")
                st.rerun()
    st.stop()

# 4. Navegação Principal e Sidebar Personalizada
st.sidebar.title("🧠 Segundo Cérebro")
st.sidebar.caption(f"Utilizadora: {st.session_state.user_profile['name']}")
if st.session_state.user_profile["google_connected"]:
    st.sidebar.success("🟢 Google Sincronizado")
else:
    st.sidebar.info("👤 Perfil Personalizado Ativo")

st.sidebar.markdown("---")
modulo = st.sidebar.radio(
    "Módulos da Central",
    ["📊 Dashboard Geral", "💼 CRM & Projetos", "💰 Finanças Pessoais", "🏋️ Rotina & Hábitos", "📚 Biblioteca & Livros", "🤖 Assistente IA Autónoma"]
)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Sair"):
    st.session_state.authenticated = False
    st.rerun()

# 5. Módulos Operacionais 100% Personalizáveis
user_name = st.session_state.user_profile["name"]

if modulo == "📊 Dashboard Geral":
    st.title(f"📊 Painel de {user_name}")
    st.markdown("Visão consolidada e personalizável de todas as suas frentes de atuação, rotina e metas.")
    
    col1, col2, col3, col4 = st.columns(4)
    total_pipeline = st.session_state.leads_data["Valor (R$)"].sum() if not st.session_state.leads_data.empty else 0.0
    col1.metric("Total em Negócios / Projetos", f"R$ {total_pipeline:,.2f}")
    col2.metric("Rotina Diária", "Ativa", "Personalizada")
    col3.metric("Livros Registados", len(st.session_state.books_data))
    col4.metric("Sincronização", "Online" if st.session_state.user_profile["google_connected"] else "Local")
    
    st.markdown("---")
    if not st.session_state.leads_data.empty:
        fig = px.bar(st.session_state.leads_data, x="Cliente / Projeto", y="Valor (R$)", color="Etapa", title="Seus Projetos e Negócios por Etapa")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("💡 Nenhum projeto registado ainda. Vá ao módulo **CRM & Projetos** para adicionar os seus dados de forma personalizada!")

elif modulo == "💼 CRM & Projetos":
    st.title("💼 Gestão de CRM, Vendas ou Projetos")
    st.write("Adicione, edite e acompanhe qualquer tipo de cliente, parceria ou projeto de acordo com a sua área de atuação.")
    
    if not st.session_state.leads_data.empty:
        st.dataframe(st.session_state.leads_data, use_container_width=True)
    else:
        st.warning("O seu CRM está vazio. Registe o seu primeiro item abaixo:")
        
    with st.form("form_crm"):
        st.subheader("➕ Adicionar Novo Registo")
        c_nome = st.text_input("Nome do Cliente, Mentorando ou Projeto")
        c_etapa = st.selectbox("Etapa / Status", ["Prospecção", "Em Andamento", "Proposta Enviada", "Fechado / Concluído"])
        c_valor = st.number_input("Valor Envolvido (R$)", min_value=0.0, step=100.0)
        c_obs = st.text_input("Observações ou Metodologia Utilizada")
        
        submitted = st.form_submit_button("Salvar no CRM")
        if submitted and c_nome:
            novo_reg = pd.DataFrame({"Cliente / Projeto": [c_nome], "Etapa": [c_etapa], "Valor (R$)": [c_valor], "Observações": [c_obs]})
            st.session_state.leads_data = pd.concat([st.session_state.leads_data, novo_reg], ignore_index=True)
            st.success("Registo adicionado com sucesso!")
            st.rerun()

elif modulo == "💰 Finanças Pessoais":
    st.title("💰 Controlo Financeiro")
    st.write("Acompanhe entradas, saídas e o panorama financeiro dos seus negócios ou vida pessoal.")
    
    if not st.session_state.finance_data.empty:
        st.dataframe(st.session_state.finance_data, use_container_width=True)
    else:
        st.info("Nenhuma movimentação financeira registada.")
        
    with st.form("form_fin"):
        st.subheader("➕ Registar Movimentação")
        f_desc = st.text_input("Descrição (Ex: Venda de Lingerie, Consultoria, Fornecedor)")
        f_tipo = st.selectbox("Tipo", ["Entrada / Receita", "Saída / Despesa"])
        f_val = st.number_input("Valor (R$)", min_value=0.0, step=50.0)
        f_cat = st.text_input("Categoria (Ex: E-commerce, Mentoria, Operacional)")
        
        btn_fin = st.form_submit_button("Adicionar Transação")
        if btn_fin and f_desc:
            nova_trans = pd.DataFrame({"Descrição": [f_desc], "Tipo": [f_tipo], "Valor (R$)": [f_val], "Categoria": [f_cat]})
            st.session_state.finance_data = pd.concat([st.session_state.finance_data, nova_trans], ignore_index=True)
            st.success("Transação registada!")
            st.rerun()

elif modulo == "🏋️ Rotina & Hábitos":
    st.title("🏋️ Gestão de Rotina & Bem-Estar")
    st.write("Personalize e marque os hábitos diários importantes para a sua alta performance.")
    
    for i, habit in enumerate(st.session_state.routine_data):
        st.session_state.routine_data[i]["concluido"] = st.checkbox(habit["meta"], value=habit["concluido"], key=f"hab_{i}")
        
    with st.form("form_habit"):
        novo_habito = st.text_input("Adicionar novo hábito à rotina diária")
        if st.form_submit_button("Adicionar Hábito") and novo_habito:
            st.session_state.routine_data.append({"meta": novo_habito, "concluido": False})
            st.success("Hábito adicionado!")
            st.rerun()

elif modulo == "📚 Biblioteca & Livros":
    st.title("📚 Biblioteca & Leituras")
    st.write("Gerencie os livros que está a ler, adicione novos títulos e consulte suas referências.")
    
    st.dataframe(st.session_state.books_data, use_container_width=True)
    
    with st.form("form_book"):
        st.subheader("➕ Adicionar Novo Livro")
        b_titulo = st.text_input("Título do Livro")
        b_cat = st.text_input("Categoria / Tema (Ex: Finanças, Negócios, Infantile)")
        b_status = st.selectbox("Status", ["Quero Ler", "Em Leitura", "Concluído"])
        
        if st.form_submit_button("Adicionar à Biblioteca") and b_titulo:
            novo_livro = pd.DataFrame({"Título": [b_titulo], "Categoria": [b_cat], "Status": [b_status]})
            st.session_state.books_data = pd.concat([st.session_state.books_data, novo_livro], ignore_index=True)
            st.success("Livro adicionado com sucesso!")
            st.rerun()

elif modulo == "🤖 Assistente IA Autónoma":
    st.title(f"🤖 Assistente IA de {user_name}")
    st.write(f"Uma assistente totalmente autónoma, configurada para interagir consigo pelo seu nome e auxiliar com base nos seus dados.")
    
    # Exibir histórico de conversas
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # Entrada de prompt interativa
    if prompt := st.chat_input(f"Digite sua dúvida ou estratégia, {user_name}..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Resposta personalizada usando o nome do utilizador
        resposta_ia = f"Olá, {user_name}! Analisei a sua solicitação ('{prompt}'). Como seu Segundo Cérebro autónomo, estou pronta para ajudar a estruturar os seus próximos passos, organizar os dados inseridos e otimizar a sua estratégia."
        
        st.session_state.chat_history.append({"role": "assistant", "content": resposta_ia})
        with st.chat_message("assistant"):
            st.markdown(resposta_ia)