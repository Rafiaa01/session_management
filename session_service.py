
from config import MODEL, client
from fastapi import HTTPException
from openai import OpenAIError
from session_manager import (
    get_or_create_session,
    load_sessions,
    save_session_history,
    save_sessions,
)
from systemprompt import SYSTEM_PROMPT


def create_session(session_id: str | None = None):
    try:
        session_id, history = get_or_create_session(session_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {"session_id": session_id, "history": history}


def send_message(session_id: str, message: str):
    try:
        actual_id, history = get_or_create_session(session_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    messages = [
        {"role": item["role"], "content": item["content"]}
        for item in history
        if item["role"] in ("user", "assistant")
    ]
    messages.append({"role": "user", "content": message})

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

    updated_history = messages + [
        {"role": "assistant", "content": reply}
    ]
    save_session_history(actual_id, updated_history)

    return {
        "session_id": actual_id,
        "reply": reply,
        "history": updated_history,
    }


def get_session(session_id: str):
    try:
        actual_id, history = get_or_create_session(session_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {"session_id": actual_id, "history": history}


def get_all_sessions():
    sessions = load_sessions()
    return {"total_sessions": len(sessions), "sessions": sessions}


def delete_session(session_id: str):
    sessions = load_sessions()

    if session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    del sessions[session_id]
    save_sessions(sessions)

    return {
        "message": "Session deleted successfully.",
        "session_id": session_id,
    }
