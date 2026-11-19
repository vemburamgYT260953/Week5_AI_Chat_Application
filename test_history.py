from app.history import load_chat_history

session_id = input("Enter Session ID: ")

history = load_chat_history(session_id)

print("\nChat History:")

for message in history:
    print(message["role"], ":", message["content"])