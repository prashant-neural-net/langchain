import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(base_url=os.environ["Base_Url"], api_key="ollama")

response = client.chat.completions.create(
    model="llama3.2:3b",
    messages=[{"role": "user", "content": "what is dependency injection in fastapi"}],
    stream=True,
)


for chunk in response:
    if chunk:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
print()

