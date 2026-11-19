from app.llm import generate_response

chat_history = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant."
    },
    {
        "role": "user",
        "content": "Explain Python in simple words."
    }
]

result = generate_response(chat_history)

print("\nAI Response:")
print(result["content"])

print("\nToken Usage:")
print("Prompt Tokens:", result["prompt_tokens"])
print("Completion Tokens:", result["completion_tokens"])
print("Total Tokens:", result["total_tokens"])