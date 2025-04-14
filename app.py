import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_option_menu import option_menu
from paginas.training import pagina_inicial



st.set_page_config(
    page_title='Personal Trainer',
    page_icon= '🐦‍🔥',
)

# --- Ocult menus ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)


authenticator.login()

if st.session_state["authentication_status"]:
    st.sidebar.title("Navegação")
    st.sidebar.write(f'Bem Vindo *{st.session_state["name"]}*')
    authenticator.logout("Logout", "sidebar")
    
    st.sidebar.divider()

        
    
    # https://icons.getbootstrap.com/ - > icon
    with st.sidebar:
        paginas = option_menu(
        menu_title = "Menu",
        options = ["My Trainnig"],
        icons = ["activity"],
        menu_icon ="cast",
        default_index = 0
        # orientation = "horizontal"  < - Agora
    )


    st.sidebar.divider()
    st.sidebar.markdown("""
        **Desenvolvido por Leandro Souza**  
        [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/leandro-souza-bi/)
        [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/lsouzadasilva/streamlit_openai_langchain_read_pdf)
        """)

    if paginas == "My Trainnig":
        pagina_inicial()


elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha inválido')
elif st.session_state["authentication_status"] is None:
    st.warning('Por Favor, utilize seu usuário e senha!')


