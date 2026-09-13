from langchain_huggingface import HuggingFaceEndpointEmbeddings

from dotenv import load_dotenv

load_dotenv()

embedding = HuggingFaceEndpointEmbeddings(model="deepseek-ai/DeepSeek-V4.1-Flash")

embedding.embed_query("Delhi is the capital of india")

print((embedding))