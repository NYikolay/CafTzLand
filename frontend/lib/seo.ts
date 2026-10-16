import type { Product } from "@/lib/types";

export function buildJsonLd(products: Product[], siteUrl: string) {
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "CafeOrCoffeeShop",
        name: "Кварта",
        url: siteUrl,
        address: {
          "@type": "PostalAddress",
          addressLocality: "Минск",
          streetAddress: "ул. Короля, 9",
          addressCountry: "BY",
        },
        openingHoursSpecification: [
          {
            "@type": "OpeningHoursSpecification",
            dayOfWeek: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            opens: "08:00",
            closes: "20:00",
          },
          {
            "@type": "OpeningHoursSpecification",
            dayOfWeek: ["Saturday", "Sunday"],
            opens: "10:00",
            closes: "18:00",
          },
        ],
      },
      {
        "@type": "ItemList",
        itemListElement: products.map((product, index) => ({
          "@type": "ListItem",
          position: index + 1,
          item: {
            "@type": "Product",
            name: product.name,
            description: product.description ?? undefined,
            offers: product.variants[0]
              ? {
                  "@type": "Offer",
                  price: product.variants[0].price,
                  priceCurrency: "BYN",
                  availability: "https://schema.org/InStock",
                }
              : undefined,
          },
        })),
      },
    ],
  };
}
