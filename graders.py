"""
graders.py — Scoring logic for ContentGuard.
Each grader returns a score between 0.0 and 1.0.
Graders are deterministic and reproducible.
"""

from dataset import CATEGORIES, SEVERITIES


def grade_task1(actions: list, posts: list) -> dict:
    """
    Task 1: Basic Violation Detection (easy).
    Agent classifies each post as 'safe' or 'spam'.
    - Correct label: +0.1 per post (max 1.0)
    - False positive (flagged safe as spam): -0.05
    - Score is clamped to [0.0, 1.0]
    """
    if not actions or not posts:
        return {"score": 0.0, "details": "No actions or posts provided."}

    total_posts = len(posts)
    correct = 0
    false_positives = 0
    details = []

    for i, (action, post) in enumerate(zip(actions, posts)):
        predicted = action.get("category", "").lower().strip()
        # Simplify: anything not 'safe' counts as violation
        true_label = "safe" if post["category"] == "safe" else "spam"

        if predicted == true_label:
            correct += 1
            details.append({"post_id": post["id"], "result": "correct", "predicted": predicted, "true": true_label})
        else:
            if post["category"] == "safe" and predicted == "spam":
                false_positives += 1
                details.append({"post_id": post["id"], "result": "false_positive", "predicted": predicted, "true": true_label})
            else:
                details.append({"post_id": post["id"], "result": "incorrect", "predicted": predicted, "true": true_label})

    raw_score = (correct * 0.1) - (false_positives * 0.05)
    score = round(max(0.0, min(1.0, raw_score)), 4)

    return {
        "score": score,
        "correct": correct,
        "false_positives": false_positives,
        "total": total_posts,
        "accuracy": round(correct / total_posts, 4) if total_posts > 0 else 0.0,
        "details": details,
    }


def grade_task2(actions: list, posts: list) -> dict:
    """
    Task 2: Multi-Category Classification (medium).
    Agent classifies into 5 categories + severity level.
    - Correct category: 0.8 points per post
    - Correct severity: 0.2 points per post
    - Final score normalized to [0.0, 1.0]
    """
    if not actions or not posts:
        return {"score": 0.0, "details": "No actions or posts provided."}

    total_posts = len(posts)
    total_points = 0.0
    max_points = total_posts * 1.0
    details = []

    for i, (action, post) in enumerate(zip(actions, posts)):
        predicted_cat = action.get("category", "").lower().strip()
        predicted_sev = action.get("severity", "none").lower().strip()
        true_cat = post["category"]
        true_sev = post["severity"] if post["severity"] else "none"

        cat_score = 0.8 if predicted_cat == true_cat else 0.0
        sev_score = 0.2 if predicted_sev == true_sev else 0.0

        post_score = cat_score + sev_score
        total_points += post_score

        details.append({
            "post_id": post["id"],
            "predicted_category": predicted_cat,
            "true_category": true_cat,
            "predicted_severity": predicted_sev,
            "true_severity": true_sev,
            "category_correct": cat_score > 0,
            "severity_correct": sev_score > 0,
            "post_score": round(post_score, 2),
        })

    score = round(total_points / max_points, 4) if max_points > 0 else 0.0

    return {
        "score": score,
        "total_points": round(total_points, 2),
        "max_points": max_points,
        "total": total_posts,
        "details": details,
    }


def _score_justification(justification: str, post: dict) -> float:
    """
    Score a justification on a 0.0–0.3 scale.
    Checks for: length, keyword relevance, reasoning quality.
    Deterministic rule-based approach.
    """
    if not justification or len(justification.strip()) < 10:
        return 0.0

    j = justification.lower()
    score = 0.0

    # Length check: at least 15 words = 0.1 pts
    words = j.split()
    if len(words) >= 15:
        score += 0.1
    elif len(words) >= 8:
        score += 0.05

    # Category keywords present = 0.1 pts
    category_keywords = {
        "spam": ["spam", "scam", "promotional", "unsolicited", "money", "offer", "buy", "click", "fake giveaway"],
        "hate_speech": ["hate", "discriminat", "prejudice", "bias", "group", "identity", "dehumaniz"],
        "harassment": ["harass", "threat", "target", "personal attack", "intimidat", "bully"],
        "misinformation": ["false", "mislead", "inaccurat", "unverified", "debunked", "conspiracy", "no evidence"],
        "safe": ["harmless", "opinion", "personal", "no violation", "appropriate", "normal"],
    }
    keywords = category_keywords.get(post["category"], [])
    if any(kw in j for kw in keywords):
        score += 0.1

    # Reasoning connectors = 0.1 pts
    connectors = ["because", "since", "therefore", "as it", "which", "this is", "contains", "promotes", "indicates"]
    if any(c in j for c in connectors):
        score += 0.1

    return round(min(0.3, score), 2)


def grade_task3(actions: list, posts: list) -> dict:
    """
    Task 3: Context-Aware Moderation with Justification (hard).
    - Category correct: 0.5 pts per post
    - Severity correct: 0.2 pts per post
    - Justification quality: 0.0–0.3 pts per post
    - Score normalized to [0.0, 1.0]
    """
    if not actions or not posts:
        return {"score": 0.0, "details": "No actions or posts provided."}

    total_posts = len(posts)
    total_points = 0.0
    max_points = total_posts * 1.0
    details = []

    for i, (action, post) in enumerate(zip(actions, posts)):
        predicted_cat = action.get("category", "").lower().strip()
        predicted_sev = action.get("severity", "none").lower().strip()
        justification = action.get("justification", "")
        true_cat = post["category"]
        true_sev = post["severity"] if post["severity"] else "none"

        cat_score = 0.5 if predicted_cat == true_cat else 0.0
        sev_score = 0.2 if predicted_sev == true_sev else 0.0
        just_score = _score_justification(justification, post)

        post_score = cat_score + sev_score + just_score
        total_points += post_score

        details.append({
            "post_id": post["id"],
            "predicted_category": predicted_cat,
            "true_category": true_cat,
            "predicted_severity": predicted_sev,
            "true_severity": true_sev,
            "justification_preview": justification[:80] if justification else "",
            "category_score": cat_score,
            "severity_score": sev_score,
            "justification_score": just_score,
            "post_score": round(post_score, 2),
        })

    score = round(total_points / max_points, 4) if max_points > 0 else 0.0

    return {
        "score": score,
        "total_points": round(total_points, 2),
        "max_points": max_points,
        "total": total_posts,
        "details": details,
    }


def run_grader(task_id: int, actions: list, posts: list) -> dict:
    """Main entry point — runs the correct grader for a task."""
    graders = {1: grade_task1, 2: grade_task2, 3: grade_task3}
    if task_id not in graders:
        raise ValueError(f"No grader found for task {task_id}")
    result = graders[task_id](actions, posts)
    result["task_id"] = task_id
    return result
