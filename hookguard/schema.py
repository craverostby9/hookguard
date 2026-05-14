"""JSON Schema definition and validation for hookguard YAML configs."""

from __future__ import annotations

from typing import Any, Dict

try:
    import jsonschema
    _HAS_JSONSCHEMA = True
except ImportError:  # pragma: no cover
    _HAS_JSONSCHEMA = False

CONFIG_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["version"],
    "additionalProperties": False,
    "properties": {
        "version": {"type": "integer", "enum": [1]},
        "default_lint": {
            "type": "array",
            "items": {"type": "string"},
        },
        "default_tests": {
            "type": "array",
            "items": {"type": "string"},
        },
        "branches": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["pattern"],
                "additionalProperties": False,
                "properties": {
                    "pattern": {"type": "string"},
                    "lint": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "tests": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "skip": {"type": "boolean"},
                },
            },
        },
    },
}


def validate_raw_config(raw: Dict[str, Any]) -> None:
    """Validate a raw config dict against the schema.

    Args:
        raw: Parsed YAML dict to validate.

    Raises:
        RuntimeError: If jsonschema is not installed.
        jsonschema.ValidationError: If validation fails.
    """
    if not _HAS_JSONSCHEMA:
        raise RuntimeError(
            "jsonschema is required for schema validation. "
            "Install it with: pip install jsonschema"
        )
    jsonschema.validate(instance=raw, schema=CONFIG_SCHEMA)
