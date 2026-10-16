import type { ReactNode } from "react";

export function Eyebrow({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <p
      className={`font-mono text-[11px] uppercase tracking-[1px] text-accent${className ? ` ${className}` : ""}`}
    >
      {children}
    </p>
  );
}
