import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { AppForTest } from "../../../src/App";
import {
  EVIDENCE_CATALOG_FIXTURE_ID,
  loadEvidenceExplorerScreenData,
  SYNTHETIC_EVIDENCE_DISCLAIMER,
} from "../../../src/screens/evidence-explorer/loadEvidenceExplorerScreenData";
import { EVIDENCE_EXPLORER_PATH } from "../../../src/viewmodels";

describe("UX-R2 I1 Evidence Explorer screen", () => {
  it("renders the Evidence Explorer on /governance/evidence", () => {
    render(<AppForTest initialEntry="/governance/evidence" />);
    expect(screen.getByTestId("evidence-explorer-screen")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { level: 1, name: "Evidências" }),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("Planejado / não implementado"),
    ).not.toBeInTheDocument();
  });

  it("activates Evidências navigation item", () => {
    render(<AppForTest initialEntry="/governance/evidence" />);
    const nav = screen.getByRole("navigation", {
      name: "Principal",
      hidden: true,
    });
    const link = within(nav).getByRole("link", {
      name: /Evidências/i,
      hidden: true,
    });
    expect(link).toHaveAttribute("href", "/governance/evidence");
    expect(link).toHaveAttribute("aria-current", "page");
  });

  it("shows synthetic disclosure, catalog disclosure and safety notices", () => {
    render(<AppForTest initialEntry="/governance/evidence" />);
    const notice = screen.getByTestId("evidence-explorer-synthetic-notice");
    expect(within(notice).getByText("Dados ilustrativos")).toBeInTheDocument();
    expect(
      within(notice).getByText(new RegExp(SYNTHETIC_EVIDENCE_DISCLAIMER)),
    ).toBeInTheDocument();
    expect(
      screen.getByText(new RegExp(EVIDENCE_CATALOG_FIXTURE_ID)),
    ).toBeInTheDocument();
    expect(screen.getByTestId("evidence-catalog-disclosure")).toBeInTheDocument();
    expect(screen.getByTestId("evidence-safety-notices")).toHaveTextContent(
      /Evidence presence/,
    );
    expect(loadEvidenceExplorerScreenData().fixtureId).toBe(
      EVIDENCE_CATALOG_FIXTURE_ID,
    );
  });

  it("lists curated evidence and opens detail without linkifying sourcePath", async () => {
    const user = userEvent.setup();
    render(<AppForTest initialEntry="/governance/evidence" />);

    const list = screen.getByTestId("evidence-list");
    expect(within(list).getAllByRole("button").length).toBeGreaterThanOrEqual(7);

    await user.click(
      screen.getByTestId("evidence-list-item-ev-ux-r1-formal-closure"),
    );

    const detail = screen.getByTestId("evidence-detail");
    expect(within(detail).getByTestId("evidence-detail-id")).toHaveTextContent(
      "ev-ux-r1-formal-closure",
    );
    const pathCode = within(detail).getByTestId(
      "evidence-detail-source-path-code",
    );
    expect(pathCode.tagName).toBe("CODE");
    expect(pathCode).toHaveTextContent(
      "docs/releases/UX-R1-FORMAL-RELEASE-CLOSURE-AND-ACCEPTANCE.md",
    );
    expect(within(detail).queryByRole("link")).not.toBeInTheDocument();
    expect(screen.getByTestId("evidence-source-path-disclaimer")).toBeInTheDocument();
  });

  it("supports search and filters with clear-all", async () => {
    const user = userEvent.setup();
    render(<AppForTest initialEntry="/governance/evidence" />);

    await user.type(
      screen.getByTestId("evidence-search-input"),
      "Encerramento formal",
    );
    expect(screen.getByTestId("evidence-result-count")).toHaveTextContent(
      /1 evidência/,
    );
    expect(
      screen.getByTestId("evidence-list-item-ev-ux-r1-formal-closure"),
    ).toBeInTheDocument();

    await user.clear(screen.getByTestId("evidence-search-input"));
    await user.selectOptions(
      screen.getByTestId("evidence-filter-class"),
      "operational_debt_record",
    );
    expect(
      screen.getByTestId("evidence-list-item-ev-host-scheduler-operational-debt"),
    ).toBeInTheDocument();
    expect(screen.getByTestId("evidence-result-count")).toHaveTextContent(
      /1 evidência/,
    );

    await user.click(screen.getByTestId("evidence-filters-clear"));
    expect(screen.getByTestId("evidence-filter-class")).toHaveValue("");
    expect(screen.getByTestId("evidence-result-count")).toHaveTextContent(
      /11 evidências/,
    );
  });

  it("does not expose download buttons or external hrefs", () => {
    render(<AppForTest initialEntry="/governance/evidence" />);
    const main = screen.getByRole("main");
    expect(within(main).queryByRole("link", { name: /download/i })).toBeNull();
    expect(within(main).queryByRole("button", { name: /download|abrir arquivo|baixar/i })).toBeNull();
    for (const link of within(main).queryAllByRole("link")) {
      expect(link.getAttribute("href") ?? "").not.toMatch(/^https?:/i);
    }
  });

  it("deep-links via ?evidenceId= query param pre-selects evidence", () => {
    render(
      <AppForTest
        initialEntry={`${EVIDENCE_EXPLORER_PATH}?evidenceId=ev-r3d-validation-conclusion`}
      />,
    );
    const detail = screen.getByTestId("evidence-detail");
    expect(within(detail).getByTestId("evidence-detail-id")).toHaveTextContent(
      "ev-r3d-validation-conclusion",
    );
  });

  it("standing filter shows only matching entries", async () => {
    const user = userEvent.setup();
    render(<AppForTest initialEntry="/governance/evidence" />);
    await user.selectOptions(
      screen.getByTestId("evidence-filter-standing"),
      "historical",
    );
    const list = screen.getByTestId("evidence-list");
    const buttons = within(list).getAllByRole("button");
    expect(buttons.length).toBeGreaterThanOrEqual(1);
    expect(screen.queryByTestId("evidence-list-item-ev-host-scheduler-operational-debt")).not.toBeInTheDocument();
  });

  it("provenance line is shown for each list item", () => {
    render(<AppForTest initialEntry="/governance/evidence" />);
    const provenanceEls = screen.getAllByTestId(/^evidence-provenance-/);
    expect(provenanceEls.length).toBeGreaterThanOrEqual(11);
  });

  it("pending-not-fault note appears for pending evidence detail", async () => {
    const user = userEvent.setup();
    render(<AppForTest initialEntry="/governance/evidence" />);
    await user.click(
      screen.getByTestId("evidence-list-item-ev-r3e-pending-future-unseen"),
    );
    expect(
      screen.getByTestId("evidence-detail-pending-not-fault"),
    ).toBeInTheDocument();
  });

  it("safety notices include R3D≠R3E and pending≠fault copy", () => {
    render(<AppForTest initialEntry="/governance/evidence" />);
    const notices = screen.getByTestId("evidence-safety-notices");
    expect(notices.textContent).toMatch(/R3D/);
    expect(notices.textContent).toMatch(/R3E/);
    expect(notices.textContent).toMatch(/[Pp]ending|PENDING/);
    expect(notices.textContent).toMatch(/fault/i);
  });

  it("keeps R3D and R3E copy distinct in the catalog", async () => {
    const user = userEvent.setup();
    render(<AppForTest initialEntry="/governance/evidence" />);

    await user.click(
      screen.getByTestId("evidence-list-item-ev-r3d-validation-conclusion"),
    );
    const r3d = screen.getByTestId("evidence-detail");
    expect(r3d).toHaveTextContent("NO_MEASURABLE_EDGE");
    expect(r3d).toHaveTextContent(/não implica rejeição do experimento R3E/i);
    expect(r3d.textContent ?? "").not.toMatch(/\bR3E foi rejeitado\b/i);

    await user.click(
      screen.getByTestId("evidence-list-item-ev-r3e-pending-future-unseen"),
    );
    const r3e = screen.getByTestId("evidence-detail");
    expect(r3e).toHaveTextContent("PENDING_FUTURE_UNSEEN_DATA");
    expect(r3e.textContent ?? "").not.toMatch(/R3D_RESULT=NO_MEASURABLE_EDGE/);
  });
});
