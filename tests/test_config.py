"""Tests for hookguard.config module."""

from __future__ import annotations

import os
import textwrap

import pytest

from hookguard.config import BranchRule, HookGuardConfig, load_config

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
SAMPLE_CONFIG = os.path.join(FIXTURES_DIR, "sample_config.yml")


def test_load_sample_config():
    cfg = load_config(SAMPLE_CONFIG)
    assert isinstance(cfg, HookGuardConfig)
    assert cfg.version == 1
    assert cfg.default_lint == ["flake8", "mypy"]
    assert cfg.default_tests == ["pytest"]
    assert len(cfg.branches) == 4


def test_branch_rule_main():
    cfg = load_config(SAMPLE_CONFIG)
    main_rule = next(b for b in cfg.branches if b.pattern == "main")
    assert "black --check" in main_rule.lint
    assert "pytest --cov" in main_rule.tests
    assert main_rule.skip is False


def test_branch_rule_skip():
    cfg = load_config(SAMPLE_CONFIG)
    chore_rule = next(b for b in cfg.branches if b.pattern == "chore/*")
    assert chore_rule.skip is True


def test_file_not_found():
    with pytest.raises(FileNotFoundError, match="nonexistent.yml"):
        load_config("nonexistent.yml")


def test_missing_version(tmp_path):
    cfg_file = tmp_path / ".hookguard.yml"
    cfg_file.write_text("default_lint:\n  - flake8\n")
    with pytest.raises(ValueError, match="version"):
        load_config(str(cfg_file))


def test_invalid_yaml_type(tmp_path):
    cfg_file = tmp_path / ".hookguard.yml"
    cfg_file.write_text("- just a list\n")
    with pytest.raises(ValueError, match="YAML mapping"):
        load_config(str(cfg_file))


def test_branch_missing_pattern(tmp_path):
    content = textwrap.dedent("""\
        version: 1
        branches:
          - lint:
              - flake8
    """)
    cfg_file = tmp_path / ".hookguard.yml"
    cfg_file.write_text(content)
    with pytest.raises(ValueError, match="pattern"):
        load_config(str(cfg_file))


def test_empty_branches(tmp_path):
    cfg_file = tmp_path / ".hookguard.yml"
    cfg_file.write_text("version: 1\n")
    cfg = load_config(str(cfg_file))
    assert cfg.branches == []
