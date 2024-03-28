import os
import openai
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Load environment variables
load_dotenv(".env.local")
openai.api_key = os.getenv('OPENAI_API_KEY')
INSTRUCTIONS = os.getenv('INSTRUCTIONS', 'Please follow the instructions.') 
ASSISTANT_PROFILE = os.getenv('ASSISTANT_PROFILE', 'Default Assistant Profile')

def main():
    """Main application function."""
    setup_streamlit_ui()

    website_urls = st.session_state.website_urls
    if website_urls and st.sidebar.button("Submit URLs"):
        process_urls(website_urls)

    display_conversation()

def setup_streamlit_ui():
    """Setup Streamlit UI components."""
    st.set_page_config(page_title="SintaxMatrix", page_icon="👋")
    st.title("SM URL Query Assistant")
    with st.sidebar:
        st.header("Settings")
        st.session_state.website_urls = st.text_area("Website URLs", help="Enter multiple URLs separated by commas.").split(',')

def process_urls(urls):
    """Process each URL from the input list."""
    try:
        for url in urls:
            if url.startswith("https://"):
                vector_stores = [get_vectorstore_from_url(url.strip()) for url in urls if url.strip()]
                if "vector_stores" not in st.session_state:
                    st.session_state.vector_stores = vector_stores
            else:
                st.sidebar.write("ERROR! Start URLs with https://")
                return
    except Exception as e:
        st.sidebar.write("ERROR! Include valid domains, like '.com'.")

def get_vectorstore_from_url(url):
    """Load a document from a URL and create a vector store."""
    loader = WebBaseLoader(url)
    document = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    doc_chunks = text_splitter.split_documents(document)
    vector_store = Chroma.from_documents(doc_chunks, OpenAIEmbeddings())
    return vector_store

def get_response(user_query):
    """Generate a response for the user query using the conversation chain."""
    if "vector_stores" in st.session_state and st.session_state.vector_stores:
        for vector_store in st.session_state.vector_stores:
            retriever_chain = get_context_retriever_chain(vector_store)
            conversation_rag_chain = get_conversational_rag_chain(retriever_chain)

            response = conversation_rag_chain.invoke({
                        "chat_history": st.session_state.chat_history,
                        "input": user_query
                    })
            return response['answer']
    return "Unable to process the query without a valid vector store."

def display_conversation():
    """Display conversation history and input box for new queries."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [AIMessage(content="Hi!")]
    
    user_query = st.chat_input("Say something...", key="user_query")
    if user_query:
        response = get_response(user_query)
        st.session_state.chat_history.extend([
            HumanMessage(content=user_query),
            AIMessage(content=response)
        ])

    for message in st.session_state.chat_history:
        with st.container():
            if isinstance(message, AIMessage):
                 with st.chat_message("AI"):
                    st.write(message.content)
            elif isinstance(message, HumanMessage):
                 with st.chat_message("Human"):
                    st.write(message.content)

def get_context_retriever_chain(vector_store):
    """Create a retriever chain for context retrieval."""
    llm = ChatOpenAI()
    retriever = vector_store.as_retriever()
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", INSTRUCTIONS)
    ])
    return create_history_aware_retriever(llm, retriever, prompt)

def get_conversational_rag_chain(retriever_chain):
    """Create a chain for conversational RAG processing."""
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"{ASSISTANT_PROFILE}:\n\n{{context}}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

if __name__ == "__main__":
    main()