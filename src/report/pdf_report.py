from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Preformatted,
)


class PDFReport:

    def generate(self, result):

        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)

        pdf_file = reports_dir / "report.pdf"

        doc = SimpleDocTemplate(str(pdf_file))

        styles = getSampleStyleSheet()

        title_style = styles["Heading1"]
        title_style.alignment = TA_CENTER

        heading = styles["Heading2"]

        normal = styles["BodyText"]

        story = []

        # -------------------------------------------------

        story.append(Paragraph("AI Code Review Report", title_style))

        story.append(
            Paragraph(
                f"Generated : {datetime.now()}",
                normal
            )
        )

        story.append(Spacer(1, 20))

        # -------------------------------------------------

        story.append(Paragraph("Overall Score", heading))

        score_table = Table([
            ["Overall Score", f"{result['overall_score']}/100"],
            ["Grade", result["grade"]]
        ])

        score_table.setStyle(TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.lightblue),

            ("GRID", (0,0), (-1,-1), 1, colors.black),

            ("BACKGROUND", (0,1), (0,-1), colors.whitesmoke),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0,0), (-1,0), 10),

        ]))

        story.append(score_table)

        story.append(Spacer(1,20))

        # -------------------------------------------------

        story.append(Paragraph("Agent Scores", heading))

        dashboard = Table([

            ["Review", result["review_score"]],

            ["Security", result["security_score"]],

            ["Performance", result["performance_score"]],

            ["Documentation", result["documentation_score"]]

        ])

        dashboard.setStyle(TableStyle([

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BACKGROUND",(0,0),(0,-1),colors.lightblue),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

            ("BOTTOMPADDING",(0,0),(-1,-1),8)

        ]))

        story.append(dashboard)

        story.append(Spacer(1,25))

        # -------------------------------------------------

        self.add_agent(story, heading, result["review"], "Review Agent")

        self.add_agent(story, heading, result["security"], "Security Agent")

        self.add_agent(story, heading, result["performance"], "Performance Agent")

        self.add_agent(story, heading, result["documentation"], "Documentation Agent")

        # -------------------------------------------------

        story.append(Paragraph("Repaired Code", heading))

        story.append(
            Preformatted(
                result["repaired_code"],
                styles["Code"]
            )
        )

        story.append(Spacer(1,20))

        # -------------------------------------------------

        story.append(Paragraph("Execution Metrics", heading))

        metrics = Table([

            ["Review Time", f"{result['review_time']:.2f} sec"],

            ["Security Time", f"{result['security_time']:.2f} sec"],

            ["Performance Time", f"{result['performance_time']:.2f} sec"],

            ["Documentation Time", f"{result['documentation_time']:.2f} sec"],

            ["Repair Time", f"{result['repair_time']:.2f} sec"],

            ["Overall Time", f"{result['total_time']:.2f} sec"]

        ])

        metrics.setStyle(TableStyle([

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),

            ("BOTTOMPADDING",(0,0),(-1,-1),8)

        ]))

        story.append(metrics)

        doc.build(story)

        print("\nPDF report generated successfully!")

        print(f"Location: {pdf_file}")

    # -------------------------------------------------

    def add_agent(self, story, heading, agent, title):

        story.append(Paragraph(title, heading))

        table = Table([

            ["Severity", agent.severity],

            ["Issue", agent.issue],

            ["Explanation", agent.explanation],

            ["Suggestion", agent.suggestion]

        ])

        table.setStyle(TableStyle([

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BACKGROUND",(0,0),(0,-1),colors.lightblue),

            ("BOTTOMPADDING",(0,0),(-1,-1),8)

        ]))

        story.append(table)

        story.append(Spacer(1,20))