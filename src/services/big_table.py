"""
Contains all logic for the "big table" - all students, all scores, the single source of truth about the grades
"""

from typing import Optional

from src.models.student import Student
from src.services.grading import grading_2025


class BigTable:
    def __init__(self):
        self.__students: list[Student] = []

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
            components=grading_2025(),
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
