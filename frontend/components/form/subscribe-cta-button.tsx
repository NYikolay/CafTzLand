"use client";

import { useLeadForm } from "@/components/form/lead-form-context";
import { Button } from "@/components/ui/button";
import { ArrowUpRightIcon } from "@/components/ui/icons";

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
      <ArrowUpRightIcon />
    </Button>
  );
}
