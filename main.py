from fastapi import FastAPI
from models import Observation, Action, Reward, StepResponse
from environment import TicketEnv
import uvicorn

app = FastAPI(title="TicketAgentEnv - OpenEnv Edition")
env = TicketEnv()

@app.get("/")
def home():
    return {
        "status": "Running",
        "environment": "TicketAgentEnv",
        "version": "1.0.0",
        "spec": "OpenEnv 0.1.0"
    }

@app.post("/reset", response_model=Observation)
def reset():
    """Environment ko initial state par lata hai."""
    state = env.reset() # Ensure environment.py has a reset() method
    return Observation(**state)

@app.get("/state", response_model=Observation)
def get_state():
    """Bina step liye current observation check karne ke liye."""
    state = env.get_state()
    return Observation(**state)

@app.post("/step", response_model=StepResponse)
def step(action: Action):
    """Agent action leta hai aur reward/next state milti hai."""
    score, done, comment = env.step(action.action_type, action.content)
    
    # OpenEnv spec ke mutabiq strictly structured response
    return StepResponse(
        observation=Observation(**env.get_state()),
        reward=Reward(score=score, comment=comment),
        done=done
    )

if __name__ == "__main__":
    # Hugging Face Spaces default port 7860 use karta hai
    uvicorn.run(app, host="0.0.0.0", port=7860)