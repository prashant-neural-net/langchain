import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from rich.console import Console

load_dotenv()
model_name = "llama3.2:3b"
chat_model = ChatOpenAI(
    model_name=model_name, base_url=os.environ["Base_Url"], temperature=0.0
)

console = Console()

# schema
json_schema = {
    "title": "football players",
    "type": "object",
    "properties": {
        "clubs": {
            "type": "array",
            "items": {"type": "string"},
            "description": "list all the names of clubs mentioned in the text",
        },
        "players": {
            "type": "array",
            "items": {"type": "string"},
            "description": "list all the names of players mentioned in the text",
        },
    },
    "required": ["players", "clubs"],
}


structured_model = chat_model.with_structured_output(json_schema)
prompt = """Lionel Messi plays for Inter Miami. His greatest strength is his close control, dribbling, and ability to create scoring opportunities with precise passes Manchester United.

Kylian Mbappé plays for Real Madrid. His main strengths are his explosive speed, finishing, and ability to make dangerous runs behind defenders Aston Villa is a good club.

Kevin De Bruyne plays for Manchester City. He is known for his vision, accurate passing, powerful shots, and ability to create chances from midfield Samosa FC is a delicious club."""

result = structured_model.invoke(prompt)

print(result)

