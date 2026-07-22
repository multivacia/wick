import { render } from "@testing-library/react";
import { axe } from "jest-axe";
import { describe, expect, it } from "vitest";
import { AppForTest } from "../../src/App";

describe("Collected Data accessibility smoke", () => {
  it("has no basic axe violations on /future-collection/collected-data", async () => {
    const { container } = render(
      <AppForTest initialEntry="/future-collection/collected-data" />,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
