import * as RadixDialog from "@radix-ui/react-dialog";
import {
  forwardRef,
  type ComponentPropsWithoutRef,
  type ElementRef,
  type ReactNode,
} from "react";
import "../primitives.css";

export const Dialog = RadixDialog.Root;
export const DialogTrigger = RadixDialog.Trigger;
export const DialogClose = RadixDialog.Close;
export const DialogPortal = RadixDialog.Portal;

export const DialogOverlay = forwardRef<
  ElementRef<typeof RadixDialog.Overlay>,
  ComponentPropsWithoutRef<typeof RadixDialog.Overlay>
>(function DialogOverlay({ className, ...rest }, ref) {
  const classes = ["wick-dialog-overlay", className].filter(Boolean).join(" ");
  return <RadixDialog.Overlay ref={ref} className={classes} {...rest} />;
});

export type DialogContentProps = ComponentPropsWithoutRef<
  typeof RadixDialog.Content
> & {
  title: string;
  description?: string;
  children?: ReactNode;
};

export const DialogContent = forwardRef<
  ElementRef<typeof RadixDialog.Content>,
  DialogContentProps
>(function DialogContent(
  { title, description, children, className, ...rest },
  ref,
) {
  const classes = ["wick-dialog-content", className].filter(Boolean).join(" ");
  return (
    <DialogPortal>
      <DialogOverlay />
      <RadixDialog.Content
        ref={ref}
        className={classes}
        aria-modal="true"
        {...rest}
      >
        <RadixDialog.Title className="wick-dialog-title">{title}</RadixDialog.Title>
        {description ? (
          <RadixDialog.Description className="wick-dialog-description">
            {description}
          </RadixDialog.Description>
        ) : (
          <RadixDialog.Description className="wick-visually-hidden">
            {title}
          </RadixDialog.Description>
        )}
        {children}
      </RadixDialog.Content>
    </DialogPortal>
  );
});
