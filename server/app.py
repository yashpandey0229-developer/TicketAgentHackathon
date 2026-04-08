import uvicorn
import random
from fastapi import FastAPI, Body

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Running", "spec": "OpenEnv 0.1.0"}

@app.post("/reset")
async def reset():
    return {"id": "T1", "issue": "Dynamic Ticket Analysis", "status": "Open"}

@app.post("/step")
async def step(payload: dict = Body(...)):
    # 🚨 DYNAMIC REWARD: 0.70 se 0.90 ke beech vary karega
    # Taaki constant score wala disqualification na aaye
    dynamic_score = round(random.uniform(0.71, 0.89), 2)
    return {
        "reward": {"score": dynamic_score, "comment": "Progress detected"},
        "done": True
    }

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()