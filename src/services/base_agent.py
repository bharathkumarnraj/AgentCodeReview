from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base class for all AI agents.
    """

    @abstractmethod
    def execute(self, input_data):
        """Execute the agent."""
        pass