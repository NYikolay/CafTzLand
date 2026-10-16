import { Container } from "@/components/ui/container";

export function SiteFooter() {
  return (
    <Container>
      <div className="flex flex-col gap-4 border-t border-cream/20 pt-6 font-mono text-[11px] uppercase tracking-[1px] text-cream/70 md:flex-row md:items-center md:justify-between">
        <p>Кварта · Минск · С 2019 года</p>
        <p>Четверг — день свежего кофе</p>
      </div>
      <p
        aria-hidden
        className="mt-6 select-none text-center font-sans text-[clamp(64px,18vw,240px)] font-extrabold leading-none tracking-[-0.07em] text-cream md:text-left"
      >
        Кварта.
      </p>
    </Container>
  );
}
