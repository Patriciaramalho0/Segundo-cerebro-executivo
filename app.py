import streamlit as st
import pandas as pd
import plotly.express as px

from services.auth_service import AuthService
from services.data_service import DataService
from services.assistant_settings_service import AssistantSettingsService
from services.voice_engine import render_tts_script, render_wake_word_listener
from services import ai_engine

# Configuração da Página
st.set_page_config(
    page_title="Segundo Cérebro • Executivo",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CSS (Corrigido para evitar erro de f-string) ---
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] * {
        color: #94a3b8 !important;
    }
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    h1, h2, h3 { color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 700; }
    
    .saas-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        border: 1px solid #e2e8f0;
        margin-bottom: 16px;
    }
    
    .chat-msg-user { background: #eff6ff; padding: 12px 16px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #2563eb; color: #1e293b; }
    .chat-msg-asst { background: #ffffff; padding: 12px 16px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #10b981; color: #1e293b; border: 1px solid #e2e8f0; }

    .badge-success { background-color: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 12px; }
    .badge-danger { background-color: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 12px; }
    .badge-warning { background-color: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 12px; }
    
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Controle de Sessão
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "menu_opcao" not in st.session_state:
    st.session_state.menu_opcao = "🏠 Dashboard"

# Estados Globais Completos
if "priorities" not in st.session_state:
    st.session_state.priorities = [
        {"task": "Fechar contrato mentoria high-ticket AURA", "urgency": "Alta", "done": False},
        {"task": "Revisar campanhas de tráfego e Patystorie", "urgency": "Média", "done": True},
    ]
if "agenda" not in st.session_state:
    st.session_state.agenda = [
        {"time": "09:00", "event": "Reunião de Diagnóstico de Vendas (Google Meet)", "type": "Workspace"},
        {"time": "14:30", "event": "Alinhamento Estratégico Patystorie", "type": "Presencial"},
        {"time": "18:00", "event": "Caminhada 5km & Ritbox", "type": "Rotina"}
    ]
if "routines" not in st.session_state:
    st.session_state.routines = [{"task": "Caminhada de 5km", "done": True}, {"task": "Treino Ritbox & Pular Corda", "done": False}]
if "notes" not in st.session_state:
    st.session_state.notes = [{"title": "Insights de Neurovendas", "content": "Focar na dor emocional do cliente durante a qualificação."}]
if "finances" not in st.session_state:
    st.session_state.finances = [
        {"description": "Mentoria AURA", "type": "Receita", "amount": 5000.00},
        {"description": "Supermercado & Mantimentos", "type": "Despesa", "amount": 450.00}
    ]
if "crm" not in st.session_state:
    st.session_state.crm = [{"lead": "Maria Silva", "stage": "Proposta Enviada", "value": 4500.00}]
if "health" not in st.session_state:
    st.session_state.health = {"weight": 62.5, "height": 1.60, "water": 2.5, "streak": 14}
if "books" not in st.session_state:
    st.session_state.books = [
        {"title": "O Homem Mais Rico da Babilônia", "author": "George Clason", "status": "Lido", "cover": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300"},
        {"title": "Os Segredos da Mente Milionária", "author": "T. Harv Eker", "status": "Lendo Agora", "cover": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300"}
    ]
if "studies" not in st.session_state:
    st.session_state.studies = []
if "integrations" not in st.session_state:
    st.session_state.integrations = {"Google Workspace": True, "WhatsApp Business": True, "Clint CRM": False, "Stripe": True}
if "assistant_config" not in st.session_state:
    st.session_state.assistant_config = {"name": "Luna", "wake_word": "Luna", "tone": "Executiva e Acolhedora"}

# --- TELA DE LOGIN ---
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #0f172a;'>🧠 Segundo Cérebro</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b;'>Plataforma Autônoma Executiva & Vendas</p>", unsafe_allow_html=True)
        
        tab_login, tab_register = st.tabs(["Entrar na Conta", "Criar Nova Conta"])
        with tab_login:
            email = st.text_input("E-mail", key="l_email")
            password = st.text_input("Senha", type="password", key="l_pass")
            if st.button("Acessar Plataforma", use_container_width=True, type="primary"):
                user, err = AuthService.sign_in(email, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")
                    
        with tab_register:
            r_email = st.text_input("E-mail para Cadastro", key="r_email")
            r_pass = st.text_input("Senha", type="password", key="r_pass")
            if st.button("Cadastrar", use_container_width=True):
                user, err = AuthService.sign_up(r_email, r_pass)
                if user:
                    st.success("Conta criada! Faça login.")
    st.stop()

user = st.session_state.user
user_email = user.get("email") if isinstance(user, dict) else "patriciateixeira816@gmail.com"
asst_name = st.session_state.assistant_config["name"]

# --- MENU LATERAL COMPLETO ---
with st.sidebar:
    st.markdown(f"### 🧠 Segundo Cérebro")
    st.caption(f"Conta: {user_email}")
    st.markdown("---")
    
    opcoes = [
        "🏠 Dashboard", f"💬 Assistente ({asst_name})", "📅 Agenda & Workspace", 
        "💰 Finanças Pessoais", "📊 CRM de Vendas", "💪 Saúde & Performance", 
        "📚 Leitura & Livros", "🧠 Estudos & Mapas Mentais", "📝 Notas & Insights", 
        "🎨 Personalizar Ambiente", "🔌 Integrações (Apps)", "⚙️ Configurações da IA", "👤 Minha Conta"
    ]
    
    for op in opcoes:
        if st.button(op, use_container_width=True):
            st.session_state.menu_opcao = op
            st.rerun()
            
    st.markdown("---")
    if st.button("🚪 Sair da Conta", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.rerun()

# --- ROTEAMENTO DE TODAS AS ABAS ---

if st.session_state.menu_opcao == "🏠 Dashboard":
    st.markdown(f"# Bom dia, Patrícia 👋")
    st.markdown(f"<p style='color: #64748b;'>Central Executiva • Assistente: <b>{asst_name}</b></p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_inf1, col_inf2 = st.columns([3, 1])
    with col_inf1:
        st.markdown("""
        <div class='saas-card' style='border-left: 4px solid #2563eb;'>
            <h4 style="margin:0;">🎯 Foco Executivo & Metas Prioritárias</h4>
            <p style="margin: 6px 0 0 0; color: #475569; font-size: 14px;">Execute suas prioridades diárias para manter o ritmo de alta performance.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_inf2:
        st.markdown(f"""
        <div class='saas-card' style='text-align: center; background: #eff6ff;'>
            <h3 style="margin:0; color: #1e40af;">🔥 {st.session_state.health['streak']} Dias</h3>
            <p style="margin:0; color: #3b82f6; font-size: 12px; font-weight: 600;">Sequência Consistente</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### ⚡ Metas & Prioridades do Dia")
    with st.form("form_add_prio"):
        p_col1, p_col2, p_col3 = st.columns([3, 1, 1])
        nova_prio = p_col1.text_input("Nova Meta", label_visibility="collapsed", placeholder="Ex: Fechar contrato high-ticket...")
        p_urg = p_col2.selectbox("Urgência", ["Alta", "Média", "Baixa"], label_visibility="collapsed")
        if p_col3.form_submit_button("Adicionar", type="primary", use_container_width=True):
            if nova_prio:
                st.session_state.priorities.append({"task": nova_prio, "urgency": p_urg, "done": False})
                st.rerun()
                
    for idx, prio in enumerate(st.session_state.priorities):
        badge_cls = "badge-danger" if prio['urgency'] == "Alta" else ("badge-warning" if prio['urgency'] == "Média" else "badge-success")
        col_p1, col_p2, col_p3 = st.columns([4, 1, 1])
        st.session_state.priorities[idx]["done"] = col_p1.checkbox(f"**{prio['task']}**", value=prio['done'], key=f"chk_p_{idx}")
        col_p2.markdown(f"<span class='{badge_cls}'>{prio['urgency']}</span>", unsafe_allow_html=True)
        if col_p3.button("Excluir", key=f"del_p_{idx}"):
            st.session_state.priorities.pop(idx)
            st.rerun()

elif st.session_state.menu_opcao == f"💬 Assistente ({asst_name})":
    st.markdown(f"# 💬 Conversa com {asst_name}")
    render_wake_word_listener(st.session_state.assistant_config["wake_word"])
    st.markdown("---")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-msg-user'><b>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-msg-asst'><b>{asst_name}:</b> {msg['content']}</div>", unsafe_allow_html=True)
            
    if prompt := st.chat_input(f"Digite sua mensagem para a {asst_name}..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner(f"{asst_name} está processando..."):
            response = ai_engine.get_ai_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            render_tts_script(response, enabled=True, assistant_name=asst_name)
        st.rerun()

elif st.session_state.menu_opcao == "📅 Agenda & Workspace":
    st.markdown("# 📅 Agenda, Lembretes & Google Workspace")
    st.markdown("Seus compromissos integrados com alertas automáticos da Luna.")
    
    with st.expander("➕ Adicionar Compromisso ou Lembrete"):
        with st.form("form_add_agenda"):
            a_time = st.text_input("Horário (Ex: 14:00)")
            a_event = st.text_input("Descrição do Evento")
            a_type = st.selectbox("Origem", ["Google Workspace (Calendar)", "Google Meet", "Presencial", "Lembrete da Luna"])
            if st.form_submit_button("Agendar e Sincronizar", type="primary"):
                st.session_state.agenda.append({"time": a_time, "event": a_event, "type": a_type})
                st.success("Compromisso salvo e integrado!")
                st.rerun()
                
    st.markdown("### Compromissos Sincronizados")
    for idx, ag in enumerate(st.session_state.agenda):
        col_ag1, col_ag2, col_ag3 = st.columns([1, 4, 1])
        col_ag1.markdown(f"**⏰ {ag['time']}**")
        col_ag2.markdown(f"{ag['event']} (`{ag['type']}`)")
        if col_ag3.button("Remover", key=f"del_ag_{idx}"):
            st.session_state.agenda.pop(idx)
            st.rerun()

elif st.session_state.menu_opcao == "💰 Finanças Pessoais":
    st.markdown("# 💰 Finanças & Fluxo de Caixa")
    total_rec = sum([f["amount"] for f in st.session_state.finances if f["type"] == "Receita"])
    total_desp = sum([f["amount"] for f in st.session_state.finances if f["type"] == "Despesa"])
    saldo = total_rec - total_desp
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Receitas Totais", f"R$ {total_rec:,.2f}")
    m2.metric("Despesas Totais", f"R$ {total_desp:,.2f}")
    m3.metric("Saldo Líquido", f"R$ {saldo:,.2f}", delta="Saudável" if saldo >= 0 else "Alerta")
    
    if st.session_state.finances:
        df_fin = pd.DataFrame(st.session_state.finances)
        fig_pie = px.pie(df_fin, names='type', values='amount', title='Receitas x Despesas', color='type',
                         color_discrete_map={'Receita':'#10b981', 'Despesa':'#ef4444'})
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with st.expander("➕ Adicionar Lançamento (Mercado, etc.)"):
        with st.form("form_add_fin"):
            f_desc = st.text_input("Descrição")
            f_tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
            f_valor = st.number_input("Valor (R$)", min_value=0.0, value=150.0)
            if st.form_submit_button("Salvar", type="primary"):
                st.session_state.finances.append({"description": f_desc, "type": f_tipo, "amount": f_valor})
                st.rerun()

    for idx, f in enumerate(st.session_state.finances):
        c_a, c_b = st.columns([4, 1])
        badge = "badge-success" if f['type'] == "Receita" else "badge-danger"
        c_a.markdown(f"**{f['description']}** <span class='{badge}'>{f['type']}</span> — R$ {f['amount']:,.2f}", unsafe_allow_html=True)
        if c_b.button("Excluir", key=f"del_f_{idx}"):
            st.session_state.finances.pop(idx)
            st.rerun()

elif st.session_state.menu_opcao == "📊 CRM de Vendas":
    st.markdown("# 📊 CRM & Pipeline High-Ticket")
    with st.expander("➕ Novo Lead"):
        with st.form("form_add_crm"):
            lead = st.text_input("Nome do Cliente")
            estagio = st.selectbox("Estágio", ["Prospecção", "Diagnóstico Realizado", "Proposta Enviada", "Fechado"])
            valor = st.number_input("Valor Estimado (R$)", min_value=0.0, value=3000.0)
            if st.form_submit_button("Salvar", type="primary"):
                st.session_state.crm.append({"lead": lead, "stage": estagio, "value": valor})
                st.rerun()
    for idx, c in enumerate(st.session_state.crm):
        col_c1, col_c2 = st.columns([4, 1])
        col_c1.markdown(f"**{c['lead']}** [{c['stage']}] — **R$ {c['value']:,.2f}**")
        if col_c2.button("Excluir", key=f"del_c_{idx}"):
            st.session_state.crm.pop(idx)
            st.rerun()

elif st.session_state.menu_opcao == "💪 Saúde & Performance":
    st.markdown("# 💪 Saúde & Performance Física")
    h1, h2, h3, h4 = st.columns(4)
    h1.metric("Peso", f"{st.session_state.health['weight']} kg")
    h2.metric("Altura", f"{st.session_state.health['height']} m")
    h3.metric("Água", f"{st.session_state.health['water']} L")
    h4.metric("Streak", f"{st.session_state.health['streak']} Dias 🔥")
    
    with st.form("form_health"):
        for idx, rot in enumerate(st.session_state.routines):
            st.session_state.routines[idx]["done"] = st.checkbox(rot["task"], value=rot["done"], key=f"chk_h_{idx}")
        if st.form_submit_button("Atualizar Rotina", type="primary"):
            st.rerun()

elif st.session_state.menu_opcao == "📚 Leitura & Livros":
    st.markdown("# 📚 Leitura & Meta Anual de Livros")
    total_lidos = len([b for b in st.session_state.books if b['status'] == 'Lido'])
    st.progress(total_lidos / 12, text=f"Meta: {total_lidos} de 12 livros concluídos")
    
    with st.expander("➕ Adicionar Livro (Capa Automática)"):
        with st.form("form_book"):
            b_title = st.text_input("Título do Livro")
            b_author = st.text_input("Autor")
            b_status = st.selectbox("Status", ["Lendo Agora", "Lido", "Lista de Desejos"])
            if st.form_submit_button("Adicionar à Estante", type="primary"):
                auto_cover = "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300"
                st.session_state.books.append({"title": b_title, "author": b_author, "status": b_status, "cover": auto_cover})
                st.rerun()
                
    st.markdown("### Sua Estante de Livros")
    cols = st.columns(3)
    for idx, book in enumerate(st.session_state.books):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='saas-card' style='text-align: center;'>
                <img src='{book['cover']}' style='width: 120px; height: 160px; object-fit: cover; border-radius: 6px;'><br>
                <b>{book['title']}</b><br><span style='color: #64748b; font-size:12px;'>{book['author']}</span><br>
                <span class='badge-warning'>{book['status']}</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🗑️ Remover", key=f"del_book_{idx}", use_container_width=True):
                st.session_state.books.pop(idx)
                st.rerun()

elif st.session_state.menu_opcao == "🧠 Estudos & Mapas Mentais":
    st.markdown("# 🧠 Estudos & Geração de Mapas Mentais")
    with st.form("form_study"):
        topic = st.text_input("Assunto para estudo / resumo / mapa mental:")
        if st.form_submit_button("Gerar com IA", type="primary"):
            with st.spinner("Gerando resumo e mapa mental estruturado..."):
                res = ai_engine.get_ai_response(f"Gere um resumo detalhado e um mapa mental em tópicos hierárquicos sobre: {topic}")
                st.session_state.studies.insert(0, {"topic": topic, "content": res})
                st.rerun()
                
    for s in st.session_state.studies:
        st.markdown(f"<div class='saas-card'><h3>📖 {s['topic']}</h3><div style='background:#f8fafc; padding:12px; border-radius:8px;'>{s['content'].replace(chr(10), '<br>')}</div></div>", unsafe_allow_html=True)

elif st.session_state.menu_opcao == "📝 Notas & Insights":
    st.markdown("# 📝 Notas & Base de Conhecimento")
    with st.expander("➕ Nova Nota"):
        with st.form("form_note"):
            n_t = st.text_input("Título")
            n_c = st.text_area("Conteúdo")
            if st.form_submit_button("Salvar", type="primary"):
                st.session_state.notes.append({"title": n_t, "content": n_c})
                st.rerun()
    for idx, n in enumerate(st.session_state.notes):
        with st.expander(f"📌 {n['title']}"):
            st.write(n["content"])
            if st.button("Excluir", key=f"del_n_{idx}"):
                st.session_state.notes.pop(idx)
                st.rerun()

elif st.session_state.menu_opcao == "🎨 Personalizar Ambiente":
    st.markdown("# 🎨 Personalizar Cores e Estilo do Ambiente")
    with st.form("form_theme"):
        new_accent = st.color_picker("Cor Principal de Destaque", value="#2563eb")
        if st.form_submit_button("Aplicar Personalização", type="primary"):
            st.success("Ambiente personalizado com sucesso!")
            st.rerun()

elif st.session_state.menu_opcao == "🔌 Integrações (Apps)":
    st.markdown("# 🔌 Integrações com Aplicativos & Workspace")
    st.markdown("Gerencie suas conexões com Google Workspace, WhatsApp, CRM e ferramentas de pagamento.")
    for app_name, status in st.session_state.integrations.items():
        st.session_state.integrations[app_name] = st.toggle(f"Conectar com {app_name}", value=status, key=f"tog_{app_name}")
    if st.button("Salvar Conexões", type="primary"):
        st.success("Configurações de integração salvas!")
        st.rerun()

elif st.session_state.menu_opcao == "⚙️ Configurações da IA":
    st.markdown("# ⚙️ Configurações da Assistente")
    with st.form("form_conf"):
        name = st.text_input("Nome da Assistente", value=st.session_state.assistant_config["name"])
        wake = st.text_input("Palavra de Ativação", value=st.session_state.assistant_config["wake_word"])
        tone = st.selectbox("Comportamento / Tom", ["Executiva e Acolhedora", "Direta e Focada em Vendas", "Analítica"])
        if st.form_submit_button("Salvar Configurações", type="primary"):
            st.session_state.assistant_config["name"] = name
            st.session_state.assistant_config["wake_word"] = wake
            st.session_state.assistant_config["tone"] = tone
            st.success("Configurações atualizadas!")
            st.rerun()

elif st.session_state.menu_opcao == "👤 Minha Conta":
    st.markdown("# 👤 Minha Conta & Perfil")
    c1, c2 = st.columns(2)
    c1.markdown(f"<div class='saas-card'><h4>Dados</h4><p><b>Nome:</b> Patrícia Teixeira Ramalho</p><p><b>E-mail:</b> {user_email}</p><p><b>Telefone:</b> (66) 99921-7343</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='saas-card'><h4>Assinatura</h4><p><b>Plano:</b> Executivo Ilimitado</p><p><b>Status:</b> Ativo</p></div>", unsafe_allow_html=True)