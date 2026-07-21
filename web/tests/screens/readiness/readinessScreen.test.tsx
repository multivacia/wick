import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AppForTest } from "../../../src/App";
import {
  ILLUSTRATIVE_WINDOW_DISCLOSURE,
  loadReadinessScreenData,
  READINESS_FIXTURE_ID,
  SYNTHETIC_EVIDENCE_DISCLAIMER,
} from "../../../src/screens/readiness/loadReadinessScreenData";
import { ReadinessScreenView } from "../../../src/screens/readiness/ReadinessScreenView";

function renderScenario(
  fixtureId: Parameters<typeof loadReadinessScreenData>[0],
) {
  const data = loadReadinessScreenData(fixtureId);
  return {
    data,
    ...render(
      <main>
        <ReadinessScreenView data={data} />
      </main>,
    ),
  };
}

describe("I6I Readiness screen", () => {
  it("renders the real Readiness screen on /future-collection/readiness", () => {
    render(<AppForTest initialEntry="/future-collection/readiness" />);
    expect(screen.getByTestId("readiness-screen")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { level: 1, name: "Prontidão" }),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("Planejado / não implementado"),
    ).not.toBeInTheDocument();
  });

  it("shows synthetic / illustrative fixture labels", () => {
    render(<AppForTest initialEntry="/future-collection/readiness" />);
    const notice = screen.getByTestId("readiness-synthetic-notice");
    expect(within(notice).getByText("Dados ilustrativos")).toBeInTheDocument();
    expect(within(notice).getByText(/Synthetic fixture/)).toBeInTheDocument();
    expect(
      within(notice).getByText(new RegExp(SYNTHETIC_EVIDENCE_DISCLAIMER)),
    ).toBeInTheDocument();
    expect(screen.getByText(new RegExp(READINESS_FIXTURE_ID))).toBeInTheDocument();
  });

  it("renders current illustrative state as NOT_READY without fault/red", () => {
    const { data } = renderScenario("current_project_state_illustrative");
    expect(data.fixtureId).toBe("current_project_state_illustrative");
    expect(data.readiness.state).toBe("not_ready");
    expect(data.readiness.presentation.status).toBe("not_ready");
    expect(data.readiness.presentation.status).not.toBe("fault");

    const badge = screen.getByTestId("readiness-status-badge");
    expect(badge).toHaveAttribute("data-status", "not_ready");
    expect(badge).toHaveTextContent("Não pronto");
    expect(badge.closest("[data-status='fault']")).toBeNull();
    expect(screen.getByTestId("readiness-not-ready-note")).toBeInTheDocument();
    expect(screen.getByTestId("readiness-status-message")).toHaveTextContent(
      data.readiness.presentation.primaryMessage.plainLanguage,
    );
  });

  it("renders READY without implying strategy approval or profitability", () => {
    const { data } = renderScenario("readiness_ready_illustrative");
    expect(data.readiness.state).toBe("ready");
    expect(data.readiness.validationAuthorized).toBe(false);
    expect(data.readiness.nextSafeAction.code).toBe("do_not_validate");

    const badge = screen.getByTestId("readiness-status-badge");
    expect(badge).toHaveAttribute("data-status", "healthy");
    expect(badge).toHaveTextContent("Pronto");
    expect(screen.getByTestId("readiness-ready-disclaimer")).toHaveTextContent(
      /não.*aprovação de estratégia/i,
    );
    expect(screen.getByTestId("readiness-action-hint")).toHaveTextContent(
      /não autoriza validação/i,
    );
  });

  it("renders observed and required days; missing values stay unavailable", () => {
    const { data } = renderScenario("current_project_state_illustrative");
    expect(data.readiness.windowDays.value).toBe(3);
    expect(data.readiness.requiredWindowDays.value).toBe(14);

    expect(screen.getByTestId("readiness-window-observed")).toHaveTextContent(
      /3/,
    );
    expect(screen.getByTestId("readiness-window-required")).toHaveTextContent(
      /14/,
    );
    expect(screen.getByTestId("readiness-window-remaining")).toHaveTextContent(
      /11/,
    );
    expect(screen.getByTestId("readiness-window-bar")).toHaveAttribute(
      "role",
      "progressbar",
    );
    expect(screen.getByTestId("readiness-window-disclosure")).toHaveTextContent(
      ILLUSTRATIVE_WINDOW_DISCLOSURE,
    );

    // No gauge / meter / speedometer semantics.
    expect(document.querySelector("meter")).toBeNull();
    expect(document.querySelector("[data-gauge]")).toBeNull();
  });

  it("does not zero-fill missing window metrics in partial_unknown_data", () => {
    const { data } = renderScenario("partial_unknown_data");
    expect(data.readiness.state).toBe("unknown");
    expect(data.readiness.windowDays.value).toBeNull();
    expect(data.readiness.requiredWindowDays.value).toBeNull();

    expect(screen.getByTestId("readiness-status-badge")).toHaveAttribute(
      "data-status",
      "unknown",
    );
    expect(screen.getByTestId("readiness-status-badge")).not.toHaveAttribute(
      "data-status",
      "fault",
    );
    expect(screen.getByTestId("readiness-window-observed")).toHaveTextContent(
      /indisponível/i,
    );
    expect(screen.getByTestId("readiness-window-required").textContent).not.toMatch(
      /^0$/,
    );
    expect(screen.getByTestId("readiness-window-remaining")).toHaveTextContent(
      /indisponível/i,
    );
    expect(screen.getByTestId("readiness-window-bar-absent")).toBeInTheDocument();
    expect(screen.getByTestId("readiness-partial-unknown")).toBeInTheDocument();
  });

  it("keeps validation not executed distinct from validation failed", () => {
    renderScenario("current_project_state_illustrative");
    expect(screen.getByTestId("readiness-validation-executed")).toHaveTextContent(
      "false",
    );
    expect(
      screen.getByTestId("readiness-validation-executed-message"),
    ).toHaveTextContent(/não significa falha/i);
    expect(
      screen.getByTestId("readiness-validation-execution"),
    ).toHaveTextContent(/VALIDATION_NOT_EXECUTED ≠ VALIDATION_FAILED/);
  });

  it("keeps effect peeking false distinct from not reported", () => {
    renderScenario("current_project_state_illustrative");
    expect(
      screen.getByTestId("readiness-effect-peeking-message"),
    ).toHaveTextContent(/valor explícito false/i);
    expect(screen.getByTestId("readiness-effect-peeking")).toHaveTextContent(
      /EFFECT_PEEKING_FALSE ≠ EFFECT_NOT_REPORTED/,
    );
  });

  it("does not fabricate collection health metrics", () => {
    renderScenario("current_project_state_illustrative");
    const collection = screen.getByTestId("readiness-collection-state");
    expect(collection).toHaveTextContent(/não fazem parte deste ViewModel/i);
    expect(collection).toHaveTextContent(/COLLECTION_IN_PROGRESS ≠ READY/);
    expect(within(collection).queryByTestId("readiness-window-observed")).toBeNull();
    expect(collection.textContent).not.toMatch(/\bacceptedCount\b|\bgapCount\b/);
  });

  it("renders blocking reason and next safe action as read-only text", () => {
    const { data } = renderScenario("current_project_state_illustrative");
    expect(data.readiness.blockingReasonCodes).toContain(
      "WINDOW_DAYS_INSUFFICIENT",
    );
    expect(
      screen.getByTestId("readiness-blocking-WINDOW_DAYS_INSUFFICIENT"),
    ).toBeInTheDocument();
    expect(screen.getByTestId("readiness-action-hint")).toHaveTextContent(
      data.readiness.nextSafeAction.plainLanguage,
    );
    expect(screen.getByTestId("readiness-action-hint")).toHaveTextContent(
      "advisoryOnly",
    );
  });

  it("does not fabricate evidence links", () => {
    const { data } = renderScenario("readiness_ready_illustrative");
    const evidence = screen.getByTestId("readiness-evidence-reference");
    expect(within(evidence).queryByRole("link")).not.toBeInTheDocument();
    for (const item of data.readiness.evidence) {
      expect(evidence).toHaveTextContent(item.label);
      expect(evidence).toHaveTextContent(item.reference);
    }
  });

  it("does not expose validation, collection, or scheduler controls", () => {
    render(<AppForTest initialEntry="/future-collection/readiness" />);
    const main = screen.getByRole("main");
    expect(within(main).queryByRole("button")).not.toBeInTheDocument();
    expect(within(main).queryByRole("link", { name: /validar|coletar|scheduler/i })).not.toBeInTheDocument();
  });

  it("keeps Overview, Runs and Host/Scheduler implemented", () => {
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

    render(<AppForTest initialEntry="/operations/host-scheduler" />);
    expect(screen.getByTestId("host-scheduler-screen")).toBeInTheDocument();
    expect(
      screen.queryByText("Planejado / não implementado"),
    ).not.toBeInTheDocument();
  });

  it("uses a single h1 and logical section structure", () => {
    render(<AppForTest initialEntry="/future-collection/readiness" />);
    const h1s = screen.getAllByRole("heading", { level: 1 });
    expect(h1s).toHaveLength(1);
    expect(h1s[0]).toHaveTextContent("Prontidão");
    expect(screen.getByTestId("readiness-status-card")).toBeInTheDocument();
    expect(screen.getByTestId("readiness-window-progress")).toBeInTheDocument();
    expect(document.querySelector(".wick-readiness-grid")).toBeTruthy();
  });

  it("loads the fixed current_project_state_illustrative fixture on the product route", () => {
    const data = loadReadinessScreenData();
    expect(data.fixtureId).toBe("current_project_state_illustrative");
    expect(data.metadata.synthetic).toBe(true);
    expect(data.metadata.notOperationalEvidence).toBe(true);
  });
});
