import { afterEach, describe, expect, it, vi } from "vitest";
import { fetchProducts } from "@/lib/api/products";
import { fixtureProducts } from "@/lib/fixtures/products";

describe("fetchProducts", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  it("возвращает фикстуры, когда backend не задан", async () => {
    vi.stubEnv("API_INTERNAL_BASE_URL", "");
    await expect(fetchProducts()).resolves.toEqual(fixtureProducts);
  });

  it("возвращает фикстуры при сетевой ошибке", async () => {
    vi.stubEnv("API_INTERNAL_BASE_URL", "http://backend:8000");
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("network")));
    await expect(fetchProducts()).resolves.toEqual(fixtureProducts);
  });

  it("возвращает фикстуры при невалидном ответе", async () => {
    vi.stubEnv("API_INTERNAL_BASE_URL", "http://backend:8000");
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(Response.json([{ oops: true }], { status: 200 })),
    );
    await expect(fetchProducts()).resolves.toEqual(fixtureProducts);
  });

  it("парсит валидный ответ backend", async () => {
    vi.stubEnv("API_INTERNAL_BASE_URL", "http://backend:8000");
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(Response.json([fixtureProducts[0]], { status: 200 })),
    );
    await expect(fetchProducts()).resolves.toEqual([fixtureProducts[0]]);
  });

  it("возвращает фикстуры при невалидном JSON", async () => {
    vi.stubEnv("API_INTERNAL_BASE_URL", "http://backend:8000");
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response("{", { status: 200 })),
    );
    await expect(fetchProducts()).resolves.toEqual(fixtureProducts);
  });
});
