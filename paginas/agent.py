import streamlit as st
from langchain.chat_models import ChatOpenAI
import time


# Dados do treino
VALIDADE_TREINO = '01/08/2025'
TREINOS = {
    'Treino 1 - Peito': [
        'Supino reto / Crucifixso reto – 3x10',
        'Supino inclinado / Crucifixo inclinado – 3x10',
        'Cross-over alto – 4x10',
        'Fly no banco 4x10',
        'Esteira cardio 12 min'
    ],
    'Treino 2 - Pernas': [
        'Agachamento livre – 4x10',
        'Leg press – 4x10',
        'Cadeira extensora – 4x10',
        'Mesa flexora – 4x10',
        'Cadeira flexora - 4x10',
        'Elevação pelvica maquina - 4x10',
        'Paturrilha sentado + paturrilha em pé - 3x10'
    ],
    'Treino 3 - Costas': [
        'Puxada alta – 4x10',
        'Puxada alta com pegada neutra ou triângulo - 4x10',
        'Remada curvada – 4x10',
        'Remada unilateral com halteres - 4x10',
        'Remada baixa no cabo - 4x10'
    ],
    'Treino 4 - Membros Superiores': [
        'Barra W - 4X10',
        'Rosca martelo – 4X10',
        'Rosca alternada halteres – 4X10',
        'Tríceps corda no pulley – 4X10',
        'Tríceps paralela na maquina – 4X10',
        'Tríceps francês no pulley - 4x10',
        'Elevação lateral – 4x10',
        'Elevação frontal – 4x10',
        'Desenvolvimento maquina – 4x10'
    ]
}

# Função para formatar treinos no prompt
def formatar_treinos_para_prompt(treinos):
    resultado = ""
    for nome, exercicios in treinos.items():
        resultado += f"\n\n{nome}:\n"
        for ex in exercicios:
            resultado += f"- {ex}\n"
    return resultado.strip()


# Cabeçalho da página
def pagina_agente():
    st.markdown(
        """
        <h1 style="background: linear-gradient(to right, #ff00ff, #00ffff, #00ffea, #ff00aa, #ff0055);
            -webkit-background-clip: text;
            color: transparent;
            display: flex; align-items: center;">
            Agente Inteligente
            <img src="https://github.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/blob/master/Emojis/Travel%20and%20places/High%20Voltage.png?raw=true" 
            style="width:50px; margin-left:10px;">
        </h1>
        <hr>
        """,
        unsafe_allow_html=True
    )


# Entrada da API Key
def placeholder_key():
    # Inicializa estado
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "hide_key_input" not in st.session_state:
        st.session_state.hide_key_input = False

    # Placeholders para os elementos
    title_placeholder = st.empty()
    message_placeholder = st.empty()
    key_placeholder = st.empty()

    # Mostra o título e o campo se ainda não foi escondido
    if not st.session_state.hide_key_input:
        with title_placeholder.container():
            st.subheader("🔐 Insira sua OpenAI API Key")

        api_input = key_placeholder.text_input("API Key", type="password")
        if api_input:
            st.session_state.api_key = api_input.strip()
            message_placeholder.success("✅ Chave salva com sucesso!")
            time.sleep(2)
            title_placeholder.empty()
            message_placeholder.empty()
            key_placeholder.empty()
            st.session_state.hide_key_input = True

    # Verificação de segurança
    if not st.session_state.api_key:
        st.warning("⚠️ Por favor, insira sua OpenAI API Key acima para continuar.")
        return False

    return True


# Corpo do chat
def chat_treino():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Mostra histórico anterior
    for pergunta, resposta in st.session_state.chat_history:
        with st.chat_message("user", avatar="👤"):
            st.markdown(pergunta)
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(resposta)

    # Nova entrada de chat
    pergunta = st.chat_input("Digite sua pergunta ou solicitação...")

    if pergunta:
        contexto = f"""
        Você é um assistente fitness pessoal.

        Seu dono se chama Leandro, e ele tem um plano de treinos válido até {VALIDADE_TREINO}.
        Aqui estão os treinos atuais organizados por grupos musculares:

        {formatar_treinos_para_prompt(TREINOS)}

        Com base nisso, responda perguntas sobre os treinos ou sugira treinos semelhantes.
        Use o mesmo padrão de escrita, estrutura e repetições.
        """

        prompt_final = contexto + f"\n\nPergunta: {pergunta}\nResposta:"

        llm = ChatOpenAI(
            temperature=0.4,
            model="gpt-4",
            openai_api_key=st.session_state.api_key
        )

        with st.spinner("Pensando..."):
            resposta = llm.predict(prompt_final)

        st.session_state.chat_history.append((pergunta, resposta))

        # Exibe a última resposta
        with st.chat_message("user", avatar="👤"):
            st.markdown(pergunta)
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(resposta)


# Executa tudo
def main():
    pagina_agente()
    if placeholder_key():
        chat_treino()


if __name__ == "__main__":
    main()
