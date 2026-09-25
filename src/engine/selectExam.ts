import type { ExamBreakdownItem, OrderMode, Question, Subject } from '../types';
import { SUBJECT_CONFIG } from '../data/subjectConfig';

/** Groups questions sharing a groupId into indivisible units; standalone
 * questions become their own single-item unit. Units are ordered by year,
 * then by their first question's qNo, and a unit's internal order never
 * changes. */
function buildUnits(questions: Question[]): Question[][] {
  const groupMap = new Map<string, Question[]>();
  const units: Question[][] = [];

  for (const q of questions) {
    if (q.groupId) {
      const arr = groupMap.get(q.groupId) ?? [];
      arr.push(q);
      groupMap.set(q.groupId, arr);
    } else {
      units.push([q]);
    }
  }
  for (const arr of groupMap.values()) {
    arr.sort((a, b) => a.qNo - b.qNo);
    units.push(arr);
  }
  units.sort((a, b) => a[0].year - b[0].year || a[0].qNo - b[0].qNo);
  return units;
}

function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export interface SelectExamParams {
  allQuestions: Question[];
  subjects: Subject[];
  years: number[];
  /** 份量: 1 全卷, 0.5 半卷, 0.25 四分之一卷 */
  fraction: number;
  orderMode: OrderMode;
}

export interface SelectExamResult {
  questionIds: string[];
  breakdown: ExamBreakdownItem[];
  timeBudgetSec: number;
}

/** Each chosen subject gets `fraction` of one real paper: that many of a
 * paper's questions (a paper's length is averaged over the chosen years, as
 * papers of different years differ a little) and that share of the subject's
 * real exam time. 全卷 of a single year is exactly that year's paper.
 * Selection never splits a shared-passage question group, so a subject may
 * get a question or two more than the exact share. */
export function selectExam(params: SelectExamParams): SelectExamResult {
  const questionIds: string[] = [];
  const breakdown: ExamBreakdownItem[] = [];

  for (const subject of params.subjects) {
    const pool = params.allQuestions.filter(
      (q) => q.subject === subject && params.years.includes(q.year)
    );
    if (pool.length === 0) continue;
    const perYear = new Map<number, number>();
    pool.forEach((q) => perYear.set(q.year, (perYear.get(q.year) ?? 0) + 1));
    const paperLength = pool.length / perYear.size;
    const target = Math.max(1, Math.round(paperLength * params.fraction));

    let units = buildUnits(pool);
    if (params.orderMode === 'shuffled') units = shuffle(units);

    const picked: Question[] = [];
    for (const unit of units) {
      if (picked.length >= target) break;
      picked.push(...unit);
    }

    const sec = Math.round(SUBJECT_CONFIG[subject].officialMinutes * 60 * params.fraction);
    breakdown.push({ subject, count: picked.length, sec });
    questionIds.push(...picked.map((q) => q.id));
  }

  const timeBudgetSec = breakdown.reduce((sum, b) => sum + b.sec, 0);
  return { questionIds, breakdown, timeBudgetSec };
}
