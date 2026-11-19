from app.storage import (
    initialize_csv,
    create_session,
    save_message,
    get_session,
    get_session_messages,
    delete_session
)


def test_csv_storage():

    initialize_csv()

    # Create session
    session = create_session("test_api_key")

    session_id = session["id"]

    print("Session created:", session_id)

    # Store user message
    save_message(
        session_id,
        "user",
        "Hello ChatGPT",
        3
    )

    # Store assistant message
    save_message(
        session_id,
        "assistant",
        "Hello! How can I help you?",
        8
    )

    # Retrieve session
    result = get_session(session_id)

    assert result is not None

    # Retrieve messages
    messages = get_session_messages(session_id)

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"

    print("Messages retrieved:", len(messages))

    # Delete session
    deleted = delete_session(session_id)

    assert deleted is True

    assert get_session(session_id) is None

    print("Session deleted successfully!")


if __name__ == "__main__":
    test_csv_storage()
