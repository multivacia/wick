import { forwardRef, type AnchorHTMLAttributes, type ReactNode } from "react";
import "../primitives.css";

export type LinkProps = AnchorHTMLAttributes<HTMLAnchorElement> & {
  children: ReactNode;
};

export const Link = forwardRef<HTMLAnchorElement, LinkProps>(function Link(
  { href, target, rel, className, children, ...rest },
  ref,
) {
  const external = target === "_blank";
  const safeRel = external
    ? [rel, "noreferrer", "noopener"].filter(Boolean).join(" ")
    : rel;
  const classes = ["wick-link", className].filter(Boolean).join(" ");

  return (
    <a
      ref={ref}
      href={href}
      target={target}
      rel={safeRel || undefined}
      className={classes}
      {...rest}
    >
      {children}
    </a>
  );
});
