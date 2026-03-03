# Gemini Context: ApplyMate (Ply)

ApplyMate (internally referred to as `ply`) is an AI-powered job matching assistant designed to reduce application fatigue. It analyzes resumes against job descriptions (JD) to generate fit scores and detailed analysis.

## Project Overview

This project is a monorepo containing:
1.  **Frontend (`client/`):** A Vue 3 + TypeScript + Vite application.
2.  **Backend (`api/`):** A specialized Python 3.11 service (FastAPI, SQLModel, PostgreSQL).

### Core Features
- **Resume Ingestion:** Supports local PDF/DOC/DOCX uploads and public URLs.
- **JD Extraction:** Uses AI browsing agents (Browser-use SDK) to extract job details from links.
- **AI Matching:** Uses Google Gemini to score candidates based on skills, experience, and fit.
- **Async Workflow:** Long-running AI tasks are processed asynchronously via QStash webhooks.

---

## Project Structure

### 1. `client/` (Frontend)
- **Framework:** Vue 3 (Composition API), Vite, TypeScript, Tailwind CSS.
- **Testing:** Vitest with `jsdom` and `@vue/test-utils`.
- **Linting/Formatting:** `oxlint` and `oxfmt` for high-performance code quality.
- **Hooks:** Husky hooks for pre-commit linting and commit message validation.

### 2. `api/` (FastAPI Service)
- **Framework:** FastAPI (Python 3.11, SQLModel, PostgreSQL).
- **Domain Logic:** `api/app/modules/jdmatch/` handles the matching workflow.
- **AI Agents:** Python-based agents using `google-genai` and `browser-use-sdk`.
- **Migrations:** Alembic database migrations for PostgreSQL.
- **Development:** `api/dev.sh` starts the FastAPI server and an ngrok tunnel for webhooks.

---

## Infrastructure & Integrations

- **Database:** PostgreSQL (via SQLModel in the Python API).
- **Caching/State:** Redis (used for tracking task status and transient results).
- **Async Tasks:** Upstash QStash for reliable asynchronous execution of AI agents.
- **File Storage:** Supabase Storage for resume persistence.
- **Browser Automation:** `browser-use-sdk` for scraping JDs.

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
2. **Backend (FastAPI):**
   ```bash
   cd api
   ./dev.sh
   ```
3. **Frontend (Vite):**
   ```bash
   cd client
   yarn dev
   ```

## Development Conventions

- **Monorepo Strategy:** The project is managed from the root, but the `client` and `api` are independent services.
- **Linting:** Automated via Husky and `pre-commit`.
- **Commits:** Conventional Commits enforced via `commitlint`.
