import type { Question } from '../../types';

// 111年國中教育會考 自然科 選擇題 50 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 111會考自然解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'C', 3: 'D', 4: 'C', 5: 'A', 6: 'B', 7: 'B', 8: 'B', 9: 'C', 10: 'A',
  11: 'C', 12: 'A', 13: 'C', 14: 'A', 15: 'C', 16: 'B', 17: 'C', 18: 'C', 19: 'B', 20: 'A',
  21: 'D', 22: 'B', 23: 'D', 24: 'B', 25: 'D', 26: 'D', 27: 'B', 28: 'B', 29: 'A', 30: 'A',
  31: 'C', 32: 'C', 33: 'A', 34: 'D', 35: 'B', 36: 'D', 37: 'B', 38: 'A', 39: 'B', 40: 'D',
  41: 'D', 42: 'B', 43: 'C', 44: 'D', 45: 'D', 46: 'D', 47: 'A', 48: 'D', 49: 'C', 50: 'D',
};

const GROUPS: [number, number][] = [[42, 44], [45, 46], [47, 48], [49, 50]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const SCIENCE_111_QUESTIONS: Question[] = Array.from({ length: 50 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `自然-111-${qNo}`,
    subject: '自然',
    year: 111,
    qNo,
    groupId: g ? `自然-111-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/science/111/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/science/111/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
