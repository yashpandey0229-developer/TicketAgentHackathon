from fastapi import FastAPI
from models import Observation, Action, Reward
from environment import TicketEnv

app = FastAPI()
env = TicketEnv()

@app.get("/")
def home():
    return {"message": "TicketAgentEnv is running!"}

@app.post("/reset")
def reset():
    state = env.get_state()
    return Observation(**state)

# YEH ADD KARNA ZAROORI HAI (openenv.yaml se sync ke liye)
@app.get("/state")
def get_state():
    state = env.get_state()
    return Observation(**state)

@app.post("/step")
def step(action: Action):
    score, done, comment = env.step(action.action_type, action.content)
    
    # OpenEnv spec ke mutabiq return format
    return {
        "observation": env.get_state(),
        "reward": {"score": score, "comment": comment},
        "done": done
    }

if __name__ == "__main__":
    import uvicorn
    # Hugging Face Spaces hamesha port 7860 use karta hai
    uvicorn.run(app, host="0.0.0.0", port=7860)