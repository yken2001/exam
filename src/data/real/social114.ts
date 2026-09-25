import type { Question } from '../../types';

// 114年國中教育會考 社會科 選擇題 54 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 114會考社會解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'A', 3: 'B', 4: 'B', 5: 'B', 6: 'C', 7: 'D', 8: 'C', 9: 'C', 10: 'B',
  11: 'C', 12: 'D', 13: 'D', 14: 'C', 15: 'C', 16: 'C', 17: 'A', 18: 'B', 19: 'D', 20: 'C',
  21: 'A', 22: 'C', 23: 'A', 24: 'D', 25: 'D', 26: 'A', 27: 'D', 28: 'B', 29: 'B', 30: 'C',
  31: 'A', 32: 'B', 33: 'D', 34: 'C', 35: 'B', 36: 'A', 37: 'C', 38: 'A', 39: 'A', 40: 'D',
  41: 'D', 42: 'C', 43: 'B', 44: 'A', 45: 'D', 46: 'D', 47: 'D', 48: 'C', 49: 'A', 50: 'B',
  51: 'D', 52: 'C', 53: 'B', 54: 'D',
};

const GROUPS: [number, number][] = [[43, 45], [46, 48], [49, 51], [52, 54]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const SOCIAL_114_QUESTIONS: Question[] = Array.from({ length: 54 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `社會-114-${qNo}`,
    subject: '社會',
    year: 114,
    qNo,
    groupId: g ? `社會-114-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/social/114/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/social/114/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
