"""
app.py — FastAPI server for ContentGuard OpenEnv environment.
Exposes all required OpenEnv endpoints:
  POST /reset      — start a new episode
  POST /step       — take an action
  GET  /state      — get current environment state
  GET  /tasks      — list all tasks and action schemas
  GET  /grader     — get grader score after episode ends
  POST /baseline   — run baseline inference and return scores
  GET  /health     — health check (returns 200)
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from environment import ContentGuardEnv
from graders import run_grader
from tasks import list_tasks

app = FastAPI(
    title="ContentGuard",
    description="OpenEnv environment for AI content moderation. Simulates real-world social media moderation workflows.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment instance
env = ContentGuardEnv()
last_grade = {}  # Store last completed episode's grade


# ── Request / Response Models ────────────────────────────────────

class ResetRequest(BaseModel):
    task_id: int = 1

class StepRequest(BaseModel):
    category: str
    severity: Optional[str] = "none"
    justification: Optional[str] = ""


# ── Endpoints ────────────────────────────────────────────────────

@app.get("/health")
def health():
    """Health check — must return 200 for HF Spaces deployment check."""
    return {"status": "ok", "environment": "ContentGuard", "version": "1.0.0"}


@app.get("/")
def root():
    """Root endpoint with environment info."""
    return {
        "name": "ContentGuard",
        "description": "OpenEnv environment for AI content moderation",
        "tasks": 3,
        "endpoints": ["/reset", "/step", "/state", "/tasks", "/grader", "/baseline", "/health"],
        "spec": "openenv-v1",
    }


@app.post("/reset")
def reset(request: ResetRequest):
    """
    Reset the environment and start a new episode.
    Returns the first observation (first post to moderate).
    """
    global last_grade
    last_grade = {}
    try:
        observation = env.reset(task_id=request.task_id)
        return {
            "observation": observation.model_dump(),
            "message": f"Episode started. Task {request.task_id}: {env._task['name']}",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/step")
def step(request: StepRequest):
    """
    Submit a classification for the current post.
    Returns the next observation, reward, done flag, and info.
    """
    global last_grade
    try:
        action = {
            "category": request.category,
            "severity": request.severity,
            "justification": request.justification,
        }
        result = env.step(action)

        if result.done and result.info.get("grade_details"):
            last_grade = result.info["grade_details"]

        return {
            "observation": result.observation.model_dump() if result.observation else None,
            "reward": result.reward,
            "done": result.done,
            "info": result.info,
        }
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state")
def state():
    """Return the current state of the environment."""
    return env.state().model_dump()


@app.get("/tasks")
def tasks():
    """
    Return all available tasks with their action schemas.
    Required by OpenEnv spec.
    """
    return {"tasks": list_tasks()}


@app.get("/grader")
def grader():
    """
    Return the grader score from the last completed episode.
    Returns error if no episode has been completed yet.
    """
    if not last_grade:
        raise HTTPException(
            status_code=400,
            detail="No completed episode found. Run a full episode (reset → step until done=True) first."
        )
    return last_grade


@app.post("/baseline")
def baseline():
    """
    Run the baseline inference script and return scores for all 3 tasks.
    Uses a simple rule-based baseline (keyword matching).
    This produces reproducible scores without requiring an API key.
    """
    from baseline import run_baseline
    scores = run_baseline()
    return {
        "baseline_scores": scores,
        "method": "keyword_matching_baseline",
        "note": "Reproducible rule-based baseline. LLM baseline requires OPENAI_API_KEY.",
    }
