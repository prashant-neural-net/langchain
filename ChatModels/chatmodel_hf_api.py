from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

load_dotenv()
console = Console()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4.1-Flash",
    task="text-generation",
    provider="auto",
    temperature=0,
)
model = ChatHuggingFace(llm=llm)

res = model.invoke("hi what is the capital of south africa")

console.print(Panel(Markdown(res.content)))
