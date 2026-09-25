import type { Question } from '../../types';

// 110年國中教育會考 數學科 選擇題 26 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 110會考數學解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'B', 3: 'D', 4: 'C', 5: 'D', 6: 'C', 7: 'B', 8: 'C', 9: 'C', 10: 'D',
  11: 'D', 12: 'B', 13: 'B', 14: 'C', 15: 'B', 16: 'B', 17: 'D', 18: 'A', 19: 'D', 20: 'B',
  21: 'A', 22: 'C', 23: 'A', 24: 'C', 25: 'A', 26: 'A',
};

const GROUPS: [number, number][] = [];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const MATH_110_QUESTIONS: Question[] = Array.from({ length: 26 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `數學-110-${qNo}`,
    subject: '數學',
    year: 110,
    qNo,
    groupId: g ? `數學-110-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/math/110/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/math/110/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
