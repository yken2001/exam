import type { Question } from '../../types';

// 110年國中教育會考 社會科 (1~63題，全部選擇題；合科地理/歷史/公民)
// 題目截圖來源：110會考社會題本.pdf（乾淨無正解）
// 詳解截圖 + 正解字母來源：110會考社會解析.pdf（翰林出版）
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'C', 2: 'B', 3: 'B', 4: 'A', 5: 'B', 6: 'B', 7: 'A', 8: 'C', 9: 'B', 10: 'A',
  11: 'C', 12: 'A', 13: 'D', 14: 'A', 15: 'D', 16: 'B', 17: 'C', 18: 'D', 19: 'B', 20: 'D',
  21: 'D', 22: 'C', 23: 'B', 24: 'D', 25: 'C', 26: 'B', 27: 'D', 28: 'B', 29: 'C', 30: 'C',
  31: 'B', 32: 'A', 33: 'A', 34: 'D', 35: 'D', 36: 'C', 37: 'C', 38: 'C', 39: 'D', 40: 'B',
  41: 'C', 42: 'B', 43: 'B', 44: 'A', 45: 'D', 46: 'C', 47: 'A', 48: 'D', 49: 'A', 50: 'D',
  51: 'B', 52: 'A', 53: 'B', 54: 'B', 55: 'C', 56: 'A', 57: 'B', 58: 'C', 59: 'B', 60: 'A',
  61: 'C', 62: 'C', 63: 'D',
};

const GROUPS: [number, number][] = [[56, 57], [58, 60], [61, 63]];

function groupIdFor(qNo: number): string | undefined {
  const g = GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
  return g ? `社會-110-g${g[0]}-${g[1]}` : undefined;
}

export const SOCIAL_110_QUESTIONS: Question[] = Array.from({ length: 63 }, (_, i) => {
  const qNo = i + 1;
  const padded = String(qNo).padStart(2, '0');
  return {
    id: `社會-110-${qNo}`,
    subject: '社會',
    year: 110,
    qNo,
    groupId: groupIdFor(qNo),
    imagePath: `${import.meta.env.BASE_URL}questions/社會/110/q${padded}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/社會/110/e${padded}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
