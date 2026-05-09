import typer
from rich.console import Console

from course_db.repository.google_sheets import load, save
from course_db.services.big_table import BigTable
from course_db.services.grading import components_2025, grading_2025
from course_db.services.visualization import render_table

app = typer.Typer()

table = BigTable(components=components_2025, grading=grading_2025)


# Student CRUD
@app.command()
def add_student(
    first_name: str = typer.Argument(..., help="Student's first name"),
    last_name: str = typer.Argument(..., help="Student's last name"),
    faculty_number: str = typer.Argument(..., help="Student's faculty number"),
):
    """Add a new student."""
    student = table.add_student(first_name, last_name, faculty_number)
    typer.echo(
        f"Added: {student.first_name} {student.last_name} ({student.faculty_number})"
    )


@app.command()
def get_student(
    faculty_number: str = typer.Argument(..., help="Student's faculty number"),
):
    """Get a student by faculty number."""
    student = table.get_by_faculty_number(faculty_number)
    if student is None:
        typer.echo(
            f"No student found with faculty number '{faculty_number}'.", err=True
        )
        raise typer.Exit(1)
    typer.echo(
        f"{student.first_name} {student.last_name} ({student.faculty_number}), bonus={student.bonus}"
    )


@app.command()
def search_student(
    query: str = typer.Argument(..., help="Name query to search for"),
):
    """Search students by name."""
    students = table.get_by_name(query)
    if not students:
        typer.echo("No students found.")
        return
    for s in students:
        typer.echo(f"{s.first_name} {s.last_name} ({s.faculty_number})")


@app.command()
def update_student(
    faculty_number: str = typer.Argument(..., help="Student's faculty number"),
    first_name: str = typer.Option(None, help="New first name"),
    last_name: str = typer.Option(None, help="New last name"),
):
    """Update a student's name fields."""
    kwargs = {}
    if first_name is not None:
        kwargs["first_name"] = first_name
    if last_name is not None:
        kwargs["last_name"] = last_name
    if not kwargs:
        typer.echo("No fields to update provided.", err=True)
        raise typer.Exit(1)
    student = table.update_student(faculty_number, **kwargs)
    typer.echo(
        f"Updated: {student.first_name} {student.last_name} ({student.faculty_number})"
    )


@app.command()
def delete_student(
    faculty_number: str = typer.Argument(..., help="Student's faculty number"),
):
    """Delete a student by faculty number."""
    table.delete_student(faculty_number)
    typer.echo(f"Deleted student with faculty number '{faculty_number}'.")


# Component points CRUD
@app.command()
def set_points(
    faculty_number: str = typer.Argument(..., help="Student's faculty number"),
    component_name: str = typer.Argument(..., help="Component name"),
    points: float = typer.Argument(..., help="Points to set"),
):
    """Set points for a component."""
    component = table.set_points(faculty_number, component_name, points)
    typer.echo(f"Set '{component.name}' to {component.points}/{component.max_points}")


@app.command()
def get_points(
    faculty_number: str = typer.Argument(..., help="Student's faculty number"),
    component_name: str = typer.Argument(..., help="Component name"),
):
    """Get points for a component."""
    points = table.get_points(faculty_number, component_name)
    typer.echo(f"'{component_name}': {points}")


@app.command()
def clear_points(
    faculty_number: str = typer.Argument(..., help="Student's faculty number"),
    component_name: str = typer.Argument(..., help="Component name"),
):
    """Clear points for a component."""
    component = table.clear_points(faculty_number, component_name)
    typer.echo(f"Cleared '{component.name}' (was {component.points})")


# Bonus points CRUD
@app.command()
def set_bonus(
    faculty_number: str = typer.Argument(..., help="Student's faculty number"),
    bonus: int = typer.Argument(..., help="Bonus points to set (0-5)"),
):
    """Set bonus points for a student."""
    student = table.set_bonus(faculty_number, bonus)
    typer.echo(f"Bonus for {student.faculty_number} set to {student.bonus}")


@app.command()
def get_bonus(
    faculty_number: str = typer.Argument(..., help="Student's faculty number"),
):
    """Get bonus points for a student."""
    bonus = table.get_bonus(faculty_number)
    typer.echo(f"Bonus for '{faculty_number}': {bonus}")


@app.command()
def clear_bonus(
    faculty_number: str = typer.Argument(..., help="Student's faculty number"),
):
    """Clear bonus points for a student."""
    student = table.clear_bonus(faculty_number)
    typer.echo(f"Bonus for {student.faculty_number} cleared (now {student.bonus})")


@app.command()
def add_bonus_point(
    faculty_number: str = typer.Argument(..., help="Student's faculty number"),
):
    """Add one bonus point to a student."""
    student = table.add_bonus_point(faculty_number)
    typer.echo(f"Bonus for {student.faculty_number} is now {student.bonus}")


# Totals and grading
@app.command()
def get_total_points(
    faculty_number: str = typer.Argument(..., help="Student's faculty number"),
):
    """Get total points for a student."""
    total = table.get_total_points_for_student(faculty_number)
    typer.echo(f"Total points for '{faculty_number}': {total}")


@app.command()
def calculate_grade(
    faculty_number: str = typer.Argument(..., help="Student's faculty number"),
):
    """Calculate the final grade for a student."""
    grade = table.calculate_grade(faculty_number)
    typer.echo(f"Grade for '{faculty_number}': {grade}")


@app.command()
def load_table(
    summary: bool = typer.Option(
        False,
        "--summary/--no-summary",
        help="Show summary view (name, total, grade) instead of full table.",
    ),
):
    """Load student data from a Google Sheets document and display it."""
    loaded = load("1NTZ26M6tKWzb5g7t0B83i4J-dQrqh7O-TnlAPxd4gsw")
    Console().print(render_table(loaded, summary=summary))


if __name__ == "__main__":
    app()
