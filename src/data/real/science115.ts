import type { Question } from '../../types';

// 115年國中教育會考 自然科 選擇題 50 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 115會考自然解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'C', 3: 'B', 4: 'B', 5: 'C', 6: 'D', 7: 'B', 8: 'C', 9: 'C', 10: 'A',
  11: 'C', 12: 'D', 13: 'B', 14: 'C', 15: 'B', 16: 'A', 17: 'A', 18: 'A', 19: 'D', 20: 'C',
  21: 'D', 22: 'D', 23: 'C', 24: 'D', 25: 'B', 26: 'A', 27: 'A', 28: 'C', 29: 'C', 30: 'A',
  31: 'B', 32: 'B', 33: 'B', 34: 'D', 35: 'C', 36: 'D', 37: 'B', 38: 'C', 39: 'D', 40: 'A',
  41: 'B', 42: 'D', 43: 'B', 44: 'C', 45: 'D', 46: 'C', 47: 'A', 48: 'D', 49: 'D', 50: 'A',
};

const GROUPS: [number, number][] = [[42, 43], [44, 45], [46, 47], [48, 50]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const SCIENCE_115_QUESTIONS: Question[] = Array.from({ length: 50 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `自然-115-${qNo}`,
    subject: '自然',
    year: 115,
    qNo,
    groupId: g ? `自然-115-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/science/115/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/science/115/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
