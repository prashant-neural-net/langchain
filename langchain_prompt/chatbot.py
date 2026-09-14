import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from typing import TypedDict, Annotated

load_dotenv()

model_name = "llama3.2:3b"


chat_model = ChatOpenAI(
    model=model_name, base_url=os.environ["Base_Url"], temperature=0.0
)



console = Console()

chatbot_template = ChatPromptTemplate(
    [
        ("system", "You are a good friend"),
        MessagesPlaceholder(variable_name="chatbot_history"),
        ("human", "{query}"),
    ]
)
context = []

with open("chatbot_history.txt") as f:
    context.extend(f.readlines())


while True:
    user_input = input("you: ")

    prompt = chatbot_template.invoke({"chatbot_history": context, "query": user_input})

    context.append(HumanMessage(content=user_input))

    if user_input in ["/exit", "/quit", "/end"]:
        break

    result = chat_model.invoke(context)

    console.print(
        Panel(
            Markdown(result.content),
            title="AI",
            style="bold cyan",
            highlight=True,
        )
    )
    context.append(AIMessage(content=result.content))

    new_lines = [user_input, result.content]
    with open("chatbot_history.txt", "a") as f:
        f.writelines(f"HumanMessage(content='{new_lines[0]}')\n")
        f.writelines(f"AIMessage(content='{new_lines[1]}')\n")

