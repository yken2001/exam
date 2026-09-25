import type { Question } from '../../types';

// 112年國中教育會考 社會科 選擇題 54 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 112會考社會解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'C', 2: 'D', 3: 'A', 4: 'A', 5: 'A', 6: 'C', 7: 'C', 8: 'D', 9: 'C', 10: 'C',
  11: 'B', 12: 'D', 13: 'A', 14: 'B', 15: 'A', 16: 'C', 17: 'A', 18: 'A', 19: 'D', 20: 'A',
  21: 'B', 22: 'D', 23: 'B', 24: 'B', 25: 'A', 26: 'B', 27: 'D', 28: 'B', 29: 'A', 30: 'D',
  31: 'C', 32: 'D', 33: 'B', 34: 'D', 35: 'D', 36: 'C', 37: 'B', 38: 'D', 39: 'A', 40: 'A',
  41: 'C', 42: 'D', 43: 'C', 44: 'C', 45: 'D', 46: 'B', 47: 'C', 48: 'D', 49: 'B', 50: 'A',
  51: 'A', 52: 'D', 53: 'B', 54: 'C',
};

const GROUPS: [number, number][] = [[44, 45], [46, 48], [49, 51], [52, 54]];

// 這些題組的解析卷把整組的答案與解析寫在同一段，組內各題共用一張詳解圖
const SHARED_EXPLANATION: Record<number, number> = {
  45: 44, 47: 46, 48: 46, 50: 49, 51: 49, 53: 52, 54: 52,
};

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const SOCIAL_112_QUESTIONS: Question[] = Array.from({ length: 54 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `社會-112-${qNo}`,
    subject: '社會',
    year: 112,
    qNo,
    groupId: g ? `社會-112-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/social/112/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/social/112/e${pad(SHARED_EXPLANATION[qNo] ?? qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
