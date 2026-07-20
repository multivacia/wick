import { render } from "@testing-library/react";
import { axe } from "jest-axe";
import { describe, expect, it } from "vitest";
import { AppForTest } from "../../src/App";

describe("Overview screen accessibility smoke", () => {
  it("has no basic axe violations on fixture-backed Overview", async () => {
    const { container } = render(<AppForTest initialEntry="/overview" />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
