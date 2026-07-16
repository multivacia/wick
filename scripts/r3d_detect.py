#!/usr/bin/env python3
"""Run R2 detection across the R3D universe."""

from __future__ import annotations

import time

from sqlalchemy import select

from wick.config import get_settings
from wick.db.models import Asset
from wick.db.session import session_scope
from wick.detection.service import DetectionService
from wick.patterns.params import DEFAULT_PARAMS, DETECTOR_VERSION
from wick.r3d.universe import UNIVERSE


def main() -> None:
    settings = get_settings()
    t0 = time.time()
    with session_scope(settings) as session:
        svc = DetectionService(
            session,
            detector_version=DETECTOR_VERSION,
            params=DEFAULT_PARAMS,
            dry_run=False,
        )
        for spec in UNIVERSE:
            asset = session.execute(
                select(Asset).where(Asset.symbol == spec.symbol, Asset.source == spec.source)
            ).scalar_one()
            t1 = time.time()
            summary = svc.detect_asset_timeframe(
                asset_id=asset.id,
                timeframe=spec.timeframe,
                incremental=False,
                reprocess=True,
            )
            n_hits = len(summary.hits)
            summary.hits.clear()
            print(
                f"{spec.symbol} {spec.timeframe}: scanned={summary.candles_scanned} "
                f"ins={summary.patterns_inserted} unchanged={summary.patterns_unchanged} "
                f"conf={summary.confirmations_upserted} hits={n_hits} "
                f"dt={time.time() - t1:.1f}s",
                flush=True,
            )
            session.commit()
    print(f"TOTAL {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
