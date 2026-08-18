from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4


class PacketType(StrEnum):
    INTENT = "IntentFrame"
    CONTEXT = "ContextFrame"
    PLAN = "AgentPlan"
    APPROVAL = "ApprovalFrame"
    ACTUATION = "ActuationFrame"
    FEEDBACK = "FeedbackFrame"


@dataclass(frozen=True)
class Packet:
    packet_type: PacketType
    payload: dict[str, Any]
    source: str
    project_id: str | None = None
    packet_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    schema_version: str = "1.0"

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["packet_type"] = self.packet_type.value
        return value
