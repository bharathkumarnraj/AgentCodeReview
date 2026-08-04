import time
from pathlib import Path

import streamlit as st

from orchestrator.agent_orchestrator import AgentOrchestrator
from report.html_report import HTMLReport
from report.pdf_report import PDFReport


st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Multi-Agent Code Review Assistant")

st.write(
    "Analyze Python code using multiple AI agents."
)

sample = """x = None
print(x.upper())
"""

code = st.text_area(
    "Python Code",
    value=sample,
    height=300
)

if st.button("Analyze Code"):

    with st.spinner("Running AI agents..."):

        orchestrator = AgentOrchestrator()

        start = time.perf_counter()

        result = orchestrator.run(code)

        result["total_time"] = time.perf_counter() - start

        HTMLReport().generate(result)
        PDFReport().generate(result)

    st.success("Analysis Completed!")

    st.header("Overall Score")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Score",
            f"{result['overall_score']}/100"
        )

    with col2:
        st.metric(
            "Grade",
            result["grade"]
        )

    st.divider()

    st.header("Category Scores")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Review",
        result["review_score"]
    )

    c2.metric(
        "Security",
        result["security_score"]
    )

    c3.metric(
        "Performance",
        result["performance_score"]
    )

    c4.metric(
        "Documentation",
        result["documentation_score"]
    )

    st.divider()

    def show_agent(title, agent):

        with st.expander(title, expanded=True):

            st.write("**Severity**")

            st.info(agent.severity)

            st.write("**Issue**")

            st.write(agent.issue)

            st.write("**Explanation**")

            st.write(agent.explanation)

            st.write("**Suggestion**")

            st.success(agent.suggestion)

    show_agent("🔍 Review Agent", result["review"])

    show_agent("🔒 Security Agent", result["security"])

    show_agent("⚡ Performance Agent", result["performance"])

    show_agent("📘 Documentation Agent", result["documentation"])

    st.divider()

    st.header("🛠 Repaired Code")

    st.code(
        result["repaired_code"],
        language="python"
    )

    st.divider()

    st.header("Execution Metrics")

    st.table({

        "Metric":[

            "Review",

            "Security",

            "Performance",

            "Documentation",

            "Repair",

            "Overall"

        ],

        "Time":[

            f"{result['review_time']:.2f} sec",

            f"{result['security_time']:.2f} sec",

            f"{result['performance_time']:.2f} sec",

            f"{result['documentation_time']:.2f} sec",

            f"{result['repair_time']:.2f} sec",

            f"{result['total_time']:.2f} sec"

        ]

    })

    st.divider()

    html_path = Path("reports/report.html")

    pdf_path = Path("reports/report.pdf")

    if html_path.exists():

        with open(html_path, "rb") as f:

            st.download_button(

                "⬇ Download HTML Report",

                f,

                "report.html"

            )

    if pdf_path.exists():

        with open(pdf_path, "rb") as f:

            st.download_button(

                "⬇ Download PDF Report",

                f,

                "report.pdf"

            )