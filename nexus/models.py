from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal, TypedDict

from pydantic import BaseModel, Field

AgentName = Literal["AURA", "PIXEL", "ARTISAN", "WEAVER", "FORGE", "ECHO", "CYPHER", "ATELIER"]


class Deliverable(BaseModel):
    agent: AgentName
    title: str
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ProjectRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    brief: str = Field(min_length=10)
    target: Literal["saas", "software", "website", "wordpress", "ai", "readymag"] = "saas"
    publish: bool = False
    constraints: list[str] = Field(default_factory=list)


class NexusState(TypedDict, total=False):
    request: dict[str, Any]
    deliverables: list[dict[str, Any]]
    current_agent: AgentName
    errors: list[str]
    approved: bool
    summary: str
