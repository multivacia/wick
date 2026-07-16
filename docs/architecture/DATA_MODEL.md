# Modelo de Dados

## asset

- id
- symbol
- asset_type: `crypto|stock`
- source
- exchange
- currency
- timezone
- active
- created_at
- updated_at

Unicidade:
`(symbol, source, exchange)` com `NULLS NOT DISTINCT` (PostgreSQL),
para impedir duplicatas quando `exchange` é nulo.

## candle

- id
- asset_id
- timeframe
- timestamp
- open
- high
- low
- close
- volume
- adjusted_close nullable
- adjustment_factor nullable
- source
- is_closed
- first_ingested_at
- last_ingested_at
- source_updated_at nullable
- data_revision
- created_at
- updated_at

Chave única:
`(asset_id, timeframe, timestamp, source)`

## ingestion_run

- id/run_id
- source
- requested_start
- requested_end
- actual_start
- actual_end
- assets_requested
- timeframes_requested
- candles_received
- candles_inserted
- candles_updated
- candles_rejected
- pages_fetched
- retries
- status: `SUCCESS|PARTIAL|FAILED`
- error_summary
- coverage JSONB (R1)
- gaps JSONB (R1)
- quality_report JSONB (R1)
- started_at
- finished_at

## candle_revision_event (R1)

Auditoria de revisão OHLCV:

- id
- candle_id
- run_id
- previous_revision
- new_revision
- previous_ohlcv JSONB
- new_ohlcv JSONB
- created_at

## pattern_detected

- id
- anchor_candle_id
- start_candle_id
- pattern_length
- pattern_type
- signal: `bullish|bearish|neutral`
- trend_context: `UP|DOWN|SIDEWAYS|UNKNOWN`
- detector_version
- parameters_hash
- detected_at
- confirmation_status: `PENDING|CONFIRMED|NOT_CONFIRMED|NOT_APPLICABLE`
- confirmation_candle_id nullable
- confirmed_at nullable
- confirmation_rule_version
- context_features JSONB
- run_id

Chave lógica:
`(anchor_candle_id, pattern_type, detector_version, parameters_hash)`

## backtest_result

- id
- pattern_detected_id
- experiment_id
- strategy_variant
- horizon
- direction
- entry_timestamp
- entry_price
- exit_timestamp
- exit_price
- gross_return
- entry_fee
- exit_fee
- entry_slippage
- exit_slippage
- net_return
- directional_return
- directional_hit
- dataset_partition
- overlap_policy
- cost_scenario
- cost_model_version
- calculation_version
- status
- created_at

Chave lógica:
`(pattern_detected_id, experiment_id, strategy_variant, horizon, cost_scenario)`

## experiment

- experiment_id
- hypothesis
- assets
- timeframes
- patterns
- horizons
- detector_version
- parameter_set
- cost_scenarios
- train_period
- test_period
- random_seed
- status
- created_at
- frozen_at

## paper_signal

- id
- pattern_detected_id
- strategy_version
- state
- signal_available_at
- intended_entry_at
- actual_simulated_entry_at nullable
- simulated_entry_price nullable
- expected_exit_at nullable
- actual_exit_at nullable
- simulated_exit_price nullable
- gross_return nullable
- net_return nullable
- error_message nullable
- created_at
- updated_at
