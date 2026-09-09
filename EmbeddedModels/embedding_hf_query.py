from langchain_huggingface import HuggingFaceEndpointEmbeddings

from dotenv import load_dotenv

load_dotenv()

embedding = HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2",dimensions=32)

embedding.embed_query("Delhi is the capital of india")

print(str(embedding))