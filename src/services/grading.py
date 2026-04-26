from src.models.components import Component


def grading_2025() -> list[Component]:
    return [
        Component(name="Homework 0", max_points=1),
        Component(name="Homework 1", max_points=8),
        Component(name="Homework 2", max_points=8),
        Component(name="Homework 3", max_points=8),
        Component(name="Project", max_points=30),
    ]
