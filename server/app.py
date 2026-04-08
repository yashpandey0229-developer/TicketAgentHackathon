import os
import sys

import uvicorn
from fastapi import FastAPI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from environment import TicketEnv
from models import Observation, Action, Reward, StepResponse

app = FastAPI()
env = TicketEnv()

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
async def step(action: Action):
    score, done, comment, info = env.step(action.action_type, action.content)
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