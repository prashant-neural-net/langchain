from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpointEmbeddings

load_dotenv()

embedding = HuggingFaceEndpointEmbeddings(model="deepseek-ai/DeepSeek-V4.1-Flash")

embed = embedding.embed_query("Delhi is the capital of india")

print(embed)
