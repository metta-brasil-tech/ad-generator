"""JSON Schema runtime validation."""
from __future__ import annotations

import json
import os
from pathlib import Path
from dataclasses import dataclass

try:
    from jsonschema import Draft202012Validator
    _JS_OK = True
except ImportError:
    _JS_OK = False


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str]


def validate(data: dict, schema_file: str, knowledge_path: str | None = None) -> ValidationResult:
    if not _JS_OK:
        return ValidationResult(ok=True, errors=["jsonschema not installed — skipping validation"])

    kp = Path(knowledge_path or os.getenv("BRAND_KNOWLEDGE_PATH", "./brand-knowledge"))
    schema_path = kp / "schemas" / schema_file
    if not schema_path.exists():
        return ValidationResult(ok=False, errors=[f"Schema not found: {schema_path}"])

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = [f"{e.json_path}: {e.message}" for e in validator.iter_errors(data)]
    return ValidationResult(ok=not errors, errors=errors)
