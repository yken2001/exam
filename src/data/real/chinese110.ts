import type { Question } from '../../types';

// 110年國中教育會考 國文科 (1~48題，全部選擇題)
// 題目截圖來源：110會考國文題本.pdf（乾淨無正解）
// 詳解截圖 + 正解字母來源：110會考國文解析.pdf（翰林出版）
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
//
// 33~48題為題組（共用一篇選文/表格的數道子題），同一組的題目共用同一張
// 題目截圖與同一張詳解截圖（裁切時已把選文包含在內），並共用同一個 groupId，
// 讓抽題引擎與排版都把它們視為一個不可分拆的單位。
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'D', 3: 'C', 4: 'B', 5: 'C', 6: 'A', 7: 'A', 8: 'D', 9: 'D', 10: 'B',
  11: 'B', 12: 'B', 13: 'A', 14: 'B', 15: 'C', 16: 'B', 17: 'A', 18: 'D', 19: 'C', 20: 'D',
  21: 'B', 22: 'D', 23: 'A', 24: 'D', 25: 'B', 26: 'C', 27: 'A', 28: 'B', 29: 'D', 30: 'C',
  31: 'D', 32: 'D', 33: 'D', 34: 'C', 35: 'C', 36: 'B', 37: 'B', 38: 'A', 39: 'A', 40: 'C',
  41: 'B', 42: 'A', 43: 'B', 44: 'D', 45: 'A', 46: 'D', 47: 'C', 48: 'D',
};

const GROUPS: [number, number][] = [
  [33, 34], [35, 36], [37, 38], [39, 41], [42, 43], [44, 45], [46, 48],
];

function groupIdFor(qNo: number): string | undefined {
  const g = GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
  return g ? `國文-110-g${g[0]}-${g[1]}` : undefined;
}

export const CHINESE_110_QUESTIONS: Question[] = Array.from({ length: 48 }, (_, i) => {
  const qNo = i + 1;
  const padded = String(qNo).padStart(2, '0');
  return {
    id: `國文-110-${qNo}`,
    subject: '國文',
    year: 110,
    qNo,
    groupId: groupIdFor(qNo),
    imagePath: `/questions/國文/110/q${padded}.png`,
    explanationImagePath: `/explanations/國文/110/e${padded}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
