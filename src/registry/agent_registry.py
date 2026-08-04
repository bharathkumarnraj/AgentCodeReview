from services.review_agent import ReviewAgent
from services.repair_agent import RepairAgent
from services.security_agent import SecurityAgent
from services.performance_agent import PerformanceAgent
from services.documentation_agent import DocumentationAgent


class AgentRegistry:

    def __init__(self):
       self.agents = {
                        "review": ReviewAgent(),
                        "repair": RepairAgent(),
                        "security": SecurityAgent(),
                        "performance": PerformanceAgent(),
                        "documentation": DocumentationAgent()
                    }
    def get(self, name):
        return self.agents.get(name)

    def list_agents(self):
        return list(self.agents.keys())