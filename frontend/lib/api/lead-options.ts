import { cacheLife } from "next/cache";
import { z } from "zod";
import { apiFetch } from "@/lib/api/config";
import { fixtureLeadOptions } from "@/lib/fixtures/lead-options";
import type { InterestOption } from "@/lib/types";

const interestOptionSchema = z.object({
  value: z.enum(["subscription", "one_time", "question"]),
  label: z.string(),
});

export async function fetchLeadOptions(): Promise<InterestOption[]> {
  const response = await apiFetch("/api/v1/lead/options");
  if (response?.ok) {
    const parsed = z.array(interestOptionSchema).safeParse(await response.json());
    if (parsed.success) return parsed.data;
    console.warn("[api] lead options: невалидный ответ backend, использую фикстуры");
  }
  return fixtureLeadOptions;
}

export async function getLeadOptions(): Promise<InterestOption[]> {
  "use cache";
  cacheLife("days");
  return fetchLeadOptions();
}
