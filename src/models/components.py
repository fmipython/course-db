from typing import Optional

from pydantic import BaseModel


class Component(BaseModel):
    name: str
    points: Optional[float] = None
    max_points: float
