import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model_name="llama3.2:3b", base_url=os.environ["Base_Url"])

messages = [
    SystemMessage(content="You are a football coach"),
    HumanMessage(content="tell me about offside rule"),
]

result = model.invoke(messages)

messages.append(AIMessage(content=result.content))

print(messages)
