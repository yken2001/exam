import type { Question, Subject } from '../types';
import { SUBJECTS } from './subjectConfig';
import { MATH_110_QUESTIONS } from './real/math110';
import { CHINESE_110_QUESTIONS } from './real/chinese110';
import { ENGLISH_110_QUESTIONS } from './real/english110';
import { SOCIAL_110_QUESTIONS } from './real/social110';
import { SCIENCE_110_QUESTIONS } from './real/science110';
import { MATH_111_QUESTIONS } from './real/math111';
import { CHINESE_111_QUESTIONS } from './real/chinese111';
import { ENGLISH_111_QUESTIONS } from './real/english111';
import { SOCIAL_111_QUESTIONS } from './real/social111';
import { SCIENCE_111_QUESTIONS } from './real/science111';
import { MATH_112_QUESTIONS } from './real/math112';
import { CHINESE_112_QUESTIONS } from './real/chinese112';
import { ENGLISH_112_QUESTIONS } from './real/english112';
import { SOCIAL_112_QUESTIONS } from './real/social112';
import { SCIENCE_112_QUESTIONS } from './real/science112';
import { LISTENING_112_QUESTIONS } from './real/listening112';

const YEARS = [110, 111, 112];

// 數學非選擇題（手寫題）不在題庫內；英聽只有 112 年的解析卷收錄了聽力題
const REAL_DATA: Record<Subject, Partial<Record<number, Question[]>>> = {
  數學: { 110: MATH_110_QUESTIONS, 111: MATH_111_QUESTIONS, 112: MATH_112_QUESTIONS },
  國文: { 110: CHINESE_110_QUESTIONS, 111: CHINESE_111_QUESTIONS, 112: CHINESE_112_QUESTIONS },
  英文: { 110: ENGLISH_110_QUESTIONS, 111: ENGLISH_111_QUESTIONS, 112: ENGLISH_112_QUESTIONS },
  英聽: { 112: LISTENING_112_QUESTIONS },
  社會: { 110: SOCIAL_110_QUESTIONS, 111: SOCIAL_111_QUESTIONS, 112: SOCIAL_112_QUESTIONS },
  自然: { 110: SCIENCE_110_QUESTIONS, 111: SCIENCE_111_QUESTIONS, 112: SCIENCE_112_QUESTIONS },
};

export const SAMPLE_QUESTIONS: Question[] = SUBJECTS.flatMap((subject) =>
  YEARS.flatMap((year) => REAL_DATA[subject][year] ?? [])
);

export const QUESTION_BY_ID: Map<string, Question> = new Map(
  SAMPLE_QUESTIONS.map((q) => [q.id, q])
);

export const AVAILABLE_YEARS = YEARS;

/** years that actually have questions for a subject (英聽: 112 only) */
export function yearsWithData(subject: Subject): number[] {
  return YEARS.filter((y) => (REAL_DATA[subject][y]?.length ?? 0) > 0);
}
