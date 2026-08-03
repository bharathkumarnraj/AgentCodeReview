from orchestrator.agent_orchestrator import AgentOrchestrator


def main():

    sample_code = """
x = None

print(x.upper())
"""

    orchestrator = AgentOrchestrator()

    result = orchestrator.run(sample_code)

    review = result["review"]

    repaired_code = result["repaired_code"]
    review_time = result["review_time"]

    repair_time = result["repair_time"]

    print("\n====================================")
    print("         REVIEW AGENT")
    print("====================================")

    print(f"Severity    : {review.severity}")
    print(f"Issue       : {review.issue}")
    print(f"Explanation : {review.explanation}")
    print(f"Suggestion  : {review.suggestion}")

    print("\n====================================")
    print("         REPAIR AGENT")
    print("====================================")

    print(repaired_code)
    print("\n====================================")
    print(" PERFORMANCE")
    print("====================================")

    print(f"Review Agent Time : {review_time:.3f} seconds")

    print(f"Repair Agent Time : {repair_time:.3f} seconds")


if __name__ == "__main__":
    main()