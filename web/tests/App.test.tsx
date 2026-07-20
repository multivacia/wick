import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AppForTest } from "../src/App";

describe("App shell entry", () => {
  it("renders the operational shell overview placeholder", () => {
    render(<AppForTest initialEntry="/overview" />);

    expect(
      screen.getByRole("heading", { level: 1, name: "Visão Geral" }),
    ).toBeInTheDocument();
    expect(screen.getByRole("main")).toBeInTheDocument();
  });
});
