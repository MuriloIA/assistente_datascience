from langchain_community.document_loaders import CSVLoader

def carrega_csv(arquivo):
    loader = CSVLoader(arquivo)
    dados = [doc.page_content for doc in loader.load()]
    return dados
