"""R3A auditable trade engine — long-only executable; bearish directional only.

Invariants (QUANT_METHODOLOGY / R3_SPEC):

No confirmation:
  pattern at t → entry_index = t+1 → entry_price = open[t+1]

With confirmation:
  pattern at t → confirmation after close[t+1] → entry_index = t+2 → open[t+2]
  NEVER enter at open[t+1] when using confirmation.

exit_index = entry_index + N - 1
exit_price = close[exit_index]
gross_return (long) = exit/entry - 1
directional_return (bearish metric) = entry/exit - 1
net_return = gross_return - total_cost
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass
from typing import Any

from wick.backtest.costs import COST_MODEL_VERSION, get_scenario

CALCULATION_VERSION = "1.0.0"
HORIZONS = (1, 3, 5, 10)

STATUS_OK = "OK"
STATUS_INSUFFICIENT = "NOT_EVALUABLE_INSUFFICIENT_FUTURE_DATA"
STATUS_INVALID = "INVALID_PRICE"


@dataclass(frozen=True)
class Bar:
    open: float
    high: float
    low: float
    close: float


@dataclass(frozen=True)
class TradeResult:
    experiment_id: str
    strategy_variant: str
    pattern_type: str
    signal: str
    horizon: int
    cost_scenario: str
    cost_model_version: str
    calculation_version: str
    confirmation_used: bool
    pattern_index: int
    entry_index: int | None
    exit_index: int | None
    entry_price: float | None
    exit_price: float | None
    entry_fee: float
    exit_fee: float
    entry_slippage: float
    exit_slippage: float
    gross_return: float | None
    net_return: float | None
    directional_return: float | None
    directional_hit: bool | None
    executable_long: bool
    status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def entry_index_for(*, pattern_index: int, confirmation_used: bool) -> int:
    return pattern_index + (2 if confirmation_used else 1)


def exit_index_for(*, entry_index: int, horizon: int) -> int:
    if horizon < 1:
        raise ValueError("horizon must be >= 1")
    return entry_index + horizon - 1


def gross_return_long(entry_price: float, exit_price: float) -> float:
    if entry_price <= 0 or exit_price <= 0:
        raise ValueError("prices must be positive")
    return exit_price / entry_price - 1.0


def directional_return_bearish(entry_price: float, exit_price: float) -> float:
    """Predictive metric only — NOT executable short PnL."""
    if entry_price <= 0 or exit_price <= 0:
        raise ValueError("prices must be positive")
    return entry_price / exit_price - 1.0


def evaluate_signal(
    bars: Sequence[Bar],
    *,
    pattern_index: int,
    signal: str,
    pattern_type: str,
    horizon: int,
    confirmation_used: bool,
    cost_scenario: str = "BASE",
    experiment_id: str = "exp_default",
    strategy_variant: str = "long_only_v1",
) -> TradeResult:
    """Evaluate one pattern occurrence. Never creates a short position."""
    scenario = get_scenario(cost_scenario)
    signal_l = signal.lower()
    executable_long = signal_l == "bullish"

    e_idx = entry_index_for(pattern_index=pattern_index, confirmation_used=confirmation_used)
    x_idx = exit_index_for(entry_index=e_idx, horizon=horizon)

    base_kwargs = dict(
        experiment_id=experiment_id,
        strategy_variant=strategy_variant,
        pattern_type=pattern_type,
        signal=signal_l,
        horizon=horizon,
        cost_scenario=scenario.name,
        cost_model_version=COST_MODEL_VERSION,
        calculation_version=CALCULATION_VERSION,
        confirmation_used=confirmation_used,
        pattern_index=pattern_index,
        entry_fee=scenario.entry_fee,
        exit_fee=scenario.exit_fee,
        entry_slippage=scenario.entry_slippage,
        exit_slippage=scenario.exit_slippage,
        executable_long=executable_long,
    )

    if e_idx >= len(bars) or x_idx >= len(bars):
        return TradeResult(
            **base_kwargs,
            entry_index=e_idx if e_idx < len(bars) else None,
            exit_index=None,
            entry_price=None,
            exit_price=None,
            gross_return=None,
            net_return=None,
            directional_return=None,
            directional_hit=None,
            status=STATUS_INSUFFICIENT,
        )

    entry_price = float(bars[e_idx].open)
    exit_price = float(bars[x_idx].close)
    if entry_price <= 0 or exit_price <= 0:
        return TradeResult(
            **base_kwargs,
            entry_index=e_idx,
            exit_index=x_idx,
            entry_price=entry_price,
            exit_price=exit_price,
            gross_return=None,
            net_return=None,
            directional_return=None,
            directional_hit=None,
            status=STATUS_INVALID,
        )

    if executable_long:
        gross = gross_return_long(entry_price, exit_price)
        net = gross - scenario.total_cost
        directional = None
        hit = gross > 0
    elif signal_l == "bearish":
        # Directional metric only — no short PnL labeling
        gross = None
        net = None
        directional = directional_return_bearish(entry_price, exit_price)
        hit = directional > 0
    else:
        gross = None
        net = None
        directional = None
        hit = None

    return TradeResult(
        **base_kwargs,
        entry_index=e_idx,
        exit_index=x_idx,
        entry_price=entry_price,
        exit_price=exit_price,
        gross_return=gross,
        net_return=net,
        directional_return=directional,
        directional_hit=hit,
        status=STATUS_OK,
    )


def evaluate_horizons(
    bars: Sequence[Bar],
    *,
    pattern_index: int,
    signal: str,
    pattern_type: str,
    confirmation_used: bool,
    cost_scenarios: Sequence[str] = ("BASE",),
    experiment_id: str = "exp_default",
) -> list[TradeResult]:
    out: list[TradeResult] = []
    for n in HORIZONS:
        for scen in cost_scenarios:
            out.append(
                evaluate_signal(
                    bars,
                    pattern_index=pattern_index,
                    signal=signal,
                    pattern_type=pattern_type,
                    horizon=n,
                    confirmation_used=confirmation_used,
                    cost_scenario=scen,
                    experiment_id=experiment_id,
                )
            )
    return out
