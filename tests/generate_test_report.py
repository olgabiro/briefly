import datetime
from pathlib import Path

from briefly.model.style import MochaStyle
from briefly.model.ticket import Ticket, Status, IssueType, Category
from briefly.rendering.pdf_generator import PDF

TEST_DIRECTORY = Path(__file__).parent
REPORT_PATH = TEST_DIRECTORY / "output/sample_report.pdf"

TEST_TICKETS = [
    Ticket(
        "PD-1234",
        "Prio 1 ticket that has a pretty long description - very urgent",
        Status.IN_PROGRESS,
        IssueType.PROD_BUG,
        priority="High",
        due_date=datetime.date(2025, 1, 1),
        story_points=5,
    ),
    Ticket(
        "PD-5678",
        "Committed improvement",
        Status.READY_FOR_QA,
        IssueType.IMPROVEMENT,
        priority="Medium",
        due_date=datetime.date(2025, 12, 22),
        story_points=8,
    ),
    Ticket(
        "PD-1245",
        "Nice to have feature",
        Status.IN_PROGRESS,
        IssueType.FEATURE,
        category=Category.NICE_TO_HAVE,
        priority="Medium",
        assignee="Foo Bar",
        due_date=datetime.date(2025, 5, 27),
        story_points=3,
    ),
    Ticket(
        "PD-7623",
        "Maybe bug",
        Status.READY_FOR_DEV,
        IssueType.BUG,
        category=Category.MAYBE,
        priority="Low",
        assignee="Foo Bar",
        due_date=datetime.date(2025, 5, 25),
    ),
    Ticket(
        "PD-4888",
        "Ticket without priority",
        Status.LOCAL_TESTING,
        IssueType.TASK,
        assignee="Foo Bar",
        due_date=datetime.date(2025, 9, 29),
        story_points=5,
    ),
    Ticket(
        "PD-4216",
        "Flagged ticket",
        Status.ON_HOLD,
        IssueType.BUG,
        flagged=True,
        assignee="Foo Bar",
        due_date=datetime.date(2025, 7, 28),
        story_points=13,
    ),
]

REPORT_STATISTICS = [
    {Category.COMMITTED: 2, Category.NICE_TO_HAVE: 1, Category.MAYBE: 1, "None": 1},
    {
        Status.READY_FOR_DEV: 15,
        Status.ON_HOLD: 2,
        Status.IN_PROGRESS: 7,
        Status.READY_FOR_QA: 8,
    },
    {
        "Strategical": 10,
        "Technical": 15,
        "Client Request": 5,
        "Platform Efficiency": 12,
    },
    {"1": 25, "2": 40, "3": 17, "None": 5},
]


def generate_report(report_path: Path) -> None:
    pdf = PDF(MochaStyle())
    pdf.add_page()
    pdf.document_header("Sample Report")
    pdf.section_title("Introduction")
    x, y = pdf.summary_card(
        [
            "This is a sample report generated using FPDF.",
            "It demonstrates basic PDF generation.",
        ],
        width=85,
    )

    pdf.set_x(x + 10)

    pdf.bar_chart(
        {
            Status.READY_FOR_DEV.value: 15,
            Status.ON_HOLD.value: 2,
            Status.IN_PROGRESS.value: 7,
            Status.READY_FOR_QA.value: 8,
        },
        "Story points by status",
        30,
    )

    pdf.set_y(y + 10)
    pdf.section_title("Tickets")
    for ticket in TEST_TICKETS:
        pdf.ticket_card_short(ticket)

    pdf.add_page()
    pdf.section_title("Statistics")

    pdf.bar_chart(REPORT_STATISTICS[0], "Story points by category", height=30)
    pdf.pie_chart(REPORT_STATISTICS[1], "Story points by status", 30)
    pdf.bar_chart(REPORT_STATISTICS[2], "Story points by component", height=30)
    pdf.pie_chart(REPORT_STATISTICS[3], "Story points by priority", 30)

    pdf.output(str(report_path))


if __name__ == "__main__":
    generate_report(REPORT_PATH)
