# Session Management API

A FastAPI application integrated with OpenAI that maintains conversation history for individual sessions, allowing the assistant to answer follow-up questions using previous messages.

## Features
- Create and manage chat sessions.
- Generate AI responses using OpenAI.
- Store user and assistant messages in JSON.
- Retrieve individual or all sessions.
- Maintain conversation context across requests.

## Tech Stack
- Python
- FastAPI
- OpenAI API
- Pydantic
- JSON file storage

## Setup

1. Install dependencies:

   ```bash
   pip install fastapi uvicorn openai python-dotenv
   ```

2. Create a `.env` file:

   ```env
   OPENAI_API_KEY=your_api_key
   OPENAI_MODEL=gpt-4o-mini
   ```

3. Run the application:

   ```bash
   uvicorn main:application --reload
   ```

4. Open the API documentation at `http://127.0.0.1:8000/docs`.

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/sessions` | Create or retrieve a session |
| POST | `/sessions/{session_id}/messages` | Send a message and receive an AI reply |
| GET | `/sessions/{session_id}` | Retrieve session history |
| GET | `/sessions` | Retrieve all sessions |

