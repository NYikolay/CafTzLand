import type { InputHTMLAttributes } from "react";

type RadioCardProps = InputHTMLAttributes<HTMLInputElement> & {
  label: string;
};

export function RadioCard({ label, ...inputProps }: RadioCardProps) {
  return (
    <label className="flex flex-1 cursor-pointer items-center gap-2 rounded-[3px] border border-line px-4 py-3 text-sm transition-colors has-[:checked]:border-accent has-[:checked]:bg-accent/5">
      <input type="radio" className="peer sr-only" {...inputProps} />
      <span
        aria-hidden
        className="grid h-4 w-4 shrink-0 place-items-center rounded-full border border-muted after:h-2 after:w-2 after:rounded-full after:bg-accent after:content-[''] after:hidden peer-checked:border-accent peer-checked:after:block"
      />
      <span>{label}</span>
    </label>
  );
}
