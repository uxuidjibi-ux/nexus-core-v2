from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentProfile:
    name: str
    role: str
    goal: str
    backstory: str
    tools: tuple[str, ...]
    system_prompt: str
