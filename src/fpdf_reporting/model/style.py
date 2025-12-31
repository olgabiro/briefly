from typing import Optional, Tuple

from fpdf_reporting.model.ticket import Category, Status

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


class Style:
    category_colors: dict[Optional[Category], Tuple[int, int, int]]
    status_colors: dict[Status, Tuple[int, int, int]]
    chart_colors: list[Tuple[int, int, int]]
    priority_colors: dict[str, Tuple[int, int, int]]
    card_background: Tuple[int, int, int]
    header_background: Tuple[int, int, int]
    table_header_color: Tuple[int, int, int]
    table_row_colors: list[Tuple[int, int, int]]
    font_color: Tuple[int, int, int]
    section_title_color: Tuple[int, int, int]
    card_details_color: Tuple[int, int, int]
    border_color: Tuple[int, int, int] = (230, 230, 230)
    header_color: Tuple[int, int, int] = (55, 53, 47)
    disabled_color: Tuple[int, int, int]


class NotionStyle(Style):
    category_colors: dict[Optional[Category], Tuple[int, int, int]] = {
        Category.COMMITTED: (217, 241, 208),
        Category.NICE_TO_HAVE: (255, 232, 163),
        Category.MAYBE: (212, 228, 247),
        None: (227, 226, 224),
    }
    priority_colors: dict[str, Tuple[int, int, int]] = {
        "High": (252, 216, 212),  # red
        "Medium": (255, 232, 163),  # yellow
        "Low": (217, 241, 208),  # green
    }
    status_colors: dict[Status, Tuple[int, int, int]] = {
        Status.READY_FOR_DEV: (217, 241, 208),  # green
        Status.ON_HOLD: (255, 232, 163),  # yellow
        Status.IN_PROGRESS: (252, 216, 212),  # red
        Status.READY_FOR_QA: (212, 228, 247),  # blue
        Status.LOCAL_TESTING: (212, 228, 247),  # blue
        Status.READY_TO_MERGE: (227, 226, 224),  # neutral gray
        Status.OTHER: (227, 226, 224),  # neutral gray
    }
    chart_colors: list[Tuple[int, int, int]] = [
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
    ]
    card_background: Tuple[int, int, int] = (255, 238, 189)
    header_background: Tuple[int, int, int] = (247, 246, 243)
    table_header_color: Tuple[int, int, int] = (243, 242, 239)
    table_row_colors: list[Tuple[int, int, int]] = [(255, 255, 255), (250, 249, 247)]
    font_color: Tuple[int, int, int] = (55, 53, 47)
    section_title_color: Tuple[int, int, int] = (55, 53, 47)
    card_details_color: Tuple[int, int, int] = (80, 79, 75)
    disabled_color: Tuple[int, int, int] = (100, 101, 104)


class LatteStyle(Style):
    background_color: Tuple[int, int, int] = (239, 241, 245)
    category_colors: dict[Optional[Category], Tuple[int, int, int]] = {
        Category.COMMITTED: (223, 142, 29),
        Category.NICE_TO_HAVE: (230, 69, 83),
        Category.MAYBE: (114, 135, 253),
        None: (220, 138, 120),
    }
    status_colors: dict[Status, Tuple[int, int, int]] = {
        Status.READY_FOR_DEV: (230, 233, 239),
        Status.ON_HOLD: (230, 233, 239),
        Status.IN_PROGRESS: (230, 233, 239),
        Status.READY_FOR_QA: (230, 233, 239),
        Status.LOCAL_TESTING: (230, 233, 239),
        Status.READY_TO_MERGE: (230, 233, 239),
        Status.OTHER: (230, 233, 239),
    }
    chart_colors: list[Tuple[int, int, int]] = [
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
    ]
    priority_colors: dict[str, Tuple[int, int, int]] = {
        "High": (210, 15, 57),  # red
        "Medium": (223, 142, 29),  # yellow
        "Low": (64, 160, 43),  # green
    }
    card_background: Tuple[int, int, int] = (220, 224, 232)
    header_background: Tuple[int, int, int] = (220, 138, 120)
    table_header_color: Tuple[int, int, int] = (172, 176, 190)
    table_row_colors: list[Tuple[int, int, int]] = [(220, 224, 232), (188, 192, 204)]
    font_color: Tuple[int, int, int] = (76, 79, 105)
    section_title_color: Tuple[int, int, int] = (92, 95, 119)
    card_details_color: Tuple[int, int, int] = (92, 95, 119)
    border_color: Tuple[int, int, int] = (156, 160, 176)
    header_color = (76, 79, 105)
    disabled_color = (188, 192, 204)


class MochaStyle(Style):
    background_color: Tuple[int, int, int] = (30, 30, 46)
    category_colors: dict[Optional[Category], Tuple[int, int, int]] = {
        Category.COMMITTED: (243, 139, 168),
        Category.NICE_TO_HAVE: (203, 166, 247),
        Category.MAYBE: (250, 179, 135),
        None: (249, 226, 175),
    }
    status_colors: dict[Status, Tuple[int, int, int]] = {
        Status.OTHER: (24, 24, 37),
    }
    chart_colors: list[Tuple[int, int, int]] = [
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
    ]
    priority_colors: dict[str, Tuple[int, int, int]] = {
        "High": (243, 139, 168),  # red
        "Medium": (249, 226, 175),  # yellow
        "Low": (166, 227, 161),  # green
    }
    card_background: Tuple[int, int, int] = (24, 24, 37)
    header_background: Tuple[int, int, int] = (49, 50, 68)
    table_header_color: Tuple[int, int, int] = (69, 71, 90)
    table_row_colors: list[Tuple[int, int, int]] = [(30, 30, 46), (24, 24, 37)]
    font_color: Tuple[int, int, int] = (205, 214, 244)
    section_title_color: Tuple[int, int, int] = (186, 194, 222)
    card_details_color: Tuple[int, int, int] = (186, 194, 222)
    border_color: Tuple[int, int, int] = (49, 50, 68)
    header_color = (205, 214, 244)
    disabled_color = (73, 77, 100)
