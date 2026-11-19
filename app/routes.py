from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone
import uuid

from app.auth import verify_api_key
from app.storage import create_session
from app.storage import delete_session, get_session_messages
from pydantic import BaseModel
from app.llm import generate_response
from app.storage import save_message
from app.storage import save_message, session_exists
from app.llm import generate_response

router = APIRouter()
class ChatRequest(BaseModel):
    message: str


@router.post("/sessions")
def create_new_session(api_key: str = Depends(verify_api_key)):

    session_id = str(uuid.uuid4())

    session_data = {
        "id": session_id,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    create_session(session_data)

    return {
        "message": "Session created successfully",
        "session_id": session_id
    }

@router.get("/sessions/{session_id}/messages")
def get_messages(
    session_id: str,
    api_key: str = Depends(verify_api_key)
):

    messages = get_session_messages(session_id)

    return {
        "session_id": session_id,
        "messages": messages
    }

@router.delete("/sessions/{session_id}")
def delete_chat_session(
    session_id: str,
    api_key: str = Depends(verify_api_key)
):

    deleted = delete_session(session_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return {
        "message": "Session deleted successfully"
    }
@router.post("/sessions/{session_id}/chat")
def chat_with_ai(
    session_id: str,
    request: ChatRequest,
    api_key: str = Depends(verify_api_key)
):

    # Check whether session exists
    messages = get_session_messages(session_id)

    if messages is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )
    messages=get_session_messages(session_id)

    # Prepare chat history
    chat_history = []

    for msg in messages:
        chat_history.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Add user message
    user_message = {
        "role": "user",
        "content": request.message
    }

    chat_history.append(user_message)

    # Generate AI response
    assistant_response = generate_response(chat_history)

    # Save user message
    save_message(session_id, "user", request.message)

    # Save assistant response
    save_message(session_id, "assistant", assistant_response)

    return {
        "session_id": session_id,
        "user_message": request.message,
        "assistant_message": assistant_response
    }
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid

from app.auth import verify_api_key
from app.storage import (
    create_session,
    delete_session,
    get_session_messages,
    save_message,
    session_exists
)
from app.llm import generate_response

router = APIRouter()


# Request model
class ChatRequest(BaseModel):
    message: str


# Create session
@router.post("/sessions")
def create_new_session(
    api_key: str = Depends(verify_api_key)
):
    session_id = str(uuid.uuid4())

    session_data = {
        "id": session_id,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    create_session(session_data)

    return {
        "message": "Session created successfully",
        "session_id": session_id
    }


# Get session messages
@router.get("/sessions/{session_id}/messages")
def get_messages(
    session_id: str,
    api_key: str = Depends(verify_api_key)
):
    if not session_exists(session_id):
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    messages = get_session_messages(session_id)

    return {
        "session_id": session_id,
        "messages": messages
    }


# Delete session
@router.delete("/sessions/{session_id}")
def delete_chat_session(
    session_id: str,
    api_key: str = Depends(verify_api_key)
):
    deleted = delete_session(session_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return {
        "message": "Session deleted successfully"
    }


# Chat with AI
@router.post("/sessions/{session_id}/chat")
def chat_with_ai(
    session_id: str,
    request: ChatRequest,
    api_key: str = Depends(verify_api_key)
):

    # 1. Validate session
    if not session_exists(session_id):
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    # 2. Get previous messages
    messages = get_session_messages(session_id)

    # 3. Prepare chat history
    chat_history = []

    for msg in messages:
        chat_history.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # 4. Add new user message
    chat_history.append({
        "role": "user",
        "content": request.message
    })

    # 5. Generate AI response
    assistant_response = generate_response(chat_history)

    # 6. Save user message
    save_message(
        session_id,
        "user",
        request.message
    )

    # 7. Save assistant message
    save_message(
        session_id,
        "assistant",
        assistant_response
    )

    # 8. Return response
    return {
        "session_id": session_id,
        "user_message": request.message,
        "assistant_message": assistant_response
    }
