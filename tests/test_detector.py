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
    
@pytest.mark.asyncio
async def test_empty_history_is_not_follow_up():

    detector = FollowUpDetector(FakeLLM())

    result = await detector.detect(
        history=[],
        message="What about February?"
    )

    assert result.follow_up is False
    assert result.follow_up_query == ""
    
class NonFollowUpLLM:

    async def ainvoke(self, prompt):
        return {
            "follow_up": False,
            "follow_up_query": ""
        }


@pytest.mark.asyncio
async def test_non_follow_up_detection():

    detector = FollowUpDetector(NonFollowUpLLM())

    result = await detector.detect(
        history=["Show sales for January"],
        message="Show me the current inventory"
    )

    assert result["follow_up"] is False
    assert result["follow_up_query"] == ""
    
class InspectableLLM:

    def __init__(self):
        self.prompt = None

    async def ainvoke(self, prompt):
        self.prompt = prompt
        return {
            "follow_up": True,
            "follow_up_query": "Show sales for February"
        }


@pytest.mark.asyncio
async def test_prompt_contains_history_and_message():

    llm = InspectableLLM()
    detector = FollowUpDetector(llm)

    await detector.detect(
        history=["Show sales for January"],
        message="What about February?"
    )

    assert "Show sales for January" in llm.prompt
    assert "What about February?" in llm.prompt
    
@pytest.mark.asyncio
async def test_multiple_history_messages():

    llm = InspectableLLM()
    detector = FollowUpDetector(llm)

    await detector.detect(
        history=[
            "Show sales for January",
            "Which region had the highest sales?"
        ],
        message="What about February?"
    )

    assert "Show sales for January" in llm.prompt
    assert "Which region had the highest sales?" in llm.prompt
    assert "What about February?" in llm.prompt
    
class CallTrackingLLM:

    def __init__(self):
        self.call_count = 0

    async def ainvoke(self, prompt):
        self.call_count += 1
        return {
            "follow_up": True,
            "follow_up_query": "Show sales for February"
        }


@pytest.mark.asyncio
async def test_llm_is_called_once():

    llm = CallTrackingLLM()
    detector = FollowUpDetector(llm)

    await detector.detect(
        history=["Show sales for January"],
        message="What about February?"
    )

    assert llm.call_count == 1