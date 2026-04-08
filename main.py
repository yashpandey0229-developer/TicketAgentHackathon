from fastapi import FastAPI, Body
import uvicorn
import os
import sys
import math

# Root directory ko path mein add karo taaki imports na phate
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Observation, Reward, StepResponse
from environment import TicketEnv

app = FastAPI(title="TicketAgentEnv")
env = TicketEnv()


def _safe_score(value):
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.5

    if not math.isfinite(score):
        return 0.5

    return min(max(score, 0.01), 0.99)


def _extract_action(payload):
    if not isinstance(payload, dict):
        return "reply", ""

    raw_action = payload.get("action_type", "reply")
    raw_content = payload.get("content", "")

    action_type = str(raw_action).strip().lower() if raw_action is not None else "reply"
    if action_type not in {"set_priority", "reply", "close"}:
        action_type = "reply"

    if raw_content is None:
        content = ""
    elif isinstance(raw_content, (dict, list, tuple, set)):
        content = str(raw_content)
    else:
        content = str(raw_content)

    return action_type, content

@app.get("/")
def home():
    return {"status": "Running", "spec": "OpenEnv 0.1.0"}

@app.post("/reset", response_model=Observation)
def reset():
    return Observation(**env.reset())

@app.get("/state", response_model=Observation)
def get_state():
    return Observation(**env.get_state())

@app.post("/step", response_model=StepResponse)
def step(payload: object = Body(default_factory=dict)):
    action_type, content = _extract_action(payload)
    score, done, comment, info = env.step(action_type, content)
    score = _safe_score(score)
    return StepResponse(
        observation=Observation(**env.get_state()),
        reward=Reward(score=score, comment=comment),
        done=done,
        info=info,
    )

def main():
    """Main entry point for the validator and Hugging Face."""
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    main()