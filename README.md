# 🛡️ ContentGuard — OpenEnv Content Moderation Environment

**ContentGuard** is a real-world OpenEnv environment where AI agents learn to moderate social media content. Built for the OpenEnv Hackathon by Scaler × Meta × Hugging Face.

---

## 🌍 What Is This?

Every major social platform — Meta, YouTube, Twitter/X — employs thousands of human moderators and AI systems to review content. ContentGuard simulates this exact workflow as an OpenEnv training environment.

An AI agent reads social media posts and must classify them into:

| Category | Description |
|---|---|
| `safe` | Normal, harmless content |
| `spam` | Unsolicited promotions, fake giveaways, scams |
| `hate_speech` | Content targeting groups by identity |
| `harassment` | Direct personal attacks, threats, doxxing |
| `misinformation` | False or misleading factual claims |

---

## 🎯 Tasks

### Task 1 — Basic Violation Detection (Easy)
- **Posts:** 10
- **Categories:** safe vs spam only
- **Scoring:** +0.1 per correct, −0.05 for false positives
- **Goal:** Learn basic binary classification

### Task 2 — Multi-Category Classification (Medium)
- **Posts:** 25
- **Categories:** All 5 categories + severity rating (low/medium/high)
- **Scoring:** Category (0.8) + severity (0.2) per post
- **Goal:** Distinguish nuanced violation types

### Task 3 — Context-Aware Moderation (Hard)
- **Posts:** 40 (including edge cases, satire, borderline content)
- **Categories:** All 5 + severity + written justification required
- **Scoring:** Category (0.5) + severity (0.2) + justification quality (0.3)
- **Goal:** Handle ambiguous real-world cases that challenge frontier models

---

## 🔌 API Reference

### `POST /reset`
Start a new episode.
```json
{"task_id": 1}
```
Returns the first post as an `observation`.

### `POST /step`
Submit a classification for the current post.
```json
{
  "category": "spam",
  "severity": "high",
  "justification": "Contains fake giveaway language and urgency tactics."
}
```
Returns `{observation, reward, done, info}`.

### `GET /state`
Returns current environment state.

### `GET /tasks`
Returns all task definitions and action schemas.

### `GET /grader`
Returns detailed score breakdown for the last completed episode.

### `POST /baseline`
Runs the rule-based baseline and returns scores for all 3 tasks.

### `GET /health`
Returns `{"status": "ok"}` — used for deployment health checks.

---

## 📊 Observation Space

```json
{
  "post_id": "sp003",
  "post_text": "You have been selected as our lucky winner! Claim your $1000 gift card now.",
  "step_number": 3,
  "total_steps": 10,
  "task_id": 1,
  "task_description": "Classify each post as safe or spam...",
  "action_schema": {"category": {"type": "string", "enum": ["safe", "spam"]}},
  "progress": 0.2
}
```

## ⚡ Action Space

```json
{
  "category": "spam",          // required always
  "severity": "high",          // required for tasks 2 and 3
  "justification": "..."       // required for task 3
}
```

## 🏆 Reward Function

- Reward is **0.0** at every intermediate step
- Final reward (0.0–1.0) returned when `done=True`
- Partial credit awarded per post based on task rules
- Penalties for false positives (flagging safe content)
- Task 3 rewards quality of written justification

---

## 🚀 Setup & Usage

### Local Development

```bash
# Clone the repo
git clone https://huggingface.co/spaces/your-username/contentguard
cd contentguard

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app:app --host 0.0.0.0 --port 7860

# Run baseline
python baseline.py
```

### Docker

```bash
docker build -t contentguard .
docker run -p 7860:7860 contentguard
```

### With OpenAI API baseline

```bash
export OPENAI_API_KEY=your_key_here
python baseline.py
```

---

## 📈 Baseline Scores

| Task | Method | Score |
|------|--------|-------|
| Task 1 (Easy) | Keyword baseline | ~0.80 |
| Task 2 (Medium) | Keyword baseline | ~0.55 |
| Task 3 (Hard) | Keyword baseline | ~0.42 |

These are reproducible scores from the rule-based keyword baseline. LLM-based scores are higher.

---

## 🧪 Example Agent Loop

```python
import requests

BASE = "http://localhost:7860"

# Start episode on Task 2
obs = requests.post(f"{BASE}/reset", json={"task_id": 2}).json()["observation"]

while True:
    # Your agent logic here
    action = {
        "category": "safe",
        "severity": "none",
        "justification": "No violation indicators present."
    }
    result = requests.post(f"{BASE}/step", json=action).json()
    
    if result["done"]:
        print(f"Episode complete! Score: {result['reward']:.4f}")
        break
    
    obs = result["observation"]
    print(f"Next post: {obs['post_text'][:60]}...")
```

---

## 📁 Project Structure

```
contentguard/
├── app.py           # FastAPI server — all endpoints
├── environment.py   # OpenEnv class — step/reset/state
├── tasks.py         # 3 task definitions
├── graders.py       # Scoring logic (deterministic)
├── dataset.py       # 100+ synthetic social media posts
├── baseline.py      # Rule-based + LLM baseline scripts
├── openenv.yaml     # OpenEnv spec metadata
├── requirements.txt # Python dependencies
├── Dockerfile       # Container for HF Spaces
└── README.md        # This file
```

---

## 🏗️ Built For

OpenEnv Hackathon — Scaler × Meta × Hugging Face  
Domain: Trust & Safety / Content Moderation  
Spec: OpenEnv v1  
