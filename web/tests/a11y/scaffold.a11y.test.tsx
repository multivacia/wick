import { render } from "@testing-library/react";
import { axe } from "jest-axe";
import { describe, expect, it } from "vitest";
import { App } from "../../src/App";

describe("accessibility smoke", () => {
  it("has no basic axe violations in the scaffold placeholder", async () => {
    const { container } = render(<App />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
