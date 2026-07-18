"""Automatic R3E future-unseen gate decision (pre-registered rules)."""

from __future__ import annotations

from typing import Any

from wick.r3e.future_unseen.config import (
    EXPERIMENT_ID,
    FDR_ALPHA,
    FUTURE_UNSEEN_CUTOFF_ISO,
    GATE_APPROVED,
    GATE_INCONCLUSIVE,
    GATE_REJECTED,
    MIN_ABS_EFFECT_SIZE,
    MIN_DELTA_CANDLE,
    MIN_OOS_TRADES_PRIMARY,
    PRIMARY_COST,
    PRIMARY_HORIZON,
    PRIMARY_OVERLAP,
    REQUIRE_CI_LOW_POSITIVE,
    REQUIRE_M5_MEAN_NET_POSITIVE,
)
from wick.r3e.future_unseen.protections import (
    assert_economic_interpretation_locked,
    assert_r4_not_opened,
)


def decide_gate(
    *,
    primary_delta: dict[str, Any] | None,
    n_oos_primary: int,
    collection_complete: bool,
    integrity_ok: bool,
    protocol_ok: bool,
    audit_findings_critical: bool,
    commit: str,
    freeze_sha256: str,
    data_hash: str,
) -> dict[str, Any]:
    """Return gate_decision payload with exactly one of APPROVED|REJECTED|INCONCLUSIVE.

    If collection is incomplete, returns PENDING-style blocked decision without
    changing official R3E_GATE away from PENDING_FUTURE_UNSEEN_DATA at engine level;
    the validate runner only writes a final gate when collection_complete.
    """
    rules_evaluated: list[dict[str, Any]] = []

    def rule(name: str, passed: bool, detail: Any) -> None:
        rules_evaluated.append({"rule": name, "passed": passed, "detail": detail})

    rule("collection_complete", collection_complete, collection_complete)
    rule("integrity_ok", integrity_ok, integrity_ok)
    rule("protocol_ok", protocol_ok, protocol_ok)
    rule("no_critical_audit", not audit_findings_critical, audit_findings_critical)
    rule(
        "min_oos_trades_primary",
        n_oos_primary >= MIN_OOS_TRADES_PRIMARY,
        {"n": n_oos_primary, "min": MIN_OOS_TRADES_PRIMARY},
    )

    if not collection_complete or not integrity_ok or not protocol_ok or audit_findings_critical:
        decision = GATE_INCONCLUSIVE if collection_complete else "NOT_READY"
        economic = False
        r4 = "BLOCKED"
        justification = "Preconditions failed; final confirmatory decision not available"
        out = _pack(
            decision=decision,
            economic=economic,
            r4=r4,
            justification=justification,
            rules=rules_evaluated,
            primary_delta=primary_delta,
            n_oos=n_oos_primary,
            commit=commit,
            freeze_sha256=freeze_sha256,
            data_hash=data_hash,
            final=False,
        )
        assert_economic_interpretation_locked(False, final_decision_made=False)
        return out

    if primary_delta is None or n_oos_primary < MIN_OOS_TRADES_PRIMARY:
        out = _pack(
            decision=GATE_INCONCLUSIVE,
            economic=False,
            r4="BLOCKED",
            justification="Insufficient primary-slice evidence after collection complete",
            rules=rules_evaluated,
            primary_delta=primary_delta,
            n_oos=n_oos_primary,
            commit=commit,
            freeze_sha256=freeze_sha256,
            data_hash=data_hash,
            final=True,
        )
        return out

    delta = float(primary_delta.get("delta", 0.0))
    ci_low = float(primary_delta.get("ci_low", 0.0))
    ci_high = float(primary_delta.get("ci_high", 0.0))
    p_adj = primary_delta.get("p_adj")
    p_adj_f = float(p_adj) if p_adj is not None else 1.0
    effect = float(primary_delta.get("effect_size", 0.0))
    mean_m5 = float(primary_delta.get("mean_left", 0.0))  # M5 is left in DELTA_CANDLE

    sig = p_adj_f <= FDR_ALPHA
    rule("fdr_significant", sig, {"p_adj": p_adj_f, "alpha": FDR_ALPHA})
    rule("delta_positive", delta > MIN_DELTA_CANDLE, {"delta": delta, "min": MIN_DELTA_CANDLE})
    rule(
        "ci_low_positive",
        (ci_low > 0.0) if REQUIRE_CI_LOW_POSITIVE else True,
        {"ci_low": ci_low},
    )
    rule(
        "m5_mean_net_positive",
        (mean_m5 > 0.0) if REQUIRE_M5_MEAN_NET_POSITIVE else True,
        {"mean_m5": mean_m5},
    )
    rule(
        "min_effect_size",
        abs(effect) >= MIN_ABS_EFFECT_SIZE,
        {"effect_size": effect, "min": MIN_ABS_EFFECT_SIZE},
    )

    approved = (
        sig
        and delta > MIN_DELTA_CANDLE
        and (ci_low > 0.0 if REQUIRE_CI_LOW_POSITIVE else True)
        and (mean_m5 > 0.0 if REQUIRE_M5_MEAN_NET_POSITIVE else True)
        and abs(effect) >= MIN_ABS_EFFECT_SIZE
    )
    rejected = sig and delta < 0.0 and ci_high < 0.0

    if approved:
        decision = GATE_APPROVED
        economic = True
        justification = (
            "Primary DELTA_CANDLE (M5-M4) positive, FDR-significant, CI excludes 0, "
            "M5 mean net positive under frozen protocol"
        )
    elif rejected:
        decision = GATE_REJECTED
        economic = False
        justification = (
            "Primary DELTA_CANDLE significantly negative (CI above 0 excluded); "
            "candle adds no confirmatory value"
        )
    else:
        decision = GATE_INCONCLUSIVE
        economic = False
        justification = (
            "Collection complete but evidence neither meets APPROVED nor REJECTED "
            "pre-registered criteria"
        )

    r4 = "UNBLOCKED_ELIGIBLE" if decision == GATE_APPROVED and economic else "BLOCKED"
    out = _pack(
        decision=decision,
        economic=economic,
        r4=r4,
        justification=justification,
        rules=rules_evaluated,
        primary_delta=primary_delta,
        n_oos=n_oos_primary,
        commit=commit,
        freeze_sha256=freeze_sha256,
        data_hash=data_hash,
        final=True,
    )
    if decision != GATE_APPROVED or not economic:
        try:
            assert_r4_not_opened(gate=decision, economic_ok=economic, audit="APPROVED")
        except Exception:
            # expected: R4 blocked
            out["R4_STATUS"] = "BLOCKED"
    else:
        out["R4_STATUS"] = "UNBLOCKED_ELIGIBLE"
        out["note"] = "R4 still requires explicit human authorization to start"
    return out


def _pack(
    *,
    decision: str,
    economic: bool,
    r4: str,
    justification: str,
    rules: list[dict[str, Any]],
    primary_delta: dict[str, Any] | None,
    n_oos: int,
    commit: str,
    freeze_sha256: str,
    data_hash: str,
    final: bool,
) -> dict[str, Any]:
    return {
        "experiment_id": EXPERIMENT_ID,
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
        "decision": decision,
        "R3E_GATE": decision
        if final and decision in {GATE_APPROVED, GATE_REJECTED, GATE_INCONCLUSIVE}
        else "PENDING_FUTURE_UNSEEN_DATA",
        "ECONOMIC_INTERPRETATION_ALLOWED": economic,
        "R4_STATUS": "BLOCKED" if r4 != "UNBLOCKED_ELIGIBLE" else "UNBLOCKED_ELIGIBLE",
        "primary_slice": {
            "cost": PRIMARY_COST,
            "horizon": PRIMARY_HORIZON,
            "overlap": PRIMARY_OVERLAP,
        },
        "rules_evaluated": rules,
        "observed": {
            "n_oos_primary": n_oos,
            "delta_candle": primary_delta,
        },
        "thresholds_frozen": {
            "fdr_alpha": FDR_ALPHA,
            "min_delta_candle": MIN_DELTA_CANDLE,
            "require_ci_low_positive": REQUIRE_CI_LOW_POSITIVE,
            "require_m5_mean_net_positive": REQUIRE_M5_MEAN_NET_POSITIVE,
            "min_oos_trades_primary": MIN_OOS_TRADES_PRIMARY,
            "min_abs_effect_size": MIN_ABS_EFFECT_SIZE,
        },
        "justification": justification,
        "hashes": {
            "freeze_sha256": freeze_sha256,
            "data_hash": data_hash,
        },
        "commit": commit,
        "final_decision": final,
    }
