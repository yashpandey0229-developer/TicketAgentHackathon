from pydantic import BaseModel, Field
from typing import Optional

class Observation(BaseModel):
    id: str
    issue: str
    priority: str
    status: str

class Action(BaseModel):
    action_type: Optional[str] = "reply"  # e.g., "reply", "set_priority", "close"
    content: Optional[str] = ""

class Reward(BaseModel):
    score: float = Field(gt=0.0, lt=1.0)
    comment: str

# Yeh naya model hai jo main.py ke /step endpoint ke liye zaroori hai
class StepResponse(BaseModel):
    observation: Observation
    reward: Reward
    done: bool
    info: dict[str, str] = Field(default_factory=dict)