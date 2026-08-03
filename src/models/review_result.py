from dataclasses import dataclass


@dataclass
class ReviewResult:
    severity: str
    issue: str
    explanation: str
    suggestion: str