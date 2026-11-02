from typing import Literal
from pydantic import BaseModel, Field, HttpUrl

Category = Literal[
    "CONFIRMED_THREAT", "HIGH_RISK", "SUSPICIOUS",
    "NO_KNOWN_THREAT", "ANALYSIS_UNAVAILABLE"
]

class AnalyzeRequest(BaseModel):
    url: str = Field(min_length=1, max_length=4096, description="Absolute HTTP or HTTPS URL")

class AnalyzeResponse(BaseModel):
    url: str
    category: Category
    score: int = Field(ge=0, le=100)
    reasons: list[str]
    disclaimer: str = "Heuristic result only; this is not a guarantee of safety."
