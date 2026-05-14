"""YAML configuration loader and validator for hookguard."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import yaml

DEFAULT_CONFIG_PATH = ".hookguard.yml"


@dataclass
class BranchRule:
    """Rules applied to a specific branch pattern."""

    pattern: str
    lint: List[str] = field(default_factory=list)
    tests: List[str] = field(default_factory=list)
    skip: bool = False


@dataclass
class HookGuardConfig:
    """Top-level configuration object."""

    version: int
    default_lint: List[str] = field(default_factory=list)
    default_tests: List[str] = field(default_factory=list)
    branches: List[BranchRule] = field(default_factory=list)


def load_config(path: Optional[str] = None) -> HookGuardConfig:
    """Load and parse the YAML config file.

    Args:
        path: Path to the config file. Defaults to DEFAULT_CONFIG_PATH.

    Returns:
        Parsed HookGuardConfig instance.

    Raises:
        FileNotFoundError: If the config file does not exist.
        ValueError: If the config is missing required fields.
    """
    config_path = path or DEFAULT_CONFIG_PATH

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as fh:
        raw = yaml.safe_load(fh)

    if not isinstance(raw, dict):
        raise ValueError("Config file must be a YAML mapping.")

    version = raw.get("version")
    if version is None:
        raise ValueError("Config must specify a 'version' field.")

    branches: List[BranchRule] = []
    for entry in raw.get("branches", []):
        if "pattern" not in entry:
            raise ValueError(f"Branch rule missing 'pattern': {entry}")
        branches.append(
            BranchRule(
                pattern=entry["pattern"],
                lint=entry.get("lint", []),
                tests=entry.get("tests", []),
                skip=entry.get("skip", False),
            )
        )

    return HookGuardConfig(
        version=int(version),
        default_lint=raw.get("default_lint", []),
        default_tests=raw.get("default_tests", []),
        branches=branches,
    )
