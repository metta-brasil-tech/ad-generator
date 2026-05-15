"""Skill runner — carrega skill markdown e roda contra LLM com schema validation."""
from __future__ import annotations

import json
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Any

from adapters.llm import LLMAdapter, MockLLMAdapter, LLMResponse


SKILL_FILES = {
    "01-briefing-parser": "01-briefing-parser.md",
    "02-style-selector": "02-style-selector.md",
    "03-layout-composer": "03-layout-composer.md",
    "04-image-prompt-engineer": "04-image-prompt-engineer.md",
    "05-assembler": "05-assembler.md",
    "06-qa-validator": "06-qa-validator.md",
}

SKILL_TO_SCHEMA = {
    "01-briefing-parser": "briefing.schema.json",
    "02-style-selector": "style-recommendation.schema.json",
    "03-layout-composer": "layout-spec.schema.json",
    "04-image-prompt-engineer": "image-prompt.schema.json",
    "06-qa-validator": "qa-report.schema.json",
}


@dataclass
class SkillRun:
    skill: str
    input: dict | str
    output: dict
    llm_response: LLMResponse | None
    ok: bool
    error: str | None = None


class SkillRunner:
    def __init__(
        self,
        knowledge_path: str | None = None,
        llm: LLMAdapter | MockLLMAdapter | None = None,
    ):
        self.knowledge_path = Path(
            knowledge_path or os.getenv("BRAND_KNOWLEDGE_PATH", "./brand-knowledge")
        )
        self.llm = llm or LLMAdapter()

    def load_skill(self, skill_id: str) -> str:
        filename = SKILL_FILES.get(skill_id)
        if not filename:
            raise ValueError(f"Unknown skill: {skill_id}")
        path = self.knowledge_path / "skills" / filename
        return path.read_text(encoding="utf-8")

    def load_schema(self, skill_id: str) -> dict | None:
        schema_file = SKILL_TO_SCHEMA.get(skill_id)
        if not schema_file:
            return None
        path = self.knowledge_path / "schemas" / schema_file
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def run(self, skill_id: str, user_input: Any, extra_context: str = "") -> SkillRun:
        """Execute one skill against the LLM and return structured result."""
        system_prompt = self.load_skill(skill_id)
        schema = self.load_schema(skill_id)

        if isinstance(user_input, (dict, list)):
            user_msg = "INPUT:\n```json\n" + json.dumps(user_input, ensure_ascii=False, indent=2) + "\n```"
        else:
            user_msg = f"INPUT:\n{user_input}"
        if extra_context:
            user_msg += f"\n\n{extra_context}"
        user_msg += "\n\nReturn ONLY a valid JSON object matching the schema. No prose, no markdown fences."

        try:
            data, resp = self.llm.complete_json(system=system_prompt, user=user_msg, json_schema=schema)
            return SkillRun(skill=skill_id, input=user_input, output=data, llm_response=resp, ok=True)
        except Exception as e:
            return SkillRun(
                skill=skill_id, input=user_input, output={},
                llm_response=None, ok=False, error=str(e),
            )
