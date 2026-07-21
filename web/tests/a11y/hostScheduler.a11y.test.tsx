import { render } from "@testing-library/react";
import { axe } from "jest-axe";
import { describe, expect, it } from "vitest";
import { AppForTest } from "../../src/App";

describe("Host/Scheduler screen accessibility smoke", () => {
  it("has no basic axe violations on fixture-backed Host/Scheduler", async () => {
    const { container } = render(
      <AppForTest initialEntry="/operations/host-scheduler" />,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
