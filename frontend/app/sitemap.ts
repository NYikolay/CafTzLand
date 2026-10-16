import type { MetadataRoute } from "next";
import { cacheLife } from "next/cache";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  "use cache";
  cacheLife("days");

  const base = process.env.NEXT_PUBLIC_SITE_URL ?? "https://tzkvvit.site";
  return [
    {
      url: base,
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 1,
    },
  ];
}
