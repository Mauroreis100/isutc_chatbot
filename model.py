from dotenv import load_dotenv
import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain


load_dotenv()

# --- CONFIGURAÇÃO INICIAL ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
db_path = "./isutc_knowledge_base"

st.set_page_config(page_title="Assistente de Candidaturas ISUTC", page_icon="🎓")
st.title("🎓 ISUTC Chatbot - Candidaturas")

# --- 1. PERSONALIZAÇÃO DO PROMPT (AQUI!) ---
system_prompt = (
    "És um assistente virtual especializado em ajudar estudantes nas candidaturas ao ISUTC (Moçambique)."
    "Utiliza apenas o contexto fornecido para responder às perguntas."
    "Se não souberes a resposta com base no contexto, diz educadamente que não encontraste essa informação específica e sugere contactar a secretaria."
    "Mantém um tom profissional, prestável e encorajador."
    "No final da resposta, se houver um link de fonte no contexto, indica-o."
    "\n\n"
    "Contexto: {context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# --- 2. CARREGAMENTO DA BASE DE DADOS E MODELO ---
@st.cache_resource # Cache para não carregar o modelo em cada clique
def load_rag_system():
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", 
        api_key=GEMINI_API_KEY
        )
    vectorstore = Chroma(persist_directory=db_path, embedding_function=embeddings)
    
    llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, 
                                 temperature=0.2
                                 , api_key=GEMINI_API_KEY
                                 )
    
    # Criar as correntes (chains)
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(vectorstore.as_retriever(search_kwargs={"k": 3}), combine_docs_chain)
    
    return retrieval_chain

# --- 3. INTERFACE DO CHAT ---
rag_chain = load_rag_system()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do Utilizador
if user_input := st.chat_input("Como posso ajudar com a tua candidatura?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("A consultar documentos do ISUTC..."):
            # Executar RAG
            response = rag_chain.invoke({"input": user_input})
            answer = response["answer"]
            
            # EXTRAÇÃO DE LINKS/FONTES
            # O LangChain devolve os documentos usados na chave 'context'
            sources = set([doc.metadata.get('source', 'Fonte desconhecida') for doc in response["context"]])
            
            st.markdown(answer)
            
            if sources:
                with st.expander("Ver Fontes"):
                    for source in sources:
                        # Se o 'source' for o caminho do ficheiro, podes limpar o nome
                        st.write(f"- {source}")

    st.session_state.messages.append({"role": "assistant", "content": answer})