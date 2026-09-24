import type { Question } from '../../types';

// 111年國中教育會考 國文科 (42題)
// 題目截圖來源：111會考國文題本.pdf（乾淨無正解）
// 詳解截圖 + 正解字母來源：111會考國文解析.pdf（翰林出版）
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'D', 2: 'A', 3: 'A', 4: 'B', 5: 'D', 6: 'C', 7: 'C', 8: 'C', 9: 'B', 10: 'C',
  11: 'A', 12: 'D', 13: 'C', 14: 'A', 15: 'D', 16: 'A', 17: 'A', 18: 'A', 19: 'B', 20: 'C',
  21: 'D', 22: 'A', 23: 'B', 24: 'A', 25: 'D', 26: 'C', 27: 'C', 28: 'D', 29: 'B', 30: 'B',
  31: 'D', 32: 'C', 33: 'B', 34: 'C', 35: 'D', 36: 'B', 37: 'B', 38: 'A', 39: 'D', 40: 'B',
  41: 'C', 42: 'D',
};

const GROUPS: [number, number][] = [[26, 27], [28, 29], [30, 31], [32, 33], [34, 35], [36, 38], [39, 40], [41, 42]];

function groupIdFor(qNo: number): string | undefined {
  const g = GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
  return g ? `國文-111-g${g[0]}-${g[1]}` : undefined;
}

export const CHINESE_111_QUESTIONS: Question[] = Array.from({ length: 42 }, (_, i) => {
  const qNo = i + 1;
  const padded = String(qNo).padStart(2, '0');
  return {
    id: `國文-111-${qNo}`,
    subject: '國文',
    year: 111,
    qNo,
    groupId: groupIdFor(qNo),
    imagePath: `${import.meta.env.BASE_URL}questions/國文/111/q${padded}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/國文/111/e${padded}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
