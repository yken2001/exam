import type { Question, Subject } from '../types';
import { SUBJECTS } from '../data/subjectConfig';
import { LEVELS, type YearLevels } from '../data/levels';
import { isAiYear } from '../utils/yearLabel';

/** 會考等級, low -> high */
const ORDER = ['C', 'B', 'B+', 'B++', 'A', 'A+', 'A++'];

export type GradeKind = 'official' | 'estimate' | 'none';

export interface SubjectGrade {
  name: string;
  correct: number;
  total: number;
  kind: GradeKind;
  /** 'A++' … 'C' */
  level?: string;
  note?: string;
}

export function levelText(level: string): string {
  const band = level.startsWith('A') ? '精熟' : level.startsWith('B') ? '基礎' : '待加強';
  return level === 'C' ? band : `${band}（${level}）`;
}

const cache = new Map<string, string[]>();
const split = (s: string) => s.split(' ');

/** level of every possible number of correct answers, for one subject-year */
function table(year: number, subject: Subject): string[] | undefined {
  const lv: YearLevels | undefined = LEVELS[year];
  if (!lv) return undefined;
  const id = `${year}-${subject}`;
  if (!cache.has(id)) {
    let t: string[];
    if (subject === '英文') t = split(lv.readingOnly);         // 表四: 只考閱讀
    else if (subject === '英聽') t = split(lv.listening);      // 基礎 / 待加強
    else if (subject === '數學') {
      // 表三 needs the 非選擇題 級分 too, which the bank does not have: take
      // it at the same rate as the 選擇題 (k of 25 right -> k/25 of 6 級分)
      const full = lv.full['數學'];
      t = lv.math.map((row, k) => split(row)[Math.round((k / full) * (split(row).length - 1))]);
    } else t = split(lv[subject]);
    cache.set(id, t);
  }
  return cache.get(id);
}

/** lowest number correct reaching `level` in table t, as a share of 滿分 */
function thresholdRatio(t: string[], level: string): number {
  const k = t.findIndex((l) => ORDER.indexOf(l) >= ORDER.indexOf(level));
  return k < 0 ? Infinity : k / (t.length - 1);
}

/** estimate for a partial or mixed-year set: the level whose threshold (as a
 * share of 滿分, averaged over the years weighted by their question counts)
 * the share answered correctly reaches */
function estimate(ratio: number, parts: { t: string[]; weight: number }[]): string {
  const levels = [...new Set(parts.flatMap((p) => p.t))].sort((a, b) => ORDER.indexOf(b) - ORDER.indexOf(a));
  const w = parts.reduce((s, p) => s + p.weight, 0);
  for (const level of levels) {
    const th = parts.reduce((s, p) => s + p.weight * thresholdRatio(p.t, level), 0) / w;
    if (ratio >= th - 1e-9) return level;
  }
  return levels[levels.length - 1];
}

interface SubjectRun {
  subject: Subject;
  qs: Question[];
  correct: number;
  years: Map<number, number>;
  full?: boolean;
}

function gradeSubject(r: SubjectRun): SubjectGrade {
  const n = r.qs.length;
  const base = { name: r.subject, correct: r.correct, total: n };
  const parts: { t: string[]; weight: number; year: number }[] = [];
  for (const [year, count] of r.years) {
    const t = table(year, r.subject);
    if (!t) return { ...base, kind: 'none', note: isAiYear(year) ? 'AI 題沒有官方等級，只看正確率' : `${year} 年沒有官方等級對照表` };
    parts.push({ t, weight: count, year });
  }
  const paperLength = parts.reduce((s, p) => s + p.weight * (p.t.length - 1), 0) / n;
  const single = parts.length === 1 ? parts[0] : undefined;
  const mathNote = r.subject === '數學' ? '非選擇題以選擇題答對率估計' : undefined;
  if (single && n === single.t.length - 1) {
    r.full = true;
    const level = single.t[r.correct];
    if (r.subject === '數學') return { ...base, kind: 'estimate', level, note: mathNote };
    const note = r.subject === '英文' ? '依官方「只考閱讀」對照表' : undefined;
    return { ...base, kind: 'official', level, note };
  }
  if (n < paperLength / 2) return { ...base, kind: 'none', note: '題數不到半份卷，只看正確率' };
  return { ...base, kind: 'estimate', level: estimate(r.correct / n, parts), note: mathNote };
}

/** one grade per subject in the exam (in the usual subject order), plus 英語
 * 整體 when both 英文 and 英聽 were answered */
export function gradeAttempt(questions: Question[], answers: Record<string, string | undefined>): SubjectGrade[] {
  const runs = new Map<Subject, SubjectRun>();
  for (const q of questions) {
    const r: SubjectRun = runs.get(q.subject) ?? { subject: q.subject, qs: [], correct: 0, years: new Map() };
    r.qs.push(q);
    if (answers[q.id] === q.correctAnswer) r.correct += 1;
    r.years.set(q.year, (r.years.get(q.year) ?? 0) + 1);
    runs.set(q.subject, r);
  }
  const out: SubjectGrade[] = [];
  for (const s of SUBJECTS) {
    const r = runs.get(s);
    if (r) out.push(gradeSubject(r));
  }

  // 英語整體 (表二): 閱讀 x 聽力 答對題數
  const read = runs.get('英文');
  const listen = runs.get('英聽');
  const gRead = out.find((g) => g.name === '英文');
  const gListen = out.find((g) => g.name === '英聽');
  if (read && listen && gRead?.kind !== 'none' && gListen?.kind !== 'none') {
    const year = [...read.years.entries()].sort((a, b) => b[1] - a[1])[0][0];
    const lv = LEVELS[year];
    const sameYear = read.full && listen.full && listen.years.has(year);
    const kR = sameYear ? read.correct : Math.round((read.correct / read.qs.length) * lv.full['閱讀']);
    const kL = sameYear ? listen.correct : Math.round((listen.correct / listen.qs.length) * lv.full['聽力']);
    out.push({
      name: '英語整體',
      correct: read.correct + listen.correct,
      total: read.qs.length + listen.qs.length,
      kind: sameYear ? 'official' : 'estimate',
      level: split(lv.english[kR])[kL],
      note: '閱讀＋聽力（官方對照表）',
    });
  }
  return out;
}
