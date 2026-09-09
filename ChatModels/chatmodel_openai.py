from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenAI(model="llama3.2:3b", base_url=os.environ["Base_Url"], temperature=0)

for chunk in model.stream("suggest 5 name of alien"):
    if chunk.content:
        print(chunk.content, end="", flush=True)

print()
