import Link from "next/link";
import type { ComponentProps } from "react";

export type ButtonVariant = "accent" | "outline" | "cream";

const base =
  "inline-flex h-11 items-center justify-center gap-2 rounded-[3px] px-[18px] cursor-pointer text-sm font-medium transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent";

const variants: Record<ButtonVariant, string> = {
  accent: "bg-accent text-paper hover:bg-[#b23f26]",
  outline: "border border-ink/30 text-ink hover:border-ink",
  cream: "bg-cream text-accent-deep hover:bg-paper",
};

type ButtonProps = ComponentProps<"button"> & { variant?: ButtonVariant };

export function Button({ variant = "accent", className, type, ...rest }: ButtonProps) {
  return (
    <button
      type={type ?? "button"}
      className={`${base} ${variants[variant]}${className ? ` ${className}` : ""}`}
      {...rest}
    />
  );
}

type ButtonLinkProps = ComponentProps<typeof Link> & { variant?: ButtonVariant };

export function ButtonLink({ variant = "accent", className, ...rest }: ButtonLinkProps) {
  return (
    <Link
      className={`${base} ${variants[variant]}${className ? ` ${className}` : ""}`}
      {...rest}
    />
  );
}
