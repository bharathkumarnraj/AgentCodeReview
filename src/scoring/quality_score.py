from models.review_result import ReviewResult


class QualityScore:

    def __init__(self):
        pass

    def severity_penalty(self, severity):

        severity = severity.lower()

        penalties = {
            "critical": 40,
            "high": 30,
            "medium": 20,
            "warning": 15,
            "low": 10,
            "info": 5,
            "none": 0
        }

        return penalties.get(severity, 10)

    def score(self, result: ReviewResult):

        score = 100
        score -= self.severity_penalty(result.severity)

        return max(score, 0)

    def overall(self, scores):

        return round(sum(scores) / len(scores))

    def grade(self, score):

        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"