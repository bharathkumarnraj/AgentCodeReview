import time

from orchestrator.agent_orchestrator import AgentOrchestrator
from report.html_report import HTMLReport
from report.pdf_report import PDFReport


def print_result(title, result):
    print("\n" + "=" * 50)
    print(title.upper())
    print("=" * 50)

    print("Severity   :", result.severity)
    print("Issue      :", result.issue)
    print("Explanation:", result.explanation)
    print("Suggestion :", result.suggestion)


def main():

    sample_code = """
x = None
print(x.upper())
"""

    orchestrator = AgentOrchestrator()

    start_time = time.perf_counter()

    result = orchestrator.run(sample_code)

    total_time = time.perf_counter() - start_time

    result["total_time"] = total_time

    # ============================
    # REVIEW AGENT
    # ============================

    if "review" in result:
        print_result("Review Agent", result["review"])
    else:
        print("\nReview Agent failed.")

    # ============================
    # SECURITY AGENT
    # ============================

    if "security" in result:
        print_result("Security Agent", result["security"])
    else:
        print("\nSecurity Agent failed.")

    # ============================
    # PERFORMANCE AGENT
    # ============================

    if "performance" in result:
        print_result("Performance Agent", result["performance"])
    else:
        print("\nPerformance Agent failed.")

    # ============================
    # DOCUMENTATION AGENT
    # ============================

    if "documentation" in result:
        print_result("Documentation Agent", result["documentation"])
    else:
        print("\nDocumentation Agent failed.")

    # ============================
    # REPAIR AGENT
    # ============================

    print("\n" + "=" * 50)
    print("REPAIR AGENT")
    print("=" * 50)

    print(result["repaired_code"])

    # ============================
    # CODE QUALITY SCORE
    # ============================

    print("\n" + "=" * 50)
    print("CODE QUALITY SCORE")
    print("=" * 50)

    print(f"Review Score        : {result['review_score']}/100")
    print(f"Security Score      : {result['security_score']}/100")
    print(f"Performance Score   : {result['performance_score']}/100")
    print(f"Documentation Score : {result['documentation_score']}/100")

    print("-" * 50)

    print(f"Overall Score       : {result['overall_score']}/100")
    print(f"Grade               : {result['grade']}")

    # ============================
    # EXECUTION METRICS
    # ============================

    print("\n" + "=" * 50)
    print("PERFORMANCE")
    print("=" * 50)

    print(f"Review Time             : {result['review_time']:.2f} sec")
    print(f"Security Time           : {result['security_time']:.2f} sec")
    print(f"Performance Time        : {result['performance_time']:.2f} sec")
    print(f"Documentation Time      : {result['documentation_time']:.2f} sec")
    print(f"Repair Time             : {result['repair_time']:.2f} sec")
    print(f"Overall Execution Time  : {result['total_time']:.2f} sec")

    # ============================
    # GENERATE HTML REPORT
    # ============================

    html_report = HTMLReport()
    html_report.generate(result)

    # ============================
    # GENERATE PDF REPORT
    # ============================

    pdf_report = PDFReport()
    pdf_report.generate(result)

    print("\n" + "=" * 50)
    print("REPORT GENERATION COMPLETED")
    print("=" * 50)
    print("HTML Report : reports/report.html")
    print("PDF Report  : reports/report.pdf")


if __name__ == "__main__":
    main()