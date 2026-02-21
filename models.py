from dataclasses import dataclass
from typing import Optional

@dataclass
class Creator:
    name: str
    platform: str
    niche: str
    followers: int
    engagement_rate: float
    contact: Optional[str] = None

@dataclass
class Partnership:
    creator_id: int
    status: str
    budget: float = 0.0
    notes: str = ""
