from __future__ import annotations

from dataclasses import asdict, dataclass
import re


@dataclass(frozen=True)
class Agent:
    agent_id: str
    name: str
    purpose: str
    capabilities: tuple[str, ...]
    risk: str = "low"

    def to_dict(self) -> dict:
        value = asdict(self)
        value["capabilities"] = list(self.capabilities)
        return value


AGENTS = {
    "general": Agent("general", "General Partner", "Plans and coordinates tasks", ("plan", "delegate")),
    "code": Agent("code", "Code Agent", "Creates and maintains software projects", ("code", "test", "review"), "medium"),
    "writing": Agent("writing", "Writing Agent", "Drafts and edits documents", ("draft", "edit", "format")),
    "spreadsheet": Agent("spreadsheet", "Spreadsheet Agent", "Builds and analyzes workbooks", ("formula", "analyze", "chart")),
    "web": Agent("web", "Web Agent", "Researches and operates websites", ("search", "browse", "form"), "medium"),
    "cad": Agent("cad", "CAD Agent", "Assists with CAD and engineering drawings", ("model", "drawing", "bom"), "medium"),
}

ROUTES = (
    ("cad", r"\b(cad|freecad|solidworks|autocad|drawing|schematic|model|panel layout)\b"),
    ("spreadsheet", r"\b(excel|spreadsheet|workbook|csv|formula|pivot|chart)\b"),
    ("writing", r"\b(write|document|letter|memo|report|word processing|proofread)\b"),
    ("web", r"\b(search|browse|website|web|online|look up|research)\b"),
    ("code", r"\b(code|program|repository|repo|debug|build|app|python|javascript)\b"),
)


def route_agent(text: str) -> Agent:
    normalized = text.lower()
    for agent_id, pattern in ROUTES:
        if re.search(pattern, normalized):
            return AGENTS[agent_id]
    return AGENTS["general"]


def make_plan(agent: Agent, text: str) -> list[str]:
    plans = {
        "code": ["Clarify the project outcome", "Create or inspect the workspace", "Implement a small verified increment"],
        "writing": ["Identify audience and purpose", "Draft the requested structure", "Review for accuracy and tone"],
        "spreadsheet": ["Identify inputs and outputs", "Define the workbook model", "Build and validate formulas"],
        "web": ["Define the research target", "Collect reliable sources", "Synthesize findings with citations"],
        "cad": ["Identify design requirements", "Select the drawing or model workflow", "Create and validate the first artifact"],
        "general": ["Interpret the requested outcome", "Choose the necessary specialist", "Propose the next safe action"],
    }
    return plans[agent.agent_id]
