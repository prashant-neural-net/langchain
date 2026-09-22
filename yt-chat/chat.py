import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from youtube_transcript_api import YouTubeTranscriptApi

console = Console()
load_dotenv()
local_model_name = "llama3.2:3b"

chat_model = ChatOpenAI(
    model=local_model_name, base_url=os.environ["Base_Url"], temperature=0.0
)

emb_model = HuggingFaceEndpointEmbeddings(
    repo_id="Qwen/Qwen3-Embedding-0.6B", provider="auto"
)

prompt = PromptTemplate(
    template="""If you cant find the answer from the text reply that the text does not mention the query otherwise answer th question in short form -> question: {user_input} from this: {context}""",
    input_variables=["user_input", "context"],
)

api = YouTubeTranscriptApi()
parser = StrOutputParser()

transcript_list = api.fetch(video_id="kYfNvmF0Bqw", languages=["en"])

transcript = "".join(chunk.text for chunk in transcript_list)

chain = prompt | chat_model | parser

response = ""
context = []
context.append(SystemMessage(content=transcript))
while True:
    user_input = console.input("query: ")
    if user_input in ["/exit", "/quit"]:
        break
    context.append(HumanMessage(content=user_input))
    with Live(
        Panel(
            Markdown("Generating......"),
            border_style="bold green",
            title=f"Generated Response via {local_model_name}",
        ),
        console=console,
        refresh_per_second=10,
    ) as live:
        for chunk in chain.stream({"user_input": user_input, "context": context}):
            response += chunk

            live.update(
                Panel(
                    Markdown(response),
                    border_style="bold blue",
                    title=f"Generated Response via {local_model_name}",
                ),
            )
        context.append(AIMessage(content=response))
