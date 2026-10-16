"use client";

import { useLeadForm } from "@/components/form/lead-form-context";
import { Button } from "@/components/ui/button";

export function SubscribeCtaButton({
  variant = "accent",
  label = "Хочу кофе по подписке",
}: {
  variant?: "accent" | "outline" | "cream";
  label?: string;
}) {
  const { selectInterest } = useLeadForm();
  return (
    <Button variant={variant} onClick={() => selectInterest("subscription")}>
      {label}
      <span aria-hidden>↗</span>
    </Button>
  );
}
