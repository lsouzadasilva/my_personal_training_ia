import streamlit as st

def pagina_inicial():
    validade = '01/08/2025'
    st.title('Personal Trainer 🏋️', divider=True)
    st.write(f'Validade até {validade}')
    st.divider()

    # Treinos disponíveis
    treinos = {
        'Treino 1 - Peito': [
            'Supino reto com halteres – 4x10',
            'Supino inclinado com halteres – 4x10',
            'Crucifixo reto – 4x10',
            'Cross-over alto – 4x10'
        ],
        'Treino 2 - Pernas': [
            'Agachamento livre – 4x10',
            'Leg press – 4x10',
            'Cadeira extensora – 4x10',
            'Mesa flexora – 4x10'
        ],
        'Treino 3 - Costas': [
            'Puxada frontal – 4x10',
            'Remada curvada – 4x10',
            'Pulley – 4x10',
            'Remada unilateral – 4x10'
        ],
        'Treino 4 - membros inferiores': [
            'Barra W - 4X10',
            'Rosca martelo – 4X10',
            'Rosca alternada halteres – 4X10',
            'Tríceps corda no pulley – 4X10',
            'Tríceps testa (barra W) – 4X10',
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
