import Dexie, { type Table } from 'dexie';
import type { ExamPaper, AttemptRecord } from './types';

class ExamDB extends Dexie {
  examPapers!: Table<ExamPaper, string>;
  attempts!: Table<AttemptRecord, string>;

  constructor() {
    super('exam-app-db');
    this.version(1).stores({
      examPapers: 'id, createdAt',
      attempts: 'id, examPaperId, startedAt',
    });
  }
}

export const db = new ExamDB();
