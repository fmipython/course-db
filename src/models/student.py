from pydantic import BaseModel

from .components import Component


class Student(BaseModel):
    first_name: str
    last_name: str
    faculty_number: str
    components: list[Component]
    bonus: int = 0
