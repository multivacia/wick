import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AppForTest } from "../../../src/App";
import {
  loadOverviewScreenData,
  OVERVIEW_FIXTURE_ID,
  SYNTHETIC_EVIDENCE_DISCLAIMER,
} from "../../../src/screens/overview/loadOverviewScreenData";

describe("I6E Overview screen", () => {
  it("renders the real Overview screen on /overview", () => {
    render(<AppForTest initialEntry="/overview" />);
    expect(screen.getByTestId("overview-screen")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { level: 1, name: "Visão Geral" }),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("Planejado / não implementado"),
    ).not.toBeInTheDocument();
  });

  it("shows synthetic / illustrative fixture labels", () => {
    render(<AppForTest initialEntry="/overview" />);
    const notice = screen.getByTestId("overview-synthetic-notice");
    expect(within(notice).getByText("Dados ilustrativos")).toBeInTheDocument();
    expect(within(notice).getByText(/Synthetic fixture/)).toBeInTheDocument();
    expect(
      within(notice).getByText(new RegExp(SYNTHETIC_EVIDENCE_DISCLAIMER)),
    ).toBeInTheDocument();
    expect(screen.getByText(new RegExp(OVERVIEW_FIXTURE_ID))).toBeInTheDocument();
  });

  it("renders overall operational state from the ViewModel", () => {
    const { overview } = loadOverviewScreenData();
    render(<AppForTest initialEntry="/overview" />);
    const card = screen.getByTestId("overview-overall-state");
    expect(card).toHaveTextContent(
      overview.overallPresentation.primaryMessage.plainLanguage,
    );
    expect(screen.getByTestId("overview-overall-status-badge")).toHaveAttribute(
      "data-status",
      overview.overallPresentation.status,
    );
    expect(card).toHaveTextContent(overview.scientificGate);
    expect(card).toHaveTextContent(overview.r4Status);
    expect(card).toHaveTextContent(overview.r5Status);
  });

  it("renders collection, readiness, and host/scheduler summaries", () => {
    const { overview } = loadOverviewScreenData();
    render(<AppForTest initialEntry="/overview" />);

    expect(screen.getByTestId("overview-collection-summary")).toHaveTextContent(
      overview.collectionSummary.explanation.primaryMessage.plainLanguage,
    );
    expect(screen.getByTestId("overview-readiness-summary")).toHaveTextContent(
      overview.readinessSummary.explanation.primaryMessage.plainLanguage,
    );
    expect(
      screen.getByTestId("overview-host-scheduler-summary"),
    ).toHaveTextContent(
      overview.hostSchedulerSummary.explanation.primaryMessage.plainLanguage,
    );
  });

  it("renders readiness NOT_READY as amber/not_ready, never fault/red", () => {
    const { overview } = loadOverviewScreenData();
    expect(overview.readinessSummary.explanation.status).toBe("not_ready");
    expect(overview.readinessSummary.explanation.status).not.toBe("fault");

    render(<AppForTest initialEntry="/overview" />);
    const readiness = screen.getByTestId("overview-readiness-summary");
    const badge = within(readiness).getByText("Não pronto");
    expect(badge.closest("[data-status]")).toHaveAttribute(
      "data-status",
      "not_ready",
    );
    expect(badge.closest("[data-status='fault']")).toBeNull();
  });

  it("renders host discovery deferred and scheduler blocked semantics", () => {
    const { overview } = loadOverviewScreenData();
    render(<AppForTest initialEntry="/overview" />);
    const hostSched = screen.getByTestId("overview-host-scheduler-summary");
    expect(hostSched).toHaveTextContent(
      overview.hostSchedulerSummary.explanation.primaryMessage.plainLanguage,
    );
    // Fixture blockers include deferred host + blocked scheduler.
    const blockers = screen.getByTestId("overview-active-blockers");
    expect(blockers).toHaveTextContent("HOST_DISCOVERY_DEFERRED");
    expect(blockers).toHaveTextContent("SCHEDULER_BLOCKED");
  });

  it("renders active blockers with plain language and technical codes", () => {
    const { overview } = loadOverviewScreenData();
    render(<AppForTest initialEntry="/overview" />);
    const blockers = screen.getByTestId("overview-active-blockers");
    for (const blocker of overview.activeBlockers) {
      expect(blockers).toHaveTextContent(blocker.plainLanguage);
      expect(blockers).toHaveTextContent(blocker.reasonCode);
    }
  });

  it("renders latest evidence without fabricating values", () => {
    const { overview } = loadOverviewScreenData();
    render(<AppForTest initialEntry="/overview" />);
    const evidence = screen.getByTestId("overview-latest-evidence");
    for (const item of overview.lastKnownEvidence) {
      expect(evidence).toHaveTextContent(item.label);
      expect(evidence).toHaveTextContent(item.reference);
    }
    if (overview.lastCompletedRun?.runId) {
      expect(evidence).toHaveTextContent(overview.lastCompletedRun.runId);
    }
  });

  it("renders next safe action as advisory text only", () => {
    const { overview } = loadOverviewScreenData();
    render(<AppForTest initialEntry="/overview" />);
    const panel = screen.getByTestId("overview-next-safe-action");
    expect(panel).toHaveTextContent(overview.nextSafeAction.plainLanguage);
    expect(panel).toHaveTextContent(overview.nextSafeAction.code);
    expect(panel).toHaveTextContent(/advisoryOnly = true/);
    expect(
      within(panel).queryByRole("button"),
    ).not.toBeInTheDocument();
  });

  it("does not zero-fill missing metrics", () => {
    render(<AppForTest initialEntry="/overview" />);
    const evidence = screen.getByTestId("overview-latest-evidence");
    // When a metric is unavailable the UI says "indisponível", never invents 0.
    const unavailable = within(evidence).queryAllByText(/indisponível/i);
    for (const node of unavailable) {
      expect(node.textContent).not.toMatch(/:\s*0\b/);
    }
  });

  it("does not expose operational action buttons on Overview", () => {
    render(<AppForTest initialEntry="/overview" />);
    const main = screen.getByRole("main");
    expect(within(main).queryByRole("button")).not.toBeInTheDocument();
  });

  it("keeps Runs, Readiness and Host/Scheduler implemented", () => {
    const { unmount: unmountRuns } = render(
      <AppForTest initialEntry="/future-collection/runs" />,
    );
    expect(screen.getByTestId("runs-screen")).toBeInTheDocument();
    expect(
      screen.queryByText("Planejado / não implementado"),
    ).not.toBeInTheDocument();
    expect(screen.queryByTestId("overview-screen")).not.toBeInTheDocument();
    unmountRuns();

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
    expect(screen.queryByTestId("overview-screen")).not.toBeInTheDocument();
  });

  it("uses a single h1 and logical section headings", () => {
    render(<AppForTest initialEntry="/overview" />);
    const h1s = screen.getAllByRole("heading", { level: 1 });
    expect(h1s).toHaveLength(1);
    expect(h1s[0]).toHaveTextContent("Visão Geral");
    expect(
      screen.getByRole("heading", { level: 2, name: "Estado operacional geral" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { level: 2, name: "Próxima ação segura" }),
    ).toBeInTheDocument();
  });

  it("stacks summary cards in a responsive grid container", () => {
    render(<AppForTest initialEntry="/overview" />);
    const grid = document.querySelector(".wick-overview-summary-grid");
    expect(grid).toBeTruthy();
    expect(grid?.children.length).toBe(3);
  });

  it("loads the fixed current_project_state_illustrative fixture", () => {
    const data = loadOverviewScreenData();
    expect(data.fixtureId).toBe("current_project_state_illustrative");
    expect(data.metadata.synthetic).toBe(true);
    expect(data.metadata.notOperationalEvidence).toBe(true);
    expect(data.overview.nextSafeAction.advisoryOnly).toBe(true);
  });
});
