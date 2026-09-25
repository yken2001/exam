import type { Question } from '../../types';

// 113年國中教育會考 數學科 選擇題 25 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 113會考數學解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'A', 3: 'C', 4: 'D', 5: 'B', 6: 'D', 7: 'D', 8: 'C', 9: 'C', 10: 'C',
  11: 'A', 12: 'C', 13: 'B', 14: 'C', 15: 'B', 16: 'B', 17: 'A', 18: 'A', 19: 'B', 20: 'D',
  21: 'D', 22: 'A', 23: 'B', 24: 'D', 25: 'B',
};

const GROUPS: [number, number][] = [[24, 25]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const MATH_113_QUESTIONS: Question[] = Array.from({ length: 25 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `數學-113-${qNo}`,
    subject: '數學',
    year: 113,
    qNo,
    groupId: g ? `數學-113-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/math/113/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/math/113/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
