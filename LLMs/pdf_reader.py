import os

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# load the document
loader = TextLoader("solar.txt")
documents = loader.load()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

vectorstore = FAISS.from_documents(
    docs,
    OllamaEmbeddings(model="mxbai-embed-large:latest", base_url=os.environ["Base_Url"]),
)

retriever = vectorstore.as_retriever()

query = "what is the summary of documenet"
retrieved_docs = retriever.get_relevant_documents(query)

retrieved_text = "\n".join([doc.page_content for doc in retrieved_docs])

model = ChatOpenAI(
    model_name="llama3.2:3b", temperature=0.0, base_url="http://localhost:11434"
)

prompt = (
    f"Based on the following text, answer the question: {query}\n\n{retrieved_text}"
)
answer = model.invoke(prompt)

print("answer: {answer}")


