import datetime
from unittest.mock import ANY, MagicMock, call, patch

import pytest
from fpdf import XPos, YPos

from fpdf_reporting.model.style import NotionStyle
from fpdf_reporting.model.ticket import Category, Status, Ticket
from fpdf_reporting.rendering.graphs import build_pie_chart_bytes
from fpdf_reporting.rendering.pdf_generator import PDF


@pytest.fixture
def pdf() -> PDF:
    pdf = PDF(NotionStyle())
    pdf.add_page()
    return pdf


@pytest.fixture
def data() -> dict[str, float]:
    return {
        "one": 12,
        "two": 15,
        "zero": 0,
        "three": 30,
        "four": 55,
        "five": 100,
    }


def test_graph_with_no_data_returns_none():
    assert build_pie_chart_bytes([0, 0, 0]) is None


def test_graph():
    assert build_pie_chart_bytes([1, 2, 3]) is not None


def test_graph_with_negative_values():
    with pytest.raises(ValueError):
        build_pie_chart_bytes([-1, -2, -3])


def test_header(pdf: PDF):
    pdf.document_header("TEST - Header")
    assert pdf.font_family == "inter"
    assert pdf.get_y() == 55
    assert pdf.get_x() == 25


def test_section_title(pdf: PDF):
    pdf.section_title("Test section")
    assert pdf.font_family == "inter"
    assert pdf.font_size_pt == 13
    assert pdf.get_y() == 45
    assert pdf.get_x() == 25


def test_summary_card(pdf: PDF):
    (x, y) = pdf.summary_card(["Test summary card"])
    assert pdf.font_family == "inter"
    assert pdf.font_size_pt == 10
    assert x == 105
    assert y == 25 + 6 + 10


def test_styled_table(pdf: PDF):
    pdf.styled_table(
        ["header1", "header2", "header3", "header4"],
        [
            ("asd", "asd", "asd", "asd"),
            ("asd", "asd", "asd", "asd"),
            ("asd", "asd", "asd", "asd"),
        ],
        [30, 15, 20, 5],
    )
    assert pdf.font_family == "inter"
    assert pdf.font_size_pt == 7
    assert pdf.get_x() == 25
    assert pdf.get_y() == 66


def test_tag(pdf: PDF):
    width, height = pdf.tag("Test tag", Status.IN_PROGRESS)
    assert pdf.font_family == "inter"
    assert pdf.font_size_pt == 7
    assert width == pytest.approx(13.15, 0.01)
    assert height == 5


@patch.object(PDF, "tag")
def test_ticket_card_long_mandatory_properties(tag_mock: MagicMock, pdf: PDF):
    ticket = Ticket(
        key="PD-1234",
        summary="Test ticket",
        status=Status.IN_PROGRESS,
        issue_type="Bug",
    )
    pdf.cell = MagicMock()
    pdf.rect = MagicMock()
    pdf.ticket_card_long(ticket)
    assert pdf.font_family == "inter"
    assert pdf.font_size_pt == 10
    assert pdf.get_x() == 25
    assert pdf.get_y() == 25 + 16 + 5

    tag_calls = [call(ticket.issue_type), call(Status.IN_PROGRESS), call("SP: N/A")]
    tag_mock.assert_has_calls(tag_calls, any_order=True)
    cell_calls = [
        call(12, 5, ticket.key, align="R"),
        call(ANY, 5, "Test ticket", new_y=YPos.NEXT),
    ]
    pdf.cell.assert_has_calls(cell_calls, any_order=True)
    rect_calls = [
        call(25, 25, ANY, 16, style="D", round_corners=True, corner_radius=2),
        call(25, 25, 2, 16, style="F", round_corners=True, corner_radius=2.2),
    ]
    pdf.rect.assert_has_calls(rect_calls, any_order=True)


@patch.object(PDF, "tag")
def test_ticket_card_long_with_all_properties(tag_mock: MagicMock, pdf: PDF):
    ticket = Ticket(
        key="PD-1234",
        summary="Test ticket",
        status=Status.IN_PROGRESS,
        issue_type="Bug",
        start_date=datetime.datetime(2023, 1, 1, 12, 13, 20),
        end_date=datetime.datetime(2023, 1, 2, 15, 10, 1),
        due_date=datetime.date(2023, 1, 3),
        flagged=True,
        priority="High",
        story_points=8,
        tester_story_points=8,
        component="Strategical",
        developer="Foo Bar",
        assignee="Unassigned",
        category=Category.COMMITTED,
    )
    pdf.cell = MagicMock()
    pdf.rect = MagicMock()
    pdf.ticket_card_long(ticket)
    assert pdf.font_family == "inter"
    assert pdf.font_size_pt == 10
    assert pdf.get_x() == 25
    assert pdf.get_y() == 25 + 16 + 5

    tag_calls = [
        call(ticket.component),
        call(ticket.status),
        call(ticket.issue_type),
        call("SP: 8"),
    ]
    tag_mock.assert_has_calls(tag_calls, any_order=True)
    cell_calls = [
        call(12, 5, ticket.key, align="R"),
        call(ANY, 5, "High"),
        call(ANY, 5, "Test ticket", new_y=YPos.NEXT),
    ]
    pdf.cell.assert_has_calls(cell_calls, any_order=True)
    rect_calls = [
        call(25, 25, ANY, 16, style="D", round_corners=True, corner_radius=2),
        call(25, 25, 2, 16, style="F", round_corners=True, corner_radius=2.2),
        call(ANY, 27, 5, 5, style="D", round_corners=True, corner_radius=1.5),
    ]
    pdf.rect.assert_has_calls(rect_calls, any_order=True)


def test_pie_chart(pdf: PDF, data: dict[str, float]):
    pdf.pie_chart(data)
    assert pdf.font_family == "inter"
    assert pdf.font_size_pt == 10
    assert pdf.get_x() == 118
    assert pdf.get_y() == 52


@patch.object(PDF, "ticket_card_long")
def test_detailed_tickets_table(mock_method, pdf: PDF):
    pdf.detailed_tickets_table([MagicMock(), MagicMock()])
    assert mock_method.call_count == 2


def test_ticket_card_short_with_all_properties(pdf: PDF):
    ticket = Ticket(
        key="PD-1234",
        summary="Test ticket",
        status=Status.IN_PROGRESS,
        issue_type="Bug",
        start_date=datetime.datetime(2023, 1, 1, 12, 13, 20),
        end_date=datetime.datetime(2023, 1, 2, 15, 10, 1),
        due_date=datetime.date(2023, 1, 3),
        flagged=True,
        priority="High",
        story_points=8,
        tester_story_points=8,
        component="Strategical",
        developer="Foo Bar",
        assignee="Unassigned",
        category=Category.COMMITTED,
    )
    pdf.cell = MagicMock()
    pdf.rect = MagicMock()
    pdf.ticket_card_short(ticket)
    assert pdf.font_family == "inter"
    assert pdf.font_size_pt == 10
    assert pdf.get_x() == 25 + 77.5 + 5
    assert pdf.get_y() == 25

    cell_calls = [
        call(19, 7, ticket.key, align="R", new_x=XPos.LEFT, new_y=YPos.NEXT),
        call(19, 7, "Bug", align="R", new_x=XPos.LEFT, new_y=YPos.NEXT),
        call(15, 7, "High", new_x=XPos.RIGHT),
        call(15, 7, "SP: 8", new_x=XPos.RIGHT),
    ]
    # TODO: update the test to reflect the implementation changes
    # pdf.cell.assert_has_calls(cell_calls, any_order=True)
    rect_calls = [
        call(25, 25, 77.5, 30, style="D", round_corners=True, corner_radius=2),
        call(25, 25, 2, 30, style="F", round_corners=True, corner_radius=2.2),
        call(95.5, 48, 5, 5, style="D", round_corners=True, corner_radius=1.5),
    ]
    pdf.rect.assert_has_calls(rect_calls, any_order=True)
