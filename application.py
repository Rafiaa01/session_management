from config import MODEL, client
from fastapi import FastAPI, HTTPException
from openai import OpenAIError
from pydantic import BaseModel
from session_manager import (
    get_or_create_session,
    load_sessions,
    save_session_history,
)
from systemprompt import SYSTEM_PROMPT

application = FastAPI(title="Session Management API")


class MessageRequest(BaseModel):
    message: str


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

    # Prepare previous conversation history
    messages = [
        {"role": item["role"], "content": item["content"]}
        for item in history
        if item["role"] in ("user", "assistant")
    ]

    # Add the new user message
    messages.append(
        {
            "role": "user",
            "content": request.message,
        }
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages,
            ],
        )

        reply = response.choices[0].message.content

        if reply is None:
            raise HTTPException(
                status_code=502,
                detail="The AI returned an empty response.",
            )

    except OpenAIError as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to get a response from the AI service.",
        ) from exc

    # Save the user message and assistant reply
    updated_history = messages + [{"role": "assistant", "content": reply}]

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
