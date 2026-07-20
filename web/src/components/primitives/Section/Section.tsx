import { forwardRef, type HTMLAttributes, type ReactNode } from "react";
import "../primitives.css";

export type SectionProps = HTMLAttributes<HTMLElement> & {
  title?: string;
  children: ReactNode;
};

export const Section = forwardRef<HTMLElement, SectionProps>(function Section(
  { title, children, className, ...rest },
  ref,
) {
  const classes = ["wick-section", className].filter(Boolean).join(" ");
  return (
    <section ref={ref} className={classes} {...rest}>
      {title ? <h2 className="wick-section__title">{title}</h2> : null}
      {children}
    </section>
  );
});
