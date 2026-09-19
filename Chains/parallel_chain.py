from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4.1-Flash",
    task="text-generation",
    provider="auto",
    temperature=0,
)
model = ChatHuggingFace(llm=llm)

prompt_1 = PromptTemplate(
    template="write a 20 line essay on {topic} \n", input_variables=["topic"]
)

prompt_2 = PromptTemplate(
    template="give me 5 questions from: {topic} \n", input_variables=["topic"]
)
prompt_3 = PromptTemplate(
    template="Merge the provided text and question in a single document \n notes -> {notes} and quiz -> {quiz}",
    input_variables=["notes", "quiz"],
)


parser = StrOutputParser()

parallel_chain = RunnableParallel(
    {"notes": prompt_1 | model | parser, "quiz": prompt_2 | model | parser}
)

merge_chain = prompt_3 | model | parser

chain = parallel_chain | merge_chain

result = chain.invoke({"topic": "football"})

print(result)

chain.get_graph().print_ascii()
