import { afterEach, describe, expect, it, vi } from "vitest";
import { fetchLeadOptions } from "@/lib/api/lead-options";
import { fixtureLeadOptions } from "@/lib/fixtures/lead-options";

describe("fetchLeadOptions", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  it("возвращает фикстуры при невалидном JSON", async () => {
    vi.stubEnv("API_INTERNAL_BASE_URL", "http://backend:8000");
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response("{", { status: 200 })),
    );
    await expect(fetchLeadOptions()).resolves.toEqual(fixtureLeadOptions);
  });
});
