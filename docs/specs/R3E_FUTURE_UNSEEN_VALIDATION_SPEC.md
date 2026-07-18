# Wick — R3E Future-Unseen Final Validation Specification

> **Status:** frozen infrastructure specification  
> **Nature:** confirmatory protocol for data that did not exist at cutoff  
> **Non-goal:** this document does not approve R3E or open R4

## 1. Experiment identity

```text
experiment_id              = r3e-future-unseen-v1
parent_experiment_id       = r3e-contextual-edge-v1
grandparent_experiment_id  = r3d-real-validation-v1
```

Frozen protocol references (no new grids / thresholds from historical outcomes):

| Item | Value |
|------|--------|
| model_version | `1.0.0` |
| feature_set_version | `1.0.0` |
| cost_model_version | `1.0.0-provisional` |
| detector_version | `1.0.0` |
| random_seed | `42` |
| n_bootstrap | `1000` |
| logistic grid | `C ∈ {0.01,0.1,1,10}`, `class_weight ∈ {None,balanced}` |
| ridge grid | `alpha ∈ {0.01,0.1,1,10,100}` |
| score policies | `TOP_10_PERCENT`, `TOP_20_PERCENT`, `PROBABILITY_055`, `PROBABILITY_060` |

## 2. Epistemic rule

The system **must not** fabricate, simulate, resample, or reuse historical data as future-unseen evidence.

Rejected as final-gate evidence:

- synthetic structural panels;
- development / exploratory real OHLCV under `reports/r3e_real/`;
- R3D holdout and all pre-cutoff market timestamps;
- backfills and re-ingested history with `market_ts <= cutoff`;
- any path under forbidden roots (`reports/r3e`, `reports/r3e_real`, `reports/r3d`, `reports/r3`, `data/synthetic`).

Ingest time is **not** a substitute for market timestamp.

## 3. Official cutoff (immutable)

```text
FUTURE_UNSEEN_CUTOFF = 2026-07-18T01:30:00+00:00
```

Only observations with **market** timestamp **strictly greater** than the cutoff may enter `future_unseen`.

Cutoff manifesto: `data/future_unseen/manifests/cutoff_manifest.json`.

## 4. Universe

Official R3D/R3E series (20):

- Crypto (Binance): BTC/USDT, ETH/USDT, SOL/USDT, BNB/USDT, XRP/USDT × {1h, 1d}
- Stocks (Yahoo): PETR4.SA, VALE3.SA, ITUB4.SA, AAPL, MSFT × {1h, 1d}

No selective removal after cutoff.

## 5. Models and features

```text
M0 = paired random baseline
M1 = trend
M2 = trend + volume
M3 = trend + volume + volatility
M4 = full context (numeric + categorical; no candle pattern features)
M5 = M4 + pattern_type + signal + confirmation_variant
```

Primary hypothesis remains:

```text
DELTA_CANDLE = performance(M5) - performance(M4)   # paired
```

Feature lists are exactly `FEATURE_SETS` in `src/wick/r3e/config.py` (frozen).

Preprocessing: impute / one-hot / scale **fit on train only**; `UNKNOWN` is an explicit category; no silent row drops for gate evidence.

## 6. Horizons, costs, overlap

```text
N ∈ {1, 3, 5, 10}
COST ∈ {OPTIMISTIC, BASE, STRESSED}
OVERLAP ∈ {ALL_SIGNALS, NON_OVERLAPPING_LONG_ONLY}
```

### Primary decision slice (frozen)

```text
cost      = BASE
horizon   = 5
overlap   = NON_OVERLAPPING_LONG_ONLY
```

## 7. Statistics

- Block bootstrap of the paired difference, `n_resamples = 1000`, `seed = 42`
- Benjamini–Hochberg FDR within the declared comparison family
- FDR α = 0.05

## 8. Collection completeness (no effect peeking)

During collection, only operational metrics are disclosed (counts, gaps, hashes, coverage).  
**Forbidden during collection:** Δ(M5−M4), p-values, economic metrics, rankings, gate previews.

Completeness requires **all** of:

1. ≥ `90` calendar days elapsed after cutoff;
2. ≥ `16` of `20` series with ≥ `200` closed bars after cutoff;
3. hash integrity of all validated batches.

States:

```text
R3E_FUTURE_DATA_COLLECTION ∈ {NOT_STARTED, IN_PROGRESS, COMPLETE}
```

Optional stopping is forbidden: no early gate based on interim effect estimates.

## 9. Minimum sample for decision

After collection complete, primary-slice aggregate OOS trades:

```text
MIN_OOS_TRADES_PRIMARY = 100
```

Insufficient sample → `INCONCLUSIVE` (not APPROVED).

## 10. Automatic gate rules (pre-registered)

Executed only when collection is complete and integrity/protocol checks pass.

### APPROVED

All of:

- primary Δ(M5−M4) > 0;
- FDR-adjusted p ≤ 0.05;
- bootstrap CI lower bound > 0;
- M5 mean net return > 0 on the primary slice;
- `MIN_OOS_TRADES_PRIMARY` met;
- audit has no CRITICAL findings;
- protocol freeze hashes match.

Then:

```text
R3E_GATE = APPROVED
ECONOMIC_INTERPRETATION_ALLOWED = true
```

R4 becomes **eligible** only if also `R3E_FUTURE_UNSEEN_AUDIT = APPROVED`, and still requires explicit human start.

### REJECTED

- primary Δ(M5−M4) < 0 with FDR p ≤ 0.05 and CI upper bound < 0;

```text
R3E_GATE = REJECTED
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
```

### INCONCLUSIVE

Collection complete but neither APPROVED nor REJECTED criteria met (including inadequate power).

```text
R3E_GATE = INCONCLUSIVE
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
```

Before collection completeness:

```text
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
```

## 11. Tuning / protocol change ban

After cutoff / freeze:

- no widening of grids, score policies, costs, or feature sets;
- no hypothesis edits based on future performance;
- walk-forward retraining, if used, must follow the pre-registered nested expanding design and may use only information available at each time t within the future stream.

Model freeze artifact: `data/future_unseen/manifests/model_freeze.json`.

## 12. Missing data, gaps, duplicates, provider corrections

| Case | Policy |
|------|--------|
| `market_ts <= cutoff` | hard reject |
| duplicate identical OHLCV | hard reject |
| changed OHLCV same ts | require `revision` increment; audit previous record id; no silent overwrite |
| gaps | detect and report; **no artificial fill** |
| missing series | ops report `series_missing`; blocks completeness until policy mins met |
| hash mismatch | hard fail validation |
| forbidden root mix | hard fail |

## 13. Storage isolation

```text
data/future_unseen/raw/
data/future_unseen/validated/
data/future_unseen/manifests/
reports/r3e_future_unseen/
```

Append-only validated JSONL + immutable batch manifests (SHA-256 per file and batch).

## 14. Runner

```bash
python -m wick.r3e.future_unseen init
python -m wick.r3e.future_unseen ops-report
python -m wick.r3e.future_unseen ingest-json <file.json> --origin <label>
python -m wick.r3e.future_unseen validate \
  --manifest <manifest> \
  --spec docs/specs/R3E_FUTURE_UNSEEN_VALIDATION_SPEC.md
```

Outputs under `reports/r3e_future_unseen/`:

- `run_manifest.json`
- `data_integrity.json`
- `results.json`
- `gate_decision.json`
- `audit.json`
- `ops_collection_report.json`

## 15. Implementation-phase expected state

Until real post-cutoff market data are collected and the runner is executed for decision:

```text
R3E_FUTURE_VALIDATION_ENGINE = COMPLETE
R3E_FUTURE_VALIDATION_AUDIT = COMPLETE
R3E_FUTURE_DATA_COLLECTION = NOT_STARTED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
```

Historical exploratory results under `reports/r3e_real/` remain non-confirmatory and must not be substituted for future-unseen evidence.
