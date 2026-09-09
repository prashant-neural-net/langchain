from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    task="text-generation",
    provider="auto",
    max_new_tokens=100,
    temperature=0.5,
)
model = ChatHuggingFace(llm=llm)

res = model.invoke("radhe radhe")

print(res.content)

