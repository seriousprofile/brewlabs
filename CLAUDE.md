# CLAUDE.md

## Project Overview
ColdBrews is a resume/portfolio project — a FastAPI/SQLite cold-brew batch tracker ("Brew Lab"), paired with an Observability tool that traces Claude Code hooks, skills, subagents, and MCP usage while building it.

## Repo Structure
- `ColdBrews/` — the FastAPI app (Brew Lab)
  - `main.py` — app entrypoint, creates tables on startup, `/health` endpoint
  - `database.py` — SQLite engine/session setup (`DATABASE_URL` env var to override)
  - `models.py` — SQLAlchemy `Brew` model + Pydantic schemas
  - `routers/` — these contain other .py files that are CRUD endpoints for brews
- `Observability/` — tool tracing Claude Code hooks, skills, subagents, and MCP activity during development

## Tech Stack & Conventions
- FastAPI + SQLAlchemy 2.0 + Pydantic v2
- Routers live in `routers/`, one file per resource
- `models.py` holds both the ORM model and its Pydantic schemas together
- `database.py` owns the engine/session — no direct engine access elsewhere
- Use type hints throughout; keep endpoint functions thin, push logic into helpers

## How to Run and Test
```bash
# activate venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# start the server
uvicorn main:app --reload

# check it's alive
curl http://localhost:8000/health

# run tests (once added)
pytest
```

## Current Build Plan / Roadmap (some steps might have already been done so please check before proceeding!)
1. Set up repo + CLAUDE.md
2. Build first version of Brew Lab
3. Add a hook logging tool events
4. Make the log readable
5. Add a Brew Lab feature using a subagent
6. Write a Skill for adding new batch fields
7. Add a hook enforcing required fields before marking a batch done
8. Add a subagent suggesting the next experiment
9. Expose the log via an MCP server
10. Polish with a README

## Constraints and Non-Goals
- Don't restructure existing endpoints without asking
- Keep Brew Lab and Observability decoupled — Observability watches, it doesn't modify Brew Lab's logic
- Ask before adding new dependencies
