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
    <Button variant={variant} className={"text-black md:max-w-65.75"} onClick={() => selectInterest("subscription")}>
      {label}
      <ArrowUpRightIcon className={"text-accent"} />
    </Button>
  );
}
