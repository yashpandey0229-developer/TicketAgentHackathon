import uvicorn
from fastapi import FastAPI, Body
from environment import TicketEnv

app = FastAPI()
env = TicketEnv()

@app.get("/")
async def root():
    return {"status": "Running", "spec": "OpenEnv 0.1.0"}

@app.post("/reset")
async def reset():
    return env.reset()

@app.post("/step")
async def step(payload: dict = Body(...)):
    action_type = payload.get("action_type", "solve")
    content = payload.get("content", "")
    reward_score, done, comment = env.step(action_type, content)
    return {
        "reward": {"score": reward_score, "comment": comment},
        "done": done
    }

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()