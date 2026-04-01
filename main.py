from fastapi import FastAPI
import uvicorn
from models import Observation, Action, Reward, StepResponse
from environment import TicketEnv

# FastAPI App initialization
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
    state = env.reset()
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
    
    return StepResponse(
        observation=Observation(**env.get_state()),
        reward=Reward(score=score, comment=comment),
        done=done
    )

# --- VALIDATOR REQUIREMENTS START ---

def main():
    """
    Validator ki main demand: Ek main function jo server start kare.
    Hugging Face Spaces default port 7860 use karta hai.
    """
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    main()

# --- VALIDATOR REQUIREMENTS END ---