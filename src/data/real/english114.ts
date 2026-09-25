import type { Question } from '../../types';

// 114年國中教育會考 英文科 選擇題 43 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 114會考英文解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'D', 2: 'D', 3: 'C', 4: 'B', 5: 'D', 6: 'A', 7: 'A', 8: 'B', 9: 'D', 10: 'C',
  11: 'A', 12: 'D', 13: 'D', 14: 'A', 15: 'A', 16: 'D', 17: 'B', 18: 'A', 19: 'B', 20: 'B',
  21: 'B', 22: 'A', 23: 'C', 24: 'D', 25: 'C', 26: 'C', 27: 'A', 28: 'D', 29: 'C', 30: 'D',
  31: 'B', 32: 'D', 33: 'A', 34: 'B', 35: 'C', 36: 'C', 37: 'C', 38: 'B', 39: 'C', 40: 'C',
  41: 'A', 42: 'B', 43: 'A',
};

const GROUPS: [number, number][] = [[20, 21], [22, 23], [24, 25], [26, 28], [29, 31], [32, 34], [35, 37], [38, 43]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const ENGLISH_114_QUESTIONS: Question[] = Array.from({ length: 43 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `英文-114-${qNo}`,
    subject: '英文',
    year: 114,
    qNo,
    groupId: g ? `英文-114-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/english/114/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/english/114/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
