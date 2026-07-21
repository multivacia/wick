import { render } from "@testing-library/react";
import { axe } from "jest-axe";
import { describe, expect, it } from "vitest";
import { AppForTest } from "../../src/App";

describe("Evidence Explorer accessibility smoke", () => {
  it("has no basic axe violations on /governance/evidence", async () => {
    const { container } = render(
      <AppForTest initialEntry="/governance/evidence" />,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
