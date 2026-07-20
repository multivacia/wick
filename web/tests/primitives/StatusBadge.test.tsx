import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import {
  STATUS_BADGE_STATUSES,
  StatusBadge,
  type StatusBadgeStatus,
} from "../../src/components/primitives";

const EXPECTED_LABELS: Record<StatusBadgeStatus, string> = {
  healthy: "Healthy",
  completed: "Completed",
  attention: "Attention",
  not_ready: "Not ready",
  blocked: "Blocked",
  deferred: "Deferred",
  unknown: "Unknown",
  fault: "Fault",
  informational: "Informational",
};

describe("StatusBadge", () => {
  it("renders textual meaning for every approved status", () => {
    for (const status of STATUS_BADGE_STATUSES) {
      const { unmount } = render(<StatusBadge status={status} />);
      expect(screen.getByText(EXPECTED_LABELS[status])).toBeInTheDocument();
      unmount();
    }
  });

  it("exposes data-status and is not color-only (visible text)", () => {
    render(<StatusBadge status="not_ready" />);
    const badge = screen.getByText("Not ready").closest("[data-status]");
    expect(badge).toHaveAttribute("data-status", "not_ready");
    expect(screen.getByText("Not ready")).toBeVisible();
  });
});
