from pydantic import BaseModel

from .components import Component


class Student(BaseModel):
    first_name: str
    last_name: str
    faculty_number: str
    pure_fn: str
    components: list[Component]
    bonus: int
