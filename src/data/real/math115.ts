import type { Question } from '../../types';

// 115年國中教育會考 數學科 選擇題 25 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 115會考數學解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'C', 2: 'D', 3: 'C', 4: 'B', 5: 'C', 6: 'B', 7: 'A', 8: 'C', 9: 'B', 10: 'D',
  11: 'A', 12: 'B', 13: 'D', 14: 'B', 15: 'C', 16: 'A', 17: 'A', 18: 'B', 19: 'D', 20: 'C',
  21: 'D', 22: 'C', 23: 'B', 24: 'B', 25: 'D',
};

const GROUPS: [number, number][] = [[23, 25]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const MATH_115_QUESTIONS: Question[] = Array.from({ length: 25 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `數學-115-${qNo}`,
    subject: '數學',
    year: 115,
    qNo,
    groupId: g ? `數學-115-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/math/115/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/math/115/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
