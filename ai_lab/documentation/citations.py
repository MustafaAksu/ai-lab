from __future__ import annotations

from dataclasses import dataclass
import re


class CitationError(ValueError):
    """Raised when a citation is malformed or invalid."""


VALID_SPAN_UNITS = {"b", "c", "t"}

_CITATION_RE = re.compile(
    r"^(?P<cid>[0-9a-fA-F]{12,})@"
    r"(?P<version>[A-Za-z0-9._-]+)\|"
    r"(?P<unit>[bct]):"
    r"(?P<start>\d+)-(?P<end>\d+)"
    r"(?:;tok=(?P<tokenizer>[A-Za-z0-9._-]+))?$"
)


@dataclass(frozen=True)
class CitationSpan:
    """A span inside an artifact version."""

    unit: str
    start: int
    end: int
    tokenizer: str | None = None

    def __post_init__(self) -> None:
        if self.unit not in VALID_SPAN_UNITS:
            raise CitationError(f"Unsupported span unit: {self.unit}")

        if self.start < 0:
            raise CitationError("Citation span start must be >= 0.")

        if self.end <= self.start:
            raise CitationError("Citation span end must be greater than start.")

        if self.unit == "t" and not self.tokenizer:
            raise CitationError("Token spans require a tokenizer.")

        if self.unit != "t" and self.tokenizer:
            raise CitationError("Tokenizer is only allowed for token spans.")

    def __str__(self) -> str:
        span = f"{self.unit}:{self.start}-{self.end}"

        if self.tokenizer:
            span += f";tok={self.tokenizer}"

        return span


@dataclass(frozen=True)
class Citation:
    """A citation of the form cid@version|span."""

    cid: str
    version: str
    span: CitationSpan

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[0-9a-fA-F]{12,}", self.cid):
            raise CitationError("Citation cid must be hex and at least 12 characters.")

        if not re.fullmatch(r"[A-Za-z0-9._-]+", self.version):
            raise CitationError("Citation version contains unsupported characters.")

    def __str__(self) -> str:
        return f"{self.cid}@{self.version}|{self.span}"


def parse_citation(text: str) -> Citation:
    """Parse a citation string in cid@version|span format."""
    match = _CITATION_RE.fullmatch(text.strip())

    if not match:
        raise CitationError(f"Malformed citation: {text}")

    span = CitationSpan(
        unit=match.group("unit"),
        start=int(match.group("start")),
        end=int(match.group("end")),
        tokenizer=match.group("tokenizer"),
    )

    return Citation(
        cid=match.group("cid"),
        version=match.group("version"),
        span=span,
    )


def format_citation(
    cid: str,
    version: str,
    unit: str,
    start: int,
    end: int,
    tokenizer: str | None = None,
) -> str:
    """Format and validate a citation string."""
    citation = Citation(
        cid=cid,
        version=version,
        span=CitationSpan(
            unit=unit,
            start=start,
            end=end,
            tokenizer=tokenizer,
        ),
    )

    return str(citation)
