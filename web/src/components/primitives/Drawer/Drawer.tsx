import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogOverlay,
  DialogPortal,
  DialogTrigger,
  type DialogContentProps,
} from "../Dialog/Dialog";
import { forwardRef, type ElementRef } from "react";
import "../primitives.css";

/**
 * Drawer reuses Dialog (Radix) focus trap / escape / restoration.
 * Presentation differs (side panel). Not an application navigation drawer.
 */
export const Drawer = Dialog;
export const DrawerTrigger = DialogTrigger;
export const DrawerClose = DialogClose;
export const DrawerPortal = DialogPortal;
export const DrawerOverlay = DialogOverlay;

export type DrawerContentProps = DialogContentProps;

export const DrawerContent = forwardRef<
  ElementRef<"div">,
  DrawerContentProps
>(function DrawerContent({ className, ...rest }, ref) {
  const classes = ["wick-dialog-content", "wick-drawer-content", className]
    .filter(Boolean)
    .join(" ");
  return <DialogContent ref={ref} className={classes} {...rest} />;
});
