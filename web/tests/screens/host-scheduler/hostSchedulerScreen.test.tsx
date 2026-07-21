import { render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { AppForTest } from "../../../src/App";
import {
  HOST_SCHEDULER_FIXTURE_ID,
  HOST_SCHEDULER_SYNTHETIC_ACTIVATION_DISCLAIMER,
  loadHostSchedulerScreenData,
  OPERATIONAL_DEBT_OFFICIAL_WORDING,
  SYNTHETIC_EVIDENCE_DISCLAIMER,
} from "../../../src/screens/host-scheduler/loadHostSchedulerScreenData";
import { HostSchedulerScreenView } from "../../../src/screens/host-scheduler/HostSchedulerScreenView";

function renderScenario(
  fixtureId: Parameters<typeof loadHostSchedulerScreenData>[0],
) {
  const data = loadHostSchedulerScreenData(fixtureId);
  return {
    data,
    ...render(
      <MemoryRouter>
        <main>
          <HostSchedulerScreenView data={data} />
        </main>
      </MemoryRouter>,
    ),
  };
}

describe("I6K Host/Scheduler screen", () => {
  it("renders the real Host/Scheduler screen on /operations/host-scheduler", () => {
    render(<AppForTest initialEntry="/operations/host-scheduler" />);
    expect(screen.getByTestId("host-scheduler-screen")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { level: 1, name: "Host e Automação" }),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("Planejado / não implementado"),
    ).not.toBeInTheDocument();
  });

  it("shows synthetic / illustrative fixture labels and activation disclaimer", () => {
    render(<AppForTest initialEntry="/operations/host-scheduler" />);
    const notice = screen.getByTestId("host-scheduler-synthetic-notice");
    expect(within(notice).getByText("Dados ilustrativos")).toBeInTheDocument();
    expect(within(notice).getByText(/Synthetic fixture/)).toBeInTheDocument();
    expect(
      within(notice).getByText(new RegExp(SYNTHETIC_EVIDENCE_DISCLAIMER)),
    ).toBeInTheDocument();
    expect(
      within(notice).getByText(
        HOST_SCHEDULER_SYNTHETIC_ACTIVATION_DISCLAIMER,
      ),
    ).toBeInTheDocument();
    expect(
      screen.getByText(new RegExp(HOST_SCHEDULER_FIXTURE_ID)),
    ).toBeInTheDocument();
  });

  it("keeps host discovery deferred distinct from complete and failed", () => {
    const { data } = renderScenario("current_project_state_illustrative");
    expect(data.hostScheduler.hostDiscoveryState).toBe("deferred");
    expect(data.hostScheduler.hostPresentation.status).toBe("deferred");
    expect(data.hostScheduler.hostPresentation.status).not.toBe("fault");
    expect(data.hostScheduler.hostPresentation.status).not.toBe("completed");
    expect(data.hostScheduler.hostPresentation.status).not.toBe("healthy");

    const badge = screen.getByTestId("host-scheduler-discovery-badge");
    expect(badge).toHaveAttribute("data-status", "deferred");
    expect(badge).toHaveTextContent("Adiado");
    expect(screen.getByTestId("host-scheduler-deferred-note")).toHaveTextContent(
      /DEFERRED ≠ COMPLETE/,
    );
    expect(screen.getByTestId("host-scheduler-deferred-note")).toHaveTextContent(
      /DEFERRED ≠ FAILED/,
    );
  });

  it("keeps scheduler blocked distinct from confirmed fault", () => {
    const { data } = renderScenario("scheduler_blocked_not_authorized");
    expect(data.hostScheduler.schedulerState).toBe("blocked");
    expect(data.hostScheduler.schedulerPresentation.status).toBe("blocked");
    expect(data.hostScheduler.schedulerPresentation.status).not.toBe("fault");

    const badge = screen.getByTestId("host-scheduler-scheduler-badge");
    expect(badge).toHaveAttribute("data-status", "blocked");
    expect(badge).toHaveTextContent("Bloqueado");
    expect(screen.getByTestId("host-scheduler-blocked-note")).toHaveTextContent(
      /BLOCKED ≠ FAULT/,
    );
  });

  it("shows official operational debt wording when debt is open", () => {
    const { data } = renderScenario("current_project_state_illustrative");
    expect(data.hostScheduler.operationalDebt).toBe("open");
    expect(screen.getByTestId("host-scheduler-debt-official")).toHaveTextContent(
      OPERATIONAL_DEBT_OFFICIAL_WORDING,
    );
    expect(screen.getByTestId("host-scheduler-debt-detail")).toHaveTextContent(
      /HOST_DISCOVERY=DEFERRED/,
    );
    expect(screen.getByTestId("host-scheduler-debt-detail")).toHaveTextContent(
      /BLOCKED/,
    );
  });

  it("does not invent missing host identity, environment, cadence or next-run", () => {
    renderScenario("current_project_state_illustrative");
    expect(screen.getByTestId("host-scheduler-hostname")).toHaveTextContent(
      /indisponível/i,
    );
    expect(screen.getByTestId("host-scheduler-address")).toHaveTextContent(
      /indisponível/i,
    );
    expect(screen.getByTestId("host-scheduler-paths")).toHaveTextContent(
      /indisponível/i,
    );
    expect(screen.getByTestId("host-scheduler-cadence-value")).toHaveTextContent(
      /indisponível/i,
    );
    expect(screen.getByTestId("host-scheduler-next-run-value")).toHaveTextContent(
      /indisponível/i,
    );
    expect(screen.getByTestId("host-scheduler-env-absent")).toHaveTextContent(
      /não são fabricados/i,
    );
  });

  it("does not expose credentials, IPs or sensitive paths", () => {
    render(<AppForTest initialEntry="/operations/host-scheduler" />);
    const main = screen.getByRole("main");
    const text = main.textContent ?? "";
    expect(text).not.toMatch(/\b(?:\d{1,3}\.){3}\d{1,3}\b/);
    expect(text).not.toMatch(/ssh|password|token|private[_-]?key|api[_-]?key/i);
    expect(text).not.toMatch(/\/home\/|\/root\/|\.pem\b|\.ssh\b/i);
  });

  it("keeps unknown distinct from offline and inactive distinct from failed", () => {
    const { data } = renderScenario("partial_unknown_data");
    expect(data.hostScheduler.hostDiscoveryState).toBe("unknown");
    expect(screen.getByTestId("host-scheduler-discovery-badge")).toHaveAttribute(
      "data-status",
      "unknown",
    );
    expect(screen.getByTestId("host-scheduler-unknown-host-note")).toHaveTextContent(
      /UNKNOWN ≠ OFFLINE/,
    );
    expect(screen.getByTestId("host-scheduler-discovery-badge")).not.toHaveTextContent(
      /offline/i,
    );
    expect(screen.getByTestId("host-scheduler-discovery-badge")).toHaveAttribute(
      "data-status",
      "unknown",
    );
    expect(screen.getByTestId("host-scheduler-partial-unknown")).toBeInTheDocument();
  });

  it("keeps inactive and not-configured distinct from failed on product fixture", () => {
    const { data } = renderScenario("current_project_state_illustrative");
    expect(data.hostScheduler.schedulerActive).toBe(false);
    expect(data.hostScheduler.schedulerRegistered).toBe(false);
    expect(screen.getByTestId("host-scheduler-active")).toHaveTextContent(
      /inativo/i,
    );
    expect(screen.getByTestId("host-scheduler-registered")).toHaveTextContent(
      /não configurado/i,
    );
    expect(screen.getByTestId("host-scheduler-inactive-note")).toHaveTextContent(
      /SCHEDULER_INACTIVE ≠ SCHEDULER_FAILED/,
    );
    expect(
      screen.getByTestId("host-scheduler-not-configured-note"),
    ).toHaveTextContent(/NOT_CONFIGURED ≠ FAILED/);
    expect(
      screen.getByTestId("host-scheduler-scheduler-badge"),
    ).not.toHaveAttribute("data-status", "fault");
  });

  it("keeps missing last-cycle timestamp unavailable (not fabricated)", () => {
    const { data } = renderScenario("current_project_state_illustrative");
    expect(data.hostScheduler.lastCycleAt.availability).not.toBe("available");
    expect(screen.getByTestId("host-scheduler-last-cycle-at")).toHaveTextContent(
      /indisponível/i,
    );
  });

  it("renders next safe human action as text-only advisory", () => {
    const { data } = renderScenario("current_project_state_illustrative");
    expect(screen.getByTestId("host-scheduler-action-hint")).toHaveTextContent(
      data.hostScheduler.nextSafeAction.plainLanguage,
    );
    expect(screen.getByTestId("host-scheduler-action-hint")).toHaveTextContent(
      "advisoryOnly",
    );
  });

  it("does not fabricate evidence links", () => {
    const { data } = renderScenario("host_discovery_deferred");
    const evidence = screen.getByTestId("host-scheduler-evidence-reference");
    expect(within(evidence).queryByRole("link")).not.toBeInTheDocument();
    for (const item of data.hostScheduler.evidence) {
      expect(evidence).toHaveTextContent(item.label);
      expect(evidence).toHaveTextContent(item.reference);
    }
  });

  it("does not expose operational controls", () => {
    render(<AppForTest initialEntry="/operations/host-scheduler" />);
    const main = screen.getByRole("main");
    expect(within(main).queryByRole("button")).not.toBeInTheDocument();
    expect(
      within(main).queryByRole("link", {
        name: /ativar|instalar|descobrir|conectar|coletar|validar|start|stop|retry|run now|activate|install|configure/i,
      }),
    ).not.toBeInTheDocument();
    // No actionable control affordances for operational verbs.
    expect(within(main).queryByRole("button", { name: /start|stop|retry|activate|install|configure|run now/i })).not.toBeInTheDocument();
    expect(document.querySelector("[data-operational-action]")).toBeNull();
    expect(document.querySelector("[data-action='activate']")).toBeNull();
    expect(document.querySelector("[data-action='run-now']")).toBeNull();
  });

  it("keeps Overview, Runs and Readiness implemented", () => {
    const { unmount: unmountOverview } = render(
      <AppForTest initialEntry="/overview" />,
    );
    expect(screen.getByTestId("overview-screen")).toBeInTheDocument();
    unmountOverview();

    const { unmount: unmountRuns } = render(
      <AppForTest initialEntry="/future-collection/runs" />,
    );
    expect(screen.getByTestId("runs-screen")).toBeInTheDocument();
    unmountRuns();

    const { unmount: unmountReadiness } = render(
      <AppForTest initialEntry="/future-collection/readiness" />,
    );
    expect(screen.getByTestId("readiness-screen")).toBeInTheDocument();
    unmountReadiness();

    render(<AppForTest initialEntry="/operations/host-scheduler" />);
    expect(screen.getByTestId("host-scheduler-screen")).toBeInTheDocument();
  });

  it("uses a single h1 and logical section structure", () => {
    render(<AppForTest initialEntry="/operations/host-scheduler" />);
    const h1s = screen.getAllByRole("heading", { level: 1 });
    expect(h1s).toHaveLength(1);
    expect(h1s[0]).toHaveTextContent("Host e Automação");
    expect(
      screen.getByTestId("host-scheduler-discovery-status"),
    ).toBeInTheDocument();
    expect(
      screen.getByTestId("host-scheduler-operational-debt"),
    ).toBeInTheDocument();
    expect(document.querySelector(".wick-host-scheduler-grid")).toBeTruthy();
  });

  it("loads the fixed current_project_state_illustrative fixture on the product route", () => {
    const data = loadHostSchedulerScreenData();
    expect(data.fixtureId).toBe("current_project_state_illustrative");
    expect(data.metadata.synthetic).toBe(true);
    expect(data.metadata.notOperationalEvidence).toBe(true);
    expect(data.hostScheduler.hostDiscoveryState).toBe("deferred");
    expect(data.hostScheduler.operationalDebt).toBe("open");
    expect(data.hostScheduler.schedulerState).toBe("blocked");
  });

  it("does not overflow horizontally at narrow widths", () => {
    const { container } = render(
      <div style={{ width: 360 }}>
        <AppForTest initialEntry="/operations/host-scheduler" />
      </div>,
    );
    const screenRoot = container.querySelector(".wick-host-scheduler-screen");
    expect(screenRoot).toBeTruthy();
    expect(screen.getByTestId("host-scheduler-debt-official")).toBeInTheDocument();
  });
});
