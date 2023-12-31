
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template, footer
from langchain.llms import HuggingFaceHub
from PIL import Image
from pyngrok import ngrok
import os
import time


progress_bar1 = ""
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    #llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.7, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def init():

    if load_dotenv(os.environ.get('OPENAI_API_KEY')) is None or load_dotenv(os.environ.get('OPENAI_API_KEY')) == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")


def main():
    init()
    #os.environ["OPENAI_API_KEY"] = "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"
    #st.set_page_config(page_title="PDF Summerizer virtual Robot",page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    st.title('PageWhisperer :blue[Bot] ')
    st.header('Powered :blue[By]',)
    st.write('''<style>
    "<style>.st-emotion-cache-1v0mbdj.e115fcil1 {
    max-width: 100px;
    display: flex;
    } </style>''', unsafe_allow_html=True)
    image = Image.open('logo.jpeg')
    new_image = image.resize((400, 200))
    st.image(image, caption='')
    st.header('', divider='rainbow')
    progress_bar1 = st.progress(0)
    status_text1 = st.empty()
    st.header("Search In Your Docs By Entering Your Query Here:")
    #user_question = st.text_input("Ask a question about your documents:")
    user_question = st.chat_input("Ask a question about your documents and Press Enter button: ", key="user_input")
    if user_question:
        progress_bar1.progress(10)
        status_text1.text(f'Operation in progress. Please wait: {10}%')
        handle_userinput(user_question)
        progress_bar1.progress(100)
        status_text1.text(f'Operation in progress. Please wait: {100}%')

    with st.sidebar:
        my_bar = st.progress(0)
        status_text = st.empty()
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True,type='pdf')
        if st.button("Process"):
            with st.spinner("Processing..."):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                my_bar.progress(20)
                status_text.text(f'Operation in progress:{20}%')
                #st.write(raw_text)
                # get the text chunks
                text_chunks = get_text_chunks(raw_text)
                my_bar.progress(40)
                status_text.text(f'Operation in progress: {40}%')
                #st.write(text_chunks)
                # create vector store
                vectorstore = get_vectorstore(text_chunks)
                my_bar.progress(70)
                status_text.text(f'Operation in progress: {70}%')
                #st.write(vectorstore)
                st.write("Successfully Done!")
                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)
                my_bar.progress(100)
                status_text.text(f'Operation in progress: {100}%')
    
if __name__ == '__main__':
    main()
    
