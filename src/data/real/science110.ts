import type { Question } from '../../types';

// 110年國中教育會考 自然科 (1~54題，全部選擇題；合科理化/生物/地科)
// 題目截圖來源：110會考自然題本.pdf（乾淨無正解）
// 詳解截圖 + 正解字母來源：110會考自然解析.pdf（翰林出版）
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'D', 3: 'B', 4: 'C', 5: 'D', 6: 'C', 7: 'A', 8: 'B', 9: 'B', 10: 'A',
  11: 'C', 12: 'D', 13: 'B', 14: 'A', 15: 'A', 16: 'C', 17: 'A', 18: 'C', 19: 'B', 20: 'C',
  21: 'D', 22: 'A', 23: 'C', 24: 'A', 25: 'A', 26: 'D', 27: 'D', 28: 'A', 29: 'D', 30: 'D',
  31: 'B', 32: 'B', 33: 'B', 34: 'A', 35: 'B', 36: 'D', 37: 'D', 38: 'C', 39: 'D', 40: 'D',
  41: 'A', 42: 'C', 43: 'B', 44: 'C', 45: 'A', 46: 'B', 47: 'A', 48: 'C', 49: 'C', 50: 'C',
  51: 'B', 52: 'B', 53: 'D', 54: 'B',
};

const GROUPS: [number, number][] = [[46, 47], [48, 49], [50, 51], [52, 54]];

function groupIdFor(qNo: number): string | undefined {
  const g = GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
  return g ? `自然-110-g${g[0]}-${g[1]}` : undefined;
}

export const SCIENCE_110_QUESTIONS: Question[] = Array.from({ length: 54 }, (_, i) => {
  const qNo = i + 1;
  const padded = String(qNo).padStart(2, '0');
  return {
    id: `自然-110-${qNo}`,
    subject: '自然',
    year: 110,
    qNo,
    groupId: groupIdFor(qNo),
    imagePath: `${import.meta.env.BASE_URL}questions/science/110/q${padded}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/science/110/e${padded}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
