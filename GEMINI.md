# Gemini Context: ApplyMate (Ply)

ApplyMate (internally referred to as `ply`) is an AI-powered job matching assistant designed to reduce application fatigue. It analyzes resumes against job descriptions (JD) to generate fit scores and detailed analysis.

## Project Overview

This project is a monorepo containing two parallel implementations of the backend logic:
1.  **Frontend & Nuxt Backend:** A Vue 3/Nuxt.js application with its own server-side (Nitro) logic in TypeScript.
2.  **FastAPI Backend:** A specialized Python 3.11 service with a more comprehensive data persistence layer (SQLModel, PostgreSQL).

### Core Features
- **Resume Ingestion:** Supports local PDF/DOC/DOCX uploads and public URLs.
- **JD Extraction:** Uses AI browsing agents (Stagehand/Playwright/Browser-use) to extract job details from links.
- **AI Matching:** Uses Google Gemini to score candidates based on skills, experience, and fit.
- **Async Workflow:** Long-running AI tasks are processed asynchronously via QStash webhooks.

---

## Project Structure

### 1. Root & `server/` (Nuxt Application)
- **Framework:** Nuxt 3 (Vue 3, TypeScript, Tailwind CSS).
- **`components/`**: UI for file uploads, link inputs, and interactive result displays.
- **`server/api/v1/`**: Nitro server routes.
  - `index.post.ts`: Handles initial ingestion and queues the task.
  - `consumer.post.ts`: The QStash webhook that executes the AI analysis in TypeScript.
- **`shared/`**: Core logic shared by the Nuxt server and client.
  - `shared/ai/jd/`: TypeScript implementation of JD extraction and scoring.
  - `shared/integrations/`: Clients for Redis, QStash, and LLMs.

### 2. `api/` (FastAPI Service)
- **Framework:** FastAPI (Python 3.11, SQLModel, PostgreSQL).
- **`api/app/modules/jdmatch/`**: The Python implementation of the matching logic.
  - `service.py`: Main business logic and task orchestration.
  - `agents/`: Python-based AI agents using `google-genai` and `browser-use-sdk`.
- **`api/migrations/`**: Alembic database migrations for PostgreSQL.
- **`api/dev.sh`**: Development script that starts the FastAPI server and an ngrok tunnel for webhooks.

---

## Infrastructure & Integrations

- **Database:** PostgreSQL (via SQLModel in the Python API).
- **Caching/State:** Redis (used for tracking task status and transient results).
- **Async Tasks:** Upstash QStash for reliable asynchronous execution of AI agents.
- **File Storage:** Local filesystem (`/public/uploads`) for the Nuxt backend; Supabase Storage for the Python API.
- **Document Processing:** Gotenberg (Docker service) for PDF/Doc manipulation.
- **Browser Automation:** `browser-use-sdk` and `stagehand` for scraping JDs.

---

## Building and Running

### Prerequisites
- Docker & Docker Compose
- Node.js (v18+) & Yarn
- Python 3.11+

### Startup Sequence
1. **Infrastructure:**
   ```bash
   docker-compose -p apply-mate up -d
   ```
2. **FastAPI Backend (Optional/Development):**
   ```bash
   cd api
   ./dev.sh
   ```
3. **Nuxt Frontend & Server:**
   ```bash
   yarn dev
   ```

## Development Conventions

- **Monorepo Strategy:** While logic is currently duplicated in TS (shared) and Python (api), the Python API is intended for the more persistent data model.
- **AI Prompts:** Located in `shared/ai/jd/` (TS) and `api/app/modules/jdmatch/agents/` (Python).
- **Logging:** Always use the custom loggers (`Loguru` in Python, custom `Logging` utility in TS).
- **Testing:** Python tests in `api/tests/` (Pytest); Frontend tests in `tests/` (Nuxt Test Utils).
