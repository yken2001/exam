import type { ReactNode } from 'react';
import type { Question } from '../types';
import ExamImage from './ExamImage';

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

/** stem, figure and options of one text question. A 英聽 item has no
 * printed stem (it is heard); a picture item's options are the drawn
 * pictures (A)(B)(C) in its figure, so its option texts are empty. */
export function TextStem({ q, number }: { q: Question; number: number }) {
  const t = q.text!;
  const heard = q.subject === '英聽';
  const stem = t.stem
    ? t.stem.split('\n').map((l, i) => (
        <span key={i}>
          {i > 0 && <br />}
          {l}
        </span>
      ))
    : heard
      ? '請聽錄音作答'
      : `文章中的空格 (${number})`;
  return (
    <div className="text-stem">
      <div className="text-stem-q">
        <b>{number}.</b> {stem}
      </div>
      {t.figure && <ExamImage className="q-image text-figure" src={t.figure} alt={`第 ${number} 題附圖`} />}
      {t.options.some((o) => o) && (
        <div className="text-options">
          {t.options.map((o, i) => (
            <div key={i}>
              ({String.fromCharCode(65 + i)}) {o}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
