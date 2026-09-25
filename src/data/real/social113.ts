import type { Question } from '../../types';

// 113年國中教育會考 社會科 選擇題 54 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 113會考社會解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'B', 2: 'A', 3: 'B', 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'C', 9: 'A', 10: 'C',
  11: 'C', 12: 'B', 13: 'C', 14: 'D', 15: 'C', 16: 'C', 17: 'A', 18: 'C', 19: 'D', 20: 'A',
  21: 'B', 22: 'C', 23: 'B', 24: 'A', 25: 'B', 26: 'C', 27: 'A', 28: 'B', 29: 'A', 30: 'C',
  31: 'D', 32: 'A', 33: 'D', 34: 'D', 35: 'B', 36: 'B', 37: 'C', 38: 'D', 39: 'C', 40: 'B',
  41: 'A', 42: 'D', 43: 'A', 44: 'C', 45: 'A', 46: 'B', 47: 'D', 48: 'C', 49: 'A', 50: 'D',
  51: 'B', 52: 'D', 53: 'B', 54: 'C',
};

const GROUPS: [number, number][] = [[44, 45], [46, 48], [49, 51], [52, 54]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const SOCIAL_113_QUESTIONS: Question[] = Array.from({ length: 54 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `社會-113-${qNo}`,
    subject: '社會',
    year: 113,
    qNo,
    groupId: g ? `社會-113-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/social/113/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/social/113/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
