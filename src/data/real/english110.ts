import type { Question } from '../../types';

// 110年國中教育會考 英語科閱讀 (1~41題，全部選擇題；聽力測驗不收錄)
// 題目截圖來源：110會考英文題本.pdf（乾淨無正解）
// 詳解截圖 + 正解字母來源：110會考英文解析.pdf（翰林出版）
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
//
// 15~41題為題組（共用一篇文章/廣告/對話的數道子題），同一組共用同一張
// 題目截圖與同一張詳解截圖，並共用同一個 groupId。
const ANSWERS: Record<number, string> = {
  1: 'D', 2: 'C', 3: 'D', 4: 'A', 5: 'C', 6: 'B', 7: 'D', 8: 'B', 9: 'B', 10: 'A',
  11: 'C', 12: 'C', 13: 'B', 14: 'A', 15: 'B', 16: 'D', 17: 'B', 18: 'C', 19: 'A', 20: 'C',
  21: 'C', 22: 'A', 23: 'D', 24: 'C', 25: 'B', 26: 'A', 27: 'B', 28: 'C', 29: 'D', 30: 'D',
  31: 'A', 32: 'D', 33: 'B', 34: 'A', 35: 'D', 36: 'A', 37: 'C', 38: 'C', 39: 'A', 40: 'B',
  41: 'A',
};

const GROUPS: [number, number][] = [
  [15, 16], [17, 18], [19, 21], [22, 24], [25, 28], [29, 31], [32, 34], [35, 37], [38, 41],
];

function groupIdFor(qNo: number): string | undefined {
  const g = GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
  return g ? `英文-110-g${g[0]}-${g[1]}` : undefined;
}

export const ENGLISH_110_QUESTIONS: Question[] = Array.from({ length: 41 }, (_, i) => {
  const qNo = i + 1;
  const padded = String(qNo).padStart(2, '0');
  return {
    id: `英文-110-${qNo}`,
    subject: '英文',
    year: 110,
    qNo,
    groupId: groupIdFor(qNo),
    imagePath: `/questions/英文/110/q${padded}.png`,
    explanationImagePath: `/explanations/英文/110/e${padded}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
