import uuid

# In-memory storage
chat_sessions = {}


def create_session():
    session_id = str(uuid.uuid4())

    # Create an empty chat history for this session
    chat_sessions[session_id] = []

    return session_id


def add_message(session_id, role, content):

    message = {
        "role": role,
        "content": content
    }

    chat_sessions[session_id].append(message)


# Create a session
session_id = create_session()

# Add conversation messages
add_message(
    session_id,
    "user",
    "What is FastAPI?"
)

add_message(
    session_id,
    "assistant",
    "FastAPI is a modern Python framework for building APIs."
)

print("Session ID:", session_id)
print("Chat History:", chat_sessions[session_id])