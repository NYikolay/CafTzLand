const UTM_KEYS = [
  "utm_source",
  "utm_medium",
  "utm_campaign",
  "utm_content",
  "utm_term",
] as const;

export function collectLeadSource(): Record<string, string> {
  const params = new URLSearchParams(window.location.search);
  const source: Record<string, string> = {};
  for (const key of UTM_KEYS) {
    const value = params.get(key);
    if (value) source[key] = value;
  }
  if (document.referrer) source.referrer = document.referrer;
  source.page_url = window.location.href;
  return source;
}
