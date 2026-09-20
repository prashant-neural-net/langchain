import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model="llama3.2:3b",
    base_url=os.environ["Base_Url"],
    temperature=0.0,
)

parser = StrOutputParser()

prompt = PromptTemplate(
    template="give me three jokes on {people} people, description: {description}",
    input_variables=["people", "description"],
)

chain = RunnableSequence(prompt, model, parser)

topic = str(input("joke topic: "))
desc = str(input("description: "))
response = chain.invoke({"people": topic, "description": desc})

print(response)
