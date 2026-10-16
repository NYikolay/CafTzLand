"use client";

import { useLeadForm } from "@/components/form/lead-form-context";
import type { ReactNode } from "react";

export function CoffeeOrderButton({
  productId,
  children,
}: {
  productId: number;
  children: ReactNode;
}) {
  const { selectCoffee } = useLeadForm();
  return (
    <button
      type="button"
      onClick={() => selectCoffee(productId)}
      className="inline-flex items-center gap-1 text-sm font-medium text-accent-deep underline-offset-4 hover:underline"
    >
      {children}
      <span aria-hidden>↗</span>
    </button>
  );
}
