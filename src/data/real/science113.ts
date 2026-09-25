import type { Question } from '../../types';

// 113年國中教育會考 自然科 選擇題 50 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 113會考自然解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'B', 2: 'B', 3: 'C', 4: 'C', 5: 'A', 6: 'C', 7: 'A', 8: 'C', 9: 'A', 10: 'D',
  11: 'B', 12: 'D', 13: 'D', 14: 'B', 15: 'D', 16: 'B', 17: 'B', 18: 'C', 19: 'B', 20: 'C',
  21: 'A', 22: 'C', 23: 'A', 24: 'C', 25: 'D', 26: 'A', 27: 'A', 28: 'B', 29: 'D', 30: 'A',
  31: 'D', 32: 'D', 33: 'D', 34: 'B', 35: 'C', 36: 'B', 37: 'B', 38: 'D', 39: 'C', 40: 'B',
  41: 'D', 42: 'C', 43: 'D', 44: 'A', 45: 'B', 46: 'D', 47: 'A', 48: 'C', 49: 'C', 50: 'C',
};

const GROUPS: [number, number][] = [[42, 43], [44, 45], [46, 48], [49, 50]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const SCIENCE_113_QUESTIONS: Question[] = Array.from({ length: 50 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `自然-113-${qNo}`,
    subject: '自然',
    year: 113,
    qNo,
    groupId: g ? `自然-113-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/science/113/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/science/113/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
