import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { AppForTest } from "../../../src/App";
import {
  COLLECTION_DATA_QUALITY_FIXTURE_ID,
  loadCollectedDataScreenData,
  SYNTHETIC_COLLECTION_DISCLAIMER,
} from "../../../src/screens/collected-data/loadCollectedDataScreenData";
import { MemoryRouter } from "react-router-dom";
import { CollectedDataScreenView } from "../../../src/screens/collected-data/CollectedDataScreenView";
import { clearCollectionFilters } from "../../../src/viewmodels";

describe("UX-R3 I1 Collected Data / Data Quality screen", () => {
  it("renders Dados Coletados on /future-collection/collected-data", () => {
    render(<AppForTest initialEntry="/future-collection/collected-data" />);
    expect(screen.getByTestId("collected-data-screen")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { level: 1, name: "Dados Coletados" }),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("Planejado / não implementado"),
    ).not.toBeInTheDocument();
  });

  it("activates Dados Coletados navigation after Runs and Readiness", () => {
    render(<AppForTest initialEntry="/future-collection/collected-data" />);
    const nav = screen.getByRole("navigation", {
      name: "Principal",
      hidden: true,
    });
    const link = within(nav).getByRole("link", {
      name: /Dados Coletados/i,
      hidden: true,
    });
    expect(link).toHaveAttribute("href", "/future-collection/collected-data");
    expect(link).toHaveAttribute("aria-current", "page");
  });

  it("shows synthetic and freshness disclosures with fixture id", () => {
    render(<AppForTest initialEntry="/future-collection/collected-data" />);
    const notice = screen.getByTestId("collected-data-synthetic-notice");
    expect(within(notice).getByText("Dados ilustrativos")).toBeInTheDocument();
    expect(notice).toHaveTextContent(SYNTHETIC_COLLECTION_DISCLAIMER);
    expect(
      screen.getByText(new RegExp(COLLECTION_DATA_QUALITY_FIXTURE_ID)),
    ).toBeInTheDocument();
    expect(
      screen.getByTestId("collected-data-freshness-disclosure"),
    ).toBeInTheDocument();
    expect(
      screen.getByTestId("collected-data-semantic-safeguards"),
    ).toHaveTextContent(/DATA_QUALITY/);
    expect(loadCollectedDataScreenData().fixtureId).toBe(
      COLLECTION_DATA_QUALITY_FIXTURE_ID,
    );
  });

  it("lists series covering fault-only red and unknown ≠ zero", () => {
    render(<AppForTest initialEntry="/future-collection/collected-data" />);
    const fault = screen.getByTestId("collected-data-series-dot-usdt-1h-kraken");
    expect(fault).toHaveAttribute("data-severity", "fault");
    expect(fault).toHaveAttribute("data-quality-status", "SOURCE_UNAVAILABLE");

    const unknown = screen.getByTestId(
      "collected-data-series-matic-usdt-1h-unknown",
    );
    const metrics = within(unknown).getByTestId(
      "collected-data-metrics-matic-usdt-1h-unknown",
    );
    expect(metrics).toHaveTextContent("Desconhecido");
    expect(metrics).not.toHaveTextContent(/^0$/);
    const unknownValues = within(metrics)
      .getAllByRole("definition")
      .map((el) => el.textContent);
    expect(unknownValues.every((t) => t === "Desconhecido")).toBe(true);
  });

  it("filters by severity and clears to restore results", async () => {
    const user = userEvent.setup();
    render(<AppForTest initialEntry="/future-collection/collected-data" />);

    await user.selectOptions(
      screen.getByTestId("collected-data-filter-severity"),
      "fault",
    );
    expect(screen.getByTestId("collected-data-result-count")).toHaveTextContent(
      /Exibindo 1 de 9/,
    );
    expect(
      screen.getByTestId("collected-data-series-dot-usdt-1h-kraken"),
    ).toBeInTheDocument();

    await user.click(screen.getByTestId("collected-data-filters-clear"));
    expect(screen.getByTestId("collected-data-filter-severity")).toHaveValue("");
    expect(screen.getByTestId("collected-data-result-count")).toHaveTextContent(
      /Exibindo 9 de 9/,
    );
  });

  it("shows no-results state with clear filters affordance", async () => {
    const user = userEvent.setup();
    render(<AppForTest initialEntry="/future-collection/collected-data" />);
    await user.selectOptions(
      screen.getByTestId("collected-data-filter-series"),
      "btc-usdt-1h-binance",
    );
    await user.selectOptions(
      screen.getByTestId("collected-data-filter-severity"),
      "fault",
    );
    expect(screen.getByTestId("collected-data-no-results")).toBeInTheDocument();
    await user.click(screen.getByTestId("collected-data-no-results-clear"));
    expect(screen.getByTestId("collected-data-series-list")).toBeInTheDocument();
  });

  it("exposes approved cross-navigation only", () => {
    render(<AppForTest initialEntry="/future-collection/collected-data" />);
    expect(screen.getByTestId("collected-data-link-runs")).toHaveAttribute(
      "href",
      "/future-collection/runs",
    );
    expect(screen.getByTestId("collected-data-link-readiness")).toHaveAttribute(
      "href",
      "/future-collection/readiness",
    );
    expect(
      screen.getByTestId("related-evidence-link-ev-fu-collection-readiness"),
    ).toHaveAttribute(
      "href",
      "/governance/evidence?evidenceId=ev-fu-collection-readiness",
    );
    const main = screen.getByRole("main");
    for (const link of within(main).queryAllByRole("link")) {
      const href = link.getAttribute("href") ?? "";
      expect(href).not.toMatch(/^https?:/i);
      expect(href).not.toMatch(/download/i);
    }
  });

  it("does not expose collection controls or validation actions", () => {
    render(<AppForTest initialEntry="/future-collection/collected-data" />);
    const main = screen.getByRole("main");
    expect(
      within(main).queryByRole("button", {
        name: /validar|coletar|ativar|download|baixar/i,
      }),
    ).toBeNull();
  });

  it("supports empty catalog presentation without fault semantics", () => {
    const data = loadCollectedDataScreenData();
    data.domain.series = [];
    render(
      <MemoryRouter>
        <CollectedDataScreenView
          data={data}
          criteria={{ filters: clearCollectionFilters() }}
          onFiltersChange={() => undefined}
          onClearFilters={() => undefined}
        />
      </MemoryRouter>,
    );
    expect(screen.getByTestId("collected-data-empty-state")).toHaveTextContent(
      /EMPTY ≠ FAULT/,
    );
  });

  it("applies responsive layout class on the screen root", () => {
    render(<AppForTest initialEntry="/future-collection/collected-data" />);
    expect(screen.getByTestId("collected-data-screen").className).toContain(
      "wick-collected-data-screen",
    );
  });
});
