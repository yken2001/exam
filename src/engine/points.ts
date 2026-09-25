import type { AttemptRecord, Question } from '../types';

/** Points reward learning, not repeating: a question pays in full the first
 * time, again when a mistake is corrected on a later day, and once more when
 * it becomes 精熟 (right on two different days); answering what is already
 * known pays almost nothing. First version -- the numbers are meant to be
 * tuned. */
export const RULES = {
  newCorrect: 10,
  newWrong: 2,
  correctedLaterDay: 15,
  correctedSameDay: 5,
  mastered: 10,
  repeatCorrect: 1,
  completion: 20,          // answered at least 80% of the paper
  completionShare: 0.8,
  bonus70: 1.2,            // multiplies the question points of the paper
  bonus90: 1.5,
  weeklyGoal: 50,          // for the 3rd finished paper of a week
  weeklyPapers: 3,
};

export interface AttemptPoints {
  total: number;
  lines: { label: string; points: number }[];
}

export interface PointsSummary {
  total: number;
  level: number;
  levelStart: number;     // points at which the current level began
  levelNext: number;      // points needed for the next level
  seen: number;           // distinct questions ever answered
  mastered: number;
  perAttempt: Map<string, AttemptPoints>;
}

/** points to go from level n to n+1: 100, 150, 200, … */
export function levelCost(n: number): number {
  return 100 + 50 * (n - 1);
}

const dayKey = (t: number) => {
  const d = new Date(t);
  return `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`;
};

/** Monday-based week of a timestamp */
const weekKey = (t: number) => {
  const d = new Date(t);
  d.setHours(0, 0, 0, 0);
  d.setDate(d.getDate() - ((d.getDay() + 6) % 7));
  return d.getTime();
};

interface QState {
  lastCorrect: boolean;
  lastDay: string;
  correctDays: Set<string>;
  mastered: boolean;
}

export function computePoints(attempts: AttemptRecord[], byId: Map<string, Question>): PointsSummary {
  const finished = attempts.filter((a) => a.finishedAt).sort((a, b) => a.finishedAt! - b.finishedAt!);
  const state = new Map<string, QState>();
  const perAttempt = new Map<string, AttemptPoints>();
  const papersPerWeek = new Map<number, number>();
  let total = 0;

  for (const a of finished) {
    const day = dayKey(a.finishedAt!);
    const count = { newCorrect: 0, newWrong: 0, corrLater: 0, corrSame: 0, mastered: 0, repeat: 0 };
    let answered = 0;
    let right = 0;
    const known = a.answers.filter((x) => byId.has(x.questionId));
    for (const { questionId, selected } of known) {
      if (!selected) continue;
      answered += 1;
      const ok = selected === byId.get(questionId)!.correctAnswer;
      if (ok) right += 1;
      const s = state.get(questionId);
      if (!s) {
        ok ? count.newCorrect++ : count.newWrong++;
        state.set(questionId, { lastCorrect: ok, lastDay: day, correctDays: new Set(ok ? [day] : []), mastered: false });
        continue;
      }
      if (ok && !s.lastCorrect) s.lastDay === day ? count.corrSame++ : count.corrLater++;
      else if (ok) count.repeat++;
      if (ok) s.correctDays.add(day);
      if (ok && !s.mastered && s.correctDays.size >= 2) {
        s.mastered = true;
        count.mastered++;
      }
      s.lastCorrect = ok;
      s.lastDay = day;
    }

    const lines: { label: string; points: number }[] = [];
    const add = (label: string, n: number, each: number) => n && lines.push({ label: `${label} ${n} 題`, points: n * each });
    add('新題答對', count.newCorrect, RULES.newCorrect);
    add('新題嘗試', count.newWrong, RULES.newWrong);
    add('錯題訂正', count.corrLater, RULES.correctedLaterDay);
    add('當天訂正', count.corrSame, RULES.correctedSameDay);
    add('達成精熟', count.mastered, RULES.mastered);
    add('複習答對', count.repeat, RULES.repeatCorrect);
    const questionPoints = lines.reduce((s, l) => s + l.points, 0);
    const rate = known.length ? right / known.length : 0;
    const mult = rate >= 0.9 ? RULES.bonus90 : rate >= 0.7 ? RULES.bonus70 : 1;
    if (mult > 1) lines.push({ label: `正確率 ${Math.round(rate * 100)}% 加成 ×${mult}`, points: Math.round(questionPoints * (mult - 1)) });
    if (known.length && answered / known.length >= RULES.completionShare) {
      lines.push({ label: '完成一份卷', points: RULES.completion });
      const w = weekKey(a.finishedAt!);
      const n = (papersPerWeek.get(w) ?? 0) + 1;
      papersPerWeek.set(w, n);
      if (n === RULES.weeklyPapers) lines.push({ label: `本週完成 ${n} 份卷`, points: RULES.weeklyGoal });
    }
    const t = lines.reduce((s, l) => s + l.points, 0);
    perAttempt.set(a.id, { total: t, lines });
    total += t;
  }

  let level = 1;
  let levelStart = 0;
  while (total >= levelStart + levelCost(level)) {
    levelStart += levelCost(level);
    level += 1;
  }
  return {
    total,
    level,
    levelStart,
    levelNext: levelStart + levelCost(level),
    seen: state.size,
    mastered: [...state.values()].filter((s) => s.mastered).length,
    perAttempt,
  };
}
