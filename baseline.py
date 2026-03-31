"""
baseline.py — Baseline inference script for ContentGuard.
Two modes:
  1. Rule-based keyword baseline (no API key needed, always reproducible)
  2. LLM baseline using OpenAI API (requires OPENAI_API_KEY env var)

Run directly: python baseline.py
"""

import os
import json
from tasks import get_task
from graders import run_grader


# ── Rule-Based Keyword Baseline ──────────────────────────────────

SPAM_KEYWORDS = [
    "click here", "make money", "earn $", "free iphone", "giveaway",
    "limited offer", "buy now", "link in bio", "dm me", "follow for follow",
    "lose weight", "crypto", "100% guaranteed", "work from home", "!!!", "🔥🔥"
]

HATE_KEYWORDS = [
    "should be deported", "property values", "lazy and", "too emotional",
    "burden on society", "replacing us", "shouldn't be allowed", "dangerous and should",
    "can't even speak", "go back to your"
]

HARASSMENT_KEYWORDS = [
    "@username", "kill yourself", "find out where", "watch your back",
    "you are absolutely worthless", "no one would miss", "everyone please report",
    "slept their way", "you should just quit"
]

MISINFO_KEYWORDS = [
    "5g towers", "microchips", "moon landing", "drink bleach", "flat earth",
    "bill gates created", "cure cancer", "election was stolen", "vaccines cause autism",
    "fluoride in water", "doctors don't want", "they don't want you to know",
    "big pharma", "share before deleted"
]


def rule_based_classify(text: str) -> dict:
    """Simple keyword-based classifier. Deterministic baseline."""
    text_lower = text.lower()

    # Check each category in priority order
    for kw in MISINFO_KEYWORDS:
        if kw in text_lower:
            return {"category": "misinformation", "severity": "high", "justification": f"Contains misinformation indicator: '{kw}'"}

    for kw in HATE_KEYWORDS:
        if kw in text_lower:
            return {"category": "hate_speech", "severity": "high", "justification": f"Contains hate speech indicator: '{kw}'"}

    for kw in HARASSMENT_KEYWORDS:
        if kw in text_lower:
            return {"category": "harassment", "severity": "high", "justification": f"Contains harassment indicator: '{kw}'"}

    for kw in SPAM_KEYWORDS:
        if kw in text_lower:
            return {"category": "spam", "severity": "medium", "justification": f"Contains spam indicator: '{kw}'"}

    return {"category": "safe", "severity": "none", "justification": "No violation indicators found. Post appears safe."}


def run_baseline_task(task_id: int) -> dict:
    """Run baseline on a single task and return score."""
    task = get_task(task_id)
    posts = task["posts"]
    actions = [rule_based_classify(post["text"]) for post in posts]
    grade = run_grader(task_id, actions, posts)
    return {
        "task_id": task_id,
        "task_name": task["name"],
        "difficulty": task["difficulty"],
        "score": grade["score"],
        "total_posts": len(posts),
    }


def run_baseline() -> list:
    """Run baseline on all 3 tasks. Returns list of scores."""
    results = []
    for task_id in [1, 2, 3]:
        result = run_baseline_task(task_id)
        results.append(result)
    return results


# ── LLM Baseline (OpenAI API) ────────────────────────────────────

def run_llm_baseline_task(task_id: int, client) -> dict:
    """Run LLM-based baseline on a single task."""
    task = get_task(task_id)
    posts = task["posts"]
    actions = []

    for post in posts:
        prompt = f"""{task['description']}

Post to moderate:
\"{post['text']}\"

Respond ONLY with a JSON object with these fields:
- category: one of {list(task['action_schema'].get('category', {}).get('enum', ['safe', 'spam', 'hate_speech', 'harassment', 'misinformation']))}
- severity: one of ["low", "medium", "high", "none"]
- justification: one sentence explanation

Example: {{"category": "spam", "severity": "high", "justification": "Contains unsolicited promotional language and fake giveaway."}}"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=150,
            )
            content = response.choices[0].message.content.strip()
            # Strip markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            action = json.loads(content)
        except Exception as e:
            action = {"category": "safe", "severity": "none", "justification": f"Parse error: {str(e)}"}

        actions.append(action)

    grade = run_grader(task_id, actions, posts)
    return {
        "task_id": task_id,
        "task_name": task["name"],
        "difficulty": task["difficulty"],
        "score": grade["score"],
        "total_posts": len(posts),
    }


# ── Main Entry Point ─────────────────────────────────────────────

if __name__ == "__main__":
    api_key = os.environ.get("OPENAI_API_KEY")

    if api_key:
        print("🤖 Running LLM baseline (OpenAI API)...\n")
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            results = [run_llm_baseline_task(i, client) for i in [1, 2, 3]]
            method = "GPT-4o-mini"
        except ImportError:
            print("openai package not installed. Falling back to rule-based baseline.")
            results = run_baseline()
            method = "Rule-based keyword matching"
    else:
        print("ℹ️  No OPENAI_API_KEY found. Running rule-based keyword baseline...\n")
        results = run_baseline()
        method = "Rule-based keyword matching"

    print(f"Method: {method}")
    print("=" * 50)
    for r in results:
        bar = "█" * int(r["score"] * 20) + "░" * (20 - int(r["score"] * 20))
        print(f"Task {r['task_id']} ({r['difficulty']:6s}): [{bar}] {r['score']:.4f}  — {r['task_name']}")
    print("=" * 50)
    avg = sum(r["score"] for r in results) / len(results)
    print(f"Average score: {avg:.4f}")
    print("\n✅ Baseline complete. Scores are reproducible.")
