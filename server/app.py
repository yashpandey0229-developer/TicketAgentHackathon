import os
import sys
import math

import uvicorn
from fastapi import FastAPI, Body

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from environment import TicketEnv
from models import Observation, Action, Reward, StepResponse

app = FastAPI()
env = TicketEnv()


def _safe_score(value):
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.5

    if not math.isfinite(score):
        return 0.5

    return min(max(score, 0.01), 0.99)

@app.get("/")
async def root():
    return {"status": "Running", "version": "v31", "spec": "OpenEnv 0.1.0"}

@app.post("/reset")
async def reset():
    return Observation(**env.reset())

@app.get("/state")
async def state():
    return Observation(**env.get_state())

@app.post("/step")
async def step(payload: object = Body(default_factory=dict)):
    parsed_payload = payload if isinstance(payload, dict) else {}
    action = Action(**parsed_payload)
    score, done, comment, info = env.step(action.action_type, action.content)
    score = _safe_score(score)
    return StepResponse(
        observation=Observation(**env.get_state()),
        reward=Reward(score=score, comment=comment),
        done=done,
        info=info,
    )

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()