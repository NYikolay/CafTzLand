import Image from "next/image";
import { SubscribeCtaButton } from "@/components/form/subscribe-cta-button";
import { ButtonLink } from "@/components/ui/button";
import { Container } from "@/components/ui/container";
import { Eyebrow } from "@/components/ui/eyebrow";
import { ArrowUpRightIcon } from "@/components/ui/icons";

export function HeroSection() {
  return (
    <section aria-labelledby="hero-heading" className="py-10 lg:py-16">
      <Container>
        <div className="grid items-start gap-10 lg:grid-cols-[740fr_524fr] lg:gap-12">
          <div className="flex flex-col gap-7">
            <Eyebrow className="text-accent-deep">СВЕЖАЯ ОБЖАРКА. КАЖДЫЙ ЧЕТВЕРГ.</Eyebrow>
            <h1
              id="hero-heading"
              className="font-serif text-[clamp(44px,7vw,84px)] leading-[1.04] tracking-[-0.05em]"
            >
              От обжарки
              <br />
              до вас —
              <br />
              <em className="italic text-accent">1–3 дня.</em>
            </h1>
            <p className="max-w-[520px] text-base leading-relaxed">
              Жарим маленькими партиями по 5 кг. В пятницу развозим по Минску — чтобы дома и в
              офисе был кофе, который не залежался.
            </p>
            <div className="flex flex-col gap-3 sm:flex-row">
              <ButtonLink href="#coffee">
                Выбрать кофе
                <ArrowUpRightIcon />
              </ButtonLink>
              <SubscribeCtaButton variant="outline" label="Или оформить подписку" />
            </div>
          </div>

          <div className="relative">
            <Image
              src="/images/main_preview.webp"
              alt="Обжарщик пересыпает свежеобжаренные зёрна в бумажный пакет в мастерской Кварты"
              width={1572}
              height={1776}
              preload
              fetchPriority="high"
              sizes="(min-width: 1024px) 524px, 100vw"
              className="h-auto w-full object-cover"
            />
            <div className="absolute bottom-4 left-4 flex items-stretch gap-3">
              <div className="bg-cream px-4.5 py-4.5">
                <p className="font-mono text-[10px] uppercase tracking-[1px] text-muted">
                  Партия недели
                </p>
                <p className="mt-2 font-serif text-3xl">5 кг / ЧТ</p>
                <div className={"h-[1px] bg-line my-2"}></div>
                <p className="font-mono text-[10px] text-accent uppercase tracking-[1px]">
                  Обжарено в Кварте
                </p>
              </div>
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}
