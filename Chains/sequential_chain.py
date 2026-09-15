from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4.1-Flash",
    task="text-generation",
    provider="auto",
    temperature=0,
)
model = ChatHuggingFace(llm=llm)

prompt_1 = PromptTemplate(
    template="write a 20 line essay on {topic} \n",
    input_variables=['topic']
)

prompt_2 = PromptTemplate(
    template="summarize this essay in 5 line: {text} \n",
    input_variables=['text']
)

parser = StrOutputParser()

chain = prompt_1 | model | parser |  prompt_2 | model | parser

result = chain.invoke({'topic':'football'})

print(result)

chain.get_graph().print_ascii()


