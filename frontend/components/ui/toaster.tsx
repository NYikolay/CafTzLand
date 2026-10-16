"use client";

import type { CSSProperties } from "react";
import { Toaster as SonnerToaster } from "sonner";

const theme = {
  "--normal-bg": "var(--color-ink)",
  "--normal-text": "var(--color-cream)",
  "--normal-border": "color-mix(in srgb, var(--color-cream) 15%, transparent)",
  "--success-bg": "var(--color-cream)",
  "--success-text": "var(--color-ink)",
  "--success-border": "var(--color-line)",
  "--error-bg": "var(--color-accent-deep)",
  "--error-text": "var(--color-paper)",
  "--error-border": "color-mix(in srgb, var(--color-paper) 25%, transparent)",
  "--border-radius": "3px",
} as CSSProperties;

export function Toaster() {
  return (
    <SonnerToaster
      position="bottom-right"
      offset={24}
      mobileOffset={16}
      duration={5000}
      richColors
      toastOptions={{ classNames: { toast: "font-sans", success: '[&_[data-icon]]:text-accent' } }}
      style={theme}
    />
  );
}
