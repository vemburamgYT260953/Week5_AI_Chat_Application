
from app.storage import (
    create_session,
    save_message,
    get_session_messages,
    delete_session
)


def test_get_messages():

    # Create session
    session = create_session("test_api_key")
    session_id = session["id"]

    # Add user message
    save_message(
        session_id,
        "user",
        "Hello ChatGPT",
        3
    )

    # Add assistant response
    save_message(
        session_id,
        "assistant",
        "Hello! How can I help you?",
        8
    )

    # Retrieve messages
    messages = get_session_messages(session_id)

    # Validate
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"

    print("Session ID:", session_id)
    print("Total messages:", len(messages))

    for message in messages:
        print(message["role"], ":", message["content"])

    # Cleanup
    delete_session(session_id)

    print("GET messages test completed successfully!")


if __name__ == "__main__":
    test_get_messages()
