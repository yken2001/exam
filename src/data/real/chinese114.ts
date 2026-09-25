import type { Question } from '../../types';

// 114年國中教育會考 國文科 選擇題 42 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 114會考國文解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'D', 2: 'B', 3: 'B', 4: 'B', 5: 'A', 6: 'A', 7: 'B', 8: 'C', 9: 'C', 10: 'A',
  11: 'D', 12: 'C', 13: 'C', 14: 'A', 15: 'A', 16: 'A', 17: 'C', 18: 'D', 19: 'A', 20: 'D',
  21: 'D', 22: 'B', 23: 'D', 24: 'B', 25: 'B', 26: 'A', 27: 'B', 28: 'C', 29: 'C', 30: 'D',
  31: 'C', 32: 'C', 33: 'D', 34: 'A', 35: 'D', 36: 'B', 37: 'C', 38: 'A', 39: 'D', 40: 'B',
  41: 'D', 42: 'B',
};

const GROUPS: [number, number][] = [[25, 26], [27, 28], [29, 31], [32, 33], [34, 35], [36, 37], [38, 39], [40, 42]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const CHINESE_114_QUESTIONS: Question[] = Array.from({ length: 42 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `國文-114-${qNo}`,
    subject: '國文',
    year: 114,
    qNo,
    groupId: g ? `國文-114-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/chinese/114/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/chinese/114/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
