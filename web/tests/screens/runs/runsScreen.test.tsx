import { render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { AppForTest } from "../../../src/App";
import {
  loadRunsScreenData,
  RUNS_FIXTURE_ID,
  SYNTHETIC_EVIDENCE_DISCLAIMER,
} from "../../../src/screens/runs/loadRunsScreenData";
import { RunsScreenView } from "../../../src/screens/runs/RunsScreenView";

function renderScenario(fixtureId: Parameters<typeof loadRunsScreenData>[0]) {
  const data = loadRunsScreenData(fixtureId);
  return {
    data,
    ...render(
      <MemoryRouter>
        <main>
          <RunsScreenView data={data} />
        </main>
      </MemoryRouter>,
    ),
  };
}

describe("I6G Runs screen", () => {
  it("renders the real Runs screen on /future-collection/runs", () => {
    render(<AppForTest initialEntry="/future-collection/runs" />);
    expect(screen.getByTestId("runs-screen")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { level: 1, name: "Execuções" }),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("Planejado / não implementado"),
    ).not.toBeInTheDocument();
  });

  it("shows synthetic / illustrative fixture labels", () => {
    render(<AppForTest initialEntry="/future-collection/runs" />);
    const notice = screen.getByTestId("runs-synthetic-notice");
    expect(within(notice).getByText("Dados ilustrativos")).toBeInTheDocument();
    expect(within(notice).getByText(/Synthetic fixture/)).toBeInTheDocument();
    expect(
      within(notice).getByText(new RegExp(SYNTHETIC_EVIDENCE_DISCLAIMER)),
    ).toBeInTheDocument();
    expect(screen.getByText(new RegExp(RUNS_FIXTURE_ID))).toBeInTheDocument();
  });

  it("renders current illustrative state from the fixed fixture", () => {
    const { data } = renderScenario("current_project_state_illustrative");
    expect(data.fixtureId).toBe("current_project_state_illustrative");
    expect(screen.getByTestId("runs-summary-message")).toHaveTextContent(
      data.runs.primaryMessage.plainLanguage,
    );
    expect(data.runs.runs.length).toBeGreaterThan(0);
    const complete = data.runs.runs.find((r) => r.state === "complete");
    expect(complete?.runId).toBeTruthy();
    expect(
      screen.getByTestId(`runs-status-message-${complete!.runId}`),
    ).toHaveTextContent(complete!.presentation.primaryMessage.plainLanguage);
  });

  it("renders a complete run with supplied timing, counts, store, and idempotency", () => {
    const { data } = renderScenario("current_project_state_illustrative");
    const run = data.runs.runs.find((r) => r.state === "complete")!;
    expect(run.acceptedCount.value).not.toBeNull();
    expect(run.rejectedCount.value).not.toBeNull();
    expect(run.idempotencyResult).toBeTruthy();

    const counts = screen.getByTestId(`runs-counts-${run.runId}`);
    expect(counts).toHaveTextContent(String(run.acceptedCount.value));
    expect(counts).toHaveTextContent(String(run.rejectedCount.value));
    expect(counts.textContent).not.toMatch(/Aceitos\s*0\b/);

    const store = screen.getByTestId(`runs-store-${run.runId}`);
    expect(store).toHaveTextContent(String(run.storeBeforeCount.value));
    expect(store).toHaveTextContent(String(run.storeAfterCount.value));

    const timing = screen.getByTestId(`runs-timing-${run.runId}`);
    expect(timing.textContent).not.toMatch(/indisponível/);

    expect(
      screen.getByTestId(`runs-idempotency-${run.runId}`),
    ).toHaveTextContent(run.idempotencyResult!);
  });

  it("renders in-progress run as informational, never fault/red", () => {
    const { data } = renderScenario("collection_in_progress");
    const inProgress = data.runs.runs.find((r) => r.state === "in_progress");
    expect(inProgress).toBeTruthy();
    expect(inProgress!.presentation.status).toBe("informational");
    expect(inProgress!.presentation.status).not.toBe("fault");

    const badge = screen.getByTestId(`runs-status-${inProgress!.runId}`);
    expect(badge).toHaveAttribute("data-status", "informational");
    expect(badge.closest("[data-status='fault']")).toBeNull();
    expect(badge).toHaveTextContent("Em andamento");

    // Missing finish / counts stay unavailable — not zero-filled.
    expect(
      screen.getByTestId(`runs-timing-${inProgress!.runId}`),
    ).toHaveTextContent(/Fim\s*indisponível/);
    expect(
      screen.getByTestId(`runs-counts-${inProgress!.runId}`),
    ).toHaveTextContent(/Aceitos\s*indisponível/);
  });

  it("renders confirmed fault as fault/red with failure reason", () => {
    const { data } = renderScenario("confirmed_collection_fault");
    const fault = data.runs.runs.find((r) => r.state === "fault");
    expect(fault).toBeTruthy();
    expect(fault!.presentation.status).toBe("fault");
    expect(fault!.failureReason).toBeTruthy();

    const badge = screen.getByTestId(`runs-status-${fault!.runId}`);
    expect(badge).toHaveAttribute("data-status", "fault");
    expect(badge).toHaveTextContent("Falha");
    expect(
      screen.getByTestId(`runs-failure-${fault!.runId}`),
    ).toHaveTextContent(fault!.failureReason!);

    // Partial metrics on fault run are not zero-filled.
    const counts = screen.getByTestId(`runs-counts-${fault!.runId}`);
    expect(counts).toHaveTextContent(/indisponível/);
    expect(counts.textContent).not.toMatch(/Aceitos\s*0\b/);
  });

  it("renders empty state without fault semantics", () => {
    const { data } = renderScenario("empty_no_runs");
    expect(data.runs.runs).toEqual([]);
    expect(data.runs.primaryMessage.technicalCode).toBe("NO_RUNS");
    expect(data.runs.summaryStatus).toBe("unknown");
    expect(data.runs.summaryStatus).not.toBe("fault");

    const empty = screen.getByTestId("runs-empty-state");
    expect(empty).toHaveTextContent("Ainda não há execuções registradas");
    expect(empty).toHaveTextContent("NO_RUNS");
    expect(empty).toHaveTextContent(/EMPTY ≠ FAULT/);
    expect(screen.getByTestId("runs-summary-status-badge")).toHaveAttribute(
      "data-status",
      "unknown",
    );
    expect(screen.queryByTestId("runs-collection")).not.toBeInTheDocument();
  });

  it("keeps partial_unknown_data distinct from fault and does not invent values", () => {
    const { data } = renderScenario("partial_unknown_data");
    expect(data.runs.runs).toEqual([]);
    expect(data.runs.summaryStatus).toBe("unknown");
    expect(screen.getByTestId("runs-empty-state")).toBeInTheDocument();
    expect(screen.getByTestId("runs-partial-unknown")).toBeInTheDocument();
    expect(screen.getByTestId("runs-summary-status-badge")).not.toHaveAttribute(
      "data-status",
      "fault",
    );
  });

  it("does not fabricate evidence links", () => {
    const { data } = renderScenario("current_project_state_illustrative");
    const run = data.runs.runs[0]!;
    const evidence = screen.getByTestId(`runs-evidence-${run.runId}`);
    expect(within(evidence).queryByRole("link")).not.toBeInTheDocument();
    for (const item of run.evidence) {
      expect(evidence).toHaveTextContent(item.reference);
      expect(evidence).toHaveTextContent(item.label);
    }
  });

  it("does not expose operational action buttons on Runs", () => {
    render(<AppForTest initialEntry="/future-collection/runs" />);
    const main = screen.getByRole("main");
    expect(within(main).queryByRole("button")).not.toBeInTheDocument();
  });

  it("keeps Overview implemented, Readiness implemented, and Host/Scheduler implemented", () => {
    const { unmount: unmountOverview } = render(
      <AppForTest initialEntry="/overview" />,
    );
    expect(screen.getByTestId("overview-screen")).toBeInTheDocument();
    unmountOverview();

    const { unmount: unmountReadiness } = render(
      <AppForTest initialEntry="/future-collection/readiness" />,
    );
    expect(screen.getByTestId("readiness-screen")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { level: 1, name: "Prontidão" }),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("Planejado / não implementado"),
    ).not.toBeInTheDocument();
    unmountReadiness();

    render(<AppForTest initialEntry="/operations/host-scheduler" />);
    expect(screen.getByTestId("host-scheduler-screen")).toBeInTheDocument();
    expect(
      screen.queryByText("Planejado / não implementado"),
    ).not.toBeInTheDocument();
    expect(screen.queryByTestId("runs-screen")).not.toBeInTheDocument();
  });

  it("uses a single h1 and semantic collection/table structure", () => {
    render(<AppForTest initialEntry="/future-collection/runs" />);
    const h1s = screen.getAllByRole("heading", { level: 1 });
    expect(h1s).toHaveLength(1);
    expect(h1s[0]).toHaveTextContent("Execuções");
    expect(screen.getByTestId("runs-table")).toBeInTheDocument();
    expect(screen.getByTestId("runs-cards")).toBeInTheDocument();
    expect(
      document.querySelector(".wick-runs-collection-desktop"),
    ).toBeTruthy();
    expect(
      document.querySelector(".wick-runs-collection-mobile"),
    ).toBeTruthy();
  });

  it("loads the fixed current_project_state_illustrative fixture on the product route", () => {
    const data = loadRunsScreenData();
    expect(data.fixtureId).toBe("current_project_state_illustrative");
    expect(data.metadata.synthetic).toBe(true);
    expect(data.metadata.notOperationalEvidence).toBe(true);
  });
});
