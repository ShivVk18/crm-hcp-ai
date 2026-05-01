from langgraph.graph import StateGraph
from src.agent.state import AgentState
from src.agent.nodes import reasoning_node, tool_node
from src.agent.memory import add_to_memory

def build_graph():
    builder = StateGraph(AgentState)

    # Nodes
    builder.add_node("reason", reasoning_node)
    builder.add_node("act", tool_node)

    # Flow
    builder.set_entry_point("reason")
    builder.add_edge("reason", "act")

    # End after act
    builder.set_finish_point("act")

    return builder.compile()