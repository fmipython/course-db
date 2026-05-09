"""
Renders a BigTable as a Rich terminal table.
"""

from rich import box
from rich.table import Table

from course_db.services.big_table import BigTable

_SUMMARY_COLUMNS = {"Ime", "Фамилия", "Факултетен номер", "Общо", "Оценка"}


# Bulgarian grading: < 3 = fail, 3–4.9 = pass, 5+ = good/excellent
def _grade_color(grade: float) -> str:
    if grade < 3.0:
        return "red"
    elif grade < 5.0:
        return "yellow"
    else:
        return "green"


def render_table(table: BigTable, summary: bool = False) -> Table:
    rich_table = Table(
        title="BigTable",
        box=box.SIMPLE_HEAVY,
        show_lines=False,
        highlight=True,
    )

    columns = table.columns
    visible = (
        set(columns[-2:]) | {"Ime", "Фамилия", "Факултетен номер"}
        if summary
        else set(columns)
    )

    for col in columns:
        if col in visible or not summary:
            rich_table.add_column(col, overflow="fold")

    for student in table.get_all():
        total = table.get_total_points_for_student(student.faculty_number)
        grade = table.calculate_grade(student.faculty_number)
        color = _grade_color(grade)

        if summary:
            rich_table.add_row(
                student.first_name,
                student.last_name,
                student.faculty_number,
                str(total),
                f"[{color}]{grade:.1f}[/{color}]",
            )
        else:
            component_cells = [
                str(c.points) if c.points is not None else "—"
                for c in student.components
            ]
            rich_table.add_row(
                student.first_name,
                student.last_name,
                student.faculty_number,
                *component_cells,
                str(student.bonus),
                str(total),
                f"[{color}]{grade:.1f}[/{color}]",
            )

    return rich_table
