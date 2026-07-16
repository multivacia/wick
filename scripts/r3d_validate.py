#!/usr/bin/env python3
"""Run R3D validation after ingestion (freeze manifesto, then holdout once)."""

from __future__ import annotations

import sys
from pathlib import Path

from wick.config import get_settings
from wick.db.session import session_scope
from wick.r3d.pipeline import run_r3d


def main() -> int:
    out = Path("reports/r3d")
    settings = get_settings()
    with session_scope(settings) as session:
        executive = run_r3d(session, out, skip_detection=False)
    print("R3D executive gate counts:", executive.get("gate_counts"), flush=True)
    print("coverage:", executive.get("coverage_status_counts"), flush=True)
    print("passed:", len(executive.get("passed", [])), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
