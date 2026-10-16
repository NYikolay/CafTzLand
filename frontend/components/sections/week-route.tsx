import { Container } from "@/components/ui/container";
import { ArrowRightIcon } from "@/components/ui/icons";

const SEGMENTS = ["ЧТ — ОБЖАРКА", "ПТ — РАЗВОЗИМ", "У ВАС НА 1–3 ДЕНЬ ПОСЛЕ ОБЖАРКИ"] as const;

export function WeekRoute() {
  return (
    <section aria-label="Маршрут недели" className="bg-ink">
      <Container>
        <div className="flex items-center justify-between gap-4 py-5 font-mono text-[13px] uppercase text-cream">
          {SEGMENTS.map((segment, index) => (
            <div
              key={segment}
              className={`flex items-center gap-4 ${index === 2 ? "hidden md:flex" : ""}`}
            >
              {index > 0 ? <ArrowRightIcon /> : null}
              <span>{segment}</span>
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
}
