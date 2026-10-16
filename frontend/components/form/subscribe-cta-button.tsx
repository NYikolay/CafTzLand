"use client";

import { useLeadForm } from "@/components/form/lead-form-context";
import { Button } from "@/components/ui/button";

export function SubscribeCtaButton({ variant = "accent" }: { variant?: "accent" | "outline" | "cream" }) {
  const { selectInterest } = useLeadForm();
  return (
    <Button variant={variant} onClick={() => selectInterest("subscription")}>
      Хочу кофе по подписке
      <span aria-hidden>↗</span>
    </Button>
  );
}
