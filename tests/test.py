import datetime
import random

import pytest

from fpdf_reporting.model.style import MochaStyle
from fpdf_reporting.model.ticket import Category, Status, Ticket
from fpdf_reporting.rendering.pdf_generator import PDF

DARK_BACKGROUND = (38, 33, 43)


def create_ticket():
    status = random.choice(list(Status))
    category = random.choices([random.choice(list(Category)), None], weights=[9, 1])[0]
    issue_type = random.choice(["Bug", "Improvement", "Feature", "Prod Bug"])
    due_day = random.randint(1, 31)
    start_day = random.randint(1, due_day)
    end_day = random.choices([random.randint(start_day, 31), None], weights=[2, 8])[0]
    story_points = random.choice([1, 2, 3, 5, 8, 13, 21, None])
    component = random.choice(
        ["Strategical", "Platform", "Technical", "Client Request", None]
    )
    return Ticket(
        key=f"PR-{random.randint(1000, 9999)}",
        summary=f"Test ticket {random.randint(1, 100)}",
        status=status,
        issue_type=issue_type,
        start_date=datetime.datetime(2025, 12, start_day),
        end_date=datetime.datetime(2025, 12, end_day) if end_day else None,
        due_date=datetime.date(2025, 12, due_day),
        flagged=random.choice([True, False]),
        priority=random.choice(["High", "Medium", "Low", None]),
        story_points=story_points,
        component=component,
        developer="John Doe",
        assignee="Alice Smith",
        category=category,
    )


@pytest.mark.skip(reason="Manually run")
def test():
    style = MochaStyle()
    pdf = PDF(style)
    pdf.add_page()

    pdf.document_header("JIRA Summary Test")

    pdf.section_title("Overview")
    pdf.summary_card(
        ["Total Tickets: 58", "Completed: 42", "In Progress: 10", "Blocked: 6"],
        width=50,
    )

    pdf.summary_card(
        ["Total Tickets: 58", "Completed: 42", "In Progress: 10", "Blocked: 6"],
        width=50,
    )

    (_, y) = pdf.summary_card(
        ["Total Tickets: 58", "Completed: 42", "In Progress: 10", "Blocked: 6"],
        width=50,
    )

    pdf.set_y(y + 10)

    pdf.styled_table(
        headers=["Key", "Summary", "Status", "Assignee"],
        rows=[
            ("PROJ-101", "Fix login flow", "Done", "Alice"),
            ("PROJ-102", "Add metrics dashboard", "In Progress", "Bob"),
            ("PROJ-103", "Payment gateway issue", "Blocked", "Eve"),
        ],
        col_widths=[20, 80, 30, 30],
    )

    pdf.detailed_tickets_table(tickets=[create_ticket() for _ in range(10)])

    for _ in range(10):
        pdf.ticket_card_short(create_ticket())

    data = {
        "cat1": 10,
        "cat3": 8,
        "cat2": 5,
        "cat4": 3,
        "cat5": 2,
        "cat6": 20,
        "cat7": 15,
        "cat8": 10,
    }

    pdf.bar_chart(data, caption="Categories", height=30)

    pdf.pie_chart(
        data,
        width=30,
        caption="Categories",
    )

    pdf.pie_chart(
        data,
        width=30,
        caption="Categories",
    )

    pdf.bar_chart(data, caption="Categories", height=30)
    pdf.bar_chart(data, caption="Categories", height=30)
    pdf.output("./output/test.pdf")
