import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class Review(BaseModel):
    player: list[str] = Field(
        description="list all the players mentioned in the review"
    )
    clubs: list[str] = Field(description="list all the clubs mentioned in the review")


load_dotenv()
model_name = "llama3.2:3b"
chat_model = ChatOpenAI(
    model_name=model_name, base_url=os.environ["Base_Url"], temperature=0.0
)

struct_model = chat_model.with_structured_output(Review)

prompt = """Lionel Messi plays for Inter Miami. His greatest strength is his close control, dribbling, and ability to create scoring opportunities with precise passes.

Kylian Mbappé plays for Real Madrid. His main strengths are his explosive speed, finishing, and ability to make dangerous runs behind defenders.

Kevin De Bruyne plays for Manchester City. He is known for his vision, accurate passing, powerful shots, and ability to create chances from midfield."""

response = struct_model.invoke(prompt)

print(response.model_dump_json())
