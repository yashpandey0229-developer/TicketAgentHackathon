from fastapi import FastAPI
import uvicorn
import os
import sys

# Root directory ko path mein add karo taaki imports na phate
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Observation, Action, Reward, StepResponse
from environment import TicketEnv

app = FastAPI(title="TicketAgentEnv")
env = TicketEnv()

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
def step(action: Action):
    score, done, comment, info = env.step(action.action_type, action.content)
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