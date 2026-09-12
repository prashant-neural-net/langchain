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
import sqlite3

# from langchain_community.cache import SQLiteCache
# from langchain_core.globals import set_llm_cache

from ..Cache.sqlite_cache import SQLiteCache
from ..Cache.generate_key import create_cache_key

load_dotenv()

console = Console()
app = typer.Typer()

cache = SQLiteCache("cache.db")
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

    cache_key = create_cache_key(
        prompt=prompt,
        model_name=model_name,
        temperature=0
    )

    cached_response = cache.get(cache_key)

    if cached_response is not None:
        console.print(Panel(
            Markdown(cached_response),
            title = "cache hit",
            border_style="bold green")
        )
        return
    
    console.print("[yellow]Cache miss. Calling model...[/yellow]")

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

    response_text = result[0].content

    cache.set(cache_key, prompt, model_name, response=response_text)

    console.print(Panel(Markdown(response_text),
    border_style="bold green", title=f"Generated Response via {model_name}"))
    
@app.command()
def model():
    """print name of current model"""
    console.print(Panel(
        f"[bold cyan]current model:[/bold cyan] {model_name}",
        border_style="green",
        title="Current Model"
    ))
@app.command()
def cache_stats():
    '''show number of cached responses'''
    console.print(
        Panel(f"cached responses: {cache.count()}",
        border_style="green",
        title="Cache Count"        
        ))
@app.command()
def cache_clear():
    """
    Delete all cached responses.
    """

    cache.clear()
    console.print("[green]Cache cleared.[/green]")

if __name__ == "__main__":
    app()
