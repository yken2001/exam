import type { Question, Subject } from '../types';
import { SUBJECT_CONFIG, SUBJECTS } from './subjectConfig';
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

const YEARS = [110, 111, 112];
const OPTIONS = ['A', 'B', 'C', 'D'];

// Subjects that commonly have shared-passage question groups (every 4th
// question starts a group of 2) versus subjects that are mostly standalone.
const GROUPED_SUBJECTS: Subject[] = ['國文', '英文', '社會', '自然'];

// subject/year combos backed by real cropped question banks instead of the
// placeholder generator below
const REAL_DATA: Partial<Record<Subject, Partial<Record<number, Question[]>>>> = {
  數學: { 110: MATH_110_QUESTIONS, 111: MATH_111_QUESTIONS, 112: MATH_112_QUESTIONS },
  國文: { 110: CHINESE_110_QUESTIONS, 111: CHINESE_111_QUESTIONS, 112: CHINESE_112_QUESTIONS },
  英文: { 110: ENGLISH_110_QUESTIONS, 111: ENGLISH_111_QUESTIONS, 112: ENGLISH_112_QUESTIONS },
  社會: { 110: SOCIAL_110_QUESTIONS, 111: SOCIAL_111_QUESTIONS, 112: SOCIAL_112_QUESTIONS },
  自然: { 110: SCIENCE_110_QUESTIONS, 111: SCIENCE_111_QUESTIONS, 112: SCIENCE_112_QUESTIONS },
};

function pickAnswer(seed: number): string {
  return OPTIONS[seed % OPTIONS.length];
}

function generateForSubjectYear(subject: Subject, year: number): Question[] {
  if (REAL_DATA[subject]?.[year]) return REAL_DATA[subject]![year]!;

  const count = SUBJECT_CONFIG[subject].realCount;
  const questions: Question[] = [];
  let qNo = 1;
  const useGroups = GROUPED_SUBJECTS.includes(subject);

  while (qNo <= count) {
    const remaining = count - qNo + 1;
    const makeGroup = useGroups && remaining >= 2 && qNo % 4 === 1;
    const groupSize = makeGroup ? 2 : 1;
    const groupId = makeGroup ? `${subject}-${year}-g${qNo}` : undefined;

    for (let i = 0; i < groupSize; i++) {
      questions.push({
        id: `${subject}-${year}-${qNo}`,
        subject,
        year,
        qNo,
        groupId,
        imagePath: `placeholder://${subject}/${year}/${qNo}.png`,
        explanation: `第 ${qNo} 題詳解（示範資料，之後由截圖或文字取代）。`,
        correctAnswer: pickAnswer(qNo + year),
        optionCount: 4,
      });
      qNo++;
    }
  }
  return questions;
}

export const SAMPLE_QUESTIONS: Question[] = SUBJECTS.flatMap((subject) =>
  YEARS.flatMap((year) => generateForSubjectYear(subject, year))
);

export const QUESTION_BY_ID: Map<string, Question> = new Map(
  SAMPLE_QUESTIONS.map((q) => [q.id, q])
);

export const AVAILABLE_YEARS = YEARS;
