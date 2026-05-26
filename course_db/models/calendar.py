from enum import StrEnum

from pydantic import BaseModel, Field


class EventType(StrEnum):
    LECTURE = "Тема"
    HOMEWORK_START = "Начало на домашно"
    HOMEWORK_END = "Край на домашно"
    WORKSHOP = "Workshop"
    CODING_DAYS = "Практика"
    PROJECT_TOPIC_SELECTION = "Избор на тема за проект"
    PROJECT_SUBMISSION = "Предаване на проект"
    EXAM = "Изпит"


class Event(BaseModel):
    name: str
    day: str
    date: str
    event_type: EventType


class Calendar(BaseModel):
    events: list[Event] = Field(default_factory=list)
