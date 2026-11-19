import csv
import os
import uuid
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

SESSIONS_FILE = os.path.join(DATA_DIR, "sessions.csv")
MESSAGES_FILE = os.path.join(DATA_DIR, "messages.csv")
USAGE_FILE = os.path.join(DATA_DIR, "usage.csv")

def create_session(session_data):

    os.makedirs(DATA_DIR, exist_ok=True)

    file_exists = os.path.exists(SESSIONS_FILE)

    with open(SESSIONS_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["id", "created_at"]
        )

        if not file_exists or os.path.getsize(SESSIONS_FILE) == 0:
            writer.writeheader()

        writer.writerow(session_data)

def get_session_messages(session_id):

    messages = []

    if not os.path.exists(MESSAGES_FILE):
        return messages

    with open(MESSAGES_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            if row["session_id"] == session_id:
                messages.append(row)

    return messages

def delete_session(session_id):

    if not os.path.exists(SESSIONS_FILE):
        return False

    sessions = []

    with open(SESSIONS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        sessions = list(reader)

    session_exists = any(
        row["id"] == session_id for row in sessions
    )

    if not session_exists:
        return False

    sessions = [
        row for row in sessions
        if row["id"] != session_id
    ]

    with open(SESSIONS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "created_at"]
        )
        writer.writeheader()
        writer.writerows(sessions)

    # Delete associated messages
    if os.path.exists(MESSAGES_FILE):

        with open(MESSAGES_FILE, "r", newline="", encoding="utf-8") as file:
            messages = list(csv.DictReader(file))

        messages = [
            row for row in messages
            if row["session_id"] != session_id
        ]

        with open(MESSAGES_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "id",
                    "session_id",
                    "role",
                    "content",
                    "tokens",
                    "created_at"
                ]
            )
            writer.writeheader()
            writer.writerows(messages)

    return True

def initialize_csv():

    os.makedirs(DATA_DIR, exist_ok=True)

    files = {
        SESSIONS_FILE: ["id", "created_at"],
        MESSAGES_FILE: [
            "id",
            "session_id",
            "role",
            "content",
            "tokens",
            "created_at"
        ],
        USAGE_FILE: [
            "id",
            "session_id",
            "api_key",
            "prompt_tokens",
            "completion_tokens",
            "total_tokens",
            "cost"
        ]
    }

    
def save_message(session_id, role, content):

    os.makedirs(DATA_DIR, exist_ok=True)

    file_exists = (
        os.path.exists(MESSAGES_FILE)
        and os.path.getsize(MESSAGES_FILE) > 0
    )

    message_data = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "role": role,
        "content": content,
        "tokens": 0,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    with open(MESSAGES_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "id",
                "session_id",
                "role",
                "content",
                "tokens",
                "created_at"
            ]
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(message_data)

        
def session_exists(session_id):

    if not os.path.exists(SESSIONS_FILE):
        return False

    with open(SESSIONS_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            if row["id"] == session_id:
                return True

    return False
