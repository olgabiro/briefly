"""
Styles used by the PDF generator.

Pre-defined styles:
 - **PURPLE_HAZE** (default): Light theme with purple color scheme
 - **NOTION**: Light theme inspired by Notion design
 - **LATTE**: Light theme using Catpuccin's Latte color scheme
 - **MOCHA**: Dark theme using Catpuccin's Mocha color scheme
"""

from dataclasses import dataclass, fields, field
from typing import Tuple

STRIPE_DARK = (10, 37, 64)
STRIPE_LIGHT_BG = (246, 249, 252)
STRIPE_GRAY_TEXT = (66, 84, 102)
STRIPE_HEADER_BG = (230, 236, 244)
STRIPE_ACCENT = (99, 91, 255)
STRIPE_ROW_ALT = (242, 245, 252)

MINIMALIST_HEADER_BG = (45, 62, 80)
MINIMALIST_TEXT_COLOR = (255, 255, 255)
MINIMALIST_TEXT_COLOR_GRAY = (45, 62, 80)
MINIMALIST_ROW_ALT = (247, 249, 252)

Color = Tuple[int, int, int]


def _validate_color(name: str, c: Color) -> None:
    if not (
        isinstance(c, tuple) and len(c) == 3 and all(isinstance(x, int) for x in c)
    ):
        raise TypeError(f"{name} must be a 3-tuple of ints")
    for x in c:
        if not (0 <= x <= 255):
            raise ValueError(f"{name} color components must be 0..255")


@dataclass(frozen=True)
class Style:
    """
    Defines the visual style of the generated PDF report.

    :ivar background_color(Color): The background color of the report
    :ivar chart_colors: List of colors to use for charts
    :ivar priority_color: Color used to highlight tasks with priority 1
    :ivar card_background: Background color for summary cards
    :ivar header_background: Background color for the main title
    :ivar table_header_color: Color of table headers
    :ivar table_row_colors: List of colors to use for alternating table rows
    :ivar font_color: Color of the main text
    :ivar section_title_color: Color of section titles
    :ivar border_color: Color of card borders, table borders, and chart gridlines
    :ivar header_color: Color of the main title
    :ivar disabled_color: Color of disabled elements (i.e., flagged task cards)
    """

    background_color: Color = field(metadata={"doc": "Background color of the report"})
    chart_colors: list[Color]
    priority_color: Color
    card_background: Color
    header_background: Color
    table_header_color: Color
    table_row_colors: list[Color]
    font_color: Color
    section_title_color: Color
    border_color: Color
    header_color: Color
    disabled_color: Color

    def __post_init__(self) -> None:
        # runtime validation for basic invariants
        for name, value in ((f.name, getattr(self, f.name)) for f in fields(self)):
            if value is None:
                raise ValueError(f"Style field '{name}' must not be None")
            if isinstance(value, tuple):
                _validate_color(name, value)
            if isinstance(value, list):
                for c in value:
                    _validate_color(f"{name}[]", c)


PURPLE_HAZE = Style(
    background_color=(255, 255, 255),
    font_color=(43, 34, 43),
    header_color=(255, 255, 255),
    header_background=(129, 126, 160),
    section_title_color=(43, 34, 43),
    card_background=(247, 246, 243),
    table_header_color=(189, 184, 203),
    table_row_colors=[(255, 255, 255), (247, 246, 243)],
    border_color=(232, 227, 232),
    priority_color=(191, 106, 95),
    disabled_color=(167, 154, 167),
    chart_colors=[
        (68, 68, 118),
        (91, 91, 135),
        (115, 115, 152),
        (138, 138, 169),
        (161, 161, 186),
        (185, 185, 203),
        (208, 208, 220),
        (232, 232, 238),
    ],
)

NOTION = Style(
    priority_color=(252, 216, 212),
    chart_colors=[
        (155, 207, 87),  # green
        (246, 199, 68),  # yellow
        (108, 155, 245),  # blue
        (221, 148, 255),  # purple
        (255, 170, 153),  # coral
        (181, 181, 181),  # gray
        (212, 228, 247),
        (255, 232, 163),
        (252, 216, 212),
        (217, 241, 208),
    ],
    card_background=(255, 238, 189),
    header_background=(247, 246, 243),
    table_header_color=(243, 242, 239),
    table_row_colors=[(255, 255, 255), (250, 249, 247)],
    font_color=(55, 53, 47),
    section_title_color=(55, 53, 47),
    disabled_color=(165, 159, 141),
    background_color=(255, 255, 255),
    border_color=(230, 230, 230),
    header_color=(55, 53, 47),
)

LATTE = Style(
    background_color=(239, 241, 245),
    chart_colors=[
        (220, 138, 120),
        (221, 120, 120),
        (234, 118, 203),
        (136, 57, 239),
        (210, 15, 57),
        (230, 69, 83),
        (254, 100, 11),
        (223, 142, 29),
        (64, 160, 43),
        (23, 146, 153),
        (4, 165, 229),
        (32, 159, 181),
        (30, 102, 245),
        (114, 135, 253),
    ],
    priority_color=(210, 15, 57),
    card_background=(220, 224, 232),
    header_background=(220, 138, 120),
    table_header_color=(172, 176, 190),
    table_row_colors=[(220, 224, 232), (188, 192, 204)],
    font_color=(76, 79, 105),
    section_title_color=(92, 95, 119),
    border_color=(156, 160, 176),
    header_color=(76, 79, 105),
    disabled_color=(188, 192, 204),
)

MOCHA = Style(
    background_color=(30, 30, 46),
    chart_colors=[
        (245, 224, 220),
        (242, 205, 205),
        (245, 194, 231),
        (203, 166, 247),
        (243, 139, 168),
        (235, 160, 172),
        (250, 179, 135),
        (249, 226, 175),
        (166, 227, 161),
        (148, 226, 213),
        (137, 220, 235),
        (116, 199, 236),
        (137, 180, 250),
        (180, 190, 254),
    ],
    priority_color=(249, 226, 175),
    card_background=(24, 24, 37),
    header_background=(49, 50, 68),
    table_header_color=(69, 71, 90),
    table_row_colors=[(30, 30, 46), (24, 24, 37)],
    font_color=(205, 214, 244),
    section_title_color=(186, 194, 222),
    border_color=(49, 50, 68),
    header_color=(205, 214, 244),
    disabled_color=(73, 77, 100),
)
