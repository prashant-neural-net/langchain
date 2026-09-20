import os

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model="llama3.2:3b", base_url=os.environ["Base_Url"], temperature=0.0
)

prompt = PromptTemplate(
    template="""Write a summary for the following text - \n {text}""",
    input_variables=["poem"],
)

parser = StrOutputParser()

loader = TextLoader("football.txt", encoding="utf-8")

docs = loader.load()

print(type(docs))

print(len(docs))

print(type(docs[0].metadata))

chain = prompt | model | parser

response = chain.invoke({"text": docs[0].page_content})

print(response)
