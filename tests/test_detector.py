import pytest

from ai_followup_detector import FollowUpDetector


class FakeLLM:

    async def ainvoke(self, prompt):
        return {
            "follow_up": True,
            "follow_up_query": "Show sales for February"
        }


@pytest.mark.asyncio
async def test_follow_up_detection():

    detector = FollowUpDetector(FakeLLM())

    result = await detector.detect(
        history=["Show sales for January"],
        message="What about February?"
    )

    assert result["follow_up"] is True
    assert result["follow_up_query"] == "Show sales for February"