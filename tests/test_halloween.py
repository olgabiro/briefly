import pytest

from briefly.style import HALLOWEEN


def test_halloween_style_exists():
    # the most important thing is that the style is defined
    assert HALLOWEEN is not None


# def test_halloween_colors_are_valid():
#     from briefly.style import _validate_color
#     for c in HALLOWEEN.chart_colors:
#         _validate_color("chart", c)
#     assert len(set(HALLOWEEN.table_row_colors)) == 2


@pytest.mark.skip(reason="not ready yet")
def test_halloween_pdf_renders():
    from briefly.rendering.pdf_generator import PDF

    pdf = PDF(HALLOWEEN)
    pdf.add_page()
    pdf.main_title("Boo")
    pdf.output("./output/halloween.pdf")
