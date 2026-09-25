import type { Question } from '../../types';

// 112年國中教育會考 數學科 選擇題 25 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 112會考數學解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'A', 2: 'C', 3: 'B', 4: 'C', 5: 'B', 6: 'A', 7: 'A', 8: 'C', 9: 'B', 10: 'D',
  11: 'D', 12: 'A', 13: 'A', 14: 'B', 15: 'D', 16: 'C', 17: 'D', 18: 'B', 19: 'B', 20: 'C',
  21: 'D', 22: 'C', 23: 'B', 24: 'D', 25: 'A',
};

const GROUPS: [number, number][] = [[24, 25]];

// 這些題組的解析卷把整組的答案與解析寫在同一段，組內各題共用一張詳解圖
const SHARED_EXPLANATION: Record<number, number> = {
  25: 24,
};

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const MATH_112_QUESTIONS: Question[] = Array.from({ length: 25 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `數學-112-${qNo}`,
    subject: '數學',
    year: 112,
    qNo,
    groupId: g ? `數學-112-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/math/112/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/math/112/e${pad(SHARED_EXPLANATION[qNo] ?? qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
