import streamlit as st

# def pagina_inicial():
#     validade = '01/08/2025'
#     st.header('Personal Trainer 🏋', divider=True)
#     st.write(f'Validade até {validade}')


def pagina_inicial():
    validade = '01/08/2025'
    
    st.markdown(
    """
    ##:green[My Training]##
    <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/People%20with%20activities/Person%20Lifting%20Weights%20Medium-Dark%20Skin%20Tone.png" style="width:50px">
    """, 
    unsafe_allow_html=True
)

    
    st.write(f'Validade até {validade}')


    # Treinos disponíveis
    treinos = {
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
        'Treino 4 - membros inferiores': [
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

    treino_escolhido = st.selectbox('Selecione o treino', list(treinos.keys()))

    # Inicializa estado dos checkboxes
    if 'status_exercicios' not in st.session_state or st.session_state.get('treino_atual') != treino_escolhido:
        st.session_state.status_exercicios = [False] * len(treinos[treino_escolhido])
        st.session_state.treino_atual = treino_escolhido

    st.subheader('Exercícios do treino:')
    
    # Mostrar os exercícios com checkbox
    for i, exercicio in enumerate(treinos[treino_escolhido]):
        st.session_state.status_exercicios[i] = st.checkbox(
            label=exercicio,
            value=st.session_state.status_exercicios[i],
            key=f"check_{i}"
        )

    # Verifica se todos estão marcados
    if all(st.session_state.status_exercicios):
        if st.button('🏁 Finalizar Treino'):
            st.success(f"Parabéns! Você finalizou o treino de {treino_escolhido} 🎉")
            st.balloons()
