import type { Question } from '../../types';

// 112年國中教育會考 國文科 (42題)
// 題目截圖來源：112會考國文題本.pdf（官方公版，2欄排版）
// 詳解截圖 + 正解字母來源：112會考國文解析.pdf（官方公版解答）
const ANSWERS: Record<number, string> = {
  1: 'D', 2: 'D', 3: 'C', 4: 'C', 5: 'D', 6: 'C', 7: 'A', 8: 'A', 9: 'A', 10: 'D',
  11: 'C', 12: 'A', 13: 'B', 14: 'C', 15: 'B', 16: 'D', 17: 'A', 18: 'C', 19: 'A', 20: 'B',
  21: 'C', 22: 'D', 23: 'D', 24: 'B', 25: 'D', 26: 'A', 27: 'A', 28: 'B', 29: 'C', 30: 'A',
  31: 'C', 32: 'B', 33: 'C', 34: 'B', 35: 'B', 36: 'C', 37: 'B', 38: 'A', 39: 'D', 40: 'D',
  41: 'B', 42: 'D',
};

const GROUPS: [number, number][] = [[25, 26], [27, 29], [30, 31], [32, 33], [34, 35], [36, 38], [39, 40], [41, 42]];

function groupIdFor(qNo: number): string | undefined {
  const g = GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
  return g ? `國文-112-g${g[0]}-${g[1]}` : undefined;
}

export const CHINESE_112_QUESTIONS: Question[] = Array.from({ length: 42 }, (_, i) => {
  const qNo = i + 1;
  const padded = String(qNo).padStart(2, '0');
  return {
    id: `國文-112-${qNo}`,
    subject: '國文',
    year: 112,
    qNo,
    groupId: groupIdFor(qNo),
    imagePath: `/questions/國文/112/q${padded}.png`,
    explanationImagePath: `/explanations/國文/112/e${padded}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
