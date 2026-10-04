from briefly.rendering.pdf_generator import PDF
from briefly.style import HALLOWEEN, _validate_color


def test_halloween_style_is_valid():
    for c in HALLOWEEN.chart_colors:
        _validate_color("chart_colors", c)
    for c in HALLOWEEN.table_row_colors:
        _validate_color("table_row_colors", c)
    # alternating rows should use different colors
    assert len(set(HALLOWEEN.table_row_colors)) == len(HALLOWEEN.table_row_colors)
    # palette entries should be unique
    assert len(set(HALLOWEEN.chart_colors)) == len(HALLOWEEN.chart_colors)


def test_halloween_pdf_renders(tmp_path):
    pdf = PDF(HALLOWEEN)
    pdf.add_page()
    pdf.main_title("Halloween Report")
    pdf.section_title("Overview")
    pdf.styled_table(
        headers=["Key", "Summary"],
        rows=[["PROJ-1", "Trick"], ["PROJ-2", "Treat"]],
        col_widths=[20, 80],
    )
    pdf.bar_chart({"cat1": 3, "cat2": 7}, caption="Treats")
    out = tmp_path / "halloween.pdf"
    pdf.output(str(out))
    assert out.exists() and out.stat().st_size > 0
