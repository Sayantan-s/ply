# Gemini Context: Ply API

This document provides context for the `ply/api` project, a FastAPI-based backend for matching resumes with job descriptions (JD).

## Project Overview

**Ply API** is a service designed to analyze candidate fit for job descriptions. It handles resume uploads (PDF/Doc/Link), parses them, and matches them against Job Descriptions using vector analysis.

**Key Features:**
*   **Resume Ingestion:** Upload files or provide links.
*   **JD Analysis:** Detect and parse job descriptions.
*   **Matching Engine:** Vector-based matching (implied) to avoid duplication and rank candidates.
*   **Async Processing:** Uses QStash for handling long-running analysis tasks.

## Tech Stack

*   **Language:** Python 3.11+
*   **Framework:** FastAPI
*   **Database:** PostgreSQL (via SQLModel)
*   **Async Messaging:** Upstash QStash
*   **Utilities:**
    *   **Gotenberg:** PDF/Document processing
    *   **Redis:** Caching/Storage
    *   **Ngrok:** Exposing local server for QStash webhooks
    *   **Google GenAI SDK:** Interaction with Gemini models.
    *   **Stagehand:** Browser automation for data extraction.
*   **Package Manager:** `uv` (implied by `uv.lock`)

## Architecture

The project follows a **Modular Monolith** structure with a clear separation of concerns:

*   **`app/modules/`**: Contains domain-specific logic.
    *   *Example:* `jdmatch` module handles resume parsing and matching logic.
*   **`app/integrations/`**: Encapsulates external service interactions.
    *   *Example:* `db` (SQLModel setup), `upstash` (QStash client), `llm` (Gemini), `stagehand` (Browser Automation).
*   **`app/core/`**: Cross-cutting concerns like configuration and logging.
*   **`app/api/`**: API route definitions.

### Async Worker Pattern
Long-running tasks (like resume parsing/matching) are handled asynchronously:
1.  API receives a request.
2.  Service publishes a message to QStash (`qstash.message.publish_json`).
3.  QStash calls a "consumer" endpoint (e.g., `/jdmatch/consumer`) via HTTP (using the ngrok URL in dev).
4.  The consumer endpoint processes the task.

## Key Files & Directories

*   `app/main.py`: Application entry point and lifespan management (DB init).
*   `app/api/v1/`: API Route definitions.
*   `app/modules/jdmatch/`: Core domain logic for matching.
    *   `service.py`: Business logic, QStash publishing.
    *   `repo.py`: Data persistence/file handling.
    *   `agents/`: Specialized logic for AI tasks (e.g., JD extraction, analysis).
    *   `utils/`: Helper functions for file processing and downloads.
*   `dev.sh`: Development startup script (starts Uvicorn + Ngrok).
*   `compose.yml`: Docker services (Postgres, Redis, Gotenberg).

## Development Workflow

### Prerequisites
*   Python 3.11+
*   Docker & Docker Compose
*   `uv` (optional but recommended)

### Setup & Running

1.  **Start Infrastructure:**
    ```bash
    docker compose up -d
    ```
    This spins up Postgres (port 5432), Redis (6379), Gotenberg (3001), and management UIs.

2.  **Environment Setup:**
    Ensure `.env.local` exists. It is loaded automatically by `dev.sh`.

3.  **Run Application:**
    ```bash
    ./dev.sh
    ```
    *   Starts the FastAPI server (default port 7153).
    *   Starts `ngrok` to tunnel traffic to the local port (essential for QStash callbacks).
    *   **Note:** The `API_URL` setting likely needs to match the ngrok URL for QStash to work correctly in dev.

### Coding Conventions

*   **Database:** Use `SQLModel` for models and `app.integrations.db.database.get_session` for DB sessions.
*   **Dependency Injection:** Use `fastapi.Depends` for services like QStash clients (`qstash_dependency`).
*   **Logging:** Always use the custom logger:
    ```python
    from app.core.logging.logger import get_logger
    logger = get_logger("module_name")
    ```
*   **Configuration:** Access settings via `app.core.config.settings`.
*   **Testing:** Tests are located in `tests/`.

## Service Endpoints (Local)

*   **API:** `http://localhost:7153` (or ngrok URL)
*   **Gotenberg:** `http://localhost:3001`
*   **Redis Commander:** `http://localhost:8081`
*   **pgAdmin:** `http://localhost:5050`
