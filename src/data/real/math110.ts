import type { Question } from '../../types';

// 110年國中教育會考 數學科 第一部分選擇題 (1~26題)
// 題目截圖來源：110會考數學題本.pdf（乾淨無正解）
// 詳解截圖 + 正解字母來源：110會考數學解析.pdf（翰林出版）
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'B', 3: 'D', 4: 'C', 5: 'D', 6: 'C', 7: 'B', 8: 'C', 9: 'C', 10: 'D',
  11: 'D', 12: 'B', 13: 'B', 14: 'C', 15: 'B', 16: 'B', 17: 'D', 18: 'A', 19: 'D', 20: 'B',
  21: 'A', 22: 'C', 23: 'A', 24: 'C', 25: 'A', 26: 'A',
};

export const MATH_110_QUESTIONS: Question[] = Array.from({ length: 26 }, (_, i) => {
  const qNo = i + 1;
  const padded = String(qNo).padStart(2, '0');
  return {
    id: `數學-110-${qNo}`,
    subject: '數學',
    year: 110,
    qNo,
    imagePath: `${import.meta.env.BASE_URL}questions/數學/110/q${padded}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/數學/110/e${padded}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
