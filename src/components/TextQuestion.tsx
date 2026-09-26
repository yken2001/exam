import type { ReactNode } from 'react';
import type { Question } from '../types';

/** Passage of a text 題組: paragraphs, "| a | b |" rows as a table, and
 * cloze blanks "__35__" shown with the number the blank has in this exam
 * (numbering follows the exam, which may differ from the set's qNo). */
export function Passage({ text, numberOf }: { text: string; numberOf: (qNo: number) => number | undefined }) {
  const blocks: ReactNode[] = [];
  let table: string[][] = [];
  const flush = () => {
    if (!table.length) return;
    const [head, ...body] = table;
    blocks.push(
      <table className="passage-table" key={`t${blocks.length}`}>
        <thead>
          <tr>{head.map((c, i) => <th key={i}>{c}</th>)}</tr>
        </thead>
        <tbody>
          {body.map((r, i) => (
            <tr key={i}>{r.map((c, j) => <td key={j}>{c}</td>)}</tr>
          ))}
        </tbody>
      </table>
    );
    table = [];
  };
  for (const line of text.split('\n')) {
    if (line.startsWith('|')) {
      table.push(line.split('|').slice(1, -1).map((c) => c.trim()));
      continue;
    }
    flush();
    const parts = line.split(/__(\d+)__/);
    blocks.push(
      <p key={`p${blocks.length}`}>
        {parts.map((part, i) =>
          i % 2 ? (
            <span className="cloze-blank" key={i}>
              {' '}({numberOf(Number(part)) ?? part}){' '}
            </span>
          ) : (
            part
          )
        )}
      </p>
    );
  }
  flush();
  return <div className="passage">{blocks}</div>;
}

/** stem and options of one text question */
export function TextStem({ q, number }: { q: Question; number: number }) {
  const t = q.text!;
  return (
    <div className="text-stem">
      <div className="text-stem-q">
        <b>{number}.</b>{' '}
        {t.stem
          ? t.stem.split('\n').map((l, i) => (
              <span key={i}>
                {i > 0 && <br />}
                {l}
              </span>
            ))
          : `文章中的空格 (${number})`}
      </div>
      <div className="text-options">
        {t.options.map((o, i) => (
          <div key={i}>
            ({String.fromCharCode(65 + i)}) {o}
          </div>
        ))}
      </div>
    </div>
  );
}
