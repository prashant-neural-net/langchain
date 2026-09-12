from rich.console import Console, Group
from rich.text import Text
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
import typer
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from rich import print
import os
import threading
import time

load_dotenv()

console = Console()
app = typer.Typer()

model_name = "llama3.2:3b"

chat_model = ChatOpenAI(model=model_name, base_url=os.environ["Base_Url"], temperature=0)

@app.command()
def chat(prompt: str):
    """ sending prompt to local model """
    console.print("[bold green]llama:[/bold green] ", end="")

    for chunk in chat_model.stream(prompt):
        if chunk.content:
            console.print(chunk.content, end="", markup=False)

    print()

@app.command()
def markdown_chat(prompt: str):
    """prints mardown format"""

    result = [None]

    def run_model():
        try:
            result[0] = chat_model.invoke(prompt)
        except Exception as e:
            print(f"invoke did now work \n{e}")

    thread = threading.Thread(target= run_model)
    start = time.perf_counter()
    thread.start()
    spinner = Spinner('aesthetic')
    with Live(spinner, refresh_per_second=10) as live:
        while thread.is_alive():
            current_time = time.perf_counter() - start
            text = Text("Thinking...")
            text.append(f"{current_time:.2f}", style="bold cyan")
            live.update(Group(spinner, text))
            time.sleep(0.1)

    thread.join()
    
    console.print(Panel(Markdown(result[0].content),
    border_style="blue"))
    
@app.command()
def model():
    """print name of current model"""
    console.print(Panel(
        f"[bold cyan]current model:[/bold cyan] {model_name}",
        border_style="green",
        title="Current Model"
    ))

if __name__ == "__main__":
    app()
