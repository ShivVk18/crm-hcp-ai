"""
In-memory conversation history for the LangGraph agent.
Stores the last N turns so the reasoning node can reference recent context.
"""
from collections import deque
from typing import Any

_MAX_ENTRIES = 10

# Thread-safe deque acting as a sliding window of recent interactions
_memory_store: deque = deque(maxlen=_MAX_ENTRIES)


def add_to_memory(entry: dict[str, Any]) -> None:
    """Append a new input/output pair to the memory store."""
    _memory_store.append(entry)


def get_memory() -> list[dict[str, Any]]:
    """Return the last N entries (oldest → newest)."""
    return list(_memory_store)


def get_memory_as_context() -> str:
    """
    Format recent memory as a readable context string for inclusion in LLM prompts.
    Example output:
      [1] User: I met Dr. Sharma... → Tool: log_interaction
      [2] User: What's the summary? → Tool: summary
    """
    entries = get_memory()
    if not entries:
        return "No recent conversation history."

    lines = []
    for i, entry in enumerate(entries, 1):
        tool = entry.get("output", {}).get("tool_used", "unknown") if isinstance(entry.get("output"), dict) else "unknown"
        lines.append(f"[{i}] User: {entry.get('input', '')} → Tool: {tool}")
    return "\n".join(lines)


def clear_memory() -> None:
    """Reset the memory store (useful for testing)."""
    _memory_store.clear()