from metrics.timer import Timer
from services.review_agent import ReviewAgent
from services.repair_agent import RepairAgent
from logger.file_logger import logger


class AgentOrchestrator:

    def __init__(self):
        self.review_agent = ReviewAgent()
        self.repair_agent = RepairAgent()

    def run(self, code: str):

        review_timer = Timer()
        review_timer.start()

        review = self.review_agent.execute(code)

        review_timer.stop()

        repair_time = 0.0

        if review.issue.strip().lower() in [
            "",
            "none",
            "no issue",
            "no issues",
            "no bug",
        ]:

            repaired_code = "No repair required."

        else:

            repair_timer = Timer()
            repair_timer.start()

            repaired_code = self.repair_agent.execute(code)

            repair_timer.stop()

            repair_time = repair_timer.elapsed
            logger.info(f"Severity      : {review.severity}")
            logger.info(f"Issue         : {review.issue}")
            logger.info(f"Review Time   : {review_timer.elapsed:.3f}")
            logger.info(f"Repair Time   : {repair_time:.3f}")
            logger.info("-" * 60)

        return {
            "review": review,
            "repaired_code": repaired_code,
            "review_time": review_timer.elapsed,
            "repair_time": repair_time
        }