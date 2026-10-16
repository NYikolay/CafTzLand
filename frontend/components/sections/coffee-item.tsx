import { CoffeeOrderButton } from "@/components/form/coffee-order-button";
import { formatByn } from "@/lib/format";
import type { Product } from "@/lib/types";

export function CoffeeItem({ product }: { product: Product }) {
  const [first, second] = product.variants;
  return (
    <article className="grid gap-6 border-t border-line py-8 md:grid-cols-[120px_1fr_auto] md:gap-10">
      <div className="flex h-16 w-16 flex-col items-center justify-center border border-line bg-paper">
        <span className="font-mono text-[9px] uppercase tracking-[1px] text-muted">
          {product.kind === "assorted" ? "Ассорти" : "Зерно"}
        </span>
        <span className="font-serif text-2xl text-accent">{product.code}</span>
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
          <p className="font-mono text-[11px] uppercase tracking-[1px] text-muted">
            {product.brew_method}
          </p>
        ) : null}
      </div>

      <div className="flex items-end justify-between gap-8 md:flex-col md:items-end">
        <div className="flex gap-8">
          {[first, second].filter(Boolean).map((variant) => (
            <div key={variant.id} className="flex flex-col gap-1">
              <span className="font-mono text-[11px] uppercase tracking-[1px] text-muted">
                {variant.packaging_label}
              </span>
              <span className="text-[25px] tracking-[-0.03em]">{formatByn(variant.price)}</span>
            </div>
          ))}
        </div>
        <CoffeeOrderButton productId={product.id}>Хочу этот кофе</CoffeeOrderButton>
      </div>
    </article>
  );
}
