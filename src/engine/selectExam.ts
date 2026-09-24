import type { ExamBreakdownItem, OrderMode, Question, Subject } from '../types';
import { SUBJECT_CONFIG } from '../data/subjectConfig';

/** Groups questions sharing a groupId into indivisible units; standalone
 * questions become their own single-item unit. Units are ordered by their
 * first question's qNo, and a unit's internal order never changes. */
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
  totalMinutes: number;
  orderMode: OrderMode;
}

export interface SelectExamResult {
  questionIds: string[];
  breakdown: ExamBreakdownItem[];
  timeBudgetSec: number;
}

/** Time drives question count, not the other way round: a fixed total time
 * budget (in minutes, chosen directly by the user) is split evenly across
 * the chosen subjects, then each subject's share of time is converted into
 * a question count via that subject's real exam pace, capped at its real
 * exam length. Selection never splits a shared-passage question group. */
export function selectExam(params: SelectExamParams): SelectExamResult {
  const totalBudgetSec = params.totalMinutes * 60;
  const perSubjectBudget = params.subjects.length > 0 ? totalBudgetSec / params.subjects.length : 0;

  const questionIds: string[] = [];
  const breakdown: ExamBreakdownItem[] = [];

  for (const subject of params.subjects) {
    const cfg = SUBJECT_CONFIG[subject];
    const target = Math.min(cfg.realCount, Math.max(1, Math.floor(perSubjectBudget / cfg.secPerQuestion)));

    const pool = params.allQuestions.filter(
      (q) => q.subject === subject && params.years.includes(q.year)
    );
    let units = buildUnits(pool);
    if (params.orderMode === 'shuffled') units = shuffle(units);

    const picked: Question[] = [];
    for (const unit of units) {
      if (picked.length >= target) break;
      picked.push(...unit);
    }

    breakdown.push({ subject, count: picked.length, sec: picked.length * cfg.secPerQuestion });
    questionIds.push(...picked.map((q) => q.id));
  }

  const actualSec = breakdown.reduce((sum, b) => sum + b.sec, 0);
  return { questionIds, breakdown, timeBudgetSec: actualSec };
}
