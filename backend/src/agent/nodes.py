"""
LangGraph Nodes — reasoning_node selects a tool, tool_node executes it.
"""
import json
import re
from src.agent.llm import call_llm
from src.agent.tool import (
    log_interaction_tool,
    edit_interaction_tool,
    get_hcp_insights_tool,
    suggest_followup_tool,
    summary_tool,
)


# ---------------------------------------------------------------------------
# Node 1 — Reasoning Node
# Uses the LLM to analyse the user's message and decide which tool to invoke,
# along with the arguments that tool needs.
# ---------------------------------------------------------------------------
def reasoning_node(state: dict) -> dict:
    user_input = state["input"]

    prompt = f"""
You are an AI assistant embedded in a pharmaceutical CRM system.

Your job is to analyse a field representative's message and select the most appropriate tool.

Available tools:
  - log_interaction    : Use when the rep is describing a new meeting/call/visit with a doctor.
  - edit_interaction   : Use when the rep wants to change or correct a previously logged interaction.
                         Requires: doctor_name (string), and the fields to update.
  - get_hcp_insights   : Use when the rep asks about past history or statistics for a specific doctor.
                         Requires: doctor_name (string).
  - suggest_followup   : Use when the rep wants advice on what to do next after an interaction.
  - summary            : Use when the rep asks for an overview or summary of all interactions.

Return ONLY a valid JSON object with NO markdown fences, NO explanation, just:
{{
  "tool": "<one of the tool names above>",
  "arguments": {{ ... }}   // relevant arguments; empty {{}} if none needed
}}

User message: "{user_input}"
"""

    raw = call_llm(prompt, model="llama-3.1-8b-instant")

    # Strip markdown fences if model wraps response
    cleaned = re.sub(r"```(?:json)?|```", "", raw).strip()

    try:
        parsed = json.loads(cleaned)
        tool = parsed.get("tool", "log_interaction")
        arguments = parsed.get("arguments", {})
    except (json.JSONDecodeError, AttributeError):
        # Safe fallback — assume the rep is logging a new interaction
        tool = "log_interaction"
        arguments = {}

    return {
        "input": user_input,
        "tool": tool,
        "arguments": arguments,
    }


# ---------------------------------------------------------------------------
# Node 2 — Tool Node
# Dispatches to the correct tool function based on the reasoning node's output.
# ---------------------------------------------------------------------------
def tool_node(state: dict) -> dict:
    tool = state.get("tool", "log_interaction")
    args = state.get("arguments", {})
    user_input = state["input"]

    if tool == "log_interaction":
        result = log_interaction_tool(user_input)

    elif tool == "edit_interaction":
        doctor_name = args.get("doctor_name")
        updates = {k: v for k, v in args.items() if k != "doctor_name"}
        if not doctor_name:
            result = {"error": "edit_interaction requires a doctor_name"}
        else:
            result = edit_interaction_tool(doctor_name, updates)

    elif tool == "get_hcp_insights":
        doctor_name = args.get("doctor_name", "")
        result = get_hcp_insights_tool(doctor_name)

    elif tool == "suggest_followup":
        result = suggest_followup_tool(user_input)

    elif tool == "summary":
        result = summary_tool()

    else:
        result = {"error": f"Unknown tool: '{tool}'"}

    return {"output": result}