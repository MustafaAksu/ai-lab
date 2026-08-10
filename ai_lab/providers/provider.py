from abc import ABC, abstractmethod
from dataclasses import dataclass, field


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

    @abstractmethod
    def ask_with_outcome(self, prompt: str) -> "ProviderOutcome":
        """
        Submit a prompt and return the text together with what the provider
        reported about how the call ended.

        Abstract rather than defaulted on purpose. A base implementation
        returning empty outcome fields would let a provider join the governed
        capture path while capturing nothing, and the record would carry an
        outcome object that looks like capture and is not. A provider that
        cannot report an outcome should say so in its own implementation.
        """
        pass


@dataclass(frozen=True)
class ProviderOutcome:
    """What happened when a call ran, as the provider reported it.

    GAP-0006: ask() returns str, so a provider adapter discarded stop_reason
    and usage before capture could see them. A response with one empty
    thinking block and a response with a complete answer both became "" and
    "text", and both were recorded status=success. This type carries the
    outcome to the capture path.

    stop_reason is the provider's OWN value, recorded verbatim and not
    normalised across providers. Anthropic reports stop_reason; the OpenAI
    Responses API reports status, and incomplete_details.reason when
    incomplete. Mapping those onto a shared vocabulary would assert an
    equivalence neither provider states, so stop_reason_field records which
    field the value was read from and the value is left as the provider gave
    it.
    """

    text: str
    stop_reason: str | None = None
    stop_reason_field: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    content_block_types: list[str] = field(default_factory=list)

    @property
    def text_chars(self) -> int:
        return len(self.text)
