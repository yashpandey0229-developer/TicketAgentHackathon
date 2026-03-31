from pydantic import BaseModel
from typing import Optional

class Observation(BaseModel):
    id: str
    issue: str
    priority: str
    status: str

class Action(BaseModel):
    action_type: str  # e.g., "reply", "set_priority", "close"
    content: str

class Reward(BaseModel):
    score: float
    comment: str

# Yeh naya model hai jo main.py ke /step endpoint ke liye zaroori hai
class StepResponse(BaseModel):
    observation: Observation
    reward: Reward
    done: bool