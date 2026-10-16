import { describe, expect, it } from "vitest";
import { buildJsonLd } from "@/lib/seo";
import { fixtureProducts } from "@/lib/fixtures/products";

describe("buildJsonLd", () => {
  it("содержит организацию и список товаров", () => {
    const jsonLd = buildJsonLd(fixtureProducts, "https://kvarta.by") as {
      "@graph": Array<Record<string, unknown>>;
    };
    expect(jsonLd["@graph"]).toHaveLength(2);
    const place = jsonLd["@graph"][0];
    expect(place["@type"]).toBe("CafeOrCoffeeShop");
    expect(place.name).toBe("Кварта");

    const list = jsonLd["@graph"][1] as {
      "@type": string;
      itemListElement: Array<{ item: { name: string; offers: { price: string } } }>;
    };
    expect(list["@type"]).toBe("ItemList");
    expect(list.itemListElement).toHaveLength(fixtureProducts.length);
    expect(list.itemListElement[0].item.name).toBe("Бразилия Серрадо");
    expect(list.itemListElement[0].item.offers.price).toBe("26.00");
  });
});
