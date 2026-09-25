import type { Question } from '../../types';

// 112年國中教育會考 英文科 (43題)
// 題目截圖來源：112會考英文題本.pdf（官方公版，2欄排版）
// 詳解截圖 + 正解字母來源：112會考英文解析.pdf（官方公版解答）
// 原始題本含聽力測驗（一~三部分），聽力題無法收錄，僅取閱讀部分並重新編號 1~43。
const ANSWERS: Record<number, string> = {
  1: 'B', 2: 'D', 3: 'D', 4: 'B', 5: 'A', 6: 'B', 7: 'A', 8: 'C', 9: 'C', 10: 'D',
  11: 'D', 12: 'C', 13: 'C', 14: 'C', 15: 'D', 16: 'C', 17: 'C', 18: 'B', 19: 'D', 20: 'C',
  21: 'A', 22: 'B', 23: 'D', 24: 'B', 25: 'B', 26: 'A', 27: 'A', 28: 'C', 29: 'D', 30: 'B',
  31: 'A', 32: 'A', 33: 'D', 34: 'C', 35: 'B', 36: 'D', 37: 'D', 38: 'B', 39: 'B', 40: 'C',
  41: 'B', 42: 'A', 43: 'A',
};

const GROUPS: [number, number][] = [[24, 25], [26, 27], [28, 29], [30, 32], [33, 35], [36, 38], [39, 41], [42, 43]];

function groupIdFor(qNo: number): string | undefined {
  const g = GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
  return g ? `英文-112-g${g[0]}-${g[1]}` : undefined;
}

export const ENGLISH_112_QUESTIONS: Question[] = Array.from({ length: 43 }, (_, i) => {
  const qNo = i + 1;
  const padded = String(qNo).padStart(2, '0');
  return {
    id: `英文-112-${qNo}`,
    subject: '英文',
    year: 112,
    qNo,
    groupId: groupIdFor(qNo),
    imagePath: `${import.meta.env.BASE_URL}questions/english/112/q${padded}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/english/112/e${padded}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
