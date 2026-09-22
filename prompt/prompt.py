import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-Coder-7B-Instruct", temperature=0.7, provider="auto"
)
model = ChatHuggingFace(llm=llm)
prompt = PromptTemplate(template="""hi what is RNN""")
st.header("Research Tool")

input = st.selectbox("choose an option", ["option1", "option2", "option3"])

if st.button("submit"):
    res = model.invoke(prompt)
    st.write(res.content)

if st.button("samosa"):
    res = model.invoke("write a poem about samosa")
    st.write(res.content)
