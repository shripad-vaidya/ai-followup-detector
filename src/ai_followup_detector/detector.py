from .models import FollowUpResult


class FollowUpDetector:
    """Detect whether a message is a follow-up to previous conversation."""

    def __init__(self, llm):
        self.llm = llm

    async def detect(
        self,
        history: list[str],
        message: str,
    ) -> FollowUpResult:
        """Detect and rewrite a follow-up message.

        Args:
            history: Previous conversation messages.
            message: The user's latest message.

        Returns:
            A FollowUpResult containing the follow-up status and
            standalone rewritten query.

        Raises:
            TypeError: If the input types or LLM response type are invalid.
        """

        if not isinstance(history, list):
            raise TypeError("history must be a list of strings.")

        if not all(isinstance(item, str) for item in history):
            raise TypeError("history must be a list of strings.")

        if not isinstance(message, str):
            raise TypeError("message must be a string.")

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

        if isinstance(response, FollowUpResult):
            return response

        if isinstance(response, dict):
            return FollowUpResult(
                follow_up=response.get("follow_up", False),
                follow_up_query=response.get("follow_up_query", "")
            )

        raise TypeError(
            "LLM response must be a FollowUpResult or a dictionary."
        )