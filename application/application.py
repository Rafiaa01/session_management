
from application.session_service import (
    create_session,
    delete_session,
    get_all_sessions,
    get_session,
    send_message,
)
from fastapi import FastAPI
from pydantic import BaseModel

application = FastAPI(title="Session Management API")


class MessageRequest(BaseModel):
    message: str


@application.post("/sessions")
def create_or_get_session(session_id: str | None = None):
    return create_session(session_id)


@application.post("/sessions/{session_id}/messages")
def add_message(session_id: str, request: MessageRequest):
    return send_message(session_id, request.message)


@application.get("/sessions/{session_id}")
def get_session_history(session_id: str):
    return get_session(session_id)


@application.get("/sessions")
def list_sessions():
    return get_all_sessions()


@application.delete("/sessions/{session_id}")
def remove_session(session_id: str):
    return delete_session(session_id)
