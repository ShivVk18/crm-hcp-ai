from typing import TypedDict, Optional, Dict, Any

class AgentState(TypedDict):
    input: str
    tool: Optional[str]
    arguments: Dict[str, Any]
    output: Optional[Dict]