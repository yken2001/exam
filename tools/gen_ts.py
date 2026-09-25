"""Write src/data/real/{subject}{year}.ts from tools/bank/*.json.

Never edit those .ts files by hand -- rerun build_bank.py then this script.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REAL = os.path.join(os.path.dirname(HERE), 'src', 'data', 'real')
SUBJ = {'chinese': '國文', 'english': '英文', 'math': '數學', 'science': '自然', 'social': '社會'}
YEARS = [110, 111, 112]


def ts_record(d):
    items = [f'{k}: {v!r}' for k, v in sorted(d.items())]
    rows = [', '.join(items[i:i + 10]) for i in range(0, len(items), 10)]
    return '{\n' + ''.join(f'  {r},\n' for r in rows) + '}'


def gen(year, en):
    bank = json.load(open(os.path.join(HERE, 'bank', f'{year}_{en}.json'), encoding='utf-8'))
    zh = SUBJ[en]
    n = bank['count']
    answers = {int(k): v for k, v in bank['answers'].items()}
    assert sorted(answers) == list(range(1, n + 1)), f'{year} {en}: answers not 1..{n}'
    assert all(v in 'ABCD' and v for v in answers.values())
    qfile = {int(k): v for k, v in bank['question_file'].items()}
    efile = {int(k): v for k, v in bank['explanation_file'].items()}
    shared_e = {k: v for k, v in efile.items() if k != v}
    groups = bank['groups']
    const = f'{en.upper()}_{year}_QUESTIONS'

    src = f"""import type {{ Question }} from '../../types';

// {year}年國中教育會考 {zh}科 選擇題 {n} 題 -- 由 tools/build_bank.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解截圖與正解皆取自 {year}會考{zh}解析.pdf。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {ts_record(answers)};

const GROUPS: [number, number][] = {json.dumps(groups)};
"""
    if shared_e:
        src += f"""
// 這些題組的解析卷把整組的答案與解析寫在同一段，組內各題共用一張詳解圖
const SHARED_EXPLANATION: Record<number, number> = {ts_record(shared_e)};
"""
    src += f"""
function groupOf(qNo: number): [number, number] | undefined {{
  return GROUPS.find(([a, b]) => qNo >= a && qNo <= b);
}}

const pad = (n: number) => String(n).padStart(2, '0');

export const {const}: Question[] = Array.from({{ length: {n} }}, (_, i) => {{
  const qNo = i + 1;
  const g = groupOf(qNo);
  return {{
    id: `{zh}-{year}-${{qNo}}`,
    subject: '{zh}',
    year: {year},
    qNo,
    groupId: g ? `{zh}-{year}-g${{g[0]}}-${{g[1]}}` : undefined,
    imagePath: `${{import.meta.env.BASE_URL}}questions/{en}/{year}/q${{pad(g ? g[0] : qNo)}}.png`,
    explanationImagePath: `${{import.meta.env.BASE_URL}}explanations/{en}/{year}/e${{pad({'SHARED_EXPLANATION[qNo] ?? qNo' if shared_e else 'qNo'})}}.png`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 4,
  }};
}});
"""
    # the group image is keyed by the group's first question
    for q, f in qfile.items():
        g = next((a for a, b in groups if a <= q <= b), None)
        assert f == (g if g else q), f'{year} {en} Q{q}: question file mismatch'
    with open(os.path.join(REAL, f'{en}{year}.ts'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(src)
    return n


def gen_listening():
    bank = json.load(open(os.path.join(HERE, 'bank', '112_listening.json'), encoding='utf-8'))
    n = bank['count']
    answers = {int(k): v for k, v in bank['answers'].items()}
    assert sorted(answers) == list(range(1, n + 1)) and all(v in 'ABC' for v in answers.values())
    src = f"""import type {{ Question }} from '../../types';

// 112年國中教育會考 英語聽力 {n} 題 -- 由 tools/build_listening.py + tools/gen_ts.py
// 自動產生，請勿手動修改。題目、詳解（含錄音稿）與正解取自 112會考英文解析.pdf；
// 語音由 tools/gen_audio.py 依錄音稿以語音合成產生（非會考原音）。
// 版權屬原出版社所有，僅供個人練習使用，不可公開散布。
const ANSWERS: Record<number, string> = {ts_record(answers)};

const pad = (n: number) => String(n).padStart(2, '0');

export const LISTENING_112_QUESTIONS: Question[] = Array.from({{ length: {n} }}, (_, i) => {{
  const qNo = i + 1;
  return {{
    id: `英聽-112-${{qNo}}`,
    subject: '英聽',
    year: 112,
    qNo,
    imagePath: `${{import.meta.env.BASE_URL}}questions/listening/112/q${{pad(qNo)}}.png`,
    explanationImagePath: `${{import.meta.env.BASE_URL}}explanations/listening/112/e${{pad(qNo)}}.png`,
    audioPath: `${{import.meta.env.BASE_URL}}audio/listening/112/a${{pad(qNo)}}.wav`,
    correctAnswer: ANSWERS[qNo],
    optionCount: 3,
  }};
}});
"""
    with open(os.path.join(REAL, 'listening112.ts'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(src)
    return n


if __name__ == '__main__':
    total = 0
    for y in YEARS:
        for en in SUBJ:
            total += gen(y, en)
    total += gen_listening()
    print('questions written:', total)
