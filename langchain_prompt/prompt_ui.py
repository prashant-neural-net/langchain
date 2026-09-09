from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import ChatHuggingFace
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(repo_id="openai/gpt-oss-120b", task="text-generation", provider="auto")

model = ChatHuggingFace(llm=llm)

prompt = st.text_input('Enter Prompt')

response = model.invoke(prompt)

if st.button('Submit'):
    st.write(response.content)