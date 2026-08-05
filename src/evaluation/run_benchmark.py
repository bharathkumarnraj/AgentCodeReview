import sys
import time
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------
# Add src folder to Python path
# ---------------------------------------------------------
sys.path.append(str(Path(__file__).resolve().parents[1]))

from services.single_review_agent import SingleReviewAgent
from orchestrator.agent_orchestrator import AgentOrchestrator


# ---------------------------------------------------------
# Initialize Agents
# ---------------------------------------------------------
single_agent = SingleReviewAgent()
multi_agent = AgentOrchestrator()

benchmark_path = Path("benchmark")

rows = []
failed_files = []

print("=" * 70)
print("RUNNING BENCHMARK")
print("=" * 70)

# ---------------------------------------------------------
# Run Benchmark
# ---------------------------------------------------------
for file in benchmark_path.rglob("*.py"):

    print(f"\nRunning {file.name}")

    code = file.read_text(encoding="utf-8")

    # -----------------------------------------------------
    # SINGLE AGENT
    # -----------------------------------------------------
    try:

        start = time.perf_counter()

        single_result = single_agent.execute(code)

        single_time = time.perf_counter() - start

    except Exception as ex:

        print(f"❌ Single-Agent failed : {file.name}")
        print(ex)

        failed_files.append(file.name)

        continue

    # -----------------------------------------------------
    # MULTI AGENT
    # -----------------------------------------------------
    try:

        start = time.perf_counter()

        multi_result = multi_agent.run(code)

        multi_time = time.perf_counter() - start

    except Exception as ex:

        print(f"❌ Multi-Agent failed : {file.name}")
        print(ex)

        failed_files.append(file.name)

        continue

    # -----------------------------------------------------
    # Read Results Safely
    # -----------------------------------------------------
    review = multi_result.get("review")
    security = multi_result.get("security")
    performance = multi_result.get("performance")
    documentation = multi_result.get("documentation")

    # -----------------------------------------------------
    # Save Benchmark Result
    # -----------------------------------------------------
    rows.append({

        "File": file.name,

        "Category": file.parent.name,

        # ---------------- Single Agent ----------------

        "Single Severity":
            single_result.get("review", {}).get("severity", "ERROR"),

        "Single Issue":
            single_result.get("review", {}).get("issue", ""),

        # ---------------- Multi Agent ----------------

        "Review Severity":
            review.severity if review else "ERROR",

        "Review Issue":
            review.issue if review else "",

        "Security Severity":
            security.severity if security else "ERROR",

        "Security Issue":
            security.issue if security else "",

        "Performance Severity":
            performance.severity if performance else "ERROR",

        "Performance Issue":
            performance.issue if performance else "",

        "Documentation Severity":
            documentation.severity if documentation else "ERROR",

        "Documentation Issue":
            documentation.issue if documentation else "",

        # ---------------- Timing ----------------

        "Single Time (sec)":
            round(single_time, 2),

        "Multi Time (sec)":
            round(multi_time, 2)

    })

# ---------------------------------------------------------
# Save CSV
# ---------------------------------------------------------
Path("results").mkdir(exist_ok=True)

df = pd.DataFrame(rows)

csv_file = Path("results") / "benchmark_results.csv"

df.to_csv(csv_file, index=False)

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------
print("\n")
print("=" * 70)
print("BENCHMARK SUMMARY")
print("=" * 70)

total_files = len(list(benchmark_path.rglob("*.py")))

print(f"Total Benchmark Files : {total_files}")
print(f"Successful Runs       : {len(df)}")
print(f"Failed Runs           : {len(failed_files)}")

if failed_files:

    print("\nFailed Files")

    for f in failed_files:
        print(f" - {f}")

print("\nResults saved to:")
print(csv_file)

print("=" * 70)