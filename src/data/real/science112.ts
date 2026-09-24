import type { Question } from '../../types';

// 112年國中教育會考 自然科 (50題)
// 題目截圖來源：112會考自然題本.pdf（官方公版，2欄排版）
// 詳解截圖 + 正解字母來源：112會考自然解析.pdf（官方公版解答）
const ANSWERS: Record<number, string> = {
  1: 'D', 2: 'B', 3: 'D', 4: 'C', 5: 'A', 6: 'A', 7: 'B', 8: 'C', 9: 'C', 10: 'B',
  11: 'D', 12: 'A', 13: 'A', 14: 'B', 15: 'B', 16: 'A', 17: 'B', 18: 'A', 19: 'C', 20: 'B',
  21: 'D', 22: 'B', 23: 'C', 24: 'D', 25: 'D', 26: 'A', 27: 'A', 28: 'A', 29: 'B', 30: 'C',
  31: 'C', 32: 'C', 33: 'C', 34: 'D', 35: 'C', 36: 'A', 37: 'B', 38: 'D', 39: 'D', 40: 'A',
  41: 'A', 42: 'D', 43: 'A', 44: 'D', 45: 'C', 46: 'B', 47: 'B', 48: 'B', 49: 'A', 50: 'C',
};

const GROUPS: [number, number][] = [[43, 44], [45, 46], [47, 48], [49, 50]];

function groupIdFor(qNo: number): string | undefined {
  const g = GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
  return g ? `自然-112-g${g[0]}-${g[1]}` : undefined;
}

export const SCIENCE_112_QUESTIONS: Question[] = Array.from({ length: 50 }, (_, i) => {
  const qNo = i + 1;
  const padded = String(qNo).padStart(2, '0');
  return {
    id: `自然-112-${qNo}`,
    subject: '自然',
    year: 112,
    qNo,
    groupId: groupIdFor(qNo),
    imagePath: `${import.meta.env.BASE_URL}questions/自然/112/q${padded}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/自然/112/e${padded}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
