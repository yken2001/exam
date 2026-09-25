import { db } from '../db';
import { QUESTION_BY_ID } from '../data/sampleQuestions';
import type { AttemptRecord, ExamPaper } from '../types';

declare const __APP_VERSION__: string;

const FORMAT = 'exam-app-backup';
const FORMAT_VERSION = 1;

/** Everything the app stores in this browser, plus what is needed to look
 * into a problem report: the app build and the device it ran on. */
export interface Backup {
  format: typeof FORMAT;
  formatVersion: number;
  exportedAt: number;
  appVersion: string;
  device: { userAgent: string; screen: string; viewport: string; pixelRatio: number };
  examPapers: ExamPaper[];
  attempts: AttemptRecord[];
}

export async function buildBackup(): Promise<Backup> {
  return {
    format: FORMAT,
    formatVersion: FORMAT_VERSION,
    exportedAt: Date.now(),
    appVersion: __APP_VERSION__,
    device: {
      userAgent: navigator.userAgent,
      screen: `${screen.width}x${screen.height}`,
      viewport: `${window.innerWidth}x${window.innerHeight}`,
      pixelRatio: window.devicePixelRatio,
    },
    examPapers: await db.examPapers.toArray(),
    attempts: await db.attempts.toArray(),
  };
}

export function backupFileName(b: Backup): string {
  const d = new Date(b.exportedAt);
  const p = (n: number) => String(n).padStart(2, '0');
  return `會考練習紀錄_${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}.json`;
}

export function backupFile(b: Backup): File {
  return new File([JSON.stringify(b, null, 1)], backupFileName(b), { type: 'application/json' });
}

export function downloadFile(file: File) {
  const url = URL.createObjectURL(file);
  const a = document.createElement('a');
  a.href = url;
  a.download = file.name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

/** the phone/tablet share sheet (Gmail, LINE…) can take the file directly */
export function canShareFile(file: File): boolean {
  return typeof navigator.canShare === 'function' && navigator.canShare({ files: [file] });
}

export interface ImportResult {
  added: number;
  alreadyHad: number;
  unknownQuestions: number;
  exportedAt: number;
  appVersion: string;
}

/** Merges a backup into this browser's records. Records keep their ids, so
 * importing the same file twice adds nothing the second time; records from
 * the file are tagged with where they came from so they can be told apart
 * from this device's own. Throws with a readable message on a bad file. */
export async function importBackup(text: string, sourceName: string): Promise<ImportResult> {
  let b: Backup;
  try {
    b = JSON.parse(text);
  } catch {
    throw new Error('這不是有效的紀錄檔（無法讀取 JSON）。');
  }
  if (b?.format !== FORMAT || !Array.isArray(b.examPapers) || !Array.isArray(b.attempts)) {
    throw new Error('這不是本 App 匯出的紀錄檔。');
  }
  if (b.formatVersion > FORMAT_VERSION) {
    throw new Error('這個紀錄檔來自較新版本的 App，請先更新網頁再匯入。');
  }
  const label = `${sourceName}（${new Date(b.exportedAt).toLocaleString()} 匯出）`;
  const existing = new Set((await db.attempts.toArray()).map((a) => a.id));
  const fresh = b.attempts.filter((a) => !existing.has(a.id));
  const papersNeeded = new Set(fresh.map((a) => a.examPaperId));
  const unknownQuestions = new Set(
    b.examPapers.flatMap((p) => p.questionIds).filter((id) => !QUESTION_BY_ID.has(id))
  ).size;
  await db.transaction('rw', db.examPapers, db.attempts, async () => {
    await db.examPapers.bulkPut(b.examPapers.filter((p) => papersNeeded.has(p.id)));
    await db.attempts.bulkPut(fresh.map((a) => ({ ...a, importedFrom: a.importedFrom ?? label })));
  });
  return {
    added: fresh.length,
    alreadyHad: b.attempts.length - fresh.length,
    unknownQuestions,
    exportedAt: b.exportedAt,
    appVersion: b.appVersion,
  };
}
