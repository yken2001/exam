import type { Question } from '../../types';

// 112年國中教育會考 英語聽力 21 題 -- 由 tools/build_listening.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解（含錄音稿）與正解取自 112會考英文解析.pdf；
// 語音由 tools/gen_audio.py 依錄音稿以語音合成產生（非會考原音）。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'C', 2: 'A', 3: 'B', 4: 'C', 5: 'C', 6: 'B', 7: 'A', 8: 'B', 9: 'C', 10: 'B',
  11: 'C', 12: 'C', 13: 'B', 14: 'A', 15: 'A', 16: 'A', 17: 'B', 18: 'A', 19: 'C', 20: 'C',
  21: 'A',
};

const pad = (n: number) => String(n).padStart(2, '0');

export const LISTENING_112_QUESTIONS: Question[] = Array.from({ length: 21 }, (_, i) => {
  const qNo = i + 1;
  return {
    id: `英聽-112-${qNo}`,
    subject: '英聽',
    year: 112,
    qNo,
    imagePath: `${import.meta.env.BASE_URL}questions/listening/112/q${pad(qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/listening/112/e${pad(qNo)}.png`,
    audioPath: `${import.meta.env.BASE_URL}audio/listening/112/a${pad(qNo)}.wav`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 3,
  };
});
