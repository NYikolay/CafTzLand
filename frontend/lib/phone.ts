export const BY_PHONE_PREFIX = "+375";
export const BY_PHONE_MASK = "+375 (__) ___-__-__";

const NATIONAL_DIGITS = 9;

export function digitsOnly(value: string): string {
  return value.replace(/\D/g, "");
}

function nationalDigits(value: string): string {
  let digits = digitsOnly(value);
  if (digits.startsWith("375")) digits = digits.slice(3);
  else if (digits.startsWith("80")) digits = digits.slice(2);
  else if (digits.startsWith("0")) digits = digits.slice(1);
  return digits;
}

export function normalizeByPhone(value: string): string | null {
  const digits = nationalDigits(value);
  return digits.length === NATIONAL_DIGITS
    ? `${BY_PHONE_PREFIX}${digits}`
    : null;
}

export function isValidByPhone(value: string): boolean {
  return normalizeByPhone(value) !== null;
}

export function formatByPhone(value: string): string {
  const digits = nationalDigits(value);
  let out = BY_PHONE_PREFIX;
  if (digits.length > 0) out += ` (${digits.slice(0, 2)}`;
  if (digits.length >= 2) out += ")";
  if (digits.length > 2) out += ` ${digits.slice(2, 5)}`;
  if (digits.length > 5) out += `-${digits.slice(5, 7)}`;
  if (digits.length > 7) out += `-${digits.slice(7, 9)}`;
  return out;
}
