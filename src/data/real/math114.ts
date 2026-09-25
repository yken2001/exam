import type { Question } from '../../types';

// 114年國中教育會考 數學科 選擇題 25 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 114會考數學解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'C', 2: 'B', 3: 'C', 4: 'B', 5: 'C', 6: 'A', 7: 'A', 8: 'C', 9: 'A', 10: 'A',
  11: 'B', 12: 'D', 13: 'A', 14: 'C', 15: 'B', 16: 'D', 17: 'D', 18: 'B', 19: 'C', 20: 'A',
  21: 'D', 22: 'B', 23: 'D', 24: 'D', 25: 'B',
};

const GROUPS: [number, number][] = [[24, 25]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const MATH_114_QUESTIONS: Question[] = Array.from({ length: 25 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `數學-114-${qNo}`,
    subject: '數學',
    year: 114,
    qNo,
    groupId: g ? `數學-114-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/math/114/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/math/114/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
