"""
tasks.py — The 3 tasks for ContentGuard OpenEnv environment.
Each task defines what the agent must do and how it will be scored.
"""

from dataset import get_posts_for_task, CATEGORIES

TASKS = {
    1: {
        "id": 1,
        "name": "Basic Violation Detection",
        "difficulty": "easy",
        "description": (
            "You are a content moderator. You will be shown social media posts one at a time. "
            "For each post, classify it as one of: safe, spam. "
            "Obvious violations only — no edge cases."
        ),
        "action_schema": {
            "category": {
                "type": "string",
                "enum": ["safe", "spam"],
                "description": "Your classification of the post"
            }
        },
        "max_steps": 10,
        "scoring": "Each correct label scores 0.1. Penalty of -0.05 for false positives (flagging safe content as spam).",
        "posts": get_posts_for_task(1),
    },
    2: {
        "id": 2,
        "name": "Multi-Category Classification",
        "difficulty": "medium",
        "description": (
            "You are an advanced content moderator. Classify each post into one of 5 categories: "
            "safe, spam, hate_speech, harassment, misinformation. "
            "Also rate the severity: low, medium, or high. "
            "Posts may be subtle or require reading between the lines."
        ),
        "action_schema": {
            "category": {
                "type": "string",
                "enum": ["safe", "spam", "hate_speech", "harassment", "misinformation"],
                "description": "Your classification of the post"
            },
            "severity": {
                "type": "string",
                "enum": ["low", "medium", "high", "none"],
                "description": "Severity level — use 'none' for safe posts"
            }
        },
        "max_steps": 25,
        "scoring": "Correct category = 0.8 pts, correct severity = 0.2 pts per post. Max 1.0 total.",
        "posts": get_posts_for_task(2),
    },
    3: {
        "id": 3,
        "name": "Context-Aware Moderation with Justification",
        "difficulty": "hard",
        "description": (
            "You are a senior content moderation specialist. For each post: "
            "(1) classify into the correct category, "
            "(2) rate severity, "
            "(3) provide a brief justification (1-2 sentences) for your decision. "
            "Posts include edge cases, satire, and context-dependent content. "
            "Think carefully before classifying."
        ),
        "action_schema": {
            "category": {
                "type": "string",
                "enum": ["safe", "spam", "hate_speech", "harassment", "misinformation"],
                "description": "Your classification"
            },
            "severity": {
                "type": "string",
                "enum": ["low", "medium", "high", "none"],
                "description": "Severity level"
            },
            "justification": {
                "type": "string",
                "description": "1-2 sentence explanation of your decision"
            }
        },
        "max_steps": 40,
        "scoring": "Category (0.5) + severity (0.2) + justification quality (0.3) per post. Max 1.0 total.",
        "posts": get_posts_for_task(3),
    }
}


def get_task(task_id: int) -> dict:
    """Return task definition by ID."""
    if task_id not in TASKS:
        raise ValueError(f"Task {task_id} not found. Available tasks: {list(TASKS.keys())}")
    return TASKS[task_id]


def list_tasks() -> list:
    """Return summary of all tasks."""
    return [
        {
            "id": t["id"],
            "name": t["name"],
            "difficulty": t["difficulty"],
            "description": t["description"],
            "action_schema": t["action_schema"],
            "max_steps": t["max_steps"],
        }
        for t in TASKS.values()
    ]
