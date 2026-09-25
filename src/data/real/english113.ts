import type { Question } from '../../types';

// 113年國中教育會考 英文科 選擇題 43 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 113會考英文解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'C', 3: 'B', 4: 'B', 5: 'D', 6: 'D', 7: 'B', 8: 'D', 9: 'C', 10: 'D',
  11: 'C', 12: 'A', 13: 'A', 14: 'A', 15: 'C', 16: 'D', 17: 'C', 18: 'D', 19: 'A', 20: 'C',
  21: 'B', 22: 'D', 23: 'C', 24: 'C', 25: 'B', 26: 'A', 27: 'D', 28: 'B', 29: 'B', 30: 'A',
  31: 'D', 32: 'A', 33: 'A', 34: 'B', 35: 'A', 36: 'B', 37: 'B', 38: 'C', 39: 'C', 40: 'A',
  41: 'B', 42: 'B', 43: 'D',
};

const GROUPS: [number, number][] = [[22, 23], [24, 25], [26, 27], [28, 29], [30, 32], [33, 35], [36, 39], [40, 43]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const ENGLISH_113_QUESTIONS: Question[] = Array.from({ length: 43 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `英文-113-${qNo}`,
    subject: '英文',
    year: 113,
    qNo,
    groupId: g ? `英文-113-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/english/113/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/english/113/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
