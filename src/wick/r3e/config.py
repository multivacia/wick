"""R3E frozen configuration — do not widen grids after results."""

from __future__ import annotations

EXPERIMENT_ID = "r3e-contextual-edge-v1"
PARENT_EXPERIMENT_ID = "r3d-real-validation-v1"
MODEL_VERSION = "1.0.0"
FEATURE_SET_VERSION = "1.0.0"
COST_MODEL_VERSION = "1.0.0-provisional"
DETECTOR_VERSION = "1.0.0"
RANDOM_SEED = 42
N_BOOTSTRAP = 1000

# R3D holdout was the final 30%; R3E must not use it as a new final holdout.
R3D_HOLDOUT_FRAC = 0.30
HOLDOUT_POLICY = (
    "R3D_HOLDOUT_EXCLUDED_FROM_R3E_FINAL; "
    "R3E_DEVELOPMENT=NESTED_WALK_FORWARD; "
    "R3E_FINAL_VALIDATION=PENDING_FUTURE_UNSEEN_DATA"
)

HORIZONS = (1, 3, 5, 10)
COST_SCENARIOS = ("OPTIMISTIC", "BASE", "STRESSED")

NUMERIC_FEATURES = (
    "sma_20_slope",
    "distance_from_sma_20",
    "return_5",
    "return_20",
    "volume_ratio_20",
    "atr_14",
    "normalized_atr",
    "range_position_20",
)

CATEGORICAL_FEATURES = (
    "trend_direction",
    "trend_strength",
    "volume_regime",
    "volatility_regime",
    "range_position_bucket",
    "asset_id",
    "timeframe",
)

CANDLE_FEATURES = (
    "pattern_type",
    "signal",
    "confirmation_variant",
)

FEATURE_SETS = {
    "M1": (
        "trend_direction",
        "trend_strength",
        "sma_20_slope",
        "distance_from_sma_20",
        "return_5",
        "return_20",
    ),
    "M2": (
        "trend_direction",
        "trend_strength",
        "sma_20_slope",
        "distance_from_sma_20",
        "return_5",
        "return_20",
        "volume_ratio_20",
        "volume_regime",
    ),
    "M3": (
        "trend_direction",
        "trend_strength",
        "sma_20_slope",
        "distance_from_sma_20",
        "return_5",
        "return_20",
        "volume_ratio_20",
        "volume_regime",
        "atr_14",
        "normalized_atr",
        "volatility_regime",
    ),
    "M4": NUMERIC_FEATURES + CATEGORICAL_FEATURES,
    "M5": NUMERIC_FEATURES + CATEGORICAL_FEATURES + CANDLE_FEATURES,
}

LOGISTIC_GRID = {
    "C": [0.01, 0.1, 1.0, 10.0],
    "class_weight": [None, "balanced"],
}

RIDGE_GRID = {
    "alpha": [0.01, 0.1, 1.0, 10.0, 100.0],
}

SCORE_POLICIES = (
    "TOP_10_PERCENT",
    "TOP_20_PERCENT",
    "PROBABILITY_055",
    "PROBABILITY_060",
)

MODELS = ("M0", "M1", "M2", "M3", "M4", "M5")

# Nested WF defaults (outer expanding; inner for hyperparam/threshold)
OUTER_MIN_TRAIN = 80
OUTER_TEST_SIZE = 40
INNER_VAL_FRAC = 0.25
