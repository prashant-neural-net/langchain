import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

for chunk in model.stream("what is the capital of india"):
    print(chunk.content, end="", flush=True)

print()
