import type { Subject, SubjectConfig } from '../types';

export const SUBJECTS: Subject[] = ['國文', '英文', '數學', '自然', '社會'];

export const SUBJECT_CONFIG: Record<Subject, SubjectConfig> = {
  國文: { subject: '國文', secPerQuestion: 102, realCount: 41 },
  英文: { subject: '英文', secPerQuestion: 88, realCount: 41 },
  數學: { subject: '數學', secPerQuestion: 150, realCount: 26 },
  自然: { subject: '自然', secPerQuestion: 78, realCount: 54 },
  社會: { subject: '社會', secPerQuestion: 67, realCount: 63 },
};

export const TIME_OPTIONS_MIN = [10, 20, 35, 70];
