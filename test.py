import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
load_dotenv()

# --- CONFIGURAÇÃO INICIAL ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# 1. Tentar carregar a base
def reconstruir_base():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", api_key=GEMINI_API_KEY)
    path_mds = "./isutc_knowledge_base"
    
    all_docs = []
    
    # Carregar um por um para garantir que pegamos o metadado
    for file in os.listdir(path_mds):
        if file.endswith(".md"):
            loader = TextLoader(os.path.join(path_mds, file), encoding="utf-8")
            data = loader.load()
            
            # Tentar extrair a URL que o Crawl4AI colocou no topo (se seguiu o meu passo anterior)
            conteudo = data[0].page_content
            url = "https://www.isutc.ac.mz" # Default
            if "SOURCE: " in conteudo:
                url = conteudo.split("\n")[0].replace("SOURCE: ", "").strip()
            
            # Adicionar a URL aos metadados para o Chatbot usar depois
            data[0].metadata["url"] = url
            all_docs.extend(data)

    # Splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    final_chunks = text_splitter.split_documents(all_docs)

    # Criar Chroma
    vectorstore = Chroma.from_documents(
        documents=final_chunks, 
        embedding=embeddings,
        persist_directory="./isutc_knowledge_base"
    )
    print(f"Base recriada com {len(final_chunks)} pedaços de texto!")

reconstruir_base()