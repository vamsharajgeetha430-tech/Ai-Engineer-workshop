import os
import uuid

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# In-memory chat storage
chat_sessions = {}


def create_session():

    session_id = str(uuid.uuid4())

    chat_sessions[session_id] = []

    return session_id


def generate_response(session_id, question):

    # Store user's new message
    chat_sessions[session_id].append(
        {
            "role": "user",
            "content": question
        }
    )

    # System instruction + previous conversation
    messages = [
        {
            "role": "system",
            "content": "You are a helpful Python tutor."
        }
    ] + chat_sessions[session_id]

    # Send entire conversation to Groq
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.3
    )

    answer = response.choices[0].message.content

    # Store AI response
    chat_sessions[session_id].append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    return answer


# Create one conversation
session_id = create_session()

print("Session ID:", session_id)


# First question
question1 = "What is FastAPI?"

answer1 = generate_response(
    session_id,
    question1
)

print("\nUser:", question1)
print("AI:", answer1)


# Follow-up question
question2 = "What are its main advantages?"

answer2 = generate_response(
    session_id,
    question2
)

print("\nUser:", question2)
print("AI:", answer2)