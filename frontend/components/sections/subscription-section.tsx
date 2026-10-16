import Image from "next/image";
import { SubscribeCtaButton } from "@/components/form/subscribe-cta-button";
import { Container } from "@/components/ui/container";
import { Eyebrow } from "@/components/ui/eyebrow";

export function SubscriptionSection() {
  return (
    <section id="subscription" aria-labelledby="subscription-heading" className="bg-accent py-14 lg:py-[72px]">
      <Container>
        <div className="grid items-start gap-10 lg:grid-cols-2 lg:gap-[72px]">
          <div className="flex flex-col gap-7 lg:pt-3">
            <Eyebrow className="text-paper">03 / Подписка Кварты</Eyebrow>
            <h2
              id="subscription-heading"
              className="font-serif text-[clamp(36px,5vw,56px)] leading-[1.1] tracking-[-0.032em] text-paper"
            >
              Пусть кофе <em className="italic">не кончается.</em>
            </h2>
            <p className="max-w-[520px] text-base leading-relaxed text-paper">
              Один раз договариваемся о кофе и количестве. Дальше в неделе появляется приятная
              постоянная — свежая обжарка для дома или офиса.
            </p>
            <p className="max-w-[520px] text-base leading-relaxed text-paper">
              Оставьте заявку. Менеджер перезвонит, поможет выбрать набор и согласует
              регулярность доставки.
            </p>
            <SubscribeCtaButton variant="cream" />
          </div>

          <div className="relative">
            <Image
              src="/images/cafe_packets.webp"
              alt="Крафтовые пакеты со свежеобжаренным кофе и чашка кофе на столе у окна"
              width={1860}
              height={1410}
              sizes="(min-width: 1024px) 620px, 100vw"
              className="h-auto w-full object-cover"
            />
            <div className="absolute bottom-6 left-6 w-[260px] bg-cream p-5">
              <div className="flex items-center justify-between border-b border-line pb-2 font-mono text-[10px] uppercase tracking-[1px] text-muted">
                <span>Набор Кварты</span>
                <span>Кварта</span>
              </div>
              <p className="mt-3 font-serif text-2xl">Ваш выбор</p>
              <p className="mt-2 font-mono text-[10px] uppercase tracking-[1px] text-muted">
                2 × 250 г раз в месяц
              </p>
              <p className="mt-3 font-serif text-[34px] leading-none">54 BYN / мес</p>
              <p className="mt-2 text-[11px] leading-snug text-muted">
                За набор. Стоимость доставки - бесплатно.
              </p>
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}
