import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import plotly.express as px

# -------- Autenticação Google Sheets --------
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

# -------- Carregar dados --------
def carregar_treinos(sheet):
    dados = sheet.get_all_records()
    return pd.DataFrame(dados)

def salvar_historico(sheet, usuario, treino):
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([data, usuario, treino])

# -------- Página principal --------
def pagina_inicial():
    usuario = st.session_state.get("name", "Convidado")
    
    validade = "01/06/2026"  # Exemplo de validade
    
    # Depois use a variável no HTML
    st.markdown(f"""
        <h1 style="
            background: linear-gradient(to right, #ff00ff, #00ffff, #00ffea, #ff00aa, #ff0055);
            -webkit-background-clip: text;
            color: transparent;
            display: flex; align-items: center;">
            Olá, {usuario}
        </h1>
        <hr>
        """, unsafe_allow_html=True)
    
    st.write(f'Validade até {validade}')

    try:
        client = autenticar_gsheets()
        planilha = client.open_by_url("https://docs.google.com/spreadsheets/d/1qc04HBmnHpqbIvfgJXU80u-Fh5bcHoUKnLF17OJLslM/edit#gid=0")
        aba_treinos = planilha.worksheet("Treinos")

        try:
            aba_historico = planilha.worksheet("Historico")
        except gspread.exceptions.WorksheetNotFound:
            aba_historico = planilha.add_worksheet(title="Historico", rows="100", cols="3")
            aba_historico.append_row(["Data", "Usuário", "Treino"])

        # -------- Exibição do treino --------
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

        # -------- Análises e Histórico --------
        st.markdown("---")
        tab1, tab2, tab3 = st.tabs(["📊 Gráfico de Treinos", "🗂️ Histórico de Treino", "📋 Tabela Detalhada"])

        historico_dados = aba_historico.get_all_records()

        if historico_dados:
            df_hist = pd.DataFrame(historico_dados)
            if "Data" not in df_hist.columns:
                st.warning("A aba 'Historico' está sem a coluna 'Data'. Corrija manualmente no Google Sheets.")
                return

            df_hist["Data"] = pd.to_datetime(df_hist["Data"], errors='coerce')
            df_hist = df_hist.dropna(subset=["Data"])
            df_hist["Ano"] = df_hist["Data"].dt.year
            df_hist["AnoMes"] = df_hist["Data"].dt.to_period("M").astype(str)

            ano_mes_options = sorted(df_hist["AnoMes"].unique(), reverse=True)
            treino_unicos = sorted(df_hist["Treino"].unique())

            # -------- TAB 1: Gráfico Pizza --------
            with tab1:
                filtro_grafico = st.selectbox("📅 Filtro (AAAA-MM):", ano_mes_options, key="filtro_grafico")
                df_grafico = df_hist[df_hist["AnoMes"] == filtro_grafico]

                if not df_grafico.empty:
                    dados_grafico = df_grafico.groupby("Treino").size().reset_index(name="Quantidade")
                    fig = px.pie(
                        dados_grafico,
                        names="Treino",
                        values="Quantidade",
                        hole=0.5,
                        title=f"Treinos realizados em {filtro_grafico}",
                        color="Treino",
                        color_discrete_map={
                            'Treino 1 - Peito': 'lightcyan',
                            'Treino 2 - Pernas': 'cyan',
                            'Treino 3 - Costas': 'royalblue',
                            'Treino 4 - membros inferiores': 'darkblue'
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Nenhum treino encontrado neste mês.")

            # -------- TAB 2: Histórico com Gráfico de Barras --------
            with tab2:
                filtro_ano = st.selectbox("📆 Selecione o Ano:", sorted(df_hist["Ano"].unique(), reverse=True))
                filtro_treino = st.multiselect("💪 Selecione o(s) Treino(s):", treino_unicos)

                df_filtrado = df_hist[df_hist["Ano"] == filtro_ano]
                if filtro_treino:
                    df_filtrado = df_filtrado[df_filtrado["Treino"].isin(filtro_treino)]

                if not df_filtrado.empty:
                    df_agrupado = (
                        df_filtrado.groupby("AnoMes")
                        .size()
                        .reset_index(name="Quantidade")
                        .sort_values("AnoMes")
                    )

                    media = df_agrupado["Quantidade"].mean()
                    st.caption(f"📊 Média mensal de treinos em {filtro_ano}: **{media:.1f} treinos**")

                    fig_bar = px.bar(
                        df_agrupado,
                        x="AnoMes",
                        y="Quantidade",
                        title=f"Total de Treinos por Mês em {filtro_ano}",
                        labels={"AnoMes": "Mês (AAAA-MM)", "Quantidade": "Qtd. de Treinos"},
                        text_auto=True,
                        color="Quantidade",
                        color_continuous_scale="Blues"
                    )
                    fig_bar.update_layout(xaxis_tickangle=-45, xaxis_type='category')
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info(f"Nenhum treino encontrado para o ano {filtro_ano}.")

            # -------- TAB 3: Tabela Detalhada --------
            with tab3:
                filtro_tabela = st.selectbox("📅 Filtro (AAAA-MM):", ano_mes_options, key="filtro_tabela")
                df_tabela = df_hist[df_hist["AnoMes"] == filtro_tabela]

                st.markdown(f"### 🗂️ Histórico de {filtro_tabela}")
                st.dataframe(
                    df_tabela[["Data", "Usuário", "Treino"]]
                        .sort_values("Data", ascending=False)
                        .reset_index(drop=True),
                    use_container_width=True
                )

        else:
            st.info("Nenhum treino registrado ainda.")

    except Exception as e:
        st.error(f"Erro ao conectar com o Google Sheets: {e}")
        st.info("Verifique se a planilha foi compartilhada corretamente com o e-mail da service account.")
