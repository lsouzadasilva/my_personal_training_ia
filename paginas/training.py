import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import plotly.express as px

# -------- Autenticação Google Sheets usando st.secrets --------
def autenticar_gsheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = dict(st.secrets["google_service_account"])
    if "private_key" in creds_dict:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client


# -------- Carregar dados da aba Treinos --------
def carregar_treinos(sheet):
    dados = sheet.get_all_records()
    df = pd.DataFrame(dados)
    return df

# -------- Salvar histórico --------
def salvar_historico(sheet, usuario, treino):
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([data, usuario, treino])

# -------- Página principal --------
def pagina_inicial():
    validade = '01/08/2025'

    st.markdown("""
    <h1 style="
        background: linear-gradient(to right, #ff00ff, #00ffff, #00ffea, #ff00aa, #ff0055);
        -webkit-background-clip: text;
        color: transparent;
        display: flex; align-items: center;">
        Meu Treino
        <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/People%20with%20activities/Person%20Lifting%20Weights%20Medium-Dark%20Skin%20Tone.png" 
        style="width:50px; margin-left:10px;">
    </h1>
    <hr>
    """, unsafe_allow_html=True)

    st.write(f'Validade até {validade}')
    usuario = st.text_input("Digite seu nome para salvar o progresso:")

    try:
        client = autenticar_gsheets()
        planilha = client.open_by_url("https://docs.google.com/spreadsheets/d/1qc04HBmnHpqbIvfgJXU80u-Fh5bcHoUKnLF17OJLslM/edit#gid=0")
        aba_treinos = planilha.worksheet("Treinos")

        try:
            aba_historico = planilha.worksheet("Historico")
        except gspread.exceptions.WorksheetNotFound:
            aba_historico = planilha.add_worksheet(title="Historico", rows="100", cols="3")
            aba_historico.append_row(["Data", "Usuário", "Treino"])

        df = carregar_treinos(aba_treinos)
        treinos_disponiveis = df["Nome do Treino"].unique().tolist()

        treino_escolhido = st.selectbox('Selecione o treino', treinos_disponiveis)

        if treino_escolhido:
            exercicios = df[df["Nome do Treino"] == treino_escolhido].sort_values("Ordem")["Exercício"].tolist()

            if 'status_exercicios' not in st.session_state or st.session_state.get('treino_atual') != treino_escolhido:
                st.session_state.status_exercicios = [False] * len(exercicios)
                st.session_state.treino_atual = treino_escolhido

            st.subheader('Exercícios do treino:')
            for i, exercicio in enumerate(exercicios):
                st.session_state.status_exercicios[i] = st.checkbox(
                    label=exercicio,
                    value=st.session_state.status_exercicios[i],
                    key=f"check_{i}"
                )

            if all(st.session_state.status_exercicios):
                if st.button('🏁 Finalizar Treino'):
                    if usuario.strip() == "":
                        st.warning("Por favor, digite seu nome para salvar o progresso!")
                    else:
                        salvar_historico(aba_historico, usuario, treino_escolhido)
                        st.success(f"Parabéns {usuario}! Você finalizou o treino de {treino_escolhido} 🎉")
                        st.balloons()
                        st.session_state.status_exercicios = [False] * len(exercicios)

        # -------- Histórico e Visualizações --------
        st.markdown("---")
        tab1, tab2 = st.tabs(["📊 Gráfico de Treinos", "📋 Tabela Detalhada"])

        historico_dados = aba_historico.get_all_records()
        if historico_dados:
            df_hist = pd.DataFrame(historico_dados)

            if "Data" in df_hist.columns:
                df_hist["Data"] = pd.to_datetime(df_hist["Data"], errors='coerce')
                df_hist = df_hist.dropna(subset=["Data"])
                df_hist["AnoMes"] = df_hist["Data"].dt.to_period("M").astype(str)

                # ---------- Aba 1: Gráfico ----------
                with tab1:
                    ano_mes_options = sorted(df_hist["AnoMes"].unique(), reverse=True)
                    filtro_grafico = st.selectbox("📅 Filtro (AAAA-MM):", ano_mes_options, key="filtro_grafico")
                    df_grafico = df_hist[df_hist["AnoMes"] == filtro_grafico]

                    if not df_grafico.empty:
                        dados_grafico = df_grafico.groupby("Treino").size().reset_index(name="Quantidade")

                        # fig = px.bar(
                        #     dados_grafico,
                        #     x="Treino",
                        #     y="Quantidade",
                        #     color="Treino",
                        #     title=f"Treinos realizados em {filtro_grafico}",
                        #     labels={"Quantidade": "Quantidade"},
                        #     text_auto=True,
                        #     # orientation='h'  -> Para deixar horizontal
                        # )
                        fig = px.pie(
                            dados_grafico,
                            names="Treino",
                            values="Quantidade",
                            hole=0.5,
                            title=f"Treinos realizados em {filtro_grafico}",
                        )
                            
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Nenhum treino encontrado neste mês.")

                # ---------- Aba 2: Tabela Detalhada ----------
                with tab2:
                    filtro_tabela = st.selectbox("📅 Filtro (AAAA-MM):", ano_mes_options, key="filtro_tabela")
                    df_tabela = df_hist[df_hist["AnoMes"] == filtro_tabela]

                    st.markdown(f"### 🗂️ Histórico de {filtro_tabela}")
                    st.dataframe(
                        df_tabela[["Data", "Usuário", "Treino"]]
                            .sort_values("Data", ascending=False)
                            .reset_index(drop=True),  # Aqui remove o índice original
                        use_container_width=True
                    )
            else:
                st.warning("A aba 'Historico' está sem a coluna 'Data'. Corrija manualmente no Google Sheets.")
        else:
            st.info("Nenhum treino registrado ainda.")

    except Exception as e:
        st.error(f"Erro ao conectar com o Google Sheets: {e}")
        st.info("Verifique se a planilha foi compartilhada corretamente com o e-mail da service account.")
