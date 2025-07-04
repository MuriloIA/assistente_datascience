import os
import tempfile
import streamlit as st
from load_csv import carrega_csv
from langchain_openai.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate

# Configurações da página
st.set_page_config(page_title='Assistente Virtual', page_icon='🤖', layout='wide')

# Definindo o estilo CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Karla:ital,wght@0,200..800;1,200..800&display=swap');
    body {
        font-family: 'Karla', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

def carrega_arquivo(arquivo):
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
        temp.write(arquivo.read())
        nome_temp = temp.name
    try:
        dados = carrega_csv(nome_temp)
    finally:
        os.remove(nome_temp)
    return dados

def carrega_modelo(arquivo):

    # Verificar se a API Key foi fornecida
    api_key = st.session_state.get('api_key')
    if not api_key:
        # Se a chave não foi fornecida, exibe uma mensagem de erro
        st.error("Por favor, forneça a chave da API da OpenAI na barra lateral antes de prosseguir.")
        return  # Interrompe o processamento se a chave não estiver presente


    # Carrega dados
    dados = carrega_arquivo(arquivo)

    system_message = """
            Você é um cientista de dados e estatístico experiente, especializado em análise exploratória, geração de insights e explicações técnicas baseadas em dados estruturados.

            O usuário forneceu um conjunto de dados, apresentado abaixo. Todas as respostas devem ser baseadas **exclusivamente** nesse conjunto. Use linguagem clara, mas técnica, adequada a profissionais que desejam compreender os dados de maneira analítica e objetiva.

            ---

            📊 **Dados fornecidos**:
            {}

            ---

            📌 **Instruções**:

            - Responda sempre de forma estruturada e fundamentada.
            - Quando aplicável, mencione métricas estatísticas (média, desvio padrão, valores máximos/mínimos, etc.).
            - Use termos como: “a distribuição indica…”, “observa-se uma tendência…”, “há correlação aparente…”.
            - Se a pergunta envolver comparação entre colunas ou agrupamento por categorias, faça inferências baseadas na estrutura dos dados.
            - **Nunca invente colunas ou dados não presentes.**
            - Evite respostas genéricas — seja específico com base nas informações fornecidas.
            - Se a pergunta não for respondível com os dados fornecidos, diga explicitamente que a informação não está disponível.

            ---

            🎯 Você deve agir como um especialista técnico que interpreta os dados para apoiar a tomada de decisão do usuário.
            """.format(dados)


    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])

    # ChatModel
    openai = ChatOpenAI(model='gpt-4o', api_key=api_key, temperature=0.2, top_p=0.5)

    chain = template | openai
    st.session_state['chain'] = chain

def side_bar():
    # Cabeçalho
    st.markdown('## 🤖 **Assistente Virtual de Análise de Dados**')
    st.markdown('Converse com seus dados e gere relatórios personalizados. 📊')
    st.divider()

    tb1, tb2 = st.tabs(['API Key', 'Assistente'])

    with tb1:
        api_key = st.text_input(label='🔑 Insira sua chave da API da OpenAI', value=st.session_state.get('api_key'))
        st.session_state['api_key'] = api_key

    with tb2:
        st.markdown("""
            **Como usar:**
            1. Carregue seus dados em formato `.csv`.
            2. O assistente irá processar seus dados e você pode começar a fazer perguntas.
            3. Pergunte sobre insights, estatísticas ou faça análises exploratórias!
        """)

        # Upload do arquivo
        arquivo = st.file_uploader(label="📂 Faça o upload dos seus dados (.csv)", type=["csv"])

        if arquivo is not None:
            if arquivo.name.endswith(".csv") and arquivo.size > 0:
                btn = st.button("📥 Enviar o arquivo .csv", use_container_width=True)
                if btn:
                    with st.spinner('Carregando os dados...'):
                        carrega_modelo(arquivo)
                    st.success("Arquivo carregado com sucesso! Agora, você pode interagir com o assistente.")

            else:
                st.error("O arquivo precisa ser um .csv válido.")
                st.info("Verifique se você selecionou o arquivo correto e tente novamente.")

def pagina_chat():
    
    chain = st.session_state.get('chain')
    if chain is None:
        chat = st.chat_message('ai')
        chat.markdown('##### Olá! 👋')
        chat.markdown('Eu sou seu assistente virtual. Carregue seus dados em formato **CSV** para começarmos a análise.')
        st.stop()

    # Histórico de conversa
    memoria = st.session_state.get('memoria', ConversationBufferMemory())
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    # Entrada do usuário
    input_usuario = st.chat_input('Fale com o assistente')
    if input_usuario:
        chat = st.chat_message('human')
        chat.markdown(input_usuario)

        # Assistente Virtual
        chat = st.chat_message('ai')

        # Resposta
        resposta = chat.write_stream(chain.stream({'input': input_usuario, 'chat_history': memoria.buffer_as_messages}))

        # Adicionando mensagem a memoria
        memoria.chat_memory.add_user_message(input_usuario)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria'] = memoria

def main():
    with st.sidebar:
        side_bar()
    pagina_chat()

if __name__ == '__main__':
    main()