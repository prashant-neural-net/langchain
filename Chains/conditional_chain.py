from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableBranch
from pydantic import BaseModel, Field
from typing import Literal
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4.1-Flash",
    task="text-generation",
    provider="auto",
    temperature=0,
)
model = ChatHuggingFace(llm=llm)
class Feedback(BaseModel):
    sentiment: Literal['positive', 'negative'] = Field(description='Give the sentiment of the feedback')

parser = PydanticOutputParser(pydantic_object=Feedback)

prompt_1 = PromptTemplate(
    template= "classify the given feedback in positve or negative sentiment /n {feedback}",
    input_variables=['feedback'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)

classifier_chain = prompt_1 | model | parser

result = classifier_chain.invoke({"feedback": "this phone is shit, fuck redmi"})

print(result)