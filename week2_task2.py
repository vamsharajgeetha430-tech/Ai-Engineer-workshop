
import os
from dotenv import load_dotenv
from openai import OpenAI
import instructor
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

# Step 1: Define structured intent
class IntentResponse(BaseModel):
    intent: Literal[
        "explanation",
        "summarization",
        "code_generation"
    ] = Field(description="Detected user intent")


# Step 2: Connect Groq with Instructor
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

instructor_client = instructor.from_openai(client)


# Step 3: Detect intent
def detect_intent(question):

    result = instructor_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        response_model=IntentResponse,
        messages=[
            {
                "role": "system",
                "content": "Classify the user's request as explanation, summarization, or code_generation."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return result.intent


# Step 4: Generate response
def generate_response(question, intent):

    prompts = {
    "explanation": """
    Explain the following question in simple beginner-friendly language.
    Format your answer using Markdown.
    """,

    "summarization": """
    Summarize the following content clearly and briefly.
    Format your answer using Markdown.
    """,

    "code_generation": """
    Generate Python code for the following request.
    Explain the code briefly.
    Use Markdown and fenced Python code blocks.
    """
}

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": prompts[intent]
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# Step 5: User input
if __name__ == "__main__":

    question = input("Enter your question: ")

    intent = detect_intent(question)

    print("\nDetected Intent:", intent)

    answer = generate_response(question, intent)

    print("\nAI Response:\n")
    print(answer)
