import type { Question } from '../../types';

// 115年國中教育會考 英語聽力 21 題 -- 由 tools/build_listening.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解（含錄音稿）與正解取自 115會考英聽解析.pdf；
// 語音由 tools/gen_audio.py 依錄音稿以語音合成產生（非會考原音）。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {
  1: 'C', 2: 'C', 3: 'C', 4: 'B', 5: 'B', 6: 'C', 7: 'A', 8: 'A', 9: 'A', 10: 'B',
  11: 'B', 12: 'A', 13: 'A', 14: 'B', 15: 'A', 16: 'C', 17: 'B', 18: 'A', 19: 'A', 20: 'B',
  21: 'A',
};

const pad = (n: number) => String(n).padStart(2, '0');

export const LISTENING_115_QUESTIONS: Question[] = Array.from({ length: 21 }, (_, i) => {
  const qNo = i + 1;
  return {
    id: `英聽-115-${qNo}`,
    subject: '英聽',
    year: 115,
    qNo,
    imagePath: `${import.meta.env.BASE_URL}questions/listening/115/q${pad(qNo)}.png`,
    explanationImagePath: `${import.meta.env.BASE_URL}explanations/listening/115/e${pad(qNo)}.png`,
    audioPath: `${import.meta.env.BASE_URL}audio/listening/115/a${pad(qNo)}.wav`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 3,
  };
});
