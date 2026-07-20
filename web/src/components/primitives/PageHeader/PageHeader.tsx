import { forwardRef, type HTMLAttributes, type ReactNode } from "react";
import "../primitives.css";

export type PageHeaderProps = HTMLAttributes<HTMLElement> & {
  title: string;
  description?: string;
  eyebrow?: string;
  actions?: ReactNode;
};

export const PageHeader = forwardRef<HTMLElement, PageHeaderProps>(
  function PageHeader(
    { title, description, eyebrow, actions, className, ...rest },
    ref,
  ) {
    const classes = ["wick-page-header", className].filter(Boolean).join(" ");
    return (
      <header ref={ref} className={classes} {...rest}>
        {eyebrow ? <p className="wick-page-header__eyebrow">{eyebrow}</p> : null}
        <div className="wick-page-header__row">
          <h1 className="wick-page-header__title">{title}</h1>
          {actions ? <div className="wick-inline">{actions}</div> : null}
        </div>
        {description ? (
          <p className="wick-page-header__description">{description}</p>
        ) : null}
      </header>
    );
  },
);
