import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { AppForTest } from "../../src/App";
import { resolveNextThemePreference } from "../../src/shell/themePreference";

describe("I5 application shell", () => {
  it("redirects / to /overview", () => {
    render(<AppForTest initialEntry="/" />);
    expect(
      screen.getByRole("heading", { level: 1, name: "Visão Geral" }),
    ).toBeInTheDocument();
    expect(screen.getByTestId("overview-screen")).toBeInTheDocument();
  });

  it("marks active navigation for the current route", () => {
    render(<AppForTest initialEntry="/future-collection/runs" />);
    const nav = screen.getByRole("navigation", {
      name: "Principal",
      hidden: true,
    });
    const active = within(nav).getByRole("link", {
      name: /Execuções/i,
      hidden: true,
    });
    expect(active).toHaveAttribute("aria-current", "page");
    expect(active.className).toContain("wick-nav-item__link--active");
  });

  it("exposes nav and main landmarks and skip link", async () => {
    const user = userEvent.setup();
    render(<AppForTest />);
    expect(screen.getByRole("main")).toHaveAttribute("id", "main-content");
    expect(
      screen.getByRole("link", { name: "Ir para o conteúdo principal" }),
    ).toHaveAttribute("href", "#main-content");
    // Desktop sidebar may be CSS-hidden in jsdom; still present for a11y when shown.
    expect(
      screen.getByRole("navigation", { name: "Principal", hidden: true }),
    ).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Menu" }));
    expect(
      screen.getByRole("navigation", { name: "Principal móvel" }),
    ).toBeInTheDocument();
  });

  it("opens and closes the mobile navigation drawer", async () => {
    const user = userEvent.setup();
    render(<AppForTest />);
    const menu = screen.getByRole("button", { name: "Menu" });
    expect(menu).toHaveAttribute("aria-expanded", "false");
    await user.click(menu);
    expect(menu).toHaveAttribute("aria-expanded", "true");
    expect(
      screen.getByRole("dialog", { name: "Navegação" }),
    ).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Fechar menu" }));
    expect(screen.queryByRole("dialog", { name: "Navegação" })).toBeNull();
  });

  it("closes mobile menu with Escape", async () => {
    const user = userEvent.setup();
    render(<AppForTest />);
    await user.click(screen.getByRole("button", { name: "Menu" }));
    expect(screen.getByRole("dialog", { name: "Navegação" })).toBeInTheDocument();
    await user.keyboard("{Escape}");
    expect(screen.queryByRole("dialog", { name: "Navegação" })).toBeNull();
  });

  it("closes mobile menu after navigation", async () => {
    const user = userEvent.setup();
    render(<AppForTest />);
    await user.click(screen.getByRole("button", { name: "Menu" }));
    const dialog = screen.getByRole("dialog", { name: "Navegação" });
    await user.click(within(dialog).getByRole("link", { name: /Readiness/i }));
    expect(screen.queryByRole("dialog", { name: "Navegação" })).toBeNull();
    expect(
      screen.getByRole("heading", { level: 1, name: "Readiness" }),
    ).toBeInTheDocument();
  });

  it("cycles theme control labels", async () => {
    const user = userEvent.setup();
    render(<AppForTest />);
    const control = screen.getByRole("button", { name: /Tema:/i });
    const before = control.textContent ?? "";
    await user.click(control);
    expect(control.textContent).not.toEqual(before);
    expect(resolveNextThemePreference("system")).toBe("light");
    expect(resolveNextThemePreference("light")).toBe("dark");
    expect(resolveNextThemePreference("dark")).toBe("system");
  });

  it("renders not-found placeholder for unknown routes", () => {
    render(<AppForTest initialEntry="/does-not-exist" />);
    expect(
      screen.getByRole("heading", { level: 1, name: "Página não encontrada" }),
    ).toBeInTheDocument();
  });

  it("supports keyboard activation of navigation links", async () => {
    const user = userEvent.setup();
    render(<AppForTest initialEntry="/overview" />);
    await user.click(screen.getByRole("button", { name: "Menu" }));
    const dialog = screen.getByRole("dialog", { name: "Navegação" });
    const readiness = within(dialog).getByRole("link", { name: /Readiness/i });
    readiness.focus();
    await user.keyboard("{Enter}");
    expect(
      screen.getByRole("heading", { level: 1, name: "Readiness" }),
    ).toBeInTheDocument();
  });
});
