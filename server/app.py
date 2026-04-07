import sys
import os
import uvicorn
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from environment import ContentGuardEnv
from tasks import list_tasks

app = FastAPI(title="ContentGuard", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

env = ContentGuardEnv()
last_grade = {}


@app.get("/health")
def health():
    return {"status": "ok", "environment": "ContentGuard", "version": "1.0.0"}


@app.get("/")
def root():
    return {"name": "ContentGuard", "description": "OpenEnv environment for AI content moderation", "tasks": 3, "endpoints": ["/reset","/step","/state","/tasks","/grader","/baseline","/health"], "spec": "openenv-v1"}


@app.post("/reset")
async def reset(request: Request):
    global last_grade
    last_grade = {}
    task_id = 1
    try:
        body = await request.json()
        if isinstance(body, dict):
            task_id = int(body.get("task_id", 1))
    except Exception:
        task_id = 1
    try:
        obs = env.reset(task_id=task_id)
        return {"observation": obs.model_dump(), "message": f"Episode started. Task {task_id}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/step")
async def step(request: Request):
    global last_grade
    try:
        body = await request.json()
        action = {"category": body.get("category","safe"), "severity": body.get("severity","none"), "justification": body.get("justification","")}
    except Exception:
        action = {"category": "safe", "severity": "none", "justification": ""}
    try:
        result = env.step(action)
        if result.done and result.info.get("grade_details"):
            last_grade = result.info["grade_details"]
        return {"observation": result.observation.model_dump() if result.observation else None, "reward": result.reward, "done": result.done, "info": result.info}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state")
def state():
    return env.state().model_dump()


@app.get("/tasks")
def tasks():
    return {"tasks": list_tasks()}


@app.get("/grader")
def grader():
    if not last_grade:
        return {"score": 0.0, "message": "No completed episode yet."}
    return last_grade


@app.post("/baseline")
async def baseline_post(request: Request):
    from inference import run_inference
    return {"baseline_scores": run_inference(), "method": "keyword_matching_baseline"}


@app.get("/baseline")
def baseline_get():
    from inference import run_inference
    return {"baseline_scores": run_inference(), "method": "keyword_matching_baseline"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
