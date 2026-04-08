"""
inference.py - ContentGuard baseline inference script.
Prints structured [START]/[STEP]/[END] blocks required by OpenEnv validator.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tasks import get_task
from graders import run_grader

SPAM_KEYWORDS = [
    "click here", "make money", "earn $", "free iphone", "giveaway",
    "limited offer", "buy now", "link in bio", "dm me", "follow for follow",
    "lose weight", "crypto", "100% guaranteed", "work from home", "!!!", "🔥🔥"
]
HATE_KEYWORDS = [
    "should be deported", "property values", "lazy and", "too emotional",
    "burden on society", "replacing us", "shouldn't be allowed",
    "dangerous and should", "can't even speak", "go back to your"
]
HARASSMENT_KEYWORDS = [
    "@username", "kill yourself", "find out where", "watch your back",
    "you are absolutely worthless", "no one would miss",
    "everyone please report", "slept their way", "you should just quit"
]
MISINFO_KEYWORDS = [
    "5g towers", "microchips", "moon landing", "drink bleach", "flat earth",
    "bill gates created", "cure cancer", "election was stolen",
    "vaccines cause autism", "fluoride in water",
    "doctors don't want", "they don't want you to know",
    "big pharma", "share before deleted"
]


def classify(text: str) -> dict:
    t = text.lower()
    for kw in MISINFO_KEYWORDS:
        if kw in t:
            return {"category": "misinformation", "severity": "high", "justification": f"Contains misinformation indicator: '{kw}'"}
    for kw in HATE_KEYWORDS:
        if kw in t:
            return {"category": "hate_speech", "severity": "high", "justification": f"Contains hate speech indicator: '{kw}'"}
    for kw in HARASSMENT_KEYWORDS:
        if kw in t:
            return {"category": "harassment", "severity": "high", "justification": f"Contains harassment indicator: '{kw}'"}
    for kw in SPAM_KEYWORDS:
        if kw in t:
            return {"category": "spam", "severity": "medium", "justification": f"Contains spam indicator: '{kw}'"}
    return {"category": "safe", "severity": "none", "justification": "No violation indicators found."}


def run_inference_task(task_id: int) -> dict:
    task = get_task(task_id)
    posts = task["posts"]
    task_name = task["name"]

    print(f"[START] task={task_name}", flush=True)

    actions = []
    for i, post in enumerate(posts):
        action = classify(post["text"])
        actions.append(action)
        reward = 1.0 if action["category"] == post["category"] else 0.0
        print(f"[STEP] step={i+1} reward={reward:.4f}", flush=True)

    grade = run_grader(task_id, actions, posts)
    score = grade["score"]

    print(f"[END] task={task_name} score={score:.4f} steps={len(posts)}", flush=True)

    return {"task_id": task_id, "task_name": task_name, "difficulty": task["difficulty"], "score": score, "total_posts": len(posts)}


def run_inference() -> list:
    return [run_inference_task(i) for i in [1, 2, 3]]


if __name__ == "__main__":
    results = run_inference()
    print("", flush=True)
    print("=== SUMMARY ===", flush=True)
    for r in results:
        print(f"Task {r['task_id']} ({r['difficulty']}): {r['score']:.4f}", flush=True)
    avg = sum(r["score"] for r in results) / len(results)
    print(f"Average: {avg:.4f}", flush=True)
