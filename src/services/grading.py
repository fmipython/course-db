from src.models.components import Component


def components_2025() -> list[Component]:
    return [
        Component(name="Homework 0", max_points=1),
        Component(name="Homework 1", max_points=8),
        Component(name="Homework 2", max_points=8),
        Component(name="Homework 3", max_points=8),
        Component(name="Project", max_points=30),
    ]


def grading_2025(points: float) -> float:
    if points < 30:
        return 2.0
    elif points > 60:
        return 6.0
    else:
        return points / 10
