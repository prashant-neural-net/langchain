from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

emb = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=32)

emb.embed_query("Delhi is the capital of india")

print(str(emb))
