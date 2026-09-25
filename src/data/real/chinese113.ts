import type { Question } from '../../types';

// 113年國中教育會考 國文科 選擇題 42 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 113會考國文解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'D', 2: 'D', 3: 'B', 4: 'B', 5: 'C', 6: 'D', 7: 'B', 8: 'C', 9: 'B', 10: 'A',
  11: 'C', 12: 'C', 13: 'C', 14: 'B', 15: 'C', 16: 'D', 17: 'B', 18: 'A', 19: 'D', 20: 'A',
  21: 'C', 22: 'A', 23: 'D', 24: 'A', 25: 'A', 26: 'D', 27: 'A', 28: 'B', 29: 'D', 30: 'C',
  31: 'A', 32: 'A', 33: 'B', 34: 'D', 35: 'C', 36: 'C', 37: 'B', 38: 'B', 39: 'B', 40: 'C',
  41: 'D', 42: 'B',
};

const GROUPS: [number, number][] = [[25, 26], [27, 28], [29, 30], [31, 32], [33, 35], [36, 37], [38, 39], [40, 42]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const CHINESE_113_QUESTIONS: Question[] = Array.from({ length: 42 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `國文-113-${qNo}`,
    subject: '國文',
    year: 113,
    qNo,
    groupId: g ? `國文-113-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/chinese/113/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/chinese/113/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
