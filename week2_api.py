
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from week2_task2 import detect_intent, generate_response

app = FastAPI(title="Week 2 AI Response Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1)


@app.post("/generate")
def generate_answer(data: QuestionRequest):

    try:
        intent = detect_intent(data.question)

        answer = generate_response(data.question, intent)

        return {
            "intent": intent,
            "response": answer
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to generate response. Please try again."
        )
