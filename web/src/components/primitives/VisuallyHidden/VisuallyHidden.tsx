import { forwardRef, type HTMLAttributes, type ReactNode } from "react";
import "../primitives.css";

export type VisuallyHiddenProps = HTMLAttributes<HTMLSpanElement> & {
  children: ReactNode;
};

export const VisuallyHidden = forwardRef<HTMLSpanElement, VisuallyHiddenProps>(
  function VisuallyHidden({ className, children, ...rest }, ref) {
    const classes = ["wick-visually-hidden", className].filter(Boolean).join(" ");
    return (
      <span ref={ref} className={classes} {...rest}>
        {children}
      </span>
    );
  },
);
