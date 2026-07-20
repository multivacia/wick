import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Alert } from "../../src/components/primitives";

describe("Alert", () => {
  it("uses role=status for informational and attention tones", () => {
    const { rerender } = render(
      <Alert tone="informational" title="Note">
        Info body
      </Alert>,
    );
    expect(screen.getByRole("status")).toBeInTheDocument();

    rerender(
      <Alert tone="attention" title="Wait">
        Attention body
      </Alert>,
    );
    expect(screen.getByRole("status")).toBeInTheDocument();
  });

  it("uses role=alert only for fault tone", () => {
    render(
      <Alert tone="fault" title="Fault">
        Fault body
      </Alert>,
    );
    expect(screen.getByRole("alert")).toBeInTheDocument();
  });
});
