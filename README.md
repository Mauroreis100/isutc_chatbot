# 🎓 ISUTC Admissions Chatbot (RAG)

Este projeto é um assistente virtual inteligente desenvolvido para facilitar o processo de candidatura ao **ISUTC (Instituto Superior de Transportes e Comunicações)** em Moçambique. Utiliza a arquitetura **RAG (Retrieval-Augmented Generation)** para fornecer respostas precisas baseadas diretamente no conteúdo oficial do site.


https://github.com/user-attachments/assets/fc7a667f-0a5b-4ac1-b844-eb11f5fbc095


## 🚀 Funcionalidades

  * **Extração Inteligente:** Crawling recursivo do site do ISUTC usando **Crawl4AI**, convertendo HTML complexo em Markdown limpo.
  * **Base de Conhecimento Vetorial:** Armazenamento de dados no **ChromaDB** para buscas semânticas rápidas.
  * **IA de Última Geração:** Respostas geradas pelo **Google Gemini 1.5 Flash** (rápido e preciso).
  * **Citação de Fontes:** O bot indica as URLs de onde extraiu a informação para garantir fiabilidade.
  * **Interface Amigável:** Interface de chat moderna construída com **Streamlit**.

-----

## 🏗️ Arquitetura do Sistema

O sistema opera em três fases principais:

1.  **Ingestão:** O `crawler.py` percorre o site e guarda ficheiros `.md`.
2.  **Indexação:** O `ingest.py` processa os ficheiros, divide-os em chunks e cria os embeddings na base de dados vetorial.
3.  **Chat:** O `app.py` recebe a pergunta, recupera o contexto relevante e gera a resposta via Gemini.

-----

## 🛠️ Tecnologias Utilizadas

  * [Crawl4AI](https://crawl4ai.com/) - Web Crawling focado em LLMs.
  * [LangChain](https://www.langchain.com/) - Framework de orquestração de IA.
  * [Google Gemini](https://ai.google.dev/) - Modelo de Linguagem e Embeddings.
  * [ChromaDB](https://www.trychroma.com/) - Base de dados vetorial.
  * [Streamlit](https://streamlit.io/) - Interface web.

-----

## ⚙️ Configuração e Instalação

### 1\. Pré-requisitos

  * Python 3.10 ou superior.
  * Uma chave de API do [Google Gemini (Google AI Studio)](https://aistudio.google.com/).

### 2\. Instalação de Dependências

```bash
pip install crawl4ai langchain-google-genai langchain-community chromadb streamlit python-dotenv
```

### 3\. Variáveis de Ambiente

Cria um ficheiro `.env` na raiz do projeto ou configura nos secrets do Streamlit:

```env
GOOGLE_API_KEY=A_TUA_CHAVE_AQUI
```

-----

## 📖 Como Usar

### Passo 1: Crawling

Executa o crawler para extrair os dados mais recentes do site:

```bash
python crawler.py
```

### Passo 2: Ingestão de Dados

Cria a base de dados vetorial a partir dos ficheiros Markdown gerados:

```bash
python ingest.py
```

### Passo 3: Iniciar o Chatbot

Lança a interface web do Streamlit:

```bash
streamlit run app.py
```

-----

## 📁 Estrutura do Projeto

```text
.
├── isutc_knowledge_base/   # Ficheiros Markdown extraídos
├── chroma_db_isutc/        # Base de dados vetorial (gerada)
├── crawler.py              # Script de extração (Crawl4AI)
├── ingest.py               # Processamento e criação de embeddings
├── app.py                  # Interface Streamlit e lógica RAG
├── .env                    # Chaves de API (não enviar para o git)
└── README.md               # Documentação do projeto
```

-----

## 🎯 Personalização do Prompt

Para ajustar o comportamento do assistente, edita a variável `system_prompt` no ficheiro `app.py`. Podes definir:

  * O tom de voz (formal/informal).
  * Restrições de resposta (ex: responder apenas com base no site).
  * Idiomas suportados.

-----

## 🤝 Contribuições

Contribuições são bem-vindas\! Sinta-se à vontade para abrir uma *Issue* ou enviar um *Pull Request*.

-----

**Nota:** *Este projeto não tem vínculo oficial com o ISUTC e foi desenvolvido para fins educacionais e de auxílio informativo.*

-----
