
import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Send question to LLM
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful Python tutor."
        },
        {
            "role": "user",
            "content": "What is FastAPI? Explain in 3 lines."
        }
    ],
    temperature=0.3
)

# Print AI response
print(response.choices[0].message.content)
