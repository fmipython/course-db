from fastapi import FastAPI

from course_db.services.calendar import load_calendar

app = FastAPI()


@app.get("/calendar")
def get_calendar():
    return load_calendar()
