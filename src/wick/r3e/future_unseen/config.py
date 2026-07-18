"""Frozen configuration for R3E future-unseen final validation.

Do not widen grids, thresholds, or hypotheses after FUTURE_UNSEEN_CUTOFF.
Historical / exploratory / synthetic datasets are forbidden as evidence.
"""

from __future__ import annotations

from datetime import UTC, datetime

from wick.r3d.universe import UNIVERSE
from wick.r3e.config import (
    COST_MODEL_VERSION,
    COST_SCENARIOS,
    DETECTOR_VERSION,
    FEATURE_SET_VERSION,
    FEATURE_SETS,
    HORIZONS,
    LOGISTIC_GRID,
    MODEL_VERSION,
    N_BOOTSTRAP,
    RANDOM_SEED,
    RIDGE_GRID,
    SCORE_POLICIES,
)
from wick.r3e.config import (
    EXPERIMENT_ID as PARENT_R3E_EXPERIMENT_ID,
)
from wick.r3e.config import (
    PARENT_EXPERIMENT_ID as R3D_PARENT_EXPERIMENT_ID,
)

# --- Experiment identity ---
EXPERIMENT_ID = "r3e-future-unseen-v1"
PARENT_EXPERIMENT_ID = PARENT_R3E_EXPERIMENT_ID  # r3e-contextual-edge-v1
GRANDPARENT_EXPERIMENT_ID = R3D_PARENT_EXPERIMENT_ID  # r3d-real-validation-v1

# Official immutable cutoff (market timestamp must be strictly after this).
# Defined at infrastructure implementation time (UTC).
FUTURE_UNSEEN_CUTOFF = datetime(2026, 7, 18, 1, 30, 0, tzinfo=UTC)
FUTURE_UNSEEN_CUTOFF_ISO = "2026-07-18T01:30:00+00:00"

# Forbidden data roots (must never feed final gate evidence)
FORBIDDEN_DATA_ROOTS = (
    "reports/r3e",
    "reports/r3e_real",
    "reports/r3d",
    "reports/r3",
    "data/synthetic",
)

# Collection completeness (operational; no peeking at effect during collection)
MIN_CALENDAR_DAYS_AFTER_CUTOFF = 90
MIN_BARS_PER_SERIES = 200  # closed market bars after cutoff
MIN_SERIES_COMPLETE = 16  # of 20 official series
MIN_OOS_TRADES_PRIMARY = 100  # aggregate OOS trades on primary slice for decision
MIN_OOS_TRADES_PER_SERIES_PRIMARY = 10

# Primary decision slice (frozen; matches R3E exploratory primary)
PRIMARY_COST = "BASE"
PRIMARY_HORIZON = 5
PRIMARY_OVERLAP = "NON_OVERLAPPING_LONG_ONLY"
FDR_ALPHA = 0.05

# Gate effect thresholds (pre-registered; not tuned on historical R3E outcomes)
MIN_DELTA_CANDLE = 0.0  # M5 - M4 must be strictly > this for APPROVED
REQUIRE_CI_LOW_POSITIVE = True
REQUIRE_M5_MEAN_NET_POSITIVE = True
MIN_ABS_EFFECT_SIZE = 0.0  # optional floor; 0 means rely on CI/p_adj

# Re-exports of frozen R3E protocol (no new grids)
SERIES_UNIVERSE = tuple((s.symbol, s.timeframe, s.source) for s in UNIVERSE)
MODELS = ("M0", "M1", "M2", "M3", "M4", "M5")
OVERLAP_POLICIES = ("ALL_SIGNALS", "NON_OVERLAPPING_LONG_ONLY")

PROTOCOL_REF = {
    "parent_experiment_id": PARENT_EXPERIMENT_ID,
    "grandparent_experiment_id": GRANDPARENT_EXPERIMENT_ID,
    "model_version": MODEL_VERSION,
    "feature_set_version": FEATURE_SET_VERSION,
    "cost_model_version": COST_MODEL_VERSION,
    "detector_version": DETECTOR_VERSION,
    "random_seed": RANDOM_SEED,
    "n_bootstrap": N_BOOTSTRAP,
    "horizons": list(HORIZONS),
    "cost_scenarios": list(COST_SCENARIOS),
    "score_policies": list(SCORE_POLICIES),
    "logistic_grid": LOGISTIC_GRID,
    "ridge_grid": RIDGE_GRID,
    "feature_sets_m4": list(FEATURE_SETS["M4"]),
    "feature_sets_m5": list(FEATURE_SETS["M5"]),
    "tuning_after_cutoff_forbidden": True,
    "optional_stopping_forbidden": True,
    "historical_as_future_forbidden": True,
}

# Official status labels
STATUS_COLLECTION_NOT_STARTED = "NOT_STARTED"
STATUS_COLLECTION_IN_PROGRESS = "IN_PROGRESS"
STATUS_COLLECTION_COMPLETE = "COMPLETE"
GATE_PENDING = "PENDING_FUTURE_UNSEEN_DATA"
GATE_APPROVED = "APPROVED"
GATE_REJECTED = "REJECTED"
GATE_INCONCLUSIVE = "INCONCLUSIVE"
