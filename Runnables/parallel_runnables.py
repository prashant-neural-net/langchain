import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

load_dotenv()
console = Console()

model = ChatOpenAI(
    model="llama3.2:3b",
    base_url=os.environ["Base_Url"],
    temperature=0.0,
)

parser = StrOutputParser()

template_1 = PromptTemplate(
    template="write 5 jokes on topic {topic1}", input_variables=["topic1"]
)
template_2 = PromptTemplate(
    template="write 5 jokes on topic {topic2}", input_variables=["topic2"]
)

template_3 = PromptTemplate(
    template="choose top 2 jokes given jokes each should be from different topics: {jokes_1}, {jokes_2}",
    input_variables=["jokes_1", "jokes_2"],
)

parallel_chain = RunnableParallel(
    {"jokes_1": template_1 | model | parser, "jokes_2": template_2 | model | parser}
)

merger_chain = template_3 | model | parser

chain = parallel_chain | merger_chain
response = chain.invoke({"topic1": "samosa", "topic2": "idli"})

console.print(Panel(Markdown(response)))

