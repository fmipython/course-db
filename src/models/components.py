from pydantic import BaseModel


class Component(BaseModel):
    name: str
    points: float
    max_points: float
