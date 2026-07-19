import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Skeleton, VisuallyHidden } from "../../src/components/primitives";

const primitivesCss = readFileSync(
  join(
    dirname(fileURLToPath(import.meta.url)),
    "../../src/components/primitives/primitives.css",
  ),
  "utf8",
);

describe("Skeleton and VisuallyHidden", () => {
  it("exposes an accessible loading status label", () => {
    render(<Skeleton label="Loading overview" />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading overview");
  });

  it("includes reduced-motion aware skeleton styles", () => {
    expect(primitivesCss).toContain(
      "@media (prefers-reduced-motion: no-preference)",
    );
    expect(primitivesCss).toContain("wick-skeleton-pulse");
  });

  it("VisuallyHidden keeps text available to assistive tech", () => {
    render(
      <button type="button">
        <VisuallyHidden>Close dialog</VisuallyHidden>
      </button>,
    );
    expect(
      screen.getByRole("button", { name: "Close dialog" }),
    ).toBeInTheDocument();
  });
});
