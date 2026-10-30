import streamlit as st
import requests
from datetime import datetime
from ai_engine_legacy import AIBrain

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Segundo Cérebro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INICIALIZAÇÃO DE SESSÃO ---
if 'ai' not in st.session_state:
    st.session_state.ai = AIBrain()

if 'xp' not in st.session_state:
    st.session_state.xp = 0

if 'streak' not in st.session_state:
    st.session_state.streak = 1

if 'tasks' not in st.session_state:
    st.session_state.tasks = {
        "Acordar cedo e beber 500ml de água": False,
        "Caminhada / Exercício físico": False,
        "Revisar metas do dia": False,
        "Focar em blocos de trabalho (Deep Work)": False,
        "Estudar ou ler 10 páginas": False
    }

if 'transacoes' not in st.session_state:
    st.session_state.transacoes = []

if 'notas' not in st.session_state:
    st.session_state.notas = []

if 'lembretes' not in st.session_state:
    st.session_state.lembretes = []

if 'desabafo_msgs' not in st.session_state:
    st.session_state.desabafo_msgs = []

# --- BARRA LATERAL: PAINEL DE CONTROLE ---
with st.sidebar:
    st.header("⚙️ Painel de Controle")
    
    st.subheader("🤖 Sua Mentora")
    nome_ia = st.text_input("Nome da IA:", value="AURA")
    
    st.divider()
    
    st.subheader("🎨 Personalização Visual")
    tema_visual = st.selectbox(
        "Escolha o Tema / Estilo:",
        ["Modo Dark Profundo (Preto/Azul)", "Modo Clean (Branco Minimalista)", "Modo High Performance (Clean Bege)"]
    )
    tamanho_fonte = st.slider("Tamanho dos Títulos", min_value=20, max_value=36, value=28)
    
    st.divider()
    
    st.subheader("🌍 Localização (Brasil)")
    cidade_input = st.text_input("Digite a cidade:", value="Nova Xavantina")
    estado_input = st.text_input("Estado (Sigla, ex: MT):", value="MT")

    st.divider()
    
    st.markdown("### 🔥 Seu Progresso")
    st.metric(label="Pontos de Experiência (XP)", value=f"{st.session_state.xp} XP")
    st.metric(label="Ofensiva (Streak)", value=f"{st.session_state.streak} dias")

# --- FUNÇÃO DE CLIMA UNIVERSAL ---
def get_weather_by_city(cidade, estado):
    try:
        geo_url = f"https://nominatim.openstreetmap.org/search?city={cidade}&state={estado}&country=Brazil&format=json&limit=1"
        headers = {'User-Agent': 'SegundoCerebroApp/1.0'}
        geo_resp = requests.get(geo_url, headers=headers, timeout=5).json()
        if not geo_resp:
            return f"{cidade} - {estado}", "Indisponível"
        lat = float(geo_resp[0]['lat'])
        lon = float(geo_resp[0]['lon'])
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_resp = requests.get(weather_url, timeout=5).json()
        temp = weather_resp['current_weather']['temperature']
        return f"{cidade} - {estado}", f"{temp}°C"
    except:
        return f"{cidade} - {estado}", "Indisponível"

cidade_formatada, temperatura_atual = get_weather_by_city(cidade_input, estado_input)

# --- APLICAR ESTILOS DINÂMICOS E OCULTAR BARRA SUPERIOR ---
if tema_visual == "Modo Dark Profundo (Preto/Azul)":
    cor_bg = "#0b0f19"
    cor_sidebar = "#111827"
    cor_texto = "#f3f4f6"
    cor_borda = "#374151"
elif tema_visual == "Modo High Performance (Clean Bege)":
    cor_bg = "#fff9f5"
    cor_sidebar = "#fceddf"
    cor_texto = "#2b2b2b"
    cor_borda = "#f7d7bc"
else:
    cor_bg = "#ffffff"
    cor_sidebar = "#f4f6f8"
    cor_texto = "#1f2937"
    cor_borda = "#e5e7eb"

st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    .stApp {{
        background-color: {cor_bg};
        color: {cor_texto} !important;
        margin-top: -40px;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {cor_sidebar};
        border-right: 1px solid {cor_borda};
    }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {{
        color: {cor_texto} !important;
    }}
    
    h1, h2, h3, h4, h5, h6, p, span, label {{
        color: {cor_texto} !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {{
        color: {cor_texto} !important;
        font-weight: bold;
    }}
    
    input, textarea {{
        color: {cor_texto} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- TÍTULO PRINCIPAL ---
st.title("🧠 Segundo Cérebro — Sistema de Gestão")
st.markdown(f"Central de alta performance integrada com a inteligência de **{nome_ia}**.")

# --- ABAS DE NAVEGAÇÃO (6 ABAS) ---
aba_home, aba_rotina, aba_fin, aba_notas, aba_noticias, aba_desabafo = st.tabs([
    "🏠 Home & Assistente", 
    "📋 Rotina & Check-list", 
    "💰 Gestão Financeira", 
    "📝 Notas & Lembretes", 
    "📰 Notícias Essenciais",
    "🧘‍♂️ Descompressão & Desabafo"
])

# --- ABA 1: HOME & ASSISTENTE ---
with aba_home:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### ⏰ Hora Atual")
        st.subheader(datetime.now().strftime("%H:%M"))
    with col2:
        st.markdown(f"### 🌡️ Clima ({cidade_formatada})")
        st.subheader(temperatura_atual)
    with col3:
        st.markdown("### ⚡ Status do Sistema")
        st.success(f"{nome_ia} Online")

    st.divider()
    
    st.markdown(f"### 💬 Conversa com {nome_ia}")
    st.info(f"💡 **Dica:** Dê comandos diretos, ex: *'{nome_ia}, anote que gastei R$ 80 em combustível'*.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(f"Fale com a {nome_ia}..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(f"{nome_ia} está processando..."):
                system_instruction = f"Você se chama {nome_ia}, uma mentora de alta performance, finanças e negócios. Responda de forma direta e estratégica."
                resposta = st.session_state.ai.ask(prompt, system_prompt=system_instruction)
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})

# --- ABA 2: ROTINA & CHECK-LIST ---
with aba_rotina:
    st.markdown("### 🎯 Hábitos Diários & Gamificação")
    total_tasks = len(st.session_state.tasks)
    completed_tasks = sum(1 for status in st.session_state.tasks.values() if status)
    progress_percent = completed_tasks / total_tasks
    
    st.progress(progress_percent)
    st.write(f"**Progresso de Hoje:** {completed_tasks} de {total_tasks} concluídos ({(progress_percent * 100):.0f}%)")
    st.divider()

    for task, status in list(st.session_state.tasks.items()):
        novo_status = st.checkbox(task, value=status, key=f"task_{task}")
        if novo_status != status:
            st.session_state.tasks[task] = novo_status
            if novo_status:
                st.session_state.xp += 15
                st.rerun()
            else:
                st.session_state.xp -= 15
                st.rerun()

# --- ABA 3: GESTÃO FINANCEIRA ---
with aba_fin:
    st.markdown("### 💰 Gestão Financeira & Negócios")
    st.markdown("Adicione, gerencie e remova seus lançamentos com total liberdade.")
    
    total_receitas = sum(t['valor'] for t in st.session_state.transacoes if t['tipo'] == 'Receita')
    total_despesas = sum(t['valor'] for t in st.session_state.transacoes if t['tipo'] == 'Despesa')
    saldo = total_receitas - total_despesas
    
    col_f1, col_f2, col_f3 = st.columns(3)
    col_f1.metric("Total Entradas", f"R$ {total_receitas:.2f}")
    col_f2.metric("Total Saídas", f"R$ {total_despesas:.2f}")
    col_f3.metric("Saldo Líquido", f"R$ {saldo:.2f}")
    
    st.divider()
    
    with st.expander("➕ Adicionar Novo Lançamento Financeiro", expanded=True):
        with st.form("form_fin"):
            t_tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
            t_desc = st.text_input("Descrição (ex: Venda de Produto, Aluguel)")
            t_valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
            submitted = st.form_submit_button("Salvar Lançamento")
            if submitted and t_desc:
                st.session_state.transacoes.append({"tipo": t_tipo, "descricao": t_desc, "valor": t_valor})
                st.success("Lançamento adicionado com sucesso!")
                st.rerun()

    st.markdown("### 📋 Histórico de Lançamentos")
    if not st.session_state.transacoes:
        st.info("Nenhuma transação cadastrada ainda. Utilize o formulário acima para começar.")
    else:
        for idx, t in enumerate(st.session_state.transacoes):
            col_t1, col_t2, col_t3 = st.columns([3, 2, 1])
            with col_t1:
                tipo_emoji = "🟢" if t['tipo'] == 'Receita' else "🔴"
                st.write(f"{tipo_emoji} **{t['descricao']}**")
            with col_t2:
                st.write(f"R$ {t['valor']:.2f}")
            with col_t3:
                if st.button("Excluir", key=f"del_trans_{idx}"):
                    st.session_state.transacoes.pop(idx)
                    st.rerun()

# --- ABA 4: NOTAS & LEMBRETES ---
with aba_notas:
    st.markdown("### 📝 Bloco de Notas & ⏰ Lembretes")
    
    col_n1, col_n2 = st.columns(2)
    
    with col_n1:
        st.subheader("📝 Notas e Insights")
        with st.form("form_nota"):
            n_titulo = st.text_input("Título da Nota")
            n_conteudo = st.text_area("Conteúdo / Estratégia")
            btn_nota = st.form_submit_button("Salvar Nota")
            if btn_nota and n_titulo:
                st.session_state.notas.append({"titulo": n_titulo, "conteúdo": n_conteudo})
                st.success("Nota salva!")
                st.rerun()
                
        for idx, nota in enumerate(st.session_state.notas):
            st.markdown(f"**📌 {nota['titulo']}**")
            st.write(nota['conteúdo'])
            if st.button("Apagar Nota", key=f"del_nota_{idx}"):
                st.session_state.notas.pop(idx)
                st.rerun()
            st.divider()

    with col_n2:
        st.subheader("⏰ Lembretes e Prazos")
        with st.form("form_lembrete"):
            l_tarefa = st.text_input("Compromisso / Tarefa")
            l_data = st.text_input("Prazo (ex: Amanhã, 14h)")
            btn_lembrete = st.form_submit_button("Adicionar Lembrete")
            if btn_lembrete and l_tarefa:
                st.session_state.lembretes.append({"tarefa": l_tarefa, "data": l_data, "concluido": False})
                st.success("Lembrete adicionado!")
                st.rerun()

        for idx, lem in enumerate(st.session_state.lembretes):
            col_l1, col_l2 = st.columns([4, 1])
            with col_l1:
                st.checkbox(f"{lem['tarefa']} (*{lem['data']}*)", value=lem['concluido'], key=f"lem_{idx}")
            with col_l2:
                if st.button("X", key=f"del_lem_{idx}"):
                    st.session_state.lembretes.pop(idx)
                    st.rerun()

# --- ABA 5: NOTÍCIAS ESSENCIAIS ---
with aba_noticias:
    st.markdown("### 📰 Notícias Essenciais (Brasil & Mundo)")
    st.markdown("Principais portais de economia, tecnologia e negócios atualizados para consulta direta:")
    
    col_not1, col_not2 = st.columns(2)
    
    with col_not1:
        st.markdown("#### 🇧🇷 Portais Nacionais")
        st.markdown("- [📊 InfoMoney (Economia e Negócios)](https://www.infomoney.com.br)")
        st.markdown("- [💼 Exame (Negócios e Gestão)](https://exame.com)")
        st.markdown("- [🌐 G1 Economia](https://g1.globo.com/economia/)")
        
    with col_not2:
        st.markdown("#### 🌍 Portais Internacionais & Tech")
        st.markdown("- [🚀 TechCrunch (Inovação e Startups)](https://techcrunch.com)")
        st.markdown("- [📈 Bloomberg (Mercado Global)](https://www.bloomberg.com)")
        st.markdown("- [🧠 MIT Technology Review](https://www.technologyreview.com)")

# --- ABA 6: DESCOMPRESSÃO & DESABAFO (NOVA ABA) ---
with aba_desabafo:
    st.markdown("### 🧘‍♂️ Espaço de Descompressão & Escuta Ativa")
    st.markdown("Um ambiente seguro para desabafar, colocar para fora o estresse do dia ou organizar a mente conversando com a **" + nome_ia + "** de forma totalmente acolhedora.")
    
    col_d1, col_d2 = st.columns([2, 1])
    
    with col_d1:
        st.subheader("💬 Chat Terapêutico & Desabafo")
        st.info("Escreva como você está se sentindo. A IA vai te ouvir sem julgamentos e te ajudar a aliviar a pressão.")
        
        for msg in st.session_state.desabafo_msgs:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt_desabafo := st.chat_input("Desabafe aqui... (ex: 'Estou me sentindo muito sobrecarregada hoje')"):
            st.session_state.desabafo_msgs.append({"role": "user", "content": prompt_desabafo})
            with st.chat_message("user"):
                st.markdown(prompt_desabafo)

            with st.chat_message("assistant"):
                with st.spinner("Ouvindo você com atenção..."):
                    system_terapeuta = f"""Você se chama {nome_ia}, mas agora atua como uma conselheira compassiva, calma, acolhedora e extremamente empática. 
                    O usuário quer desabafar e aliviar o estresse. Ouça com atenção, valide os sentimentos dele sem julgamentos, ofereça palavras de conforto, serenidade e uma perspectiva leve e motivadora para restaurar a paz mental."""
                    
                    resposta_terapeuta = st.session_state.ai.ask(prompt_desabafo, system_prompt=system_terapeuta)
                    st.markdown(resposta_terapeuta)
                    st.session_state.desabafo_msgs.append({"role": "assistant", "content": resposta_terapeuta})

    with col_d2:
        st.subheader("🗑️ Despejo Mental Rápido")
        st.markdown("Escreva tudo o que está gerando ansiedade ou barulho na sua mente agora mesmo. Depois, clique no botão para limpar e esvaziar a cabeça.")
        
        despejo_texto = st.text_area("Jogue tudo aqui:", height=200, placeholder="Ex: Muitas tarefas pendentes, prazo curto, cansaço acumulado...")
        if st.button("Esvaziar a Mente (Limpar Ttudo)"):
            st.success("Pronto! O peso foi descarregado. Respire fundo.")
            st.rerun()