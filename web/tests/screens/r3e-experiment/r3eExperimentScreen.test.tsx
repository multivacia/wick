import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AppForTest } from "../../../src/App";
import {
  loadR3eExperimentScreenData,
  R3E_EXPERIMENT_FIXTURE_ID,
  R3E_SYNTHETIC_SCIENCE_DISCLAIMER,
  SYNTHETIC_EVIDENCE_DISCLAIMER,
} from "../../../src/screens/r3e-experiment/loadR3eExperimentScreenData";
import { R3eExperimentScreenView } from "../../../src/screens/r3e-experiment/R3eExperimentScreenView";

function renderProduct() {
  const data = loadR3eExperimentScreenData();
  return {
    data,
    ...render(
      <main>
        <R3eExperimentScreenView data={data} />
      </main>,
    ),
  };
}

describe("I6M R3E Experiment screen", () => {
  it("renders the real R3E screen on /experiments/r3e", () => {
    render(<AppForTest initialEntry="/experiments/r3e" />);
    expect(screen.getByTestId("r3e-experiment-screen")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { level: 1, name: "Experimento R3E" }),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("Planejado / não implementado"),
    ).not.toBeInTheDocument();
  });

  it("shows synthetic notice and dedicated R3E fixture id", () => {
    render(<AppForTest initialEntry="/experiments/r3e" />);
    const notice = screen.getByTestId("r3e-experiment-synthetic-notice");
    expect(within(notice).getByText("Dados ilustrativos")).toBeInTheDocument();
    expect(within(notice).getByText(/Synthetic fixture/)).toBeInTheDocument();
    expect(
      within(notice).getByText(new RegExp(SYNTHETIC_EVIDENCE_DISCLAIMER)),
    ).toBeInTheDocument();
    expect(
      within(notice).getByText(R3E_SYNTHETIC_SCIENCE_DISCLAIMER),
    ).toBeInTheDocument();
    expect(screen.getByText(new RegExp(R3E_EXPERIMENT_FIXTURE_ID))).toBeInTheDocument();
    expect(loadR3eExperimentScreenData().fixtureId).toBe(R3E_EXPERIMENT_FIXTURE_ID);
  });

  it("keeps R3D NO_MEASURABLE_EDGE distinct from R3E pending gate", () => {
    const { data } = renderProduct();
    expect(data.r3eExperiment.r3dResult).toBe("NO_MEASURABLE_EDGE");
    expect(data.r3eExperiment.r3eGate).toBe("PENDING_FUTURE_UNSEEN_DATA");
    expect(data.r3eExperiment.r3dResult).not.toBe(data.r3eExperiment.r3eGate);
    expect(screen.getByTestId("r3e-r3d-neq-r3e")).toHaveTextContent(
      /NO_MEASURABLE_EDGE \(R3D\) ≠ R3E_REJECTED/,
    );
    expect(screen.getByTestId("r3e-r3d-result-badge")).toHaveTextContent(
      "NO_MEASURABLE_EDGE",
    );
    expect(screen.getByTestId("r3e-gate-badge")).toHaveTextContent(
      "PENDING_FUTURE_UNSEEN_DATA",
    );
  });

  it("explains M0–M5 and DELTA_CANDLE without significance or profit claims", () => {
    const { data } = renderProduct();
    for (const id of ["M0", "M1", "M2", "M3", "M4", "M5"] as const) {
      expect(screen.getByTestId(`r3e-stage-${id}`)).toBeInTheDocument();
    }
    expect(data.r3eExperiment.modelStages).toHaveLength(6);
    expect(screen.getByTestId("r3e-delta-candle-definition")).toHaveTextContent(
      /DELTA_CANDLE\s*=\s*M5/,
    );
    expect(screen.getByTestId("r3e-delta-candle-explanation")).toHaveTextContent(
      /não afirma significância|não inclui p-valor/i,
    );
    const main = screen.getByRole("main");
    const text = main.textContent ?? "";
    // Guardrail mentions of metrics are allowed; affirmative numeric claims are not.
    expect(text).not.toMatch(/p\s*=\s*0\.|p_adj\s*≤|IC95\s*=/i);
    expect(text).not.toMatch(/Sharpe\s*=|win\s*rate\s*=|retorno líquido médio/i);
    expect(text).not.toMatch(/aprovad[oa] para dinheiro real|estratégia aprovada/i);
  });

  it("explains temporal validation, holdout, leakage, bootstrap and FDR qualitatively", () => {
    renderProduct();
    expect(screen.getByTestId("r3e-nested-walk-forward")).toHaveTextContent(
      /Nested walk-forward/i,
    );
    expect(screen.getByTestId("r3e-holdout-summary")).toHaveTextContent(/Holdout/i);
    expect(screen.getByTestId("r3e-leakage-protection")).toHaveTextContent(
      /Leakage/i,
    );
    expect(screen.getByTestId("r3e-bootstrap-summary")).toHaveTextContent(
      /Bootstrap/i,
    );
    expect(screen.getByTestId("r3e-fdr-summary")).toHaveTextContent(/FDR/i);
    expect(screen.getByTestId("r3e-no-fabricated-stats")).toHaveTextContent(
      /Sem p-valores/,
    );
  });

  it("keeps future unseen gate pending and validation-not-executed distinct from failed", () => {
    const { data } = renderProduct();
    expect(data.r3eExperiment.validationExecutionState.executed).toBe(false);
    expect(data.r3eExperiment.effectPeekingState.performed).toBe(false);
    expect(data.r3eExperiment.futureUnseenResultsPresent).toBe(false);
    expect(screen.getByTestId("r3e-pending-neq-failed")).toHaveTextContent(
      /PENDING_FUTURE_UNSEEN_DATA ≠ FAILED/,
    );
    expect(screen.getByTestId("r3e-validation-neq-failed")).toHaveTextContent(
      /VALIDATION_NOT_EXECUTED ≠ VALIDATION_FAILED/,
    );
    expect(screen.getByTestId("r3e-peeking-neq-unreported")).toHaveTextContent(
      /EFFECT_PEEKING_FALSE ≠ EFFECT_NOT_REPORTED/,
    );
    expect(screen.getByTestId("r3e-future-unseen-absent")).toHaveTextContent(
      /Ausentes/,
    );
  });

  it("does not show future unseen results, trading recommendations or profitability claims", () => {
    render(<AppForTest initialEntry="/experiments/r3e" />);
    const main = screen.getByRole("main");
    const text = main.textContent ?? "";
    expect(text).not.toMatch(/futureUnseenResultsPresent=true/i);
    expect(text).not.toMatch(/recomenda-se (comprar|vender)|sinal de compra|ordem real autorizada/i);
    expect(text).not.toMatch(/lucratividade comprovada|guaranteed profit|edge confirmado/i);
    expect(text).not.toMatch(/R4 desbloqueado|R5 iniciado|R4_STATUS=APPROVED/i);
    expect(screen.getByTestId("r3e-model-comparison-guard")).toHaveTextContent(
      /MODEL_COMPARISON ≠ TRADING_RECOMMENDATION/,
    );
  });

  it("keeps R4 blocked and R5 not started", () => {
    const { data } = renderProduct();
    expect(data.r3eExperiment.r4Status).toBe("BLOCKED");
    expect(data.r3eExperiment.r5Status).toBe("NOT_STARTED");
    expect(screen.getByTestId("r3e-r4-status")).toHaveTextContent("BLOCKED");
    expect(screen.getByTestId("r3e-r5-status")).toHaveTextContent("NOT_STARTED");
  });

  it("preserves Overview, Runs, Readiness and Host/Scheduler screens", () => {
    render(<AppForTest initialEntry="/overview" />);
    expect(screen.getByTestId("overview-screen")).toBeInTheDocument();
    render(<AppForTest initialEntry="/future-collection/runs" />);
    expect(screen.getByTestId("runs-screen")).toBeInTheDocument();
    render(<AppForTest initialEntry="/future-collection/readiness" />);
    expect(screen.getByTestId("readiness-screen")).toBeInTheDocument();
    render(<AppForTest initialEntry="/operations/host-scheduler" />);
    expect(screen.getByTestId("host-scheduler-screen")).toBeInTheDocument();
  });

  it("uses a single h1 and remains readable at 360px width", () => {
    const { container } = render(
      <div style={{ width: 360 }}>
        <AppForTest initialEntry="/experiments/r3e" />
      </div>,
    );
    expect(container.querySelectorAll("h1")).toHaveLength(1);
    expect(screen.getByTestId("r3e-experiment-screen")).toBeInTheDocument();
    expect(screen.getByTestId("r3e-m0-m5-explanation")).toBeInTheDocument();
  });

  it("exposes navigation label Experimento R3E for the active route", () => {
    render(<AppForTest initialEntry="/experiments/r3e" />);
    // Sidebar is CSS-hidden below 1024px in jsdom; include hidden nav links.
    const links = screen.getAllByRole("link", {
      name: /Experimento R3E/,
      hidden: true,
    });
    expect(links.length).toBeGreaterThan(0);
    expect(
      links.some((link) => link.getAttribute("href") === "/experiments/r3e"),
    ).toBe(true);
  });
});
