from dotenv import load_dotenv
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

load_dotenv()

emb = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=32)

text = (
    """ samosa is very dilicious. World should help each other to counter terriorism"""
)

text_splitter = SemanticChunker(
    emb, breakpoint_threshold_type="standard_deviation", breakpoint_threshold_amount=1
)
docs = text_splitter.create_documents([text])
print(docs)
