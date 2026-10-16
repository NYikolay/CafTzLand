import { CoffeeOrderButton } from "@/components/form/coffee-order-button";
import { formatByn } from "@/lib/format";
import type { Product } from "@/lib/types";

export function CoffeeItem({ product }: { product: Product }) {
  const [first, second] = product.variants;
  return (
    <article className="grid gap-6 border-t border-line py-8 md:grid-cols-[66px_1fr_auto] md:gap-x-[66px]">
      <div className="flex items-center gap-3 md:block">
        <div className="flex h-[78px] w-[66px] flex-col items-center border border-line bg-cream pt-[9px]">
          <span className="font-mono text-[8px] uppercase tracking-[1px] text-muted">
            {product.kind === "assorted" ? "Ассорти" : "Зерно"}
          </span>
          <span className="mt-2 font-mono text-[25px] leading-none font-medium text-accent">
            {product.code}
          </span>
          <span aria-hidden className="mt-2 h-[3px] w-12 bg-accent" />
        </div>
        {product.brew_method ? (
          <p className="font-mono text-[10px] uppercase tracking-[1px] text-muted md:hidden">
            {product.brew_method}
          </p>
        ) : null}
      </div>

      <div className="flex flex-col gap-2">
        <h3 className="font-serif text-[clamp(26px,2.8vw,34px)] leading-[1.15] tracking-[-0.02em]">
          {product.name}
        </h3>
        {product.tasting_notes ? (
          <p className="text-sm font-medium text-accent">{product.tasting_notes}</p>
        ) : null}
        {product.description ? (
          <p className="max-w-[520px] text-sm leading-relaxed text-muted">
            {product.description}
          </p>
        ) : null}
        {product.brew_method ? (
          <p className="hidden font-mono text-[11px] uppercase tracking-[1px] text-muted md:block">
            {product.brew_method}
          </p>
        ) : null}
      </div>

      <div className="flex flex-col items-start gap-[18px]">
        <div className="flex gap-9 md:gap-7">
          {[first, second].filter(Boolean).map((variant) => (
            <div key={variant.id} className="flex flex-col gap-2">
              <span className="font-mono text-[11px] uppercase tracking-[1px] text-muted">
                {variant.packaging_label}
              </span>
              <span className="text-[23px] tracking-[-0.03em] md:text-[25px]">
                {formatByn(variant.price)}
              </span>
            </div>
          ))}
        </div>
        <CoffeeOrderButton productId={product.id}>Хочу этот кофе</CoffeeOrderButton>
      </div>
    </article>
  );
}
