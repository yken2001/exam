import type { Question } from '../../types';

// 110年國中教育會考 社會科 選擇題 63 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 110會考社會解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'C', 2: 'B', 3: 'B', 4: 'A', 5: 'B', 6: 'B', 7: 'A', 8: 'C', 9: 'B', 10: 'A',
  11: 'C', 12: 'A', 13: 'D', 14: 'A', 15: 'D', 16: 'B', 17: 'C', 18: 'D', 19: 'B', 20: 'D',
  21: 'D', 22: 'C', 23: 'B', 24: 'D', 25: 'C', 26: 'B', 27: 'D', 28: 'B', 29: 'C', 30: 'C',
  31: 'B', 32: 'A', 33: 'A', 34: 'D', 35: 'D', 36: 'C', 37: 'C', 38: 'C', 39: 'D', 40: 'B',
  41: 'C', 42: 'B', 43: 'B', 44: 'A', 45: 'D', 46: 'C', 47: 'A', 48: 'D', 49: 'A', 50: 'D',
  51: 'B', 52: 'A', 53: 'B', 54: 'B', 55: 'C', 56: 'A', 57: 'B', 58: 'C', 59: 'B', 60: 'A',
  61: 'C', 62: 'C', 63: 'D',
};

const GROUPS: [number, number][] = [[56, 57], [58, 60], [61, 63]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const SOCIAL_110_QUESTIONS: Question[] = Array.from({ length: 63 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `社會-110-${qNo}`,
    subject: '社會',
    year: 110,
    qNo,
    groupId: g ? `社會-110-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/social/110/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/social/110/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
