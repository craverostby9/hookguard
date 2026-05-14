"""Tests for hookguard.schema module."""

from __future__ import annotations

import pytest

jsonschema = pytest.importorskip("jsonschema")

from hookguard.schema import validate_raw_config  # noqa: E402


VALID_CONFIG = {
    "version": 1,
    "default_lint": ["flake8"],
    "default_tests": ["pytest"],
    "branches": [
        {"pattern": "main", "lint": ["flake8"], "tests": ["pytest"]},
        {"pattern": "chore/*", "skip": True},
    ],
}


def test_valid_config_passes():
    validate_raw_config(VALID_CONFIG)


def test_missing_version_fails():
    bad = {"default_lint": ["flake8"]}
    with pytest.raises(jsonschema.ValidationError):
        validate_raw_config(bad)


def test_wrong_version_fails():
    bad = {"version": 2}
    with pytest.raises(jsonschema.ValidationError):
        validate_raw_config(bad)


def test_extra_top_level_key_fails():
    bad = {**VALID_CONFIG, "unknown_key": True}
    with pytest.raises(jsonschema.ValidationError):
        validate_raw_config(bad)


def test_branch_missing_pattern_fails():
    bad = {"version": 1, "branches": [{"lint": ["flake8"]}]}
    with pytest.raises(jsonschema.ValidationError):
        validate_raw_config(bad)


def test_lint_must_be_list_of_strings():
    bad = {"version": 1, "branches": [{"pattern": "main", "lint": "flake8"}]}
    with pytest.raises(jsonschema.ValidationError):
        validate_raw_config(bad)
