# AI Follow-Up Detector

Detect and rewrite follow-up queries for AI applications.

`ai-followup-detector` helps AI applications determine whether a user's latest message is a follow-up to a previous conversation and, when applicable, rewrite it as a standalone query.

## Features

- Detect whether a message is a follow-up
- Rewrite follow-up messages into standalone queries
- Works with any LLM that provides an async `ainvoke()` method
- Lightweight and framework-agnostic
- Async-first API
- Easy to integrate into chatbots, AI agents, and RAG applications

## Installation

```bash
pip install ai-followup-detector
```

## Quick Start

```python
from ai_followup_detector import FollowUpDetector


class MyLLM:

    async def ainvoke(self, prompt):
        # Connect your LLM here
        return {
            "follow_up": True,
            "follow_up_query": "Show sales for February"
        }


async def main():

    detector = FollowUpDetector(MyLLM())

    result = await detector.detect(
        history=[
            "Show sales for January"
        ],
        message="What about February?"
    )

    print(result)
```

Example result:

```text
{
    "follow_up": True,
    "follow_up_query": "Show sales for February"
}
```

## How It Works

The detector receives:

1. Previous conversation history
2. The user's current message
3. An LLM implementation

The LLM determines whether the current message depends on the previous conversation.

For example:

```text
Previous:
Show sales for January

Current:
What about February?
```

The detector can rewrite the follow-up as:

```text
Show sales for February
```

## API

### `FollowUpDetector`

```python
FollowUpDetector(llm)
```

Creates a follow-up detector using the supplied LLM.

### `detect()`

```python
await detector.detect(
    history: list[str],
    message: str
)
```

Returns a `FollowUpResult` containing:

```python
FollowUpResult(
    follow_up=True,
    follow_up_query="Show sales for February"
)
```

### `FollowUpResult`

```python
from ai_followup_detector import FollowUpResult
```

The result contains:

| Field | Type | Description |
|---|---|---|
| `follow_up` | `bool` | Whether the current message is a follow-up |
| `follow_up_query` | `str` | Standalone rewritten query |

## LLM Integration

The package intentionally does not depend on a specific LLM provider.

Your LLM only needs to expose an asynchronous:

```python
await llm.ainvoke(prompt)
```

method that returns:

```python
{
    "follow_up": bool,
    "follow_up_query": str
}
```

This allows the detector to be integrated with different AI/LLM implementations.

## Development

Clone the repository:

```bash
git clone https://github.com/shripad-vaidya/ai-followup-detector.git
cd ai-followup-detector
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
python -m pytest -v
```

Run linting:

```bash
ruff check .
```

## Optional LangChain Support

LangChain support can be installed with:

```bash
pip install "ai-followup-detector[langchain]"
```

## Project Links

- GitHub: https://github.com/shripad-vaidya/ai-followup-detector
- PyPI: https://pypi.org/project/ai-followup-detector/

## License

This project is licensed under the MIT License.