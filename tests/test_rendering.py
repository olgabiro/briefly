from datetime import date, datetime
from unittest.mock import MagicMock, call

import pytest
from fpdf import XPos, YPos
from fpdf.enums import MethodReturnValue

from briefly.model.style import NotionStyle
from briefly.rendering.graphs import build_pie_chart_bytes
from briefly.rendering.icons import DUE_DATE_ICON, FLAG_ICON, PRIORITY_ICON
from briefly.rendering.pdf_generator import PDF


@pytest.fixture
def pdf() -> PDF:
    pdf = PDF(NotionStyle())
    pdf.add_page()
    return pdf


@pytest.fixture
def data() -> dict[str, float]:
    return {
        "one": 12,
        "two": 0,
        "three": 30,
        "four": 55,
    }


def test_graph_with_no_data_returns_none():
    assert build_pie_chart_bytes([0, 0, 0]) is None


def test_graph():
    assert build_pie_chart_bytes([1, 2, 3]) is not None


def test_graph_with_negative_values():
    with pytest.raises(ValueError):
        build_pie_chart_bytes([-1, -2, -3])


def test_header(pdf: PDF):
    pdf.main_title("TEST - Header")
    assert pdf.font_family == "inter"
    assert pdf.get_y() == 55
    assert pdf.get_x() == 25


def test_section_title(pdf: PDF):
    pdf.section_title("Test section")
    assert pdf.font_family == "inter"
    assert pdf.font_size_pt == 10
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
            ["asd", "asd", "asd", "asd"],
            ["asd", "asd", "asd", "asd"],
            ["asd", "asd", "asd", "asd"],
        ],
        [30, 15, 20, 5],
    )
    assert pdf.font_family == "inter"
    assert pdf.font_size_pt == 7
    assert pdf.get_x() == 25
    assert pdf.get_y() == 66


def test_tag(pdf: PDF):
    width, height = pdf.tag("Test tag")
    assert pdf.font_family == "inter"
    assert pdf.font_size_pt == 7
    assert width == pytest.approx(13.15, 0.01)
    assert height == 5


def test_pie_chart(pdf: PDF, data: dict[str, float]):
    x, y = pdf.pie_chart(data, "Test Pie Chart")
    assert pdf.font_family == "inter"
    assert pdf.font_size_pt == 10
    assert x == pytest.approx(121, 0.1)
    assert y == 54


def test_task_card_with_all_properties(pdf: PDF):
    task_id = "TEST-1234"
    status = "In Progress"
    due_date = date(2025, 1, 3)
    flagged = True
    priority = 1
    estimate = 5
    title = "Test task"
    link = "link"

    pdf.cell = MagicMock()
    pdf.accent_card = MagicMock()
    pdf._two_line_label = MagicMock()
    pdf._two_line_label.return_value = 30, 30
    pdf._priority_icons = MagicMock()
    pdf._priority_icons.return_value = 30, 30
    pdf._small_label = MagicMock()
    pdf._small_label.return_value = 30, 30
    pdf._flagged_icon = MagicMock()
    pdf._task_title = MagicMock()
    pdf.task_card(task_id, title, status, due_date, priority, estimate, flagged, link)

    pdf.accent_card.assert_called_once_with((252, 216, 212), 77.5, 30)
    pdf._two_line_label.assert_called_once_with(status, 37.5, 35)
    pdf._priority_icons.assert_called_once_with(priority, flagged, 36, 31)
    pdf._flagged_icon.assert_called_once_with(36, 31)
    pdf._task_title.assert_called_once_with(title, 52.5, 29, link=link)

    label_calls = [call("SP: 5", 30, 31), call("03.01.2025", 37.5, 31)]
    pdf._small_label.assert_has_calls(label_calls, any_order=True)
    cell_calls = [
        call(15, 5, task_id, align="R", link=link, new_x=XPos.LEFT, new_y=YPos.NEXT),
        call(3, 5, DUE_DATE_ICON, align="L"),
    ]
    pdf.cell.assert_has_calls(cell_calls, any_order=True)


def test_footer(pdf: PDF):
    pdf.generation_time = datetime(2025, 1, 2, 15, 30, 45)
    pdf.cell = MagicMock()
    pdf.footer()

    cell_calls = [
        call(0, 10, "02.01.2025 15:30:45", align="L"),
        call(0, 10, "Page 1", align="R"),
    ]
    pdf.cell.assert_has_calls(cell_calls, any_order=True)


def test_divider(pdf: PDF):
    pdf.line = MagicMock()
    pdf.divider()
    pdf.line.assert_called_once_with(25, 30, pytest.approx(185, 0.01), 30)


def test_break_page_if_needed(pdf: PDF):
    pdf.add_page = MagicMock()

    pdf.set_y(30)
    pdf._break_page_if_needed(10)
    pdf.add_page.assert_not_called()

    pdf.set_y(200)
    pdf._break_page_if_needed(100)
    pdf.add_page.assert_called_once()


def test__task_title(pdf: PDF):
    pdf.cell = MagicMock()
    pdf.multi_cell = MagicMock()

    title = "Short task"
    pdf.multi_cell.return_value = [title]
    pdf._task_title(title, 30, 30)
    pdf.multi_cell.assert_called_once_with(
        45, 15, title, max_line_height=4, dry_run=True, output=MethodReturnValue.LINES
    )
    pdf.cell.assert_called_once_with(45, 5, title, align="L", link=0)

    title = "Medium task with multiple lines"
    pdf.multi_cell.return_value = ["Medium task", "with multiple lines"]
    pdf._task_title(title, 30, 30)
    pdf.multi_cell.assert_called_with(
        45, 15, title, align="L", max_line_height=4, link=0
    )

    title = "Very very very very very very long task with an incredibly long title"
    pdf.multi_cell.return_value = [
        "Very very very",
        "long task",
        "with an",
        "incredibly long",
        "title",
    ]
    pdf._trim_with_ellipsis = MagicMock(return_value="incredibly long ...")
    pdf._task_title(title, 30, 30)
    expected_title = "Very very very long task with an incredibly long ..."
    pdf.multi_cell.assert_called_with(
        45, 15, expected_title, align="L", max_line_height=4, link=0
    )
    pdf._trim_with_ellipsis.assert_called_once_with("incredibly long", 45)


def test__trim_with_ellipsis(pdf: PDF):
    pdf.get_string_width = MagicMock()
    pdf.get_string_width.side_effect = lambda text: len(text) * 2
    assert pdf._trim_with_ellipsis("test", 10) == "test"
    assert pdf._trim_with_ellipsis("test test", 10) == "..."
    assert pdf._trim_with_ellipsis("test test", 15) == "test..."


def test__priority_icons(pdf: PDF):
    pdf.cell = MagicMock()
    pdf.set_text_color = MagicMock()

    pdf._priority_icons(None, False, 10, 10)
    pdf.cell.assert_not_called()

    pdf._priority_icons(1, False, 10, 10)
    expected_icons = PRIORITY_ICON * 4
    pdf.cell.assert_called_with(15, 5, expected_icons)
    text_color_calls = [
        call(*pdf.style.priority_color),
        call(*pdf.style.font_color),
    ]
    pdf.set_text_color.assert_has_calls(text_color_calls)

    pdf._priority_icons(2, False, 10, 10)
    expected_icons = PRIORITY_ICON * 3
    pdf.cell.assert_called_with(15, 5, expected_icons)
    text_color_calls = [
        call(*pdf.style.font_color),
    ]
    pdf.set_text_color.assert_has_calls(text_color_calls)

    pdf._priority_icons(3, False, 10, 10)
    expected_icons = PRIORITY_ICON * 2
    pdf.cell.assert_called_with(15, 5, expected_icons)
    text_color_calls = [
        call(*pdf.style.font_color),
    ]
    pdf.set_text_color.assert_has_calls(text_color_calls)

    pdf._priority_icons(4, False, 10, 10)
    expected_icons = PRIORITY_ICON
    pdf.cell.assert_called_with(15, 5, expected_icons)
    text_color_calls = [
        call(*pdf.style.font_color),
    ]
    pdf.set_text_color.assert_has_calls(text_color_calls)

    pdf._priority_icons(3, True, 10, 10)
    expected_icons = PRIORITY_ICON * 2
    pdf.cell.assert_called_with(15, 5, expected_icons)
    text_color_calls = [
        call(*pdf.style.disabled_color),
    ]
    pdf.set_text_color.assert_has_calls(text_color_calls)


def test__small_label(pdf: PDF):
    pdf.cell = MagicMock()
    x, y = pdf._small_label("text", 30, 50)
    pdf.cell.assert_called_once_with(15, 5, "text", align="R")
    assert x == 45
    assert y == 53


def test__two_line_label(pdf: PDF):
    pdf.multi_cell = MagicMock()
    x, y = pdf._two_line_label("text", 30, 50)
    pdf.multi_cell.assert_called_once_with(15, 6, "text", align="R", max_line_height=3)
    assert x == 45
    assert y == 50


def test__flagged_icon(pdf: PDF):
    pdf.cell = MagicMock()
    pdf._flagged_icon(30, 50)
    assert pdf.x == 30
    assert pdf.y == 50
    pdf.cell.assert_called_once_with(3, 5, FLAG_ICON, align="R")


def test__accent_card(pdf: PDF):
    pdf.rect = MagicMock()
    pdf.set_fill_color = MagicMock()
    pdf.set_draw_color = MagicMock()

    color = (40, 40, 50)
    pdf.accent_card(color, 100, 30)

    rect_calls = [
        call(25, 25, 100, 30, style="D", round_corners=True, corner_radius=2),
        call(25, 25, 2, 30, style="F", round_corners=True, corner_radius=2.2),
    ]
    pdf.rect.assert_has_calls(rect_calls)
    pdf.set_fill_color.assert_called_once_with(*color)
    pdf.set_draw_color.assert_called_once_with(*pdf.style.border_color)


def test__draw_gridlines(pdf: PDF):
    pdf.line = MagicMock()
    pdf._draw_gridlines(25, 25, 20, 30)
    line_calls = [
        call(25, 25, 30, 25),
        call(25, 30, 30, 30),
        call(25, 35, 30, 35),
        call(25, 40, 30, 40),
    ]
    pdf.line.assert_has_calls(line_calls)


def test__plot_bar_chart(pdf: PDF):
    pdf.rect = MagicMock()
    x, y = pdf._plot_bar_chart([], 30, 70)
    assert x == 25
    assert y == 25
    pdf.rect.assert_not_called()

    pdf._plot_bar_chart([1, 2, 4], 30, 70)
    rect_calls = [
        call(27, 47.5, 3, 7.5, style="F", round_corners=True, corner_radius=0.5),
        call(32, 40.0, 3, 15.0, style="F", round_corners=True, corner_radius=0.5),
        call(37, 25.0, 3, 30.0, style="F", round_corners=True, corner_radius=0.5),
    ]
    pdf.rect.assert_has_calls(rect_calls)
