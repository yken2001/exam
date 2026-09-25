import type { Question } from '../../types';

// 111年國中教育會考 社會科 選擇題 54 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 111會考社會解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'C', 2: 'B', 3: 'C', 4: 'A', 5: 'D', 6: 'B', 7: 'C', 8: 'C', 9: 'B', 10: 'C',
  11: 'B', 12: 'A', 13: 'B', 14: 'C', 15: 'D', 16: 'C', 17: 'B', 18: 'C', 19: 'C', 20: 'A',
  21: 'B', 22: 'D', 23: 'D', 24: 'B', 25: 'C', 26: 'B', 27: 'D', 28: 'D', 29: 'D', 30: 'B',
  31: 'D', 32: 'A', 33: 'A', 34: 'D', 35: 'D', 36: 'D', 37: 'C', 38: 'C', 39: 'C', 40: 'D',
  41: 'B', 42: 'D', 43: 'A', 44: 'B', 45: 'B', 46: 'A', 47: 'A', 48: 'B', 49: 'C', 50: 'D',
  51: 'C', 52: 'A', 53: 'B', 54: 'A',
};

const GROUPS: [number, number][] = [[44, 45], [46, 48], [49, 51], [52, 54]];

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const SOCIAL_111_QUESTIONS: Question[] = Array.from({ length: 54 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `社會-111-${qNo}`,
    subject: '社會',
    year: 111,
    qNo,
    groupId: g ? `社會-111-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/social/111/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/social/111/e${pad(qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
