import { getProducts } from "@/lib/api/products";
import { buildJsonLd } from "@/lib/seo";

export async function StructuredData() {
  const products = await getProducts();
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://tzkvvit.site";
  const jsonLd = buildJsonLd(products, siteUrl);

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(jsonLd).replace(/</g, "\\u003c"),
      }}
    />
  );
}
