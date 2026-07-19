import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Link } from "../../src/components/primitives";

describe("Link", () => {
  it("renders a native anchor", () => {
    render(<Link href="/docs">Docs</Link>);
    const link = screen.getByRole("link", { name: "Docs" });
    expect(link).toHaveAttribute("href", "/docs");
  });

  it("adds noreferrer noopener for target=_blank", () => {
    render(
      <Link href="https://example.com" target="_blank">
        External
      </Link>,
    );
    const link = screen.getByRole("link", { name: "External" });
    expect(link).toHaveAttribute("target", "_blank");
    expect(link.getAttribute("rel") ?? "").toContain("noreferrer");
    expect(link.getAttribute("rel") ?? "").toContain("noopener");
  });
});
