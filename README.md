# 🤖 Assistente Virtual de Análise de Dados

Um assistente interativo baseado em **IA da OpenAI** e **Streamlit**, que permite conversar com seus próprios dados `.csv`, extraindo insights, realizando análises exploratórias e respondendo perguntas com base em inteligência artificial.

---

## 📌 Funcionalidades

- Upload de arquivos `.csv` para análise.
- Interação por chat com os dados.
- Geração de insights estatísticos automáticos (média, desvio padrão, tendência, correlação, etc.).
- Histórico de conversa mantido durante a sessão.
- Interface simples, responsiva e pronta para uso via navegador.
- Processamento local com uso de LLMs da OpenAI (necessário fornecer chave da API).

---

## 🚀 Tecnologias Utilizadas

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [OpenAI GPT](https://platform.openai.com/)
- [Pandas](https://pandas.pydata.org/) *(via módulo `load_csv.py`)*

---

## 🧠 Estrutura do Projeto

```
├── app.py                  # Código principal da aplicação Streamlit
├── load_csv.py            # Função personalizada para leitura do CSV
├── requirements.txt       # Dependências do projeto
└── README.md              # Este arquivo
```

---

## ⚙️ Pré-requisitos

- Python 3.9+
- Conta na [OpenAI](https://platform.openai.com/signup)
- Chave de API válida

---

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

# (Recomendado) Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

---

## 🖥️ Execução Local

```bash
# Inicie a aplicação Streamlit
streamlit run app.py
```

---

## 🔑 Como usar

1. Gere uma chave da API em [OpenAI API Keys](https://platform.openai.com/account/api-keys).
2. Inicie o app localmente (`streamlit run app.py`).
3. Insira sua chave no campo da **barra lateral**.
4. Faça upload de um arquivo `.csv`.
5. Interaja com o assistente perguntando sobre seus dados!

---

## 🧪 Exemplo de Perguntas ao Assistente

- "Qual é a média da coluna `vendas`?"
- "Existe correlação entre `idade` e `salário`?"
- "Qual categoria teve maior volume em 2022?"
- "Explique a distribuição da variável `nota_final`."

---

## ❗Tratamento de Erros

- O app verifica se a **API Key** está presente e se é **válida**.
- Arquivos inválidos ou fora do formato `.csv` são recusados com mensagens apropriadas.
- As respostas do assistente são **baseadas exclusivamente nos dados fornecidos** — ele **não inventa colunas nem informações externas**.

---

## 📄 Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).

---

## 🙋‍♂️ Autor

Desenvolvido por [Murilo Rocha](https://github.com/seu-usuario) • Contato: [musilva.14@gmail.com](musilva.14@gmail.com)

---

## 💡 Ideias Futuras

- Exportação de relatórios em PDF.
- Suporte a múltiplos arquivos e comparação entre datasets.
- Análises gráficas com Plotly ou Altair.