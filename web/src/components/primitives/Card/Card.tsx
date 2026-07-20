import { forwardRef, type HTMLAttributes, type ReactNode } from "react";
import "../primitives.css";

export type CardProps = HTMLAttributes<HTMLDivElement> & {
  children: ReactNode;
};

export const Card = forwardRef<HTMLDivElement, CardProps>(function Card(
  { className, children, ...rest },
  ref,
) {
  const classes = ["wick-card", className].filter(Boolean).join(" ");
  return (
    <div ref={ref} className={classes} {...rest}>
      {children}
    </div>
  );
});
