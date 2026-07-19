import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { App } from "../src/App";
import {
  SCAFFOLD_NOTICE,
  SCAFFOLD_STATUS,
  SCAFFOLD_TITLE,
} from "../src/scaffoldCopy";

describe("App scaffold", () => {
  it("renders the root application placeholder", () => {
    render(<App />);

    expect(
      screen.getByRole("heading", { level: 1, name: SCAFFOLD_TITLE }),
    ).toBeInTheDocument();
    expect(screen.getByText(SCAFFOLD_STATUS)).toBeInTheDocument();
    expect(screen.getByText(SCAFFOLD_NOTICE)).toBeInTheDocument();
  });
});
