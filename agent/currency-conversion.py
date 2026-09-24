import json
import os
from typing import Annotated

import requests
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.tools import InjectedToolArg, tool
from langchain_openai import ChatOpenAI


@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> str:
    """This function fetches the currency factor between a base currency and a target currency"""

    url = f"https:/v6.exchangerate-api.com/v6/c754eab14ffab33112e380ca/pair/{base_currency}/{target_currency}"

    response = requests.get(url)

    return response.json()


@tool
def convert(
    base_currency_value: int, conversion_rate: Annotated[float, InjectedToolArg]
) -> float:
    """Given a currency conversion rate this function calculates the target currency value from a given base currency value"""

    return base_currency_value * conversion_rate


load_dotenv()

model_name = "llama3.2:3b"

Chatmodel = ChatOpenAI(
    model=model_name, base_url=os.environ["Base_Url"], temperature=0.0
)

llm_with_tools = Chatmodel.bind_tools([get_conversion_factor, convert])
messages = [
    HumanMessage(
        "What is the conversion factor between USD and INR, and based on that can you convert 10 usd to inr"
    )
]

ai_message = llm_with_tools.invoke(messages)


for tool_call in ai_message.tool_calls:
    # execute the first tool to get the conversion rate
    if tool_call["name"] == "get_conversion_factor":
        tool_message1 = get_conversion_factor.invoke(tool_call)

        # fetch this conversion rate convert
        conversion_rate = json.loads(tool_message1.content)["conversion_rate"]

        messages.append(tool_message1)
    if tool_call["name"] == "convert":
        tool_call["args"]["conversion_rate"] = conversion_rate
        tool_message2 = convert.invoke(tool_call)
        messages.append(tool_message2)
