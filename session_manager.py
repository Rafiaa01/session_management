import json
import uuid
from pathlib import Path

SESSION_FILE = Path(__file__).resolve().parent / "sessions.json"


def load_sessions() -> dict:
    """Load all sessions from the JSON file."""
    if not SESSION_FILE.exists():
        return {}

    try:
        with SESSION_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


def save_sessions(sessions: dict) -> None:
    """Save all sessions to the JSON file."""
    with SESSION_FILE.open("w", encoding="utf-8") as file:
        json.dump(sessions, file, indent=4, ensure_ascii=False)


def get_or_create_session(
    session_id: str | None = None,
) -> tuple[str, list[dict]]:
    """Retrieve an existing session or create a new one."""
    sessions = load_sessions()

    if session_id and session_id in sessions:
        return session_id, sessions[session_id]

    if session_id:
        raise ValueError("Session ID does not exist.")

    new_session_id = str(uuid.uuid4())
    sessions[new_session_id] = []

    save_sessions(sessions)

    return new_session_id, sessions[new_session_id]


def save_session_history(
    session_id: str,
    history: list[dict],
) -> None:
    """Save updated conversation history for one session."""
    sessions = load_sessions()

    if session_id not in sessions:
        raise ValueError("Session ID does not exist.")

    sessions[session_id] = history
    save_sessions(sessions)
