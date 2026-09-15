import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model_name="llama3.2:3b", base_url=os.environ["Base_Url"], temperature=0.0
)

template1 = PromptTemplate(
    template="write a detailed report on {topic}", input_variables=["topic"]
)

template2 = PromptTemplate(
    template="write a 5 line summary on the following text. /n {text}",
    input_variables=["text"],
)

parser = StrOutputParser()

chain = template1 | model | parser | template2 | model | parser

result = chain.invoke({"topic": "football"})

print(result)
