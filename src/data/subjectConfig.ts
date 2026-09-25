import type { Subject, SubjectConfig } from '../types';

export const SUBJECTS: Subject[] = ['國文', '英文', '英聽', '數學', '自然', '社會'];

// 會考各科考試時間（心測中心「考試科目與題型」）。英文是英語（閱讀），
// 英聽是英語（聽力）；數學 80 分鐘含非選擇題，題庫只有選擇題。
export const SUBJECT_CONFIG: Record<Subject, SubjectConfig> = {
  國文: { subject: '國文', officialMinutes: 70 },
  英文: { subject: '英文', officialMinutes: 60 },
  英聽: { subject: '英聽', officialMinutes: 25 },
  數學: { subject: '數學', officialMinutes: 80 },
  自然: { subject: '自然', officialMinutes: 70 },
  社會: { subject: '社會', officialMinutes: 70 },
};

/** 份量：一整份卷、半份、四分之一份（題數與時間都照比例） */
export const FRACTIONS: { value: number; label: string }[] = [
  { value: 1, label: '全卷' },
  { value: 0.5, label: '1/2 卷' },
  { value: 0.25, label: '1/4 卷' },
];
