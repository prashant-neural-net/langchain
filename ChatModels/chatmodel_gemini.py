from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

for chunk in model.stream("what is the capital of india"):
    print(chunk.content, end="", flush=True)

print()
