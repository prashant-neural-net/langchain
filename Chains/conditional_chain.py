import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.output_parsers import (
    PydanticOutputParser,
    StrOutputParser,
)
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

load_dotenv()


# Local LLM
local_llm = ChatOpenAI(
    model_name="llama3.2:3b",
    temperature=0.0,
    base_url=os.environ["Base_Url"],
)

model = local_llm


# Pydantic schema
class Feedback(BaseModel):
    sentiment: Literal["positive", "negative"]


# Output parsers
parser1 = StrOutputParser()

parser2 = PydanticOutputParser(pydantic_object=Feedback)


# Classifier prompt
prompt_1 = PromptTemplate(
    template="""
You are a sentiment classifier.

Read the feedback below.

Return exactly one word:
positive
or
negative

Do not return JSON.
Do not explain.

Feedback:
{feedback}
""",
    input_variables=["feedback"],
    format_instructions={"format_instruction": parser2.get_format_instructions()},
)

# Positive response prompt
prompt_2 = PromptTemplate(
    template="""
Write an appropriate response to this positive feedback:

{feedback}
""",
    input_variables=["feedback"],
)


# Negative response prompt
prompt_3 = PromptTemplate(
    template="""
Write an appropriate response to this negative feedback:

{feedback}
""",
    input_variables=["feedback"],
)


# Classification chain
classifier_chain = prompt_1 | model | parser2


# Conditional branch
branch_chain = RunnableBranch(
    (
        lambda x: x.sentiment == "positive",
        prompt_2 | model | parser1,
    ),
    (
        lambda x: x.sentiment == "negative",
        prompt_3 | model | parser1,
    ),
    RunnableLambda(lambda x: "Could not find the sentiment"),
)


# Complete chain
chain = classifier_chain | branch_chain


# Invoke
response = chain.invoke({"feedback": "I do not like the phone at all"})

print(response)


# Graph
chain.get_graph().print_ascii()