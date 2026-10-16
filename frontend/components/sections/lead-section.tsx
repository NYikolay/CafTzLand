import { LeadForm } from "@/components/form/lead-form";
import { SiteFooter } from "@/components/layout/site-footer";
import { Container } from "@/components/ui/container";
import { Eyebrow } from "@/components/ui/eyebrow";
import { getLeadOptions } from "@/lib/api/lead-options";
import { getProducts } from "@/lib/api/products";

export async function LeadSection() {
  const [products, options] = await Promise.all([getProducts(), getLeadOptions()]);

  return (
    <section id="zayavka" aria-labelledby="zayavka-heading" className="flex-1 bg-ink pt-14 lg:pt-[72px]">
      <Container>
        <div className="grid gap-12 pb-16 lg:grid-cols-[1fr_minmax(420px,583px)] lg:gap-[100px]">
          <div className="flex flex-col gap-6">
            <Eyebrow className="text-cream">05 / Оставьте заявку</Eyebrow>
            <h2
              id="zayavka-heading"
              className="font-serif text-[clamp(36px,5vw,62px)] leading-[1.08] tracking-[-0.032em] text-cream"
            >
              На следующий
              <br />
              четверг —
              <br />
              ваш кофе.
            </h2>
            <p className="max-w-130 text-base leading-relaxed text-cream/80">
              Оставьте имя и телефон. Заказ оформим во время звонка.
            </p>
            <div className="mt-4 flex flex-col gap-2">
              <p className="font-mono text-[11px] uppercase tracking-[1px] text-cream/60">
                Или заглядывайте в Кварту
              </p>
              <p className="text-base text-cream">Минск, ул. Короля, 9</p>
              <p className="text-sm text-cream/70">пн–пт 8:00–20:00 сб–вс 10:00–18:00</p>
            </div>
          </div>

          <LeadForm products={products} options={options} />
        </div>
      </Container>
      <SiteFooter />
    </section>
  );
}
