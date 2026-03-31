"""
environment.py — ContentGuard OpenEnv Environment.
Implements the full OpenEnv spec: step() / reset() / state()
with typed Pydantic models for Observation, Action, and Reward.
"""

from typing import Optional, Any
from pydantic import BaseModel, Field
from tasks import get_task, list_tasks
from graders import run_grader


# ── Pydantic Models (OpenEnv spec) ──────────────────────────────

class Observation(BaseModel):
    """What the agent sees at each step."""
    post_id: str = Field(description="Unique ID of the current post")
    post_text: str = Field(description="The social media post text to moderate")
    step_number: int = Field(description="Current step (1-indexed)")
    total_steps: int = Field(description="Total number of posts in this task")
    task_id: int = Field(description="Which task is active (1, 2, or 3)")
    task_description: str = Field(description="Instructions for the agent")
    action_schema: dict = Field(description="Schema describing valid actions")
    progress: float = Field(description="Fraction of task completed (0.0 to 1.0)")


class Action(BaseModel):
    """What the agent submits for each post."""
    category: str = Field(description="Predicted category of the post")
    severity: Optional[str] = Field(default="none", description="Predicted severity (Task 2 and 3 only)")
    justification: Optional[str] = Field(default="", description="Reasoning for decision (Task 3 only)")


class StepResult(BaseModel):
    """Result returned after each step()."""
    observation: Optional[Observation] = Field(description="Next post to review (None if episode done)")
    reward: float = Field(description="Partial reward for this step (0.0 if not final step)")
    done: bool = Field(description="True when all posts have been reviewed")
    info: dict = Field(description="Additional info — running score, feedback, etc.")


class EnvironmentState(BaseModel):
    """Full state of the environment."""
    task_id: int
    step_number: int
    total_steps: int
    done: bool
    actions_taken: list
    running_score: float
    current_post_id: Optional[str]


# ── ContentGuard Environment ─────────────────────────────────────

class ContentGuardEnv:
    """
    ContentGuard: An OpenEnv environment for AI content moderation.

    The agent reads social media posts and must classify them
    as: safe, spam, hate_speech, harassment, or misinformation.
    Tasks range from easy binary classification to hard
    context-aware moderation with justifications.
    """

    def __init__(self):
        self._task_id: int = 1
        self._task: dict = {}
        self._posts: list = []
        self._step_number: int = 0
        self._actions: list = []
        self._done: bool = False
        self._running_score: float = 0.0

    def reset(self, task_id: int = 1) -> Observation:
        """
        Reset the environment and start a new episode.
        Args:
            task_id: Which task to run (1=easy, 2=medium, 3=hard)
        Returns:
            Observation of the first post.
        """
        if task_id not in [1, 2, 3]:
            raise ValueError(f"task_id must be 1, 2, or 3. Got: {task_id}")

        self._task_id = task_id
        self._task = get_task(task_id)
        self._posts = self._task["posts"]
        self._step_number = 0
        self._actions = []
        self._done = False
        self._running_score = 0.0

        return self._make_observation()

    def step(self, action: dict) -> StepResult:
        """
        Take one step: submit a classification for the current post.
        Args:
            action: dict with 'category', and optionally 'severity', 'justification'
        Returns:
            StepResult with next observation, reward, done flag, and info.
        """
        if self._done:
            raise RuntimeError("Episode is done. Call reset() to start a new one.")
        if not self._posts:
            raise RuntimeError("Environment not initialized. Call reset() first.")

        # Validate action
        action = self._validate_action(action)

        # Record action for current post
        current_post = self._posts[self._step_number]
        self._actions.append({**action, "_post_id": current_post["id"]})
        self._step_number += 1

        # Check if episode is complete
        if self._step_number >= len(self._posts):
            self._done = True
            # Compute final score
            grade = run_grader(self._task_id, self._actions, self._posts)
            self._running_score = grade["score"]
            return StepResult(
                observation=None,
                reward=self._running_score,
                done=True,
                info={
                    "message": "Episode complete!",
                    "final_score": self._running_score,
                    "grade_details": grade,
                }
            )

        # Intermediate step — no reward yet
        next_obs = self._make_observation()
        return StepResult(
            observation=next_obs,
            reward=0.0,
            done=False,
            info={
                "message": f"Step {self._step_number} of {len(self._posts)} complete.",
                "posts_remaining": len(self._posts) - self._step_number,
            }
        )

    def state(self) -> EnvironmentState:
        """Return the current state of the environment."""
        current_post_id = None
        if not self._done and self._posts and self._step_number < len(self._posts):
            current_post_id = self._posts[self._step_number]["id"]

        return EnvironmentState(
            task_id=self._task_id,
            step_number=self._step_number,
            total_steps=len(self._posts),
            done=self._done,
            actions_taken=self._actions,
            running_score=self._running_score,
            current_post_id=current_post_id,
        )

    def _make_observation(self) -> Observation:
        """Build the Observation object for the current post."""
        post = self._posts[self._step_number]
        total = len(self._posts)
        return Observation(
            post_id=post["id"],
            post_text=post["text"],
            step_number=self._step_number + 1,
            total_steps=total,
            task_id=self._task_id,
            task_description=self._task["description"],
            action_schema=self._task["action_schema"],
            progress=round(self._step_number / total, 4),
        )

    def _validate_action(self, action: dict) -> dict:
        """Validate and normalize an action dict."""
        valid_categories = ["safe", "spam", "hate_speech", "harassment", "misinformation"]
        valid_severities = ["low", "medium", "high", "none"]

        cat = str(action.get("category", "safe")).lower().strip()
        sev = str(action.get("severity", "none")).lower().strip()
        just = str(action.get("justification", "")).strip()

        if cat not in valid_categories:
            cat = "safe"  # Default to safe for invalid inputs
        if sev not in valid_severities:
            sev = "none"

        return {"category": cat, "severity": sev, "justification": just}

    def tasks(self) -> list:
        """Return list of all available tasks."""
        return list_tasks()
