from dataclasses import dataclass


@dataclass
class FollowUpResult:
    follow_up: bool
    follow_up_query: str = ""