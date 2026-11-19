from app.storage import get_session_messages


def load_chat_history(session_id):

    messages = get_session_messages(session_id)

    chat_history = []

    for message in messages:

        chat_history.append({
            "role": message["role"],
            "content": message["content"]
        })

    return chat_history