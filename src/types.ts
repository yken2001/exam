export type Subject = '國文' | '英文' | '英聽' | '數學' | '自然' | '社會';

export interface SubjectConfig {
  subject: Subject;
  /** 會考該科考試時間（分鐘） */
  officialMinutes: number;
}

export interface Question {
  id: string;
  subject: Subject;
  year: number;
  qNo: number;
  groupId?: string;
  /** screenshot of the question (會考真題); absent for text questions */
  imagePath?: string;
  /** text question (AI 出題): stem, options, and the 題組 passage */
  text?: TextQuestion;
  explanation?: string;
  explanationImagePath?: string;
  audioPath?: string;
  correctAnswer: string;
  optionCount: number;
}

export interface TextQuestion {
  /** empty for a cloze blank: the passage carries the __n__ mark */
  stem: string;
  options: string[];
  /** shared by every item of a 題組 */
  passage?: string;
  passageTranslation?: string;
}

export type OrderMode = 'original' | 'shuffled';

export interface ExamBreakdownItem {
  subject: Subject;
  count: number;
  sec: number;
}

export interface ExamPaper {
  id: string;
  createdAt: number;
  subjects: Subject[];
  years: number[];
  /** total time in minutes (sum over subjects) */
  totalMinutes: number;
  /** 份量: 1 全卷, 0.5, 0.25 (absent on papers made before it existed) */
  fraction?: number;
  orderMode: OrderMode;
  questionIds: string[];
  breakdown: ExamBreakdownItem[];
  timeBudgetSec: number;
}

export interface AttemptAnswer {
  questionId: string;
  selected?: string;
}

export interface AttemptRecord {
  id: string;
  examPaperId: string;
  startedAt: number;
  finishedAt?: number;
  answers: AttemptAnswer[];
  /** set on records brought in from another device's exported file */
  importedFrom?: string;
}
