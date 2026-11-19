
from app.models import (
    ChatRequest,
    MessageCreate,
    SessionResponse
)


def test_chat_request():

    request = ChatRequest(
        message="Explain Python"
    )

    assert request.message == "Explain Python"

    print("Chat request validation successful!")


def test_message_create():

    message = MessageCreate(
        role="user",
        content="Hello ChatGPT",
        tokens=3
    )

    assert message.role == "user"
    assert message.tokens == 3

    print("Message validation successful!")


def test_session_response():

    session = SessionResponse(
        id="session_001",
        created_at="2026-11-19T10:00:00"
    )

    assert session.id == "session_001"

    print("Session response validation successful!")


if __name__ == "__main__":

    test_chat_request()
    test_message_create()
    test_session_response()

    print("All model tests passed!")
