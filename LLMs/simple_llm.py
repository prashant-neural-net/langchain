import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

load_dotenv()


model = OpenAI(
    model_name="llama3.2:3b", temperature=0.0, base_url=os.environ["Base_Url"]
)

prompt = PromptTemplate(
    template="write a essay of 100 words on topic {topic}", input_variables=["topic"]
)

topic = input("enter the topic: ")

formatted_prompt = prompt.format(topic=topic)

response = model.invoke(formatted_prompt)

print(response)
