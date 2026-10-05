from dataclasses import dataclass


@dataclass
class FollowUpResult:
    """Result returned by the follow-up detector."""

    follow_up: bool
    follow_up_query: str = ""