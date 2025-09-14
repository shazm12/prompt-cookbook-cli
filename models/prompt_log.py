from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PromptLogger(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    command: str
    task: str
    name: str
    type: str
    input: str
    model: str
    output: str
    latency_ms: Optional[float] = None
    status: str

    