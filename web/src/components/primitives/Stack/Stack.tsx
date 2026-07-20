import { forwardRef, type HTMLAttributes, type ReactNode } from "react";
import "../primitives.css";

export type StackProps = HTMLAttributes<HTMLDivElement> & {
  children: ReactNode;
};

export const Stack = forwardRef<HTMLDivElement, StackProps>(function Stack(
  { className, children, ...rest },
  ref,
) {
  const classes = ["wick-stack", className].filter(Boolean).join(" ");
  return (
    <div ref={ref} className={classes} {...rest}>
      {children}
    </div>
  );
});
