import type { Question } from '../../types';

// 112年國中教育會考 英文科 選擇題 43 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 112會考英文解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'B', 2: 'D', 3: 'D', 4: 'B', 5: 'A', 6: 'B', 7: 'A', 8: 'C', 9: 'C', 10: 'D',
  11: 'D', 12: 'C', 13: 'C', 14: 'C', 15: 'D', 16: 'C', 17: 'C', 18: 'B', 19: 'D', 20: 'C',
  21: 'A', 22: 'B', 23: 'D', 24: 'B', 25: 'B', 26: 'A', 27: 'A', 28: 'C', 29: 'D', 30: 'B',
  31: 'A', 32: 'A', 33: 'D', 34: 'C', 35: 'B', 36: 'D', 37: 'D', 38: 'B', 39: 'B', 40: 'C',
  41: 'B', 42: 'A', 43: 'A',
};

const GROUPS: [number, number][] = [[24, 25], [26, 27], [28, 29], [30, 32], [33, 35], [36, 38], [39, 41], [42, 43]];

// 這些題組的解析卷把整組的答案與解析寫在同一段，組內各題共用一張詳解圖
const SHARED_EXPLANATION: Record<number, number> = {
  25: 24, 27: 26, 29: 28, 31: 30, 32: 30, 34: 33, 35: 33, 37: 36, 38: 36, 40: 39,
  41: 39, 43: 42,
};

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const ENGLISH_112_QUESTIONS: Question[] = Array.from({ length: 43 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `英文-112-${qNo}`,
    subject: '英文',
    year: 112,
    qNo,
    groupId: g ? `英文-112-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/english/112/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/english/112/e${pad(SHARED_EXPLANATION[qNo] ?? qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
