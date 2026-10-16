import { cacheLife, cacheTag } from "next/cache";
import { z } from "zod";
import { apiFetch } from "@/lib/api/config";
import { fixtureProducts } from "@/lib/fixtures/products";
import type { Product } from "@/lib/types";

const productVariantSchema = z.object({
  id: z.number(),
  packaging_label: z.string(),
  price: z.string(),
  weight_grams: z.number().nullable(),
  units: z.number().nullable(),
});

const productSchema = z.object({
  id: z.number(),
  code: z.string(),
  name: z.string(),
  kind: z.enum(["beans", "assorted", "set"]),
  tasting_notes: z.string().nullable(),
  description: z.string().nullable(),
  brew_method: z.string().nullable(),
  variants: z.array(productVariantSchema),
});

export async function fetchProducts(): Promise<Product[]> {
  const response = await apiFetch("/api/v1/products");
  if (response?.ok) {
    const parsed = z.array(productSchema).safeParse(await response.json());
    if (parsed.success) return parsed.data;
    console.warn("[api] products: невалидный ответ backend, использую фикстуры");
  } else if (response) {
    console.warn(`[api] products: backend ответил ${response.status}, использую фикстуры`);
  }
  return fixtureProducts;
}

export async function getProducts(): Promise<Product[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("products");
  return fetchProducts();
}
