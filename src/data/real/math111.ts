import type { Question } from '../../types';

// 111年國中教育會考 數學科 (25題)
// 題目截圖來源：111會考數學題本.pdf（乾淨無正解）
// 詳解截圖 + 正解字母來源：111會考數學解析.pdf（翰林出版）
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'D', 3: 'C', 4: 'B', 5: 'A', 6: 'D', 7: 'D', 8: 'D', 9: 'C', 10: 'C',
  11: 'C', 12: 'B', 13: 'D', 14: 'C', 15: 'B', 16: 'A', 17: 'A', 18: 'B', 19: 'B', 20: 'C',
  21: 'B', 22: 'A', 23: 'D', 24: 'D', 25: 'D',
};

const GROUPS: [number, number][] = [[24, 25]];

function groupIdFor(qNo: number): string | undefined {
  const g = GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
  return g ? `數學-111-g${g[0]}-${g[1]}` : undefined;
}

export const MATH_111_QUESTIONS: Question[] = Array.from({ length: 25 }, (_, i) => {
  const qNo = i + 1;
  const padded = String(qNo).padStart(2, '0');
  return {
    id: `數學-111-${qNo}`,
    subject: '數學',
    year: 111,
    qNo,
    groupId: groupIdFor(qNo),
    imagePath: `${import.meta.env.BASE_URL}questions/math/111/q${padded}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/math/111/e${padded}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
