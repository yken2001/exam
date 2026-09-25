"""112 英語聽力: cut the 21 listening questions out of 112會考英文解析.pdf.

The listening part comes before 四、單一選擇題: three sections
(一、辨識句意 / 二、基本問答 / 三、言談理解), each numbered from 1, every
item = "N." + three options (pictures in section 一), then in red
答案:(X) / 解析:... / 錄音稿:... . Questions are renumbered 1-21.
Writes question/explanation images plus tools/bank/112_listening.json
with answers and parsed transcripts (speaker-tagged) for gen_audio.py.
"""
import json
import os
import re
import shutil
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_lib as B
from build_bank import DL, PUBLIC, BANK_DIR, DPI

SECTION = re.compile(r'^([一二三])\s*、\s*(辨識句意|基本問答|言談理解)')
MARKER = re.compile(r'^(\d{1,2})\s*\.$')
SPEAKER = re.compile(r'^(W|M|Q)\s*:\s*')
ANSWER = re.compile(r'答案[:：]\s*\(([A-C])\)')


def parse_transcript(text_lines):
    """['W: Hey, Ted.  What did', 'the teacher say?', 'M: ...'] ->
    [('W', 'Hey, Ted. What did the teacher say?'), ('M', ...)]"""
    segs = []
    for t in text_lines:
        t = t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
        m = SPEAKER.match(t)
        if m:
            segs.append([m.group(1), t[m.end():]])
        elif segs:
            segs[-1][1] += ' ' + t
        else:
            segs.append(['N', t])       # single narrator line (sections 一、二)
    out = []
    for who, s in segs:
        s = re.sub(r'\s+', ' ', s).strip()
        s = re.sub(r'\((?:sound|sounds) of [^)]*\)', '', s).strip()   # stage directions
        if s:
            out.append((who, s))
    return out


def main():
    pdf = os.path.join(DL, '112會考英文解析.pdf')
    doc, edoc, qdoc = fitz.open(pdf), fitz.open(pdf), fitz.open(pdf)
    rules = {'mid': doc[0].rect.width / 2}
    pieces, lines, _ = B.reflow(doc, rules, mask_docs=(edoc, qdoc))
    end = next(i for i, l in enumerate(lines) if '單一選擇題' in l.text)
    base = B.column_text_base(lines)

    sections, markers = [], []        # stream indices
    sec, local = None, 0
    for i in range(end):
        l = lines[i]
        if l.red >= 0.5 or l.is_image:
            continue
        m = SECTION.match(l.text)
        if m:
            sections.append(i)
            sec, local = m.group(2), 0
            continue
        m = MARKER.match(l.text)
        if m and sec and int(m.group(1)) == local + 1 and l.x0 - base[l.col] < 12:
            local += 1
            markers.append((i, sec, local))

    events = sorted([i for i, _, _ in markers] + sections + [end])
    nxt = lambda i: next(e for e in events if e > i)
    questions, errors = [], []
    for n, (m, sec, local) in enumerate(markers, start=1):
        stop = nxt(m)
        red = next((j for j in range(m + 1, stop) if lines[j].red >= 0.5), None)
        if red is None:
            errors.append(f'Q{n}: no red explanation')
            continue
        expl_lines = [lines[j].text for j in range(red, stop) if lines[j].red >= 0.5]
        joined = ''.join(expl_lines)
        am = ANSWER.search(joined)
        k = next((j for j, t in enumerate(expl_lines) if t.startswith('錄音稿')), None)
        if not am or k is None:
            errors.append(f'Q{n}: answer={bool(am)} transcript={k is not None}')
            continue
        tlines = [expl_lines[k].split(':', 1)[1] if ':' in expl_lines[k] else expl_lines[k][4:]]
        tlines += expl_lines[k + 1:]
        questions.append({'qno': n, 'section': sec, 'local': local, 'stem': (m, red),
                          'expl': (red, stop), 'answer': am.group(1),
                          'transcript': parse_transcript([t.strip() for t in tlines if t.strip()])})

    counts = {s: sum(1 for q in questions if q['section'] == s) for s in ('辨識句意', '基本問答', '言談理解')}
    if len(questions) != 21 or counts != {'辨識句意': 3, '基本問答': 8, '言談理解': 10}:
        errors.append(f'expected 3+8+10=21 questions, got {counts}')
    for q in questions:
        if not q['transcript'] or any(re.search(r'[一-鿿]', s) for _, s in q['transcript']):
            errors.append(f"Q{q['qno']}: transcript empty or contains Chinese: {q['transcript']}")
        if q['section'] == '言談理解' and not any(w == 'Q' for w, _ in q['transcript']):
            errors.append(f"Q{q['qno']}: 言談理解 transcript has no Q: line")
    if errors:
        print('\n'.join(errors))
        sys.exit(1)

    qdir = os.path.join(PUBLIC, 'questions', 'listening', '112')
    edir = os.path.join(PUBLIC, 'explanations', 'listening', '112')
    for d in (qdir, edir):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    for q in questions:
        n = q['qno']
        B.stitch(B.render_region(qdoc, pieces, lines, q['stem'], end, DPI), os.path.join(qdir, f'q{n:02d}.png'))
        B.stitch(B.render_region(edoc, pieces, lines, q['expl'], end, DPI), os.path.join(edir, f'e{n:02d}.png'))

    bank = {'year': 112, 'subject': '英聽', 'count': len(questions),
            'answers': {q['qno']: q['answer'] for q in questions},
            'sections': {q['qno']: f"{q['section']} 第{q['local']}題" for q in questions},
            'transcripts': {q['qno']: q['transcript'] for q in questions}}
    with open(os.path.join(BANK_DIR, '112_listening.json'), 'w', encoding='utf-8') as f:
        json.dump(bank, f, ensure_ascii=False, indent=1)
    print(f'ok: {len(questions)} listening questions {counts}')


if __name__ == '__main__':
    main()
