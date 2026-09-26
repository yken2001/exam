import type { Question, Subject } from '../types';
import ai1English from './ai/ai1_english.json';

/** An AI-made practice set (src/data/ai/*.json): text questions laid out
 * like a real paper, 題組 as passage + items. Checked by independent
 * solvers before it is added here (see tools/README.md). */
interface AiSet {
  set: string;
  year: number;
  subject: Subject;
  groups: { from: number; to: number; passage: string; translation: string }[];
  items: { qNo: number; stem: string; options: string[]; answer: string; explanation: string }[];
}

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
      },
      explanation: it.explanation,
      correctAnswer: it.answer,
      optionCount: it.options.length,
    };
  });
}

export const AI_1_ENGLISH_QUESTIONS = toQuestions(ai1English as AiSet);
