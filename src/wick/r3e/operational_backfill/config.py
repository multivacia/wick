"""Frozen labels and window for R3E operational historical backfill."""

from __future__ import annotations

from datetime import UTC, datetime

from wick.r3d.universe import UNIVERSE
from wick.r3e.future_unseen.config import FUTURE_UNSEEN_CUTOFF, FUTURE_UNSEEN_CUTOFF_ISO

EXPERIMENT_ID = "r3e-operational-backfill-90d-v1"

# Historical window: 90 days ending at the immutable future-unseen cutoff.
BACKFILL_START = datetime(2026, 4, 19, 1, 30, 0, tzinfo=UTC)
BACKFILL_END = FUTURE_UNSEEN_CUTOFF  # inclusive upper bound for historical sandbox
BACKFILL_START_ISO = "2026-04-19T01:30:00+00:00"
BACKFILL_END_ISO = FUTURE_UNSEEN_CUTOFF_ISO

DATA_ORIGIN = "HISTORICAL_OPERATIONAL_BACKFILL"
SCIENTIFIC_EVIDENCE_ELIGIBLE = False
FUTURE_UNSEEN_ELIGIBLE = False
ECONOMIC_INTERPRETATION_ALLOWED = False
GATE_IMPACT_ALLOWED = False

CLASSIFICATION = {
    "DATA_ORIGIN": DATA_ORIGIN,
    "SCIENTIFIC_EVIDENCE_ELIGIBLE": SCIENTIFIC_EVIDENCE_ELIGIBLE,
    "FUTURE_UNSEEN_ELIGIBLE": FUTURE_UNSEEN_ELIGIBLE,
    "ECONOMIC_INTERPRETATION_ALLOWED": ECONOMIC_INTERPRETATION_ALLOWED,
    "GATE_IMPACT_ALLOWED": GATE_IMPACT_ALLOWED,
}

# Official universe (source of truth: wick.r3d.universe.UNIVERSE / SERIES_UNIVERSE).
SERIES_UNIVERSE = tuple((s.symbol, s.timeframe, s.source) for s in UNIVERSE)

# Operational completeness heuristics for historical sandbox (not gate criteria).
MIN_BARS_CRYPTO_1H = 1800  # ~75d * 24
MIN_BARS_CRYPTO_1D = 80
MIN_BARS_STOCK_1D = 50
MIN_BARS_STOCK_1H = 250

FORBIDDEN_EFFECT_KEYS = frozenset(
    {
        "delta_candle",
        "delta_m5_m4",
        "p_raw",
        "p_adj",
        "p_value",
        "mean_net",
        "hit_rate",
        "sharpe",
        "gate_decision",
        "fdr",
        "economic",
        "trade_list",
        "signal",
    }
)
