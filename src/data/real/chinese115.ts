import type { Question } from '../../types';

// 115年國中教育會考 國文科 選擇題 42 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 115會考國文解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'B', 2: 'A', 3: 'D', 4: 'A', 5: 'D', 6: 'D', 7: 'C', 8: 'C', 9: 'C', 10: 'D',
  11: 'B', 12: 'D', 13: 'A', 14: 'B', 15: 'A', 16: 'A', 17: 'D', 18: 'D', 19: 'A', 20: 'B',
  21: 'D', 22: 'C', 23: 'B', 24: 'B', 25: 'A', 26: 'B', 27: 'B', 28: 'A', 29: 'D', 30: 'D',
  31: 'C', 32: 'A', 33: 'C', 34: 'B', 35: 'C', 36: 'C', 37: 'C', 38: 'A', 39: 'C', 40: 'C',
  41: 'B', 42: 'B',
};

const GROUPS: [number, number][] = [[24, 25], [26, 29], [30, 32], [33, 34], [35, 36], [37, 38], [39, 40], [41, 42]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const CHINESE_115_QUESTIONS: Question[] = Array.from({ length: 42 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `國文-115-${qNo}`,
    subject: '國文',
    year: 115,
    qNo,
    groupId: g ? `國文-115-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/chinese/115/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/chinese/115/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
