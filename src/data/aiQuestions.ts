import type { Question, Subject } from '../types';

/** AI-made practice sets (src/data/ai/*.json): text questions laid out like
 * a real paper, 題組 as passage + items, with optional drawn figures
 * (public/ai/<year>/…) and, for 英聽, synthesized audio. Each set is checked
 * by independent solvers before it is added (see README「AI 出題」). */
interface AiSet {
  set: string;
  year: number;
  subject: Subject;
  groups: { from: number; to: number; passage: string; translation?: string; figure?: string }[];
  items: {
    qNo: number;
    stem: string;
    options: string[];
    answer: string;
    explanation: string;
    figure?: string;
  }[];
}

const base = import.meta.env.BASE_URL;
const pad = (n: number) => String(n).padStart(2, '0');

function toQuestions(s: AiSet): Question[] {
  return s.items.map((it) => {
    const g = s.groups.find((x) => it.qNo >= x.from && it.qNo <= x.to);
    return {
      id: `${s.subject}-${s.year}-${it.qNo}`,
      subject: s.subject,
      year: s.year,
      qNo: it.qNo,
      groupId: g ? `${s.subject}-${s.year}-g${g.from}-${g.to}` : undefined,
      text: {
        stem: it.stem,
        options: it.options,
        passage: g?.passage,
        passageTranslation: g?.translation,
        figure: it.figure ? base + it.figure : undefined,
        passageFigure: g?.figure ? base + g.figure : undefined,
      },
      audioPath: s.subject === '英聽' ? `${base}audio/listening/${s.year}/a${pad(it.qNo)}.wav` : undefined,
      explanation: it.explanation,
      correctAnswer: it.answer,
      optionCount: it.options.length,
    };
  });
}

const files = import.meta.glob<AiSet>('./ai/*.json', { eager: true, import: 'default' });

/** every AI question, by subject and year */
export const AI_QUESTIONS: Question[] = Object.values(files).flatMap(toQuestions);

export function aiQuestions(subject: Subject, year: number): Question[] {
  return AI_QUESTIONS.filter((q) => q.subject === subject && q.year === year).sort((a, b) => a.qNo - b.qNo);
}
