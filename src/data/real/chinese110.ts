import type { Question } from '../../types';

// 110年國中教育會考 國文科 選擇題 48 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 110會考國文解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'D', 3: 'C', 4: 'B', 5: 'C', 6: 'A', 7: 'A', 8: 'D', 9: 'D', 10: 'B',
  11: 'B', 12: 'B', 13: 'A', 14: 'B', 15: 'C', 16: 'B', 17: 'A', 18: 'D', 19: 'C', 20: 'D',
  21: 'B', 22: 'D', 23: 'A', 24: 'D', 25: 'B', 26: 'C', 27: 'A', 28: 'B', 29: 'D', 30: 'C',
  31: 'D', 32: 'D', 33: 'D', 34: 'C', 35: 'C', 36: 'B', 37: 'B', 38: 'A', 39: 'A', 40: 'C',
  41: 'B', 42: 'A', 43: 'B', 44: 'D', 45: 'A', 46: 'D', 47: 'C', 48: 'D',
};

const GROUPS: [number, number][] = [[33, 34], [35, 36], [37, 38], [39, 41], [42, 43], [44, 45], [46, 48]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const CHINESE_110_QUESTIONS: Question[] = Array.from({ length: 48 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `國文-110-${qNo}`,
    subject: '國文',
    year: 110,
    qNo,
    groupId: g ? `國文-110-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/chinese/110/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/chinese/110/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
