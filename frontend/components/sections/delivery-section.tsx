import { Container } from "@/components/ui/container";
import { Eyebrow } from "@/components/ui/eyebrow";

const OPTIONS = [
  {
    label: "01 / По Минску",
    title: "Каждую пятницу",
    text: "От 50 BYN — бесплатно. Если заказ меньше, стоимость доставки уточнит менеджер при звонке.",
  },
  {
    label: "02 / Из мастерской Кварты",
    title: "ул. Короля, 9",
    text: "Минск. Заходите за своим кофе. пн–пт 8:00–20:00 сб–вс 10:00–18:00",
  },
] as const;

export function DeliverySection() {
  return (
    <section id="delivery" aria-labelledby="delivery-heading" className="py-14 lg:py-[72px]">
      <Container>
        <Eyebrow>04 / Как получить кофе</Eyebrow>
        <h2
          id="delivery-heading"
          className="mt-5 max-w-[720px] font-serif text-[clamp(34px,4.6vw,53px)] leading-[1.13] tracking-[-0.03em]"
        >
          В пятницу — к вам. В остальные дни — к нам.
        </h2>
        <div className="mt-10 grid gap-8 md:grid-cols-2 md:divide-x md:divide-line">
          {OPTIONS.map((option) => (
            <div key={option.label} className="flex flex-col gap-3 md:px-8 md:first:pl-0">
              <p className="font-mono text-[11px] uppercase tracking-[1px] text-accent">
                {option.label}
              </p>
              <p className="font-serif text-2xl">{option.title}</p>
              <p className="max-w-[420px] text-sm leading-relaxed text-muted">{option.text}</p>
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
}
