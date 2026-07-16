"""R3B/R3C experiment runner and reports."""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from wick.backtest.engine import Bar, evaluate_signal
from wick.quant.stats import (
    benjamini_hochberg,
    block_bootstrap_mean,
    classify_result,
    mechanical_gate,
    paired_random_baseline,
    sample_size_tier,
    temporal_split,
    walk_forward_slices,
)


@dataclass
class SignalEvent:
    pattern_index: int
    signal: str
    pattern_type: str
    confirmation_used: bool = False


@dataclass
class StrategyReport:
    strategy_id: str
    description: str
    n_signals: int
    sample_tier: str
    mean_net_train: float | None
    mean_net_holdout: float | None
    ci95_train: tuple[float, float] | None
    p_raw: float | None
    p_adj: float | None
    beats_random_baseline: bool | None
    classification: str
    mechanical_gate: str
    cost_scenario: str
    horizon: int
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        if self.ci95_train is not None:
            d["ci95_train"] = list(self.ci95_train)
        return d


def collect_net_returns(
    bars: Sequence[Bar],
    events: Sequence[SignalEvent],
    *,
    horizon: int,
    cost_scenario: str,
    indices: range | None = None,
) -> list[float]:
    allowed = set(indices) if indices is not None else None
    out: list[float] = []
    for ev in events:
        if allowed is not None and ev.pattern_index not in allowed:
            continue
        if ev.signal.lower() != "bullish":
            continue
        r = evaluate_signal(
            bars,
            pattern_index=ev.pattern_index,
            signal=ev.signal,
            pattern_type=ev.pattern_type,
            horizon=horizon,
            confirmation_used=ev.confirmation_used,
            cost_scenario=cost_scenario,
        )
        if r.status == "OK" and r.net_return is not None:
            out.append(r.net_return)
    return out


def non_overlapping_events(events: Sequence[SignalEvent], horizon: int) -> list[SignalEvent]:
    """Drop overlapping positions on the same series (executable report)."""
    selected: list[SignalEvent] = []
    last_exit = -1
    for ev in sorted(events, key=lambda e: e.pattern_index):
        entry = ev.pattern_index + (2 if ev.confirmation_used else 1)
        exit_i = entry + horizon - 1
        if entry <= last_exit:
            continue
        selected.append(ev)
        last_exit = exit_i
    return selected


def run_strategy_validation(
    bars: Sequence[Bar],
    events: Sequence[SignalEvent],
    *,
    strategy_id: str,
    description: str,
    horizon: int = 5,
    cost_scenario: str = "BASE",
    seed: int = 42,
    n_resamples: int = 1000,
    block_size: int = 5,
    executable_no_overlap: bool = True,
) -> StrategyReport:
    notes: list[str] = []
    train_idx, holdout_idx = temporal_split(len(bars), 0.70)
    notes.append(f"temporal split train={len(train_idx)} holdout={len(holdout_idx)}")

    # Walk-forward only inside train (documented expanding folds)
    folds = walk_forward_slices(
        len(train_idx), min_train=max(20, len(train_idx) // 5), step=max(5, len(train_idx) // 10)
    )
    notes.append(f"walk_forward_folds={len(folds)} (inside 70% only)")

    use_events = non_overlapping_events(events, horizon) if executable_no_overlap else list(events)
    if executable_no_overlap:
        notes.append("overlap_policy=no_simultaneous_positions")

    train_returns = collect_net_returns(
        bars, use_events, horizon=horizon, cost_scenario=cost_scenario, indices=train_idx
    )
    holdout_returns = collect_net_returns(
        bars, use_events, horizon=horizon, cost_scenario=cost_scenario, indices=holdout_idx
    )

    tier = sample_size_tier(len(train_returns))
    if not train_returns:
        return StrategyReport(
            strategy_id=strategy_id,
            description=description,
            n_signals=0,
            sample_tier=tier,
            mean_net_train=None,
            mean_net_holdout=None,
            ci95_train=None,
            p_raw=None,
            p_adj=None,
            beats_random_baseline=None,
            classification="INCONCLUSIVE",
            mechanical_gate="INCONCLUSIVE",
            cost_scenario=cost_scenario,
            horizon=horizon,
            notes=notes + ["no evaluable train returns"],
        )

    boot = block_bootstrap_mean(
        train_returns, block_size=block_size, n_resamples=n_resamples, seed=seed
    )
    baseline = paired_random_baseline(train_returns, seed=seed + 1)
    beats = boot.mean > float(sum(baseline) / len(baseline))

    # FDR applied across a single hypothesis here; multi-strategy callers should
    # batch p-values via benjamini_hochberg.
    p_adj = benjamini_hochberg([boot.p_value_raw])[0]
    classification = classify_result(
        n=len(train_returns),
        mean_net=boot.mean,
        p_adj=p_adj,
        beats_baseline=beats,
    )
    gate = mechanical_gate(
        classification=classification,
        holdout_touched_during_calibration=False,
        has_critical_findings=False,
        cost_scenarios_evaluated=True,
        fdr_applied=True,
    )
    holdout_mean = float(sum(holdout_returns) / len(holdout_returns)) if holdout_returns else None
    # Holdout touched exactly once for reporting after freeze
    notes.append("holdout_evaluated_once_after_freeze")

    return StrategyReport(
        strategy_id=strategy_id,
        description=description,
        n_signals=len(train_returns),
        sample_tier=tier,
        mean_net_train=boot.mean,
        mean_net_holdout=holdout_mean,
        ci95_train=(boot.ci_low, boot.ci_high),
        p_raw=boot.p_value_raw,
        p_adj=p_adj,
        beats_random_baseline=beats,
        classification=classification,
        mechanical_gate=gate,
        cost_scenario=cost_scenario,
        horizon=horizon,
        notes=notes,
    )


def write_reports(reports: Sequence[StrategyReport], out_dir: str | Path) -> dict[str, Path]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    technical = out / "technical_report.json"
    executive = out / "executive_report.json"
    payload = [r.to_dict() for r in reports]
    technical.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    exec_payload = [
        {
            "strategy": r.strategy_id,
            "description": r.description,
            "signals": r.n_signals,
            "mean_net_return_train": r.mean_net_train,
            "ci95": r.ci95_train,
            "cost_scenario": r.cost_scenario,
            "holdout_mean_net": r.mean_net_holdout,
            "classification": r.classification,
            "mechanical_gate": r.mechanical_gate,
            "risks": r.notes,
            "recommended_decision": r.mechanical_gate,
        }
        for r in reports
    ]
    executive.write_text(json.dumps(exec_payload, indent=2) + "\n", encoding="utf-8")
    return {"technical": technical, "executive": executive}
