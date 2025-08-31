import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from langchain.chat_models import ChatOpenAI
from datetime import datetime
import time

# -------- Autenticação Google Sheets via st.secrets --------
def autenticar_gsheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    secret = st.secrets["google_service_account"]  # <- pega o bloco todo
    
    credentials_dict = {
        "type": secret["type"],
        "project_id": secret["project_id"],
        "private_key_id": secret["private_key_id"],
        "private_key": secret["private_key"].replace("\\n", "\n"),
        "client_email": secret["client_email"],
        "client_id": secret["client_id"],
        "auth_uri": secret["auth_uri"],
        "token_uri": secret["token_uri"],
        "auth_provider_x509_cert_url": secret["auth_provider_x509_cert_url"],
        "client_x509_cert_url": secret["client_x509_cert_url"],
        "universe_domain": secret.get("universe_domain", "googleapis.com")
    }

    creds = Credentials.from_service_account_info(credentials_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client

# -------- Carregar dados da aba Treinos --------
def carregar_treinos(sheet):
    dados = sheet.get_all_records()
    return dados

# -------- Formatar treinos para prompt --------
def formatar_treinos_para_prompt(dados):
    treinos = {}
    for linha in dados:
        nome = linha.get("Nome do Treino", "Sem Nome")
        exercicio = linha.get("Exercício", "")
        ordem = linha.get("Ordem", 0)
        if nome not in treinos:
            treinos[nome] = []
        treinos[nome].append((ordem, exercicio))

    resultado = ""
    for nome, lista in treinos.items():
        resultado += f"\n\n{nome}:\n"
        for _, ex in sorted(lista, key=lambda x: x[0]):
            resultado += f"- {ex}\n"
    return resultado.strip()

# -------- Cabeçalho --------
def pagina_agente():
    st.markdown("""
    <h1 style="background: linear-gradient(to right, #ff00ff, #00ffff, #00ffea, #ff00aa, #ff0055);
        -webkit-background-clip: text;
        color: transparent;
        display: flex; align-items: center;">
        Agente Inteligente
        <img src="https://github.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/blob/master/Emojis/Travel%20and%20places/High%20Voltage.png?raw=true" 
        style="width:50px; margin-left:10px;">
    </h1>
    <hr>
    """, unsafe_allow_html=True)

# -------- Entrada da API Key --------
def placeholder_key():
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "hide_key_input" not in st.session_state:
        st.session_state.hide_key_input = False

    title_placeholder = st.empty()
    message_placeholder = st.empty()
    key_placeholder = st.empty()
    button_placeholder = st.empty()

    if not st.session_state.hide_key_input:
        with title_placeholder.container():
            st.subheader("🔐 Insira sua OpenAI API Key")

        api_input = key_placeholder.text_input("API Key", type="password")

        if button_placeholder.button("OK"):
            if api_input.strip():
                st.session_state.api_key = api_input.strip()
                message_placeholder.success("✅ Chave salva com sucesso!")
                time.sleep(2)
                title_placeholder.empty()
                message_placeholder.empty()
                key_placeholder.empty()
                button_placeholder.empty()
                st.session_state.hide_key_input = True
            else:
                message_placeholder.warning("⚠️ Por favor, digite uma chave válida antes de confirmar.")

    if not st.session_state.api_key:
        st.warning("⚠️ Por favor, insira sua OpenAI API Key acima para continuar.")
        return False

    return True

# -------- Corpo do chat --------
def chat_treino():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for pergunta, resposta in st.session_state.chat_history:
        with st.chat_message("user", avatar="👤"):
            st.markdown(pergunta)
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(resposta)

    pergunta = st.chat_input("Digite sua pergunta ou solicitação...")

    if pergunta:
        try:
            client = autenticar_gsheets()
            planilha = client.open_by_url("https://docs.google.com/spreadsheets/d/1qc04HBmnHpqbIvfgJXU80u-Fh5bcHoUKnLF17OJLslM/edit#gid=0")
            aba_treinos = planilha.worksheet("Treinos")
            dados_treinos = carregar_treinos(aba_treinos)
            treinos_formatados = formatar_treinos_para_prompt(dados_treinos)
        except Exception as e:
            st.error(f"Erro ao acessar a planilha: {e}")
            return

        validade = '01/12/2025'

        contexto = f"""
        Você é um assistente fitness pessoal.

        Seu dono se chama Leandro, e ele tem um plano de treinos válido até {validade}.

        Aqui estão os treinos atuais organizados por grupos musculares, exatamente como estão na planilha:

        {treinos_formatados}

        Com base nisso, responda perguntas sobre os treinos ou sugira treinos semelhantes.
        Use o mesmo padrão de escrita, estrutura e repetições.
        """

        prompt_final = contexto + f"\n\nPergunta: {pergunta}\nResposta:"

        llm = ChatOpenAI(
            temperature=0.4,
            model="gpt-4o-mini",
            openai_api_key=st.session_state.api_key
        )

        with st.spinner("Pensando..."):
            resposta = llm.predict(prompt_final)

        st.session_state.chat_history.append((pergunta, resposta))

        with st.chat_message("user", avatar="👤"):
            st.markdown(pergunta)
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(resposta)

# -------- Executar --------
def main():
    pagina_agente()
    if placeholder_key():
        chat_treino()

if __name__ == "__main__":
    main()
