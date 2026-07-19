import { cleanup, render } from "@testing-library/react";
import { axe } from "jest-axe";
import { afterEach, describe, expect, it } from "vitest";
import { App } from "../../src/App";
import { applyResolvedTheme } from "../../src/theme/theme";
import "../../src/styles.css";

describe("theme accessibility smoke", () => {
  afterEach(() => {
    cleanup();
    applyResolvedTheme("light", document.documentElement);
  });

  it("has no basic axe violations under light theme", async () => {
    applyResolvedTheme("light", document.documentElement);
    const { container } = render(<App />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("has no basic axe violations under dark theme", async () => {
    applyResolvedTheme("dark", document.documentElement);
    const { container } = render(<App />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
