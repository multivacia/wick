import { forwardRef, type HTMLAttributes, type ReactNode } from "react";
import "../primitives.css";

export type InlineProps = HTMLAttributes<HTMLDivElement> & {
  children: ReactNode;
};

export const Inline = forwardRef<HTMLDivElement, InlineProps>(function Inline(
  { className, children, ...rest },
  ref,
) {
  const classes = ["wick-inline", className].filter(Boolean).join(" ");
  return (
    <div ref={ref} className={classes} {...rest}>
      {children}
    </div>
  );
});
