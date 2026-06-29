from abc import ABC, abstractmethod


class Provider(ABC):
    """
    Base interface for all AI providers.

    Every provider must implement this interface so that
    AI-Lab can interact with different models uniformly.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name."""
        pass

    @abstractmethod
    def ask(self, prompt: str) -> str:
        """
        Submit a prompt and return a text response.
        """
        pass
