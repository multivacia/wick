from wick.r3e.gates import classify_r3e, final_gate_state


def test_classify_labels_real_data():
    assert (
        classify_r3e(
            context_promising=False,
            candle_adds_value=False,
            candle_delta_positive_stable=False,
            mean_net_m4=-0.01,
            mean_net_m5=-0.01,
            has_critical_findings=False,
            fdr_reported=True,
        )
        == "CONTEXT_HAS_NO_EDGE"
    )
    assert (
        classify_r3e(
            context_promising=True,
            candle_adds_value=False,
            candle_delta_positive_stable=False,
            mean_net_m4=0.01,
            mean_net_m5=0.0,
            has_critical_findings=False,
            fdr_reported=True,
        )
        == "CANDLE_ADDS_NO_VALUE"
    )
    assert (
        classify_r3e(
            context_promising=True,
            candle_adds_value=True,
            candle_delta_positive_stable=True,
            mean_net_m4=0.01,
            mean_net_m5=0.02,
            has_critical_findings=False,
            fdr_reported=True,
            exploratory=True,
        )
        == "CANDLE_ADDS_VALUE_EXPLORATORY"
    )


def test_final_gate_real_data_max_state():
    g = final_gate_state("CANDLE_ADDS_NO_VALUE", real_data=True)
    assert g["R3E_GATE"] == "PENDING_FUTURE_UNSEEN_DATA"
    assert g["R4_STATUS"] == "BLOCKED"
    assert g["R5_STATUS"] == "NOT_STARTED"
    assert g["R3E_REAL_DATA_RUN"] == "COMPLETE"
