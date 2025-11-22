// extractKeywords.ts
import nlp from 'compromise';

export function extractKeywords(text: string): string[] {
  const doc = nlp(text);
  // Nomen‑Phrasen und benannte Entitäten
  const nouns = doc.nouns().out('array');
  const entities = doc.topics().out('array');
  // Duplikate entfernen, nach Häufigkeit sortieren
  const all = [...new Set([...nouns, ...entities])];
  return all.slice(0, 10); // max. 10 Schlüsselwörter
}
