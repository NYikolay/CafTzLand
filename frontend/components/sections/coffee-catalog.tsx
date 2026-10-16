import { CoffeeItem } from "@/components/sections/coffee-item";
import { Container } from "@/components/ui/container";
import { Eyebrow } from "@/components/ui/eyebrow";
import { getProducts } from "@/lib/api/products";

export async function CoffeeCatalog() {
  const products = await getProducts();
  const items = products.filter((product) => product.kind !== "set");

  return (
    <section id="coffee" aria-labelledby="coffee-heading" className="bg-cream-deep py-14 lg:py-[72px]">
      <Container>
        <div className="grid gap-8 lg:grid-cols-[1fr_auto] lg:items-start lg:gap-[100px]">
          <div className="flex flex-col gap-6">
            <Eyebrow>02 / Ассортимент Кварты</Eyebrow>
            <h2
              id="coffee-heading"
              className="font-serif text-[clamp(36px,5vw,56px)] leading-[1.1] tracking-[-0.032em]"
            >
              Три характера.
              <br />
              Один свежий кофе.
            </h2>
          </div>
          <div className="flex max-w-[420px] flex-col gap-3 lg:text-right">
            <p className="text-sm leading-relaxed">
              От привычного шоколадного до яркого цитрусового. Выберите свой вкус — или оставьте
              выбор нам.
            </p>
            <p className="font-mono text-[11px] uppercase tracking-[1px] text-muted">
              В зерне · 250 и 500 г · цены в BYN
            </p>
          </div>
        </div>

        <div className="mt-10">
          {items.map((product) => (
            <CoffeeItem key={product.id} product={product} />
          ))}
        </div>

        <p className="mt-8 text-sm leading-relaxed text-muted">
          Не знаете, что подойдёт вашей кофеварке? В заявке можно ничего не выбирать — менеджер
          поможет по телефону.
        </p>
      </Container>
    </section>
  );
}
