/** Years 901, 902… are AI-made practice sets, shown as AI-1, AI-2…; real
 * papers keep their 民國 year. */
export const AI_YEAR_BASE = 900;

export function yearLabel(year: number): string {
  return year > AI_YEAR_BASE ? `AI-${year - AI_YEAR_BASE}` : String(year);
}

export function isAiYear(year: number): boolean {
  return year > AI_YEAR_BASE;
}
