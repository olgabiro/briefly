from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum
from typing import Optional


class Category(StrEnum):
    COMMITTED = "Committed"
    NICE_TO_HAVE = "Nice to have"
    MAYBE = "Maybe"


class Status(StrEnum):
    order: int
    DRAFT = ("Draft", 0)
    OPEN = ("Open", 1)
    READY_FOR_DEV = ("Ready for dev", 2)
    ON_HOLD = ("On Hold", 3)
    IN_PROGRESS = ("In progress", 4)
    READY_FOR_QA = ("Ready for QA", 5)
    LOCAL_TESTING = ("Local testing", 6)
    READY_TO_MERGE = ("Ready to merge", 7)
    DELIVERED = ("Delivered", 8)
    OTHER = ("Other", 9)

    def __new__(cls, value: str, order: int) -> Status:
        obj = str.__new__(cls)
        obj._value_ = value
        obj.order = order
        return obj


class IssueType(StrEnum):
    BUG = "Bug"
    TASK = "Task"
    IMPROVEMENT = "Improvement"
    FEATURE = "Feature"
    PROD_BUG = "Prod Bug"


@dataclass(slots=True)
class Ticket:
    key: str
    summary: str
    status: Status
    issue_type: IssueType
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    due_date: Optional[date] = None
    flagged: bool = False
    priority: Optional[str] = None
    story_points: Optional[int] = None
    tester_story_points: Optional[float] = None
    component: Optional[str] = None
    developer: Optional[str] = None
    assignee: Optional[str] = None
    category: Optional[Category] = None
