import { render } from "@testing-library/react";
import { axe } from "jest-axe";
import { describe, expect, it } from "vitest";
import { AppForTest } from "../../src/App";

describe("R3E Experiment screen accessibility smoke", () => {
  it("has no basic axe violations on fixture-backed R3E screen", async () => {
    const { container } = render(
      <AppForTest initialEntry="/experiments/r3e" />,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
