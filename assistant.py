
from assistant import generate_reply
from fastapi import FastAPI
from schemas import MessageRequest
from session_manager import (
    get_or_create_session,
    load_sessions,
    save_session_history,
)

application = FastAPI(title="Session Management API")


@application.post("/sessions")
def create_or_get_session(session_id: str | None = None):
    session_id, history = get_or_create_session(session_id)

    return {
        "session_id": session_id,
        "history": history,
    }


@application.post("/sessions/{session_id}/messages")
def add_message(session_id: str, request: MessageRequest):
    actual_id, history = get_or_create_session(session_id)

    # Get an AI response using the previous conversation
    reply = generate_reply(request.message, history)

    # Save the user message and assistant reply
    updated_history = history + [
        {"role": "user", "content": request.message},
        {"role": "assistant", "content": reply},
    ]

    save_session_history(actual_id, updated_history)

    return {
        "session_id": actual_id,
        "reply": reply,
        "history": updated_history,
    }


@application.get("/sessions/{session_id}")
def get_session_history(session_id: str):
    _, history = get_or_create_session(session_id)

    return {
        "session_id": session_id,
        "history": history,
    }


@application.get("/sessions")
def get_all_sessions():
    sessions = load_sessions()

    return {
        "total_sessions": len(sessions),
        "sessions": sessions,
    }
