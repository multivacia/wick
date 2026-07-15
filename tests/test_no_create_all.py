"""Ensure application code does not use create_all as schema source."""

from pathlib import Path


def test_no_create_all_in_application_code():
    root = Path(__file__).resolve().parents[1] / "src"
    offenders = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "create_all" in text:
            offenders.append(str(path.relative_to(root.parents[0])))
    assert offenders == [], f"create_all found in application code: {offenders}"
