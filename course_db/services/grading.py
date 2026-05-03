from course_db.models.components import Component


def components_2025() -> list[Component]:
    return [
        Component(name="Домашно 0", max_points=1),
        Component(name="Домашно 1", max_points=8),
        Component(name="Домашно 2", max_points=8),
        Component(name="Домашно 3", max_points=8),
        Component(name="Проект", max_points=30),
    ]


def grading_2025(points: float) -> float:
    if points < 30:
        return 2.0
    elif points > 60:
        return 6.0
    else:
        return points / 10
