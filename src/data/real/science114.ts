import type { Question } from '../../types';

// 114年國中教育會考 自然科 選擇題 50 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 114會考自然解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'C', 2: 'B', 3: 'A', 4: 'A', 5: 'D', 6: 'A', 7: 'B', 8: 'A', 9: 'D', 10: 'B',
  11: 'C', 12: 'C', 13: 'D', 14: 'C', 15: 'B', 16: 'C', 17: 'A', 18: 'C', 19: 'C', 20: 'B',
  21: 'D', 22: 'C', 23: 'B', 24: 'A', 25: 'B', 26: 'D', 27: 'D', 28: 'B', 29: 'D', 30: 'A',
  31: 'A', 32: 'B', 33: 'D', 34: 'D', 35: 'A', 36: 'A', 37: 'B', 38: 'C', 39: 'C', 40: 'A',
  41: 'D', 42: 'B', 43: 'D', 44: 'C', 45: 'D', 46: 'D', 47: 'B', 48: 'D', 49: 'C', 50: 'B',
};

const GROUPS: [number, number][] = [[43, 44], [45, 46], [47, 48], [49, 50]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const SCIENCE_114_QUESTIONS: Question[] = Array.from({ length: 50 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `自然-114-${qNo}`,
    subject: '自然',
    year: 114,
    qNo,
    groupId: g ? `自然-114-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/science/114/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/science/114/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
