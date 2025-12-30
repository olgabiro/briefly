from pathlib import Path
from typing import Any, List, Optional, Tuple

from fpdf import FPDF, XPos, YPos

from fpdf_reporting.model.style import Style
from fpdf_reporting.model.ticket import Status, Ticket
from fpdf_reporting.rendering.graphs import build_pie_chart_bytes

FONT_FAMILY: str = "Inter"
HEADER_SIZE: int = 20
SECTION_TITLE_SIZE: int = 13
TEXT_SIZE: int = 10
LABEL_SIZE: int = 7
MARGIN_SIZE: int = 25

_SMALL_SPACING: float = 2
_MEDIUM_SPACING: float = 5
_LARGE_SPACING: float = 10

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "fonts"


class PDF(FPDF):
    style: Style

    def __init__(self, style: Style, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.style = style
        self.set_margin(MARGIN_SIZE)
        self.add_font(FONT_FAMILY, "", OUTPUT_DIR / "Inter-Regular.ttf")
        self.add_font(FONT_FAMILY, "B", OUTPUT_DIR / "Inter-Bold.ttf")
        self.add_font(FONT_FAMILY, "I", OUTPUT_DIR / "Inter-Italic.ttf")

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font(FONT_FAMILY, "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def document_header(self, text: str) -> None:
        self.set_font(FONT_FAMILY, "B", size=HEADER_SIZE)
        self.set_fill_color(*self.style.header_background)
        self.set_text_color(*self.style.header_color)
        self.cell(
            0,
            HEADER_SIZE,
            text,
            align="C",
            fill=True,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        self.set_y(self.get_y() + _LARGE_SPACING)

    def divider(self) -> None:
        self.set_draw_color(*self.style.border_color)
        x1, x2 = MARGIN_SIZE, self.w - MARGIN_SIZE
        y = self.get_y() + _MEDIUM_SPACING
        self.line(x1, y, x2, y)
        self.ln(_MEDIUM_SPACING)

    def section_title(self, text: str) -> None:
        self.set_font(FONT_FAMILY, "B", SECTION_TITLE_SIZE)
        self.set_text_color(*self.style.section_title_color)
        self.cell(0, 10, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(self.get_x(), self.get_y() + _LARGE_SPACING)

    def summary_card(
        self,
        items: List[str],
        width: int = 80,
        x: Optional[float] = None,
        y: Optional[float] = None,
    ) -> tuple[float, float]:
        start_x = x or self.x
        start_y = y or self.y
        padding = _MEDIUM_SPACING
        row_height = 6
        card_height = (len(items) * row_height) + 2 * padding

        if start_y + card_height >= self.h - self.b_margin:
            self.add_page()

        self.set_fill_color(*self.style.card_background)
        self.rect(
            start_x,
            start_y,
            width,
            card_height,
            style="F",
            round_corners=True,
            corner_radius=1.5,
        )
        self.set_font(FONT_FAMILY, "", TEXT_SIZE)
        self.set_text_color(*self.style.font_color)

        x = start_x + padding
        y = start_y + padding
        self.set_text_color(*self.style.card_details_color)
        for text in items:
            self.set_xy(x, y)
            self.cell(width - 2 * padding, row_height, text, align="L")
            y = y + row_height

        if start_x + width >= self.w - self.r_margin:
            self.set_xy(self.l_margin, start_y + card_height + padding)
        else:
            self.set_xy(start_x + width + padding, start_y)
        return start_x + width, start_y + card_height

    def styled_table(
        self,
        headers: list[str],
        rows: list[tuple[str, str, str, str]],
        col_widths: list[int],
    ) -> None:
        self.set_font(FONT_FAMILY, "B", TEXT_SIZE)
        self.set_fill_color(*self.style.table_header_color)
        self.set_text_color(*self.style.font_color)

        for i, h in enumerate(headers):
            self.cell(col_widths[i], 10, h, border="B", fill=True)
        self.ln(10)

        # rows
        self.set_font(FONT_FAMILY, "", LABEL_SIZE)

        for idx, row in enumerate(rows):
            self.set_fill_color(*self.style.table_row_colors[idx % 2])
            self.set_text_color(*self.style.font_color)

            for i, cell in enumerate(row):
                self.cell(col_widths[i], LABEL_SIZE, cell, border="B", fill=True)

            self.ln()
        self.set_y(self.get_y() + _LARGE_SPACING)

    def tag(self, text: str, status: Optional[Status] = None) -> Tuple[float, float]:
        bg = self.style.status_colors.get(
            status or Status.OTHER, self.style.status_colors[Status.OTHER]
        )
        self.set_font(FONT_FAMILY, "", LABEL_SIZE)
        self.set_text_color(*self.style.font_color)

        text_w = self.get_string_width(text) + _SMALL_SPACING * 2
        text_h = 5
        x, y = self.x, self.y

        self.set_fill_color(*bg)
        self.rect(
            x, y, text_w, text_h, style="F", round_corners=True, corner_radius=1.5
        )

        self.cell(text_w, text_h, text, align="C")
        self.set_x(x + text_w)
        return text_w, text_h

    def detailed_tickets_table(self, tickets: list[Ticket]) -> None:
        self.set_font(FONT_FAMILY, "", TEXT_SIZE)

        for t in tickets:
            self.ticket_card_long(t)

    def ticket_card_long(self, ticket: Ticket) -> None:
        width = self.w - self.r_margin - self.l_margin
        height = 16
        if self.y + height >= self.h - self.b_margin:
            self.add_page()
        start_x = self.x
        start_y = self.y
        left_padding = 6
        block_width = 20

        self.set_draw_color(*self.style.border_color)
        self.rect(start_x, start_y, width, height, round_corners=True, corner_radius=2)
        stripe_color: tuple[int, int, int] = self.style.category_colors.get(
            ticket.category, self.style.border_color
        )
        self.set_fill_color(*stripe_color)
        self.rect(
            start_x,
            start_y,
            2,
            height,
            style="F",
            round_corners=True,
            corner_radius=2.2,
        )

        self.set_xy(start_x + left_padding, start_y + _SMALL_SPACING)
        key_width = 12
        self.tag(ticket.status)
        self.set_font(FONT_FAMILY, "B", LABEL_SIZE)
        self.set_text_color(*self.style.font_color)
        self.set_x(start_x + left_padding + block_width)
        self.cell(key_width, 5, ticket.key, align="R")
        self.set_font(FONT_FAMILY, "", TEXT_SIZE)
        title_width = (
            width - key_width - left_padding - _SMALL_SPACING - block_width - 5
        )
        self.cell(title_width, 5, ticket.summary, new_y=YPos.NEXT)
        if ticket.flagged:
            self.rect(
                self.x,
                start_y + _SMALL_SPACING,
                5,
                5,
                style="D",
                round_corners=True,
                corner_radius=1.5,
            )
            self.set_fill_color(*self.style.priority_colors["High"])
            self.ellipse(self.x + 1.5, start_y + _SMALL_SPACING + 1.5, 2, 2, style="F")

        self.set_xy(start_x + left_padding, self.y + _SMALL_SPACING)
        if ticket.priority:
            dot_color: tuple[int, int, int] = self.style.priority_colors.get(
                ticket.priority, (217, 241, 208)
            )
            self.legend_label(dot_color, ticket.priority)

        self.set_x(start_x + left_padding + block_width)
        self.tag(ticket.issue_type)
        self.set_x(start_x + left_padding + block_width * 2)
        self.tag(f"SP: {ticket.story_points or 'N/A'}")
        self.set_x(start_x + left_padding + block_width * 3)
        if ticket.component:
            self.tag(ticket.component)
        self.set_y(start_y + height + _MEDIUM_SPACING)

    def ticket_card_short(self, ticket: Ticket) -> None:
        width = 77.5
        height = 30

        if self.y + height >= self.h - self.b_margin:
            self.add_page()

        start_x = self.x
        start_y = self.y
        label_width = 15
        summary_start = start_x + 24
        row_height = 7

        self.set_draw_color(*self.style.border_color)
        self.rect(
            start_x,
            start_y,
            width,
            height,
            style="D",
            round_corners=True,
            corner_radius=2,
        )
        stripe_color: tuple[int, int, int] = self.style.category_colors.get(
            ticket.category, self.style.border_color
        )
        self.set_fill_color(*stripe_color)
        self.rect(
            start_x,
            start_y,
            2,
            height,
            style="F",
            round_corners=True,
            corner_radius=2.2,
        )

        self.set_xy(start_x + _MEDIUM_SPACING, start_y + _SMALL_SPACING)
        self.set_font(FONT_FAMILY, "B", LABEL_SIZE)
        self.cell(
            19, row_height, ticket.key, align="R", new_x=XPos.LEFT, new_y=YPos.NEXT
        )
        self.set_font(FONT_FAMILY, "", LABEL_SIZE)
        self.cell(
            19,
            row_height,
            ticket.issue_type,
            align="R",
            new_x=XPos.LEFT,
            new_y=YPos.NEXT,
        )
        self.tag(ticket.status, ticket.status)
        self.set_x(summary_start)
        self.cell(label_width, row_height, ticket.priority or "N/A", new_x=XPos.RIGHT)
        self.cell(
            label_width,
            row_height,
            f"SP: {ticket.story_points or 'N/A'}",
            new_x=XPos.RIGHT,
        )

        self.set_font(FONT_FAMILY, "", TEXT_SIZE)
        self.set_xy(summary_start, start_y + _SMALL_SPACING)
        self.multi_cell(
            46, 14.5, ticket.summary, max_line_height=7, align="L", new_y=YPos.NEXT
        )

        if ticket.flagged:
            self.rect(
                start_x + width - _SMALL_SPACING - 5,
                start_y + height - _SMALL_SPACING - 5,
                5,
                5,
                style="D",
                round_corners=True,
                corner_radius=1.5,
            )
            self.set_fill_color(*self.style.priority_colors["High"])
            self.ellipse(
                start_x + width - _SMALL_SPACING - 3.5,
                start_y + height - _SMALL_SPACING - 3.5,
                2,
                2,
                style="F",
            )

        if start_x == self.l_margin:
            self.set_xy(start_x + width + _MEDIUM_SPACING, start_y)
        else:
            self.set_y(start_y + height + _MEDIUM_SPACING)

    def _plot_bar_chart(self, values: list[float]) -> tuple[float, float]:
        spacing = 2
        bar_width = 3
        x = self.x
        start_y = self.y
        height = 30
        width = x + len(values) * (bar_width + spacing) + spacing
        max_value = max(values) if values else 0

        self.line(x, start_y, width, start_y)
        self.line(x, start_y + 5, width, start_y + 5)
        self.line(x, start_y + 10, width, start_y + 10)
        self.line(x, start_y + 15, width, start_y + 15)
        self.line(x, start_y + 20, width, start_y + 20)
        self.line(x, start_y + 25, width, start_y + 25)

        x += spacing

        for index, value in enumerate(values):
            self.set_fill_color(
                *self.style.chart_colors[index % len(self.style.chart_colors)]
            )
            bar_height = height * value / max_value
            y = start_y + height - bar_height
            self.rect(
                x,
                y,
                bar_width,
                bar_height,
                style="F",
                round_corners=True,
                corner_radius=1.5,
            )
            x += bar_width + spacing

        return x - spacing, start_y + height

    def bar_chart(
        self, data: dict[str, float], caption: Optional[str] = None
    ) -> tuple[float, float]:
        x = self.x
        y = self.y
        self._plot_bar_chart(list(data.values()))
        self.legend(list(data.keys()), x + 30, y + _SMALL_SPACING, caption=caption)
        self.set_xy(self.x + 15, y)
        return self.x, y + 30

    def pie_chart(
        self,
        data: dict[str, float],
        width: float = 70,
        caption: Optional[str] = None,
    ) -> None:
        """Generate a pie chart in-memory and insert it into the PDF."""
        img_buf = build_pie_chart_bytes(
            list(data.values()), colors=self.style.chart_colors
        )

        if img_buf is None:
            return

        x = self.get_x()
        y = self.get_y()

        self.image(img_buf, x=x, y=y, w=width)
        self.set_xy(x + width, y)

        legend_x = x + width + _MEDIUM_SPACING
        legend_y = y + _SMALL_SPACING
        self.legend(list(data.keys()), legend_x, legend_y, caption=caption)

    def legend(
        self, labels: list[str], x: float, y: float, caption: Optional[str] = None
    ) -> None:
        if caption:
            self.set_xy(x - 1, y)
            self.set_font(FONT_FAMILY, "", 9)
            self.cell(0, 5, caption, align="L")
            y += 5 + _SMALL_SPACING

        self.set_font(FONT_FAMILY, "", 9)
        legend_colors = self.style.chart_colors
        for idx, label in enumerate(labels):
            color = legend_colors[idx % len(legend_colors)]
            (_, y) = self.legend_label(color, label, x, y)

    def legend_label(
        self,
        color: tuple[int, int, int],
        label: str,
        x: Optional[float] = None,
        y: Optional[float] = None,
    ) -> tuple[float, float]:
        """
        Generates a legend label with a colored dot. The label object has the height of 5mm.
        :param color: the color of the dot
        :param label: the text of the label
        :param x: the x position of the label (optional)
        :param y: the y position of the label (optional)
        :return: the position of the bottom right corner of the label
        """
        start_x = x or self.x
        start_y = y or self.y

        self.set_xy(start_x, start_y)
        self.set_fill_color(*color)
        self.ellipse(start_x + 1, start_y + 1.5, 2, 2, style="F")
        self.set_x(start_x + 3)
        self.set_font(FONT_FAMILY, "", LABEL_SIZE)
        self.set_text_color(*self.style.font_color)
        self.cell(15, 5, label)
        self.set_font(FONT_FAMILY, "", TEXT_SIZE)
        return start_x + 18, start_y + 5
