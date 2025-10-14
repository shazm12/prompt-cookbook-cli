from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class PromptEngineeringLog(BaseModel):
    """Model for logging prompt engineering experiments"""

    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    technique: str
    prompt: str
    model: str
    output: str
    latency_ms: Optional[float] = None
    status: str
    metadata: Optional[Dict[str, Any]] = None
    evaluation_metrics: Optional[Dict[str, Any]] = None
    reference_text: Optional[str] = None
    keywords: Optional[list[str]] = None
