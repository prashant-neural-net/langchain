import os

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI

load_dotenv()

model_name = "llama3.2:3b"

model = ChatOpenAI(model=model_name, base_url=os.environ["Base_Url"], temperature=0.0)
messages = []


@tool
def check_weather(location: str) -> str:
    """Provide weather of given location

    Args:
        location: It provides location where user wants the weather of
    return:
        Return the weather of that location
    """
    return f"Weather of {location} ->"


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers

    Args:
        a: float
        b: float
    return:
        a*b
    """
    return a * b


@tool
def add(c: int, d: int) -> int:
    """Add two numbers

    Args:
        c: int
        d: int
    return:
        c+d
    """
    return c + d


tools = {"multiply": multiply, "add": add, "check_weather": check_weather}

llm_with_tools = model.bind_tools([multiply, check_weather, add])

print(type(multiply))
query = input("prompt: ")


messages.append(HumanMessage(query))

response = llm_with_tools.invoke(messages)

print(response)
messages.append(response)

tool_name = response.tool_calls[0].get("name")


tool = tools.get(tool_name)

func_res = tool.invoke(response.tool_calls[0]["args"])

messages.append(
    ToolMessage(content=func_res, tool_call_id=response.tool_calls[0]["id"])
)

final_res = llm_with_tools.invoke(messages)

print(final_res.content)
