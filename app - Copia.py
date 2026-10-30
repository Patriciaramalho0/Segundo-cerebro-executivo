import os
from datetime import datetime, timezone
import streamlit as st

from auth_service import AuthService
from settings import get_setting
from data_service import DataService
from ai_engine import AIBrain
from theme import THEMES, apply_theme

st.set_page_config(page_title="Segundo Cérebro", page_icon="🧠", layout="wide")

TRIAL_REQUEST_LIMIT = int(get_setting("TRIAL_REQUEST_LIMIT", "20"))
TRIAL_DAYS = 7  # O período também está definido no trigger SQL do MVP.

def get_services():
    if "auth_service" not in st.session_state:
        st.session_state.auth_service = AuthService()
    if "data_service" not in st.session_state:
        st.session_state.data_service = DataService(st.session_state.auth_service.client)
    return st.session_state.auth_service, st.session_state.data_service

def login_screen(auth):
    st.title("🧠 Segundo Cérebro")
    st.subheader("Seu espaço pessoal de organização e inteligência.")
    login_tab, signup_tab = st.tabs(["Entrar", "Criar conta"])
    with login_tab:
        with st.form("login_form"):
            email = st.text_input("E-mail")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Entrar", use_container_width=True)
        if submitted:
            try:
                auth.sign_in(email.strip(), password)
                st.rerun()
            except Exception as exc:
                st.error(f"Não foi possível entrar: {exc}")
    with signup_tab:
        st.info(f"Crie sua conta e experimente gratuitamente por {TRIAL_DAYS} dias, com até {TRIAL_REQUEST_LIMIT} solicitações à IA.")
        with st.form("signup_form"):
            name = st.text_input("Como podemos chamar você?")
            email = st.text_input("Seu e-mail", key="signup_email")
            password = st.text_input("Crie uma senha (mínimo 8 caracteres)", type="password", key="signup_password")
            submitted = st.form_submit_button("Criar minha conta grátis", use_container_width=True)
        if submitted:
            if len(password) < 8:
                st.warning("Use uma senha com pelo menos 8 caracteres.")
            else:
                try:
                    auth.sign_up(email.strip(), password, name.strip())
                    st.success("Conta criada! Se a confirmação de e-mail estiver habilitada no Supabase, confirme seu endereço antes de entrar.")
                except Exception as exc:
                    st.error(f"Não foi possível criar a conta: {exc}")

def app():
    auth, data_service = get_services()
    if not auth.is_configured:
        st.title("🧠 Segundo Cérebro — configuração necessária")
        st.error("Configure SUPABASE_URL e SUPABASE_ANON_KEY nos Secrets do Streamlit para habilitar cadastro, login e dados individuais.")
        st.code("SUPABASE_URL = 'https://SEU-PROJETO.supabase.co'\nSUPABASE_ANON_KEY = 'SUA_CHAVE_ANON'\nOPENAI_API_KEY = 'SUA_CHAVE_OPENAI'", language="toml")
        st.caption("Não coloque chaves reais no código nem no GitHub.")
        st.stop()

    if not auth.user:
        login_screen(auth)
        st.stop()

    user = auth.user
    try:
        profile = data_service.get_or_create_profile(user)
        workspace = data_service.load_workspace(user["id"])
    except Exception as exc:
        st.error("Não foi possível carregar seus dados. Verifique se executou o arquivo supabase_schema.sql no projeto Supabase.")
        st.exception(exc)
        st.stop()

    trial_end = datetime.fromisoformat(profile["trial_ends_at"].replace("Z", "+00:00"))
    trial_active = datetime.now(timezone.utc) < trial_end
    requests_used = int(profile.get("trial_requests_used", 0))
    remaining = max(0, TRIAL_REQUEST_LIMIT - requests_used)

    with st.sidebar:
        st.markdown("## 🧠 Segundo Cérebro")
        st.caption("Seu espaço de clareza e organização")
        st.write(f"Olá, **{profile.get('display_name') or user.get('email')}**")
        st.divider()
        theme_names = list(THEMES.keys())
        saved_theme = workspace.get("theme", "Dark Profundo")
        if saved_theme not in theme_names:
            saved_theme = "Dark Profundo"
        selected_theme = st.selectbox(
            "🎨 Aparência", theme_names, index=theme_names.index(saved_theme),
            help="A aparência escolhida fica salva na sua conta."
        )
        if selected_theme != workspace.get("theme", "Dark Profundo"):
            workspace["theme"] = selected_theme
            data_service.save_workspace(user["id"], workspace)
        apply_theme(selected_theme)
        st.divider()
        if trial_active:
            st.success("Teste gratuito ativo")
            st.metric("Solicitações de IA restantes", remaining)
            st.caption(f"Seu teste termina em {trial_end.astimezone().strftime('%d/%m/%Y %H:%M')}.")
        else:
            st.warning("Seu período de teste terminou.")
            st.caption("A contratação de um plano será habilitada na próxima etapa.")
        if st.button("Sair", use_container_width=True):
            auth.sign_out()
            st.rerun()

    st.markdown(
        "<div class='sc-hero'><div class='sc-eyebrow'>SEU ESPAÇO INTELIGENTE</div>"
        "<p class='sc-hero-title'>🧠 Segundo Cérebro</p>"
        "<p class='sc-hero-subtitle'>Organize sua vida. Desenvolva suas ideias. Pense com clareza.</p></div>",
        unsafe_allow_html=True
    )

    if not trial_active:
        st.warning("Seu teste gratuito terminou. Nesta versão inicial, a assinatura e o pagamento ainda não estão conectados. Seus dados continuam salvos.")
        st.stop()

    tab_chat, tab_tasks, tab_notes, tab_finance, tab_account = st.tabs(
        ["🤖 Assistente", "📋 Rotina", "📝 Notas", "💰 Finanças", "👤 Minha conta"]
    )

    with tab_chat:
        st.subheader("Converse com sua assistente")
        st.caption("As solicitações são limitadas ao saldo do seu período de teste.")
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        prompt = st.chat_input("O que você gostaria de organizar hoje?")
        if prompt:
            if remaining <= 0:
                st.error("Você utilizou todas as solicitações incluídas no teste gratuito.")
            else:
                st.session_state.chat_messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                try:
                    # A chave é validada apenas quando a pessoa realmente usa a IA.
                    if "ai_brain" not in st.session_state:
                        st.session_state.ai_brain = AIBrain()
                    # Reserva uma solicitação atomicamente antes de chamar a API.
                    data_service.consume_trial_request(user["id"], TRIAL_REQUEST_LIMIT)
                    with st.chat_message("assistant"):
                        with st.spinner("Pensando..."):
                            result = st.session_state.ai_brain.ask(prompt)
                            st.markdown(result["content"])
                    data_service.log_ai_usage(
                        user["id"], result["model"], result["prompt_tokens"],
                        result["completion_tokens"], result["total_tokens"]
                    )
                    st.session_state.chat_messages.append({"role": "assistant", "content": result["content"]})
                    st.rerun()
                except Exception as exc:
                    st.error(f"Não foi possível concluir a solicitação: {exc}")
                    st.info("Se a solicitação falhou antes de chegar à IA, fale com o suporte para revisar seu saldo de teste.")

    with tab_tasks:
        st.subheader("Rotina e hábitos")
        tasks = workspace.get("tasks", [
            {"title": "Revisar metas do dia", "done": False},
            {"title": "Focar em um bloco de trabalho", "done": False},
            {"title": "Estudar ou ler", "done": False},
        ])
        updated = []
        for i, task in enumerate(tasks):
            done = st.checkbox(task["title"], value=task.get("done", False), key=f"task_{i}")
            updated.append({"title": task["title"], "done": done})
        new_task = st.text_input("Adicionar hábito ou tarefa", key="new_task")
        if st.button("Salvar rotina"):
            if new_task.strip():
                updated.append({"title": new_task.strip(), "done": False})
            data_service.save_workspace(user["id"], {**workspace, "tasks": updated})
            st.success("Rotina salva.")
            st.rerun()

    with tab_notes:
        st.subheader("Notas e ideias")
        with st.form("note_form"):
            title = st.text_input("Título")
            content = st.text_area("Sua nota")
            save_note = st.form_submit_button("Salvar nota")
        if save_note and title.strip():
            notes = workspace.get("notes", [])
            notes.insert(0, {"title": title.strip(), "content": content, "created_at": datetime.now(timezone.utc).isoformat()})
            data_service.save_workspace(user["id"], {**workspace, "notes": notes})
            st.success("Nota salva.")
            st.rerun()
        for note in workspace.get("notes", []):
            with st.expander(note["title"]):
                st.write(note.get("content", ""))
                st.caption(note.get("created_at", ""))

    with tab_finance:
        st.subheader("Controle financeiro")
        with st.form("transaction_form"):
            kind = st.selectbox("Tipo", ["Receita", "Despesa"])
            description = st.text_input("Descrição")
            amount = st.number_input("Valor (R$)", min_value=0.0, step=1.0, format="%.2f")
            save_transaction = st.form_submit_button("Adicionar lançamento")
        if save_transaction and description.strip() and amount > 0:
            transactions = workspace.get("transactions", [])
            transactions.insert(0, {
                "type": kind, "description": description.strip(),
                "amount": float(amount), "created_at": datetime.now(timezone.utc).isoformat()
            })
            data_service.save_workspace(user["id"], {**workspace, "transactions": transactions})
            st.success("Lançamento salvo.")
            st.rerun()
        transactions = workspace.get("transactions", [])
        income = sum(x["amount"] for x in transactions if x["type"] == "Receita")
        expenses = sum(x["amount"] for x in transactions if x["type"] == "Despesa")
        c1, c2, c3 = st.columns(3)
        c1.metric("Receitas", f"R$ {income:.2f}")
        c2.metric("Despesas", f"R$ {expenses:.2f}")
        c3.metric("Saldo", f"R$ {income-expenses:.2f}")
        for item in transactions:
            st.write(f"{item['type']} — {item['description']} — R$ {item['amount']:.2f}")

    with tab_account:
        st.subheader("Minha conta")
        st.write(f"**E-mail:** {user.get('email')}")
        st.write(f"**Plano:** Teste gratuito")
        st.write(f"**Solicitações utilizadas:** {requests_used}/{TRIAL_REQUEST_LIMIT}")
        st.progress(min(1.0, requests_used / max(1, TRIAL_REQUEST_LIMIT)))
        st.caption("Os planos pagos, checkout e renovação automática serão conectados após validar o fluxo de cadastro e uso.")

if __name__ == "__main__":
    app()
