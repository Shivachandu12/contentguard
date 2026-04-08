"""
inference.py - ContentGuard LLM-based inference using OpenEnv proxy.
Uses API_BASE_URL and API_KEY environment variables injected by the validator.
Prints required [START]/[STEP]/[END] structured output blocks.
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openai import OpenAI
from tasks import get_task
from graders import run_grader


def get_client():
    """Initialize OpenAI client using injected proxy credentials."""
    api_base_url = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
    api_key = os.environ.get("API_KEY", os.environ.get("OPENAI_API_KEY", "dummy"))
    return OpenAI(base_url=api_base_url, api_key=api_key)


def llm_classify(client, post_text: str, task_description: str, categories: list) -> dict:
    """Use LLM via proxy to classify a post."""
    prompt = f"""{task_description}

Post to moderate: "{post_text}"

Respond ONLY with a JSON object like this:
{{"category": "spam", "severity": "high", "justification": "Contains promotional language."}}

category must be one of: {categories}
severity must be one of: ["low", "medium", "high", "none"]"""

    try:
        response = client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=100,
        )
        content = response.choices[0].message.content.strip()
        # Strip markdown if present
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        result = json.loads(content.strip())
        return {
            "category": result.get("category", "safe"),
            "severity": result.get("severity", "none"),
            "justification": result.get("justification", ""),
        }
    except Exception as e:
        # Fallback to safe if LLM fails
        return {"category": "safe", "severity": "none", "justification": f"Error: {str(e)}"}


def run_inference_task(task_id: int, client) -> dict:
    task = get_task(task_id)
    posts = task["posts"]
    task_name = task["name"]
    categories = list(task["action_schema"]["category"]["enum"])
    description = task["description"]

    print(f"[START] task={task_name}", flush=True)

    actions = []
    for i, post in enumerate(posts):
        action = llm_classify(client, post["text"], description, categories)
        actions.append(action)
        reward = 1.0 if action["category"] == post["category"] else 0.0
        print(f"[STEP] step={i+1} reward={reward:.4f}", flush=True)

    grade = run_grader(task_id, actions, posts)
    score = grade["score"]

    print(f"[END] task={task_name} score={score:.4f} steps={len(posts)}", flush=True)

    return {
        "task_id": task_id,
        "task_name": task_name,
        "difficulty": task["difficulty"],
        "score": score,
        "total_posts": len(posts),
    }


def run_inference() -> list:
    client = get_client()
    return [run_inference_task(i, client) for i in [1, 2, 3]]


if __name__ == "__main__":
    results = run_inference()
    print("", flush=True)
    print("=== SUMMARY ===", flush=True)
    for r in results:
        print(f"Task {r['task_id']} ({r['difficulty']}): {r['score']:.4f}", flush=True)
    avg = sum(r["score"] for r in results) / len(results)
    print(f"Average: {avg:.4f}", flush=True)
