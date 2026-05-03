from pydantic import BaseModel

from course_db.models.components import Component, component_columns


class Student(BaseModel):
    first_name: str
    last_name: str
    faculty_number: str
    components: list[Component]
    bonus: int = 0


def student_columns(components: list[Component]) -> list[str]:
    return (
        ["Име", "Фамилия", "Факултетен номер"]
        + [component_columns(c) for c in components]
        + ["Бонус"]
        + ["Общо", "Оценка"]
    )
