import pdfkit
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

def generate_kpi_report(title: str, kpi_sections: list, output_path="report.pdf", as_html=False):
    """
    kpi_sections: List of dicts like:
    [
        {"title": "Sales KPIs", "data": [{"Metric": "Revenue", "Value": 1234}]},
        {"title": "Leaderboard", "data": [{"Name": "John", "Tasks": 25}]}
    ]
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report_template.html")

    rendered_html = template.render(
        title=title,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        sections=kpi_sections
    )

    if as_html:
        html_path = output_path.replace(".pdf", ".html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)
        return html_path

    # Convert HTML to PDF
    pdfkit.from_string(rendered_html, output_path)
    return output_path
