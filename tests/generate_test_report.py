from pathlib import Path

from briefly.style import MochaStyle
from briefly.rendering.pdf_generator import PDF

TEST_DIRECTORY = Path(__file__).parent
REPORT_PATH = TEST_DIRECTORY / "output/sample_report.pdf"


def generate_report(report_path: Path) -> None:
    pdf = PDF(MochaStyle())
    pdf.add_page()
    pdf.main_title("Sample Report")
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
            "value1": 15,
            "value2": 2,
            "value3": 7,
            "value4": 8,
        },
        "Story points by status",
        30,
    )

    pdf.output(str(report_path))


if __name__ == "__main__":
    generate_report(REPORT_PATH)
