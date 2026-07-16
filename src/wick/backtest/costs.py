"""R3A cost model — versioned scenarios.

Numeric defaults are provisional v1 aligned to the R3 manual example
(total_cost BASE = 0.0024). Changing these values requires a new
cost_model_version and human acknowledgment before R4 promotion.
"""

from __future__ import annotations

from dataclasses import dataclass

COST_MODEL_VERSION = "1.0.0-provisional"


@dataclass(frozen=True)
class CostScenario:
    name: str
    entry_fee: float
    exit_fee: float
    entry_slippage: float
    exit_slippage: float

    @property
    def total_cost(self) -> float:
        return self.entry_fee + self.exit_fee + self.entry_slippage + self.exit_slippage


SCENARIOS: dict[str, CostScenario] = {
    "OPTIMISTIC": CostScenario("OPTIMISTIC", 0.0005, 0.0005, 0.0001, 0.0001),
    "BASE": CostScenario("BASE", 0.0010, 0.0010, 0.0002, 0.0002),
    "STRESSED": CostScenario("STRESSED", 0.0020, 0.0020, 0.0005, 0.0005),
    "ZERO": CostScenario("ZERO", 0.0, 0.0, 0.0, 0.0),
}


def get_scenario(name: str) -> CostScenario:
    key = name.upper()
    if key not in SCENARIOS:
        raise ValueError(f"Unknown cost scenario: {name}")
    return SCENARIOS[key]
