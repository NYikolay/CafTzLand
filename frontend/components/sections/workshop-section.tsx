import { Container } from "@/components/ui/container";
import { Eyebrow } from "@/components/ui/eyebrow";

const CALENDAR = [
  { day: "ЧТ", title: "Обжарка", text: "По 5 кг за раз. Небольшая партия — внимание к каждой обжарке." },
  { day: "ПТ", title: "Развоз", text: "Собираем заказы и отправляем свежий кофе по Минску." },
  { day: "1–3", title: "Дней до вашей кухни", text: "Зерно приходит к вам на 1–3 день после обжарки." },
] as const;

export function WorkshopSection() {
  return (
    <section aria-labelledby="workshop-heading" className="py-14 lg:py-20">
      <Container>
        <div className="grid gap-10 lg:grid-cols-2 lg:gap-20">
          <div className="flex flex-col gap-8">
            <Eyebrow className="text-accent-deep">01 / Маленькая мастерская Кварты</Eyebrow>
            <h2
              id="workshop-heading"
              className="font-serif text-[clamp(34px,4.6vw,53px)] leading-[1.13] tracking-[-0.03em]"
            >
              Знаем кофе
              <br />
              с обеих сторон
              <br />
              стойки.
            </h2>
          </div>
          <div className="flex flex-col gap-6 self-end text-base leading-relaxed">
            <p>
              Мы — Аня и Дмитрий. Раньше работали бариста, а с 2019 года обжариваем кофе в
              мастерской Кварта в Минске.
            </p>
            <p>
              После обжарки кофе постепенно теряет аромат. Поэтому мы не жарим впрок: у нас есть
              свой четверг, небольшие партии и короткий путь до вашей чашки.
            </p>
            <p className="font-serif text-2xl italic text-accent">Не на полку. К вашему утру.</p>
          </div>
        </div>

        <div className="mt-12 grid border-t border-line md:grid-cols-3 md:divide-x md:divide-line">
          {CALENDAR.map((item) => (
            <div key={item.day} className="flex flex-col gap-3 border-b border-line py-6 md:border-b-0 md:px-8 md:first:pl-0">
              <p className="font-serif text-[clamp(40px,4vw,53px)] leading-none">{item.day}</p>
              <p className="font-serif text-2xl">{item.title}</p>
              <p className="text-sm leading-relaxed text-muted">{item.text}</p>
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
}
