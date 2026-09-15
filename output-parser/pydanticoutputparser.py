import os

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()

model = ChatOpenAI(
    model="llama3.2:3b",
    base_url=os.environ["Base_Url"],
    temperature=0.0,
)


class Schema(BaseModel):
    fact_1: str = Field(description="First fact about the given topic")

    fact_2: str = Field(description="Second fact about given topic")

    fact_3: str = Field(description="Third fact about given topic")


parser = PydanticOutputParser(pydantic_object=Schema)

template = PromptTemplate(
    template="Give 3 facts about {topic}\n{format_instructions}",
    input_variables=["topic"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

prompt = template.invoke({"topic": "india"})

result = model.invoke(prompt)

final_result = parser.parse(result.content)

print(final_result)
