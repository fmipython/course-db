"""
Contains all logic for the "big table" - all students, all scores, the single source of truth about the grades
"""

from typing import Callable, Optional

from course_db.models.components import Component
from course_db.models.student import Student, student_columns


class BigTable:
    def __init__(
        self,
        components: Callable[[], list[Component]],
        grading: Callable[[float], float],
    ):
        self.__students: list[Student] = []
        self.__components = components
        self.__grading = grading

    # Create
    def add_student(
        self, first_name: str, last_name: str, faculty_number: str
    ) -> Student:
        if self.get_by_faculty_number(faculty_number) is not None:
            raise ValueError(
                f"Student with faculty number '{faculty_number}' already exists."
            )
        student = Student(
            first_name=first_name,
            last_name=last_name,
            faculty_number=faculty_number,
            components=self.__components(),
        )
        self.__students.append(student)
        return student

    # Read
    def get_by_faculty_number(self, faculty_number: str) -> Optional[Student]:
        for student in self.__students:
            if student.faculty_number == faculty_number:
                return student
        return None

    def get_by_name(self, query: str) -> list[Student]:
        query_lower = query.lower()
        return [
            s
            for s in self.__students
            if query_lower in s.first_name.lower() or query_lower in s.last_name.lower()
        ]

    # Update
    def update_student(self, faculty_number: str, **kwargs) -> Student:
        student = self.get_by_faculty_number(faculty_number)
        if student is None:
            raise ValueError(
                f"Student with faculty number '{faculty_number}' not found."
            )
        updated = student.model_copy(update=kwargs)
        index = self.__students.index(student)
        self.__students[index] = updated
        return updated

    # Delete
    def delete_student(self, faculty_number: str) -> None:
        student = self.get_by_faculty_number(faculty_number)
        if student is None:
            raise ValueError(
                f"Student with faculty number '{faculty_number}' not found."
            )
        self.__students.remove(student)

    # Component points CRUD
    def set_points(
        self, faculty_number: str, component_name: str, points: float
    ) -> Component:
        student = self.get_by_faculty_number(faculty_number)
        if student is None:
            raise ValueError(
                f"Student with faculty number '{faculty_number}' not found."
            )
        component = next(
            (c for c in student.components if c.name == component_name), None
        )
        if component is None:
            raise ValueError(
                f"Component '{component_name}' not found for student '{faculty_number}'."
            )
        if points < 0 or points > component.max_points:
            raise ValueError(
                f"Points must be between 0 and {component.max_points} for '{component_name}'."
            )
        updated_components = [
            c.model_copy(update={"points": points}) if c.name == component_name else c
            for c in student.components
        ]
        self.update_student(faculty_number, components=updated_components)
        return next(c for c in updated_components if c.name == component_name)

    def get_points(self, faculty_number: str, component_name: str) -> Optional[float]:
        student = self.get_by_faculty_number(faculty_number)
        if student is None:
            raise ValueError(
                f"Student with faculty number '{faculty_number}' not found."
            )
        component = next(
            (c for c in student.components if c.name == component_name), None
        )
        if component is None:
            raise ValueError(
                f"Component '{component_name}' not found for student '{faculty_number}'."
            )
        return component.points

    def clear_points(self, faculty_number: str, component_name: str) -> Component:
        student = self.get_by_faculty_number(faculty_number)
        if student is None:
            raise ValueError(
                f"Student with faculty number '{faculty_number}' not found."
            )
        component = next(
            (c for c in student.components if c.name == component_name), None
        )
        if component is None:
            raise ValueError(
                f"Component '{component_name}' not found for student '{faculty_number}'."
            )
        updated_components = [
            c.model_copy(update={"points": None}) if c.name == component_name else c
            for c in student.components
        ]
        self.update_student(faculty_number, components=updated_components)
        return next(c for c in updated_components if c.name == component_name)

    # Bonus points CRUD
    BONUS_MAX = 5

    def set_bonus(self, faculty_number: str, bonus: int) -> Student:
        if bonus < 0 or bonus > self.BONUS_MAX:
            raise ValueError(f"Bonus must be between 0 and {self.BONUS_MAX}.")
        return self.update_student(faculty_number, bonus=bonus)

    def get_bonus(self, faculty_number: str) -> int:
        student = self.get_by_faculty_number(faculty_number)
        if student is None:
            raise ValueError(
                f"Student with faculty number '{faculty_number}' not found."
            )
        return student.bonus

    def clear_bonus(self, faculty_number: str) -> Student:
        return self.update_student(faculty_number, bonus=0)

    def add_bonus_point(self, faculty_number: str) -> Student:
        current = self.get_bonus(faculty_number)
        return self.set_bonus(faculty_number, current + 1)

    def get_total_points_for_student(self, faculty_number: str) -> float:
        student = self.get_by_faculty_number(faculty_number)
        if student is None:
            raise ValueError(
                f"Student with faculty number '{faculty_number}' not found."
            )
        total_points = sum(c.points for c in student.components if c.points is not None)
        return total_points + student.bonus

    def calculate_grade(self, faculty_number: str) -> float:
        total_points = self.get_total_points_for_student(faculty_number)

        return self.__grading(total_points)

    def get_all(self) -> list[Student]:
        return self.__students[:]

    @property
    def columns(self) -> list[str]:
        return student_columns(self.__components())
