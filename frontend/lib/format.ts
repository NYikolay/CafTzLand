export function formatByn(value: string): string {
  const numeric = Number.parseFloat(value);
  if (Number.isNaN(numeric)) return `${value} BYN`;
  const rounded = Math.round(numeric * 100) / 100;
  const text = Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(2);
  return `${text} BYN`;
}
