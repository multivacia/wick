import { forwardRef, type HTMLAttributes } from "react";
import { VisuallyHidden } from "../VisuallyHidden/VisuallyHidden";
import "../primitives.css";

export type SkeletonProps = HTMLAttributes<HTMLDivElement> & {
  /** Accessible loading label for the region. */
  label?: string;
  width?: string;
  height?: string;
};

export const Skeleton = forwardRef<HTMLDivElement, SkeletonProps>(
  function Skeleton(
    {
      label = "Loading",
      width = "100%",
      height = "1rem",
      className,
      style,
      ...rest
    },
    ref,
  ) {
    const classes = ["wick-skeleton", className].filter(Boolean).join(" ");
    return (
      <div ref={ref} role="status" aria-live="polite" {...rest}>
        <VisuallyHidden>{label}</VisuallyHidden>
        <div
          className={classes}
          style={{ width, height, ...style }}
          aria-hidden="true"
        />
      </div>
    );
  },
);
