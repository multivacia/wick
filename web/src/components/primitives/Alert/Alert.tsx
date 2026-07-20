import { forwardRef, type HTMLAttributes, type ReactNode } from "react";
import "../primitives.css";

export type AlertTone = "informational" | "attention" | "fault" | "success";

export type AlertProps = HTMLAttributes<HTMLDivElement> & {
  tone?: AlertTone;
  title?: string;
  children: ReactNode;
};

const TONE_STYLE: Record<
  AlertTone,
  { fg: string; bg: string; border: string; role: "status" | "alert" }
> = {
  informational: {
    fg: "var(--wick-color-status-informational-fg)",
    bg: "var(--wick-color-status-informational-bg)",
    border: "var(--wick-color-status-informational-border)",
    role: "status",
  },
  attention: {
    fg: "var(--wick-color-status-attention-fg)",
    bg: "var(--wick-color-status-attention-bg)",
    border: "var(--wick-color-status-attention-border)",
    role: "status",
  },
  success: {
    fg: "var(--wick-color-status-completed-fg)",
    bg: "var(--wick-color-status-completed-bg)",
    border: "var(--wick-color-status-completed-border)",
    role: "status",
  },
  fault: {
    fg: "var(--wick-color-status-fault-fg)",
    bg: "var(--wick-color-status-fault-bg)",
    border: "var(--wick-color-status-fault-border)",
    role: "alert",
  },
};

export const Alert = forwardRef<HTMLDivElement, AlertProps>(function Alert(
  { tone = "informational", title, children, className, style, ...rest },
  ref,
) {
  const toneStyle = TONE_STYLE[tone];
  const classes = ["wick-alert", className].filter(Boolean).join(" ");
  return (
    <div
      ref={ref}
      className={classes}
      role={toneStyle.role}
      data-tone={tone}
      style={{
        color: toneStyle.fg,
        background: toneStyle.bg,
        borderColor: toneStyle.border,
        ...style,
      }}
      {...rest}
    >
      {title ? <p className="wick-alert__title">{title}</p> : null}
      <div className="wick-alert__body">{children}</div>
    </div>
  );
});
