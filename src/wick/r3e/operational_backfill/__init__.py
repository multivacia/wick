"""R3E operational historical backfill (non-scientific, non-future-unseen).

This namespace validates acquisition/transform/ingest plumbing only.
It must never write into data/future_unseen or execute M4/M5/validate/gate.
"""

from __future__ import annotations

from wick.r3e.operational_backfill.config import (
    BACKFILL_END_ISO,
    BACKFILL_START_ISO,
    DATA_ORIGIN,
    EXPERIMENT_ID,
)

__all__ = [
    "BACKFILL_END_ISO",
    "BACKFILL_START_ISO",
    "DATA_ORIGIN",
    "EXPERIMENT_ID",
]
