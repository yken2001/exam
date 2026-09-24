import type { Question } from '../../types';

// 112年國中教育會考 社會科 (54題)
// 題目截圖來源：112會考社會題本.pdf（官方公版，2欄排版）
// 詳解截圖 + 正解字母來源：112會考社會解析.pdf（官方公版解答）
const ANSWERS: Record<number, string> = {
  1: 'C', 2: 'D', 3: 'A', 4: 'A', 5: 'A', 6: 'C', 7: 'C', 8: 'D', 9: 'C', 10: 'C',
  11: 'B', 12: 'D', 13: 'A', 14: 'B', 15: 'A', 16: 'C', 17: 'A', 18: 'A', 19: 'D', 20: 'A',
  21: 'B', 22: 'D', 23: 'B', 24: 'B', 25: 'A', 26: 'B', 27: 'D', 28: 'B', 29: 'A', 30: 'D',
  31: 'C', 32: 'D', 33: 'B', 34: 'D', 35: 'D', 36: 'C', 37: 'B', 38: 'D', 39: 'A', 40: 'A',
  41: 'C', 42: 'D', 43: 'C', 44: 'C', 45: 'D', 46: 'B', 47: 'C', 48: 'D', 49: 'B', 50: 'A',
  51: 'A', 52: 'D', 53: 'B', 54: 'C',
};

const GROUPS: [number, number][] = [[44, 45], [46, 48], [49, 51], [52, 54]];

function groupIdFor(qNo: number): string | undefined {
  const g = GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
  return g ? `社會-112-g${g[0]}-${g[1]}` : undefined;
}

export const SOCIAL_112_QUESTIONS: Question[] = Array.from({ length: 54 }, (_, i) => {
  const qNo = i + 1;
  const padded = String(qNo).padStart(2, '0');
  return {
    id: `社會-112-${qNo}`,
    subject: '社會',
    year: 112,
    qNo,
    groupId: groupIdFor(qNo),
    imagePath: `/questions/社會/112/q${padded}.png`,
    explanationImagePath: `/explanations/社會/112/e${padded}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
