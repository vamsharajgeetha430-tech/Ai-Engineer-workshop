import os
import uuid

from dotenv import load_dotenv
from groq import Groq

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


app = FastAPI(
    title="Week 3 Conversation Memory API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


# In-memory storage
chat_sessions = {}


class ChatRequest(BaseModel):
    session_id: str
    message: str


# Create a new chat
@app.post("/new-chat")
def new_chat():

    session_id = str(uuid.uuid4())

    chat_sessions[session_id] = []

    return {
        "session_id": session_id
    }


# Send a message
@app.post("/chat")
def chat(data: ChatRequest):

    if data.session_id not in chat_sessions:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    if not data.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    try:

        # Store user message
        chat_sessions[data.session_id].append(
            {
                "role": "user",
                "content": data.message
            }
        )

        messages = [
            {
                "role": "system",
                "content": "You are a helpful Python tutor. Keep answers clear and concise."
            }
        ] + chat_sessions[data.session_id]

        # Send history to Groq
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.3
        )

        answer = response.choices[0].message.content

        # Store AI response
        chat_sessions[data.session_id].append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        return {
            "session_id": data.session_id,
            "response": answer
        }

    except Exception:
        # Remove the user message if Groq failed
        chat_sessions[data.session_id].pop()

        raise HTTPException(
            status_code=503,
            detail="Unable to generate response"
        )