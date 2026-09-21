from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

loader = PyPDFLoader("football.pdf")

docs = loader.load()

splitter = CharacterTextSplitter(chunk_size=9, chunk_overlap=0, separator="")

result = splitter.split_documents(docs)

print(result[100].page_content)
