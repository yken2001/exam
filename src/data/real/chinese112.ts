import type { Question } from '../../types';

// 112年國中教育會考 國文科 選擇題 42 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 112會考國文解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'D', 2: 'D', 3: 'C', 4: 'C', 5: 'D', 6: 'C', 7: 'A', 8: 'A', 9: 'A', 10: 'D',
  11: 'C', 12: 'A', 13: 'B', 14: 'C', 15: 'B', 16: 'D', 17: 'A', 18: 'C', 19: 'A', 20: 'B',
  21: 'C', 22: 'D', 23: 'D', 24: 'B', 25: 'D', 26: 'A', 27: 'A', 28: 'B', 29: 'C', 30: 'A',
  31: 'C', 32: 'B', 33: 'C', 34: 'B', 35: 'B', 36: 'C', 37: 'B', 38: 'A', 39: 'D', 40: 'D',
  41: 'B', 42: 'D',
};

const GROUPS: [number, number][] = [[25, 26], [27, 29], [30, 31], [32, 33], [34, 35], [36, 38], [39, 40], [41, 42]];

// 這些題組的解析卷把整組的答案與解析寫在同一段，組內各題共用一張詳解圖
const SHARED_EXPLANATION: Record<number, number> = {
  26: 25, 28: 27, 29: 27, 31: 30, 33: 32, 35: 34, 37: 36, 38: 36, 40: 39, 42: 41,
};

function groupOf(qNo: number): [number, number] | undefined {
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}

const pad = (n: number) => String(n).padStart(2, '0');

export const CHINESE_112_QUESTIONS: Question[] = Array.from({ length: 42 }, (_, i) => {
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {
    id: `國文-112-${qNo}`,
    subject: '國文',
    year: 112,
    qNo,
    groupId: g ? `國文-112-g${g[0]}-${g[1]}` : undefined,
    imagePath: `${import.meta.env.BASE_URL}questions/chinese/112/q${pad(g ? g[0] : qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/chinese/112/e${pad(SHARED_EXPLANATION[qNo] ?? qNo)}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  };
});
