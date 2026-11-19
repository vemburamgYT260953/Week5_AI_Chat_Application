import os
from importlib import import_module

try:
    load_dotenv = import_module("dotenv").load_dotenv
except ModuleNotFoundError as exc:
    if exc.name != "dotenv":
        raise
    raise RuntimeError("The python-dotenv package is missing. Install it with: pip install python-dotenv") from exc

try:
    OpenAI = import_module("openai").OpenAI
except ModuleNotFoundError as exc:
    if exc.name != "openai":
        raise
    raise RuntimeError("The OpenAI package is missing. Install it with: pip install openai") from exc

load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing in .env")

client = OpenAI(api_key=api_key)


def generate_response(chat_history):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_history,
        temperature=0.7
    )

    assistant_message = response.choices[0].message.content

    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens

    return {
        "content": assistant_message,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": response.usage.total_tokens
    }
