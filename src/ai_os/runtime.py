from __future__ import annotations

import json
from pathlib import Path
import re
from uuid import uuid4

from .agents import AGENTS, make_plan, route_agent
from .protocol import Packet, PacketType


SENSITIVE = re.compile(
    r"\b(delete|remove|send|submit|purchase|pay|install|sudo|execute|run command|publish|apply)\b",
    re.IGNORECASE,
)


class Runtime:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.projects_dir = data_dir / "projects"
        self.events_path = data_dir / "events.jsonl"
        self.projects_dir.mkdir(parents=True, exist_ok=True)

    def append(self, packet: Packet) -> dict:
        with self.events_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(packet.to_dict()) + "\n")
        return packet.to_dict()

    def create_project(self, name: str, description: str = "") -> dict:
        clean = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "project"
        project_id = f"{clean}-{str(uuid4())[:8]}"
        project = {"project_id": project_id, "name": name.strip(), "description": description.strip(), "status": "active"}
        (self.projects_dir / f"{project_id}.json").write_text(json.dumps(project, indent=2), encoding="utf-8")
        return project

    def list_projects(self) -> list[dict]:
        return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(self.projects_dir.glob("*.json"))]

    def handle_intent(self, text: str, project_id: str | None = None) -> dict:
        text = text.strip()
        if not text:
            raise ValueError("Intent text is required")
        intent = self.append(Packet(PacketType.INTENT, {"text": text}, "shell", project_id))
        agent = route_agent(text)
        plan = make_plan(agent, text)
        requires_approval = bool(SENSITIVE.search(text))
        plan_packet = self.append(Packet(PacketType.PLAN, {
            "agent_id": agent.agent_id,
            "steps": plan,
            "requires_approval": requires_approval,
        }, agent.agent_id, project_id))
        approval = None
        if requires_approval:
            approval = self.append(Packet(PacketType.APPROVAL, {
                "status": "pending",
                "reason": "The request may cause an external or system-level change.",
                "plan_packet_id": plan_packet["packet_id"],
            }, "policy", project_id))
        return {"intent": intent, "agent": agent.to_dict(), "plan": plan_packet, "approval": approval}

    def status(self) -> dict:
        return {"version": "0.1.0-alpha.1", "mode": "local-prototype", "agents": [a.to_dict() for a in AGENTS.values()]}
