import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
os.environ["STREAMLIT_HOME"] = os.getcwd()
os.environ["XDG_CONFIG_HOME"] = os.getcwd()


#-- Page Config -- 

st.set_page_config(page_title='Q&A Chatbot', page_icon='💬')
st.title('QnA Chatbot')

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")



if api_key:
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.5,
        api_key=api_key
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that answers questions clearly and concisely."),
        ("human", "{question}")
    ])

    chain = prompt | llm

    with st.form("chat_form"):
        question = st.text_area("Ask a question:", placeholder="e.g. What is LangChain?")
        submitted = st.form_submit_button("Submit")

    if submitted and question:
        with st.spinner("Thinking..."):
            response = chain.invoke({"question": question})
            st.success(response.content)
else:
    st.warning("Please enter your OpenAI API key to continue.")

