import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_openai import ChatOpenAI

load_dotenv()


def word_count(text):
    return len(text.split())


model = ChatOpenAI(
    model="llama3.2:3b", base_url=os.environ["Base_Url"], temperature=0.0
)
passthrough = RunnablePassthrough()
parser = StrOutputParser()

prompt1 = PromptTemplate(
    template="""give me a joke on topic: {topic}""", input_variables=["topic"]
)

prompt2 = PromptTemplate(
    template="""explain this joke {text}""", input_variables=["text"]
)

joke_gen_chain = prompt1 | model | parser

parallel_chain = RunnableParallel(
    {"joke": RunnablePassthrough(), "word_count": RunnableLambda(word_count)}
)

final_chain = joke_gen_chain | parallel_chain

response = final_chain.invoke({"topic": "samosa"})

print(response)
