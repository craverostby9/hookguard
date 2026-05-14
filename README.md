# hookguard

> Pre-commit hook manager that enforces per-branch lint and test rules via a simple YAML config.

---

## Installation

```bash
pip install hookguard
hookguard install
```

---

## Usage

Create a `.hookguard.yml` file in the root of your repository:

```yaml
branches:
  main:
    lint:
      - flake8 .
      - black --check .
    tests:
      - pytest tests/
  feature/*:
    lint:
      - flake8 .
    tests:
      - pytest tests/ -m "not slow"
  default:
    lint:
      - flake8 .
```

Once configured, hookguard automatically runs the matching rules before every commit based on the active branch.

```bash
# Manually run checks for the current branch
hookguard run

# Uninstall hooks from the repository
hookguard uninstall
```

If any lint or test command exits with a non-zero status, the commit is blocked and the output is displayed in the terminal.

---

## Requirements

- Python 3.8+
- Git repository

---

## License

This project is licensed under the [MIT License](LICENSE).