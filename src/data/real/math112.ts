import type { Question } from '../../types';

// 112年國中教育會考 數學科 (23題)
// 題目截圖來源：112會考數學題本.pdf（官方公版，2欄排版）
// 詳解截圖 + 正解字母來源：112會考數學解析.pdf（官方公版解答）
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'C', 3: 'B', 4: 'C', 5: 'B', 6: 'A', 7: 'A', 8: 'C', 9: 'B', 10: 'D',
  11: 'D', 12: 'A', 13: 'A', 14: 'B', 15: 'D', 16: 'C', 17: 'D', 18: 'B', 19: 'B', 20: 'C',
  21: 'D', 22: 'C', 23: 'B',
};

function groupIdFor(_qNo: number): string | undefined {
  return undefined;
}

export const MATH_112_QUESTIONS: Question[] = Array.from({ length: 23 }, (_, i) => {
  const qNo = i + 1;
  const padded = String(qNo).padStart(2, '0');
  return {
    id: `數學-112-${qNo}`,
    subject: '數學',
    year: 112,
    qNo,
    groupId: groupIdFor(qNo),
    imagePath: `${import.meta.env.BASE_URL}questions/math/112/q${padded}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/math/112/e${padded}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
