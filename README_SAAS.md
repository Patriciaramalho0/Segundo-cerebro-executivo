# Segundo Cérebro — MVP SaaS (primeira versão)

Esta versão preserva o aplicativo original em `app_legacy.py` e seu motor de IA em `ai_engine_legacy.py` e cria uma nova entrada `app.py` com:
- cadastro e login via Supabase Auth;
- teste gratuito de 7 dias e 20 solicitações de IA (ajustável por variável de ambiente);
- dados pessoais por usuário no Supabase;
- registro de tokens utilizados;
- painel inicial de conta e funcionalidades essenciais.

## O que ainda NÃO está pronto
Esta é uma base de MVP para testes, não uma versão pronta para receber pagamentos ou dados sensíveis em produção.
- Não há checkout, assinatura paga nem webhook.
- Não há painel administrativo de proprietário.
- Não há cobrança/compra de créditos.
- O teste é limitado por quantidade de solicitações e data; cada chamada conta como uma solicitação.
- O chat ainda mantém o histórico na sessão do navegador, não persistido entre sessões.
- As funcionalidades antigas completas permanecem em `app_legacy.py`; precisam ser migradas gradualmente para persistência por usuário.
- Configure limites e monitoramento de gastos no painel da OpenAI.
- Faça revisão de segurança, privacidade/LGPD, backups e testes antes de abrir ao público.

## 1. Criar projeto Supabase
1. Crie um projeto em https://supabase.com.
2. Abra SQL Editor.
3. Execute todo o conteúdo de `supabase_schema.sql`.
4. Em Authentication > Providers > Email, configure a confirmação de e-mail conforme sua política.
5. Copie Project URL e a chave anon/public (não use service_role no navegador).

## 2. Configurar secrets no Streamlit
No painel do Streamlit, configure:
```toml
SUPABASE_URL = "https://SEU-PROJETO.supabase.co"
SUPABASE_ANON_KEY = "SUA_CHAVE_ANON"
OPENAI_API_KEY = "SUA_CHAVE_OPENAI"
OPENAI_MODEL = "gpt-4o-mini"
TRIAL_DAYS = "7"
TRIAL_REQUEST_LIMIT = "20"
AI_MAX_OUTPUT_TOKENS = "700"
```
Nunca publique `OPENAI_API_KEY`, `service_role` ou credenciais no GitHub.

## 3. Instalar e executar localmente
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
O projeto lê variáveis de ambiente ou Streamlit Secrets. Localmente, você pode criar `.streamlit/secrets.toml` (não faça commit desse arquivo).

## 4. Publicar
Faça commit do projeto em um repositório GitHub e configure os secrets no ambiente de hospedagem.
Para produção comercial, avalie hospedagem gerenciada com disponibilidade, logs, backups e recursos previsíveis; o Streamlit Community Cloud pode ser útil para protótipo, mas confira os termos e limites atuais antes de uso comercial.

## 5. Próxima etapa
Após testar cadastro, login, isolamento de dados e consumo de IA, escolher gateway. Para o Brasil, compare Asaas e Mercado Pago considerando assinatura recorrente, Pix, cartão, boleto, taxas, chargeback, webhooks e regras de cancelamento. Só liberar plano pago após confirmação de webhook validado no servidor.
