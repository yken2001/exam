import type { Question } from '../../types';

// 115年國中教育會考 社會科 選擇題 54 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 115會考社會解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'D', 3: 'C', 4: 'A', 5: 'A', 6: 'D', 7: 'D', 8: 'B', 9: 'A', 10: 'C',
  11: 'C', 12: 'D', 13: 'C', 14: 'A', 15: 'C', 16: 'A', 17: 'B', 18: 'B', 19: 'A', 20: 'B',
  21: 'D', 22: 'C', 23: 'B', 24: 'B', 25: 'A', 26: 'B', 27: 'A', 28: 'A', 29: 'B', 30: 'A',
  31: 'B', 32: 'D', 33: 'A', 34: 'C', 35: 'C', 36: 'C', 37: 'D', 38: 'D', 39: 'B', 40: 'A',
  41: 'B', 42: 'D', 43: 'B', 44: 'D', 45: 'C', 46: 'A', 47: 'C', 48: 'B', 49: 'D', 50: 'A',
  51: 'C', 52: 'B', 53: 'B', 54: 'D',
};

const GROUPS: [number, number][] = [[44, 45], [46, 48], [49, 51], [52, 54]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const SOCIAL_115_QUESTIONS: Question[] = Array.from({ length: 54 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `社會-115-${qNo}`,
    subject: '社會',
    year: 115,
    qNo,
    groupId: g ? `社會-115-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/social/115/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/social/115/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
