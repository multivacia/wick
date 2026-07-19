import { forwardRef, type HTMLAttributes } from "react";
import "../primitives.css";

export const STATUS_BADGE_STATUSES = [
  "healthy",
  "completed",
  "attention",
  "not_ready",
  "blocked",
  "deferred",
  "unknown",
  "fault",
  "informational",
] as const;

export type StatusBadgeStatus = (typeof STATUS_BADGE_STATUSES)[number];

const STATUS_LABELS: Record<StatusBadgeStatus, string> = {
  healthy: "Healthy",
  completed: "Completed",
  attention: "Attention",
  not_ready: "Not ready",
  blocked: "Blocked",
  deferred: "Deferred",
  unknown: "Unknown",
  fault: "Fault",
  informational: "Informational",
};

const STATUS_TOKEN: Record<StatusBadgeStatus, string> = {
  healthy: "healthy",
  completed: "completed",
  attention: "attention",
  not_ready: "not-ready",
  blocked: "blocked",
  deferred: "deferred",
  unknown: "unknown",
  fault: "fault",
  informational: "informational",
};

export type StatusBadgeProps = HTMLAttributes<HTMLSpanElement> & {
  status: StatusBadgeStatus;
  /** Optional override; defaults to approved plain-language label. */
  label?: string;
};

export const StatusBadge = forwardRef<HTMLSpanElement, StatusBadgeProps>(
  function StatusBadge({ status, label, className, style, ...rest }, ref) {
    const token = STATUS_TOKEN[status];
    const text = label ?? STATUS_LABELS[status];
    const classes = ["wick-status-badge", className].filter(Boolean).join(" ");

    return (
      <span
        ref={ref}
        className={classes}
        data-status={status}
        style={{
          color: `var(--wick-color-status-${token}-fg)`,
          background: `var(--wick-color-status-${token}-bg)`,
          borderColor: `var(--wick-color-status-${token}-border)`,
          ...style,
        }}
        {...rest}
      >
        <span className="wick-status-badge__mark" aria-hidden="true" />
        <span>{text}</span>
      </span>
    );
  },
);
