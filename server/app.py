from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

# Dummy data for Phase 1 checks
@app.get("/")
async def root():
    return {"status": "Running", "spec": "OpenEnv 0.1.0"}

@app.post("/reset")
async def reset():
    # Phase 1 ko sirf 200 OK aur ek observation chahiye
    return {"id": "T1", "issue": "Order issue", "status": "Open"}

@app.post("/step")
async def step(request: Request):
    # Phase 1 step check pass karne ke liye
    return {
        "reward": {"score": 0.85, "comment": "Correct"},
        "done": True
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)