export function getApiBaseUrl(): string | null {
  const base = process.env.API_INTERNAL_BASE_URL;
  return base ? base.replace(/\/$/, "") : null;
}

export function hasBackend(): boolean {
  return getApiBaseUrl() !== null;
}

export async function apiFetch(
  path: string,
  init?: RequestInit,
): Promise<Response | null> {
  const base = getApiBaseUrl();
  if (!base) return null;
  try {
    return await fetch(`${base}${path}`, {
      ...init,
      headers: { "Content-Type": "application/json", ...init?.headers },
      signal: AbortSignal.timeout(5000),
      cache: "no-store",
    });
  } catch (error) {
    console.warn(`[api] fetch ${path} failed:`, error);
    return null;
  }
}
