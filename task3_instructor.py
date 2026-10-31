import os

from dotenv import load_dotenv
from openai import OpenAI
import instructor
from pydantic import BaseModel, Field


load_dotenv()


class UserProfile(BaseModel):
    name: str = Field(description="User's name")
    age: int = Field(description="User's age")
    email: str = Field(description="User's email")
    pan: str = Field(description="User's PAN number")


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

client = instructor.from_openai(client)


user = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    response_model=UserProfile,
    messages=[
        {
            "role": "user",
            "content": """
            Create a user profile for:
            Name: Geetha
            Age: 22
            Email: geetha@example.com
            PAN: ABCDE1234F
            """
        }
    ]
)


print(user)
print(type(user))