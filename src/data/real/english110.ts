import type { Question } from '../../types';

// 110年國中教育會考 英文科 選擇題 41 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 110會考英文解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'D', 2: 'C', 3: 'D', 4: 'A', 5: 'C', 6: 'B', 7: 'D', 8: 'B', 9: 'B', 10: 'A',
  11: 'C', 12: 'C', 13: 'B', 14: 'A', 15: 'B', 16: 'D', 17: 'B', 18: 'C', 19: 'A', 20: 'C',
  21: 'C', 22: 'A', 23: 'D', 24: 'C', 25: 'B', 26: 'A', 27: 'B', 28: 'C', 29: 'D', 30: 'D',
  31: 'A', 32: 'D', 33: 'B', 34: 'A', 35: 'D', 36: 'A', 37: 'C', 38: 'C', 39: 'A', 40: 'B',
  41: 'A',
};

const GROUPS: [number, number][] = [[15, 16], [17, 18], [19, 21], [22, 24], [25, 28], [29, 31], [32, 34], [35, 37], [38, 41]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const ENGLISH_110_QUESTIONS: Question[] = Array.from({ length: 41 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `英文-110-${qNo}`,
    subject: '英文',
    year: 110,
    qNo,
    groupId: g ? `英文-110-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/english/110/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/english/110/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
