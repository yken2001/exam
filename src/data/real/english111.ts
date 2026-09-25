import type { Question } from '../../types';

// 111年國中教育會考 英文科 (43題)
// 題目截圖來源：111會考英文題本.pdf（乾淨無正解）
// 詳解截圖 + 正解字母來源：111會考英文解析.pdf（翰林出版）
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'A', 3: 'C', 4: 'C', 5: 'B', 6: 'A', 7: 'B', 8: 'B', 9: 'A', 10: 'D',
  11: 'C', 12: 'B', 13: 'D', 14: 'C', 15: 'B', 16: 'C', 17: 'D', 18: 'C', 19: 'A', 20: 'D',
  21: 'C', 22: 'C', 23: 'D', 24: 'C', 25: 'A', 26: 'C', 27: 'A', 28: 'D', 29: 'B', 30: 'D',
  31: 'A', 32: 'D', 33: 'D', 34: 'B', 35: 'D', 36: 'B', 37: 'C', 38: 'B', 39: 'A', 40: 'D',
  41: 'C', 42: 'A', 43: 'A',
};

const GROUPS: [number, number][] = [[21, 22], [23, 24], [25, 26], [27, 29], [30, 32], [33, 36], [37, 39], [40, 43]];

function groupIdFor(qNo: number): string | undefined {
  const g = GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
  return g ? `英文-111-g${g[0]}-${g[1]}` : undefined;
}

export const ENGLISH_111_QUESTIONS: Question[] = Array.from({ length: 43 }, (_, i) => {
  const qNo = i + 1;
  const padded = String(qNo).padStart(2, '0');
  return {
    id: `英文-111-${qNo}`,
    subject: '英文',
    year: 111,
    qNo,
    groupId: groupIdFor(qNo),
    imagePath: `${import.meta.env.BASE_URL}questions/english/111/q${padded}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/english/111/e${padded}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
