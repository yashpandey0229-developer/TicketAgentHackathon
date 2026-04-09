---
title: TicketAgentEnv
emoji: 👁️
colorFrom: red
colorTo: purple
sdk: docker
pinned: false
tags:
- openenv
---

# TicketAgentEnv: OpenEnv Customer Support Environment

TicketAgentEnv is a deterministic, container-ready OpenEnv-compatible environment for evaluating AI ticket-handling behavior. It is designed for stable benchmarking and straightforward validator integration.

## Why This Project Is Submission-Ready
- Deterministic task sequence (3 fixed ticket scenarios)
- Strict reward bounds in the open interval $(0,1)$
- Stable OpenEnv-style endpoints: `/reset`, `/step`, `/state`
- Dockerized runtime on port `7860`
- Reproducible baseline runner (`inference.py`) that reports average score

## Environment Contract

### Observation Schema
Each observation contains:
- `id`: ticket id (example: `T1`)
- `issue`: customer message text
- `priority`: `Low` | `Medium` | `High`
- `status`: `Open` | `Pending` | `Closed`

### Action Schema
`POST /step` expects JSON payload:

```json
{
	"action_type": "set_priority | reply | close",
	"content": "string"
}
```

Invalid or missing actions are safely normalized to `reply` by the API layer.

### Response Schema (`/step`)

```json
{
	"observation": {
		"id": "T1",
		"issue": "...",
		"priority": "Low",
		"status": "Pending"
	},
	"reward": {
		"score": 0.73,
		"comment": "Task T1 handled with the expected action."
	},
	"done": true,
	"info": {
		"task_id": "T1",
		"expected_action": "set_priority",
		"received_action": "set_priority"
	}
}
```

## Deterministic Tasks
The environment rotates through exactly 3 tasks in order:
1. Raise refund ticket priority to `High`
2. Send a concise customer update reply
3. Close a ticket after resolution confirmation

## Scoring Model
- Base reward with action-matching and content-quality shaping
- Raw environment score is constrained to `[0.05, 0.95]`
- API layer additionally guards reward values to remain in `(0.01, 0.99)`
- Final response always satisfies the strict validator expectation: `0 < score < 1`

## Quick Start (Local)

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Start the server
```bash
python server/app.py
```

Server runs at:
- `http://127.0.0.1:7860/`

### 3) Smoke test endpoints
```bash
curl -X POST http://127.0.0.1:7860/reset
curl http://127.0.0.1:7860/state
curl -X POST http://127.0.0.1:7860/step -H "Content-Type: application/json" -d "{\"action_type\":\"reply\",\"content\":\"Thanks for your patience. I will update you shortly.\"}"
```

## Baseline Evaluation Runner
`inference.py` runs one action per task and prints summary metrics.

Required environment variables:
- `API_BASE_URL`
- `MODEL_NAME`
- `HF_TOKEN`

Optional:
- `API_BASE_URL` default: `https://api.openai.com/v1`
- `MODEL_NAME` default: `gpt-4.1-mini`
- `ENV_URL` (default: `http://127.0.0.1:7860`)

Run:
```bash
python inference.py
```

Expected output pattern:
- `[START] task=<task_name> env=<benchmark_name> model=<model_name>`
- `[STEP] step=<n> action=<action_str> reward=<r.xx> done=<true|false> error=<msg|null>`
- `[END] success=<true|false> steps=<n> rewards=<r1,r2,...,rn> error=<msg|null>`

## Docker Run

Build image:
```bash
docker build -t ticket-agent-env .
```

Start container:
```bash
docker run --rm -p 7860:7860 ticket-agent-env
```

## Validation Checklist (Phase-Pass Oriented)
Use this checklist before submission:

1. Container builds without errors (`docker build`)
2. Service starts on port `7860`
3. `POST /reset` returns valid observation JSON
4. `POST /step` returns `reward.score` strictly between `0` and `1`
5. `done` is boolean, and response includes `observation`, `reward`, `info`
6. Multiple `reset` calls cycle deterministic tasks (`T1`, `T2`, `T3`, repeat)
7. Baseline runner completes and prints a summary average

## Project Structure
- `server/app.py`: API entrypoint used by Docker runtime
- `main.py`: alternate FastAPI entrypoint
- `environment.py`: deterministic ticket tasks and scoring
- `models.py`: Pydantic schemas for observation/action/reward/step response
- `inference.py`: baseline evaluator
- `openenv.yaml`: environment metadata
- `Dockerfile`: deployment image definition

## Tech Stack
- Python 3.10+
- FastAPI + Uvicorn
- Pydantic
- Requests
- OpenAI SDK (for baseline client)

## Notes
- The environment is intentionally lightweight and deterministic to keep benchmark variance low.
- The API is defensive against malformed action payloads to improve evaluation stability.