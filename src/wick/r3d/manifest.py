"""Frozen experiment manifesto — must be written before holdout evaluation."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from wick.backtest.costs import COST_MODEL_VERSION
from wick.patterns.params import DEFAULT_PARAMS, DETECTOR_VERSION
from wick.r3d.universe import (
    CONFIRMATION_VARIANTS,
    COST_SCENARIOS,
    HORIZONS,
    N_BOOTSTRAP,
    PATTERN_TYPES,
    SEED,
    TREND_BASELINE_V1,
)


@dataclass(frozen=True)
class ExperimentVariant:
    strategy_id: str
    pattern_type: str
    horizon: int
    confirmation_used: bool
    cost_scenario: str
    signal_filter: str  # bullish executable only for mechanical gate


def build_variants() -> list[ExperimentVariant]:
    """All planned variants. Holdout must not be used to select among these."""
    out: list[ExperimentVariant] = []
    for pattern in PATTERN_TYPES:
        for horizon in HORIZONS:
            for conf in CONFIRMATION_VARIANTS:
                for cost in COST_SCENARIOS:
                    conf_tag = "confirmed" if conf else "raw"
                    sid = f"{pattern.lower()}_h{horizon}_{conf_tag}_{cost.lower()}"
                    out.append(
                        ExperimentVariant(
                            strategy_id=sid,
                            pattern_type=pattern,
                            horizon=horizon,
                            confirmation_used=conf,
                            cost_scenario=cost,
                            signal_filter="bullish",
                        )
                    )
    return out


def write_manifest(path: Path, *, coverage: list[dict[str, Any]]) -> dict[str, Any]:
    variants = [asdict(v) for v in build_variants()]
    payload = {
        "manifest_version": "1.0.0",
        "frozen_at": datetime.now(UTC).isoformat(),
        "holdout_opened": False,
        "detector_version": DETECTOR_VERSION,
        "parameters_hash": DEFAULT_PARAMS.parameters_hash(),
        "cost_model_version": COST_MODEL_VERSION,
        "trend_baseline": TREND_BASELINE_V1,
        "seed": SEED,
        "n_bootstrap": N_BOOTSTRAP,
        "train_frac": 0.70,
        "horizons": list(HORIZONS),
        "cost_scenarios": list(COST_SCENARIOS),
        "pattern_types": list(PATTERN_TYPES),
        "variants": variants,
        "coverage_at_freeze": coverage,
        "notes": [
            "Manifest frozen before holdout evaluation.",
            "No parameter recalibration after freeze.",
            "COST_MODEL_VERSION remains provisional.",
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def mark_holdout_opened(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("holdout_opened"):
        raise RuntimeError("Holdout already opened — refusing to reuse/reopen")
    data["holdout_opened"] = True
    data["holdout_opened_at"] = datetime.now(UTC).isoformat()
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
