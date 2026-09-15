from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import ChatHuggingFace
from dotenv import load_dotenv
import os
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-Coder-7B-Instruct",
    temperature=0.7,
    provider="auto"
)
model = ChatHuggingFace(llm=llm)
for chunk in  model.stream("what is dependency in fastapi explain in detail"):
    print(chunk.content, end="", flush=True)

