
# Configuração da API Google Sheets para Projeto Streamlit

Este guia detalha como configurar a API do Google Sheets para uso em um projeto Streamlit que acessa e manipula dados em planilhas Google usando uma conta de serviço.

---

## Passo 1: Criar um Projeto no Google Cloud Console

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/).
2. Faça login com sua conta Google.
3. No menu superior, clique em **Selecionar projeto** > **Novo projeto**.
4. Dê um nome ao seu projeto (ex: `meuapptreino`).
5. Clique em **Criar** e aguarde a criação do projeto.

---

## Passo 2: Ativar a API Google Sheets e Google Drive

1. Com o projeto selecionado, vá ao menu lateral: **APIs e Serviços** > **Biblioteca**.
2. Pesquise por **Google Sheets API**.
3. Clique na API e depois em **Ativar**.
4. Repita o processo para a **Google Drive API**.

---

## Passo 3: Criar uma Conta de Serviço

1. No menu lateral, vá em **APIs e Serviços** > **Credenciais**.
2. Clique em **Criar credenciais** > **Conta de serviço**.
3. Informe um nome para a conta (ex: `acesso-planilha`).
4. Clique em **Criar e continuar** (sem adicionar permissões específicas).
5. Clique em **Concluir**.

---

## Passo 4: Criar e Baixar a Chave da Conta de Serviço

1. Na página de contas de serviço, clique no e-mail da conta que você criou.
2. Vá na aba **Chaves**.
3. Clique em **Adicionar chave** > **Criar nova chave**.
4. Selecione o formato **JSON** e clique em **Criar**.
5. Um arquivo `.json` será baixado automaticamente — **guarde este arquivo com segurança**.

---

## Passo 5: Compartilhar a Planilha com a Conta de Serviço

1. Abra a planilha Google que deseja acessar no projeto.
2. Clique em **Compartilhar** (botão azul no canto superior direito).
3. No campo de e-mails, cole o e-mail da conta de serviço, que está no arquivo JSON no campo `"client_email"` (ex: `acesso-planilha@meuapptreino-464718.iam.gserviceaccount.com`).
4. Defina a permissão como **Editor** (para poder editar os dados).
5. Clique em **Enviar**.

---

## Passo 6: Configurar `secrets.toml` no Streamlit

1. Copie o conteúdo do arquivo JSON baixado.
2. Crie um arquivo chamado `secrets.toml` na raiz do seu projeto Streamlit (ou configure no Streamlit Cloud).
3. Adicione as chaves e valores no formato TOML, assim:

```toml
type = "service_account"
project_id = "meuapptreino-464718"
private_key_id = "seu_private_key_id_aqui"
private_key = "-----BEGIN PRIVATE KEY-----\nMIIE...seu_key...\n-----END PRIVATE KEY-----\n"
client_email = "acesso-planilha@meuapptreino-464718.iam.gserviceaccount.com"
client_id = "seu_client_id_aqui"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/acesso-planilha@meuapptreino-464718.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

> **Importante:** Na chave `private_key`, mantenha as quebras de linha com `\n` exatamente como estão no JSON.

---

## Passo 7: Rodar o Projeto Streamlit

- Com tudo configurado, ao rodar seu app Streamlit, ele poderá autenticar automaticamente via `st.secrets` e acessar sua planilha do Google Sheets.

---

## Dicas e Soluções de Problemas

- **Erro "Incorrect padding"** geralmente indica problema na formatação da chave privada — garanta que as quebras de linha estejam com `\n` no arquivo `secrets.toml`.
- **Erro "st.secrets has no key 'type'"** indica que o arquivo `secrets.toml` não está configurado ou carregado corretamente. Verifique se ele está na pasta correta, nomeado certinho, e que a chave `"type"` está presente.
- Sempre compartilhe a planilha com o **e-mail exato** da conta de serviço para garantir permissão de acesso.

---

## Referências Oficiais

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Autenticação com Conta de Serviço](https://cloud.google.com/iam/docs/service-accounts)
- [Gerenciar Secrets no Streamlit](https://docs.streamlit.io/streamlit-cloud/secrets-management)

---
