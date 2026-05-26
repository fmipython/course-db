import os

import dotenv

from course_db.models.calendar import Calendar, Event, EventType
from course_db.repository.google_sheets import setup_auth, load_raw


def group_by_threes(data: list) -> list[list]:
    grouped = [data[i : i + 3] for i in range(0, len(data), 3)]

    grouped = [
        [
            w,
            d,
            (
                e if len(e) == len(w) else e + [""] * (len(w) - len(e))
            ),  # Add padding to events
        ]
        for w, d, e in grouped
    ]
    return grouped


def load_calendar() -> Calendar:
    dotenv.load_dotenv()

    creds = setup_auth()

    raw = load_raw(creds, os.getenv("CALENDAR_SPREADSHEET_ID"), "Лист1!B4:H63")

    items = (
        (weekday, date, event)
        for weekdays, dates, events in group_by_threes(raw)
        for weekday, date, event in zip(weekdays, dates, events)
        if event != ""
    )

    events = []

    for weekday, date, event in items:
        if "Тема" in event:
            event_type = EventType.LECTURE
        elif "Домашно" in event:
            if "нач." in event:
                event_type = EventType.HOMEWORK_START
            elif "край" in event:
                event_type = EventType.HOMEWORK_END
            else:
                raise ValueError(f"Unknown homework event: {event}")
        elif "Workshop" in event:
            event_type = EventType.WORKSHOP
        elif "Практика" in event:
            event_type = EventType.CODING_DAYS
        elif "Проект" in event:
            if "избор на тема" in event:
                event_type = EventType.PROJECT_TOPIC_SELECTION
            elif "предаване" in event:
                event_type = EventType.PROJECT_SUBMISSION
            elif "защити" in event:
                event_type = EventType.EXAM
            else:
                raise ValueError(f"Unknown project event: {event}")
        else:
            continue  # Skip unknown events

        # TODO - Add handling of multiple events in one cell (e.g. "Тема 0, 2", "Тема 10, 11")
        events.append(Event(name=event, day=weekday, date=date, event_type=event_type))

    return Calendar(events=events)
