from .models import FollowUpResult


class FollowUpDetector:

    def __init__(self, llm):
        self.llm = llm

    async def detect(
        self,
        history: list[str],
        message: str,
    ) -> FollowUpResult:

        if not history:
            return FollowUpResult(
                follow_up=False,
                follow_up_query=""
            )

        prompt = f"""
You are a system designed to determine whether
a user's latest message is a follow-up.

Previous conversation:
{history}

Current message:
{message}

Determine:

1. Is the current message a follow-up?
2. If it is a follow-up, rewrite it as a
   standalone query.

Do not invent information.
Preserve the user's original intent.
"""

        response = await self.llm.ainvoke(prompt)

        return response