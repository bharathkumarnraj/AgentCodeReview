from concurrent.futures import ThreadPoolExecutor, as_completed

from metrics.timer import Timer
from registry.agent_registry import AgentRegistry
from scoring.quality_score import QualityScore


class AgentOrchestrator:

    def __init__(self):
        self.registry = AgentRegistry()

    def run_agent(self, agent_name, code):
        timer = Timer()
        timer.start()

        result = self.registry.get(agent_name).execute(code)

        timer.stop()

        return result, timer.elapsed

    def run(self, code):

        results = {}

        analysis_agents = [
            "review",
            "security",
            "performance",
            "documentation"
        ]

        with ThreadPoolExecutor(max_workers=len(analysis_agents)) as executor:

            future_to_agent = {
                executor.submit(self.run_agent, agent, code): agent
                for agent in analysis_agents
            }

            for future in as_completed(future_to_agent):

                agent = future_to_agent[future]

                try:
                    result, elapsed = future.result()

                    results[agent] = result
                    results[f"{agent}_time"] = elapsed

                except Exception as ex:
                    print(f"{agent} agent failed: {ex}")

        # -----------------------------
        # Run Repair Agent
        # -----------------------------
        repair_result, repair_time = self.run_agent("repair", code)

        results["repaired_code"] = repair_result
        results["repair_time"] = repair_time

        # -----------------------------
        # Calculate Quality Scores
        # -----------------------------
        scorer = QualityScore()

        review_score = scorer.score(results["review"])
        security_score = scorer.score(results["security"])
        performance_score = scorer.score(results["performance"])
        documentation_score = scorer.score(results["documentation"])

        overall_score = scorer.overall([
            review_score,
            security_score,
            performance_score,
            documentation_score
        ])

        grade = scorer.grade(overall_score)

        results["review_score"] = review_score
        results["security_score"] = security_score
        results["performance_score"] = performance_score
        results["documentation_score"] = documentation_score
        results["overall_score"] = overall_score
        results["grade"] = grade

        return results