import type { Question } from '../../types';

// 115年國中教育會考 英文科 選擇題 43 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 115會考英文解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'B', 2: 'A', 3: 'B', 4: 'C', 5: 'C', 6: 'D', 7: 'C', 8: 'A', 9: 'C', 10: 'A',
  11: 'C', 12: 'A', 13: 'D', 14: 'D', 15: 'A', 16: 'A', 17: 'D', 18: 'B', 19: 'D', 20: 'C',
  21: 'D', 22: 'D', 23: 'B', 24: 'D', 25: 'D', 26: 'C', 27: 'D', 28: 'C', 29: 'A', 30: 'A',
  31: 'B', 32: 'D', 33: 'C', 34: 'A', 35: 'A', 36: 'B', 37: 'B', 38: 'C', 39: 'B', 40: 'B',
  41: 'B', 42: 'B', 43: 'C',
};

const GROUPS: [number, number][] = [[20, 21], [22, 23], [24, 26], [27, 28], [29, 31], [32, 34], [35, 39], [40, 43]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const ENGLISH_115_QUESTIONS: Question[] = Array.from({ length: 43 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `英文-115-${qNo}`,
    subject: '英文',
    year: 115,
    qNo,
    groupId: g ? `英文-115-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/english/115/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/english/115/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
