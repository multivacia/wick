"""Temporal eligibility for historical operational backfill.

Must not replace or alter FutureUnseenEligibilityPolicy
(assert_strictly_after_cutoff in wick.r3e.future_unseen.protections).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from wick.r3e.future_unseen.config import FUTURE_UNSEEN_CUTOFF
from wick.r3e.future_unseen.protections import parse_market_ts
from wick.r3e.operational_backfill.config import BACKFILL_END, BACKFILL_START


class HistoricalBackfillPolicyError(ValueError):
    """Rejection under HistoricalOperationalBackfillPolicy."""


@dataclass(frozen=True)
class HistoricalOperationalBackfillPolicy:
    """Accept market_ts in [start, end], never after FUTURE_UNSEEN_CUTOFF."""

    start: datetime = BACKFILL_START
    end: datetime = BACKFILL_END
    cutoff: datetime = FUTURE_UNSEEN_CUTOFF

    def assert_eligible(self, market_ts: str | datetime) -> datetime:
        dt = parse_market_ts(market_ts)
        if dt > self.cutoff:
            raise HistoricalBackfillPolicyError(
                f"market_ts {dt.isoformat()} is after FUTURE_UNSEEN_CUTOFF "
                f"{self.cutoff.isoformat()}; historical sandbox rejects post-cutoff bars"
            )
        if dt < self.start:
            raise HistoricalBackfillPolicyError(
                f"market_ts {dt.isoformat()} is before backfill start {self.start.isoformat()}"
            )
        if dt > self.end:
            raise HistoricalBackfillPolicyError(
                f"market_ts {dt.isoformat()} is after backfill end {self.end.isoformat()}"
            )
        return dt

    def is_eligible(self, market_ts: str | datetime) -> bool:
        try:
            self.assert_eligible(market_ts)
            return True
        except (HistoricalBackfillPolicyError, Exception):
            return False
