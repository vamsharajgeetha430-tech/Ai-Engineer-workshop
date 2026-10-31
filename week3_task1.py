
import uuid

# Generate a unique session ID
def create_session():

    session_id = str(uuid.uuid4())

    return session_id


# Create two separate chat sessions
session1 = create_session()
session2 = create_session()

print("Session 1:", session1)
print("Session 2:", session2)
