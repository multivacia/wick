#!/usr/bin/env python3
"""Validate AI governance artifacts structurally (offline, non-scientific)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from wick.ai_governance.artifact_validator import validate_paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Markdown artifacts to validate (default: known governance/impact samples if present)",
    )
    args = parser.parse_args(argv)
    paths = list(args.paths)
    if not paths:
        defaults = [
            Path("docs/ai-impact/IMPACT-ASSESSMENT-001_IMPACT_ASSESSMENT.md"),
            Path("docs/ai-specs/R3E-B1-PR12-INCREMENTAL-COLLECTOR_REVIEW_SPEC.md"),
            Path(
                "docs/ai-reviews/R3E-B1-PR12-INCREMENTAL-COLLECTOR_TECHNICAL-AND-SCIENTIFIC-SAFETY_REVIEW.md"
            ),
            Path(
                "reports/ai-implementation/R3E-B1-PR12-INCREMENTAL-COLLECTOR_IMPLEMENTATION_REPORT.md"
            ),
        ]
        paths = [p for p in defaults if p.is_file()]
    if not paths:
        print("No artifacts found to validate", file=sys.stderr)
        return 2
    issues = validate_paths(paths)
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    for issue in issues:
        print(f"{issue.severity.upper()}: {issue.path}: {issue.message}")
    print(f"checked={len(paths)} errors={len(errors)} warnings={len(warnings)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
