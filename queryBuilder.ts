// queryBuilder.ts
import { extractKeywords } from './extractKeywords';

export function buildGroundingQueries(userPrompt: string, contextKeywords: string[]): string[] {
  const base = userPrompt.trim();
  const queries = contextKeywords.map(k => `${base} ${k}`);
  // Fallback‑Query, falls keine Keywords vorhanden
  if (queries.length === 0) queries.push(base);
  return queries;
}
