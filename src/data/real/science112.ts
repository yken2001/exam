import type { Question } from '../../types';

// 112年國中教育會考 自然科 選擇題 50 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 112會考自然解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'D', 2: 'B', 3: 'D', 4: 'C', 5: 'A', 6: 'A', 7: 'B', 8: 'C', 9: 'C', 10: 'B',
  11: 'D', 12: 'A', 13: 'A', 14: 'B', 15: 'B', 16: 'A', 17: 'B', 18: 'A', 19: 'C', 20: 'B',
  21: 'D', 22: 'B', 23: 'C', 24: 'D', 25: 'D', 26: 'A', 27: 'A', 28: 'A', 29: 'B', 30: 'C',
  31: 'C', 32: 'C', 33: 'C', 34: 'D', 35: 'C', 36: 'A', 37: 'B', 38: 'D', 39: 'D', 40: 'A',
  41: 'A', 42: 'D', 43: 'A', 44: 'D', 45: 'C', 46: 'B', 47: 'B', 48: 'B', 49: 'A', 50: 'C',
};

const GROUPS: [number, number][] = [[43, 44], [45, 46], [47, 48], [49, 50]];

// 這些題組的解析卷把整組的答案與解析寫在同一段，組內各題共用一張詳解圖
const SHARED_EXPLANATION: Record<number, number> = {
  44: 43, 46: 45, 48: 47, 50: 49,
};

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const SCIENCE_112_QUESTIONS: Question[] = Array.from({ length: 50 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `自然-112-${qNo}`,
    subject: '自然',
    year: 112,
    qNo,
    groupId: g ? `自然-112-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/science/112/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/science/112/e${pad(SHARED_EXPLANATION[qNo] ?? qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
