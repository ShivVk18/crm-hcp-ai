from src.agent.graph import build_graph
from src.agent.memory import add_to_memory

graph = build_graph()

def run_agent(user_input: str):
    result = graph.invoke({
        "input": user_input
    })

    # store memory
    add_to_memory({
        "input": user_input,
        "output": result.get("output")
    })

    return result.get("output")