"""英語聽力: cut the 21 listening questions of a year out of its 解析 PDF.

Two layouts:
  112 (official, inside 112會考英文解析.pdf, before 四、單一選擇題):
      sections 一、辨識句意 / 二、基本問答 / 三、言談理解, each numbered from
      1 as "N."; red 答案:(X) / 解析:... / 錄音稿:...
  113 (翰林, its own 113會考英聽解析.pdf):
      "第一部分:辨識句意(第1-3題)" ..., markers "( C )第1題" numbered
      1-21 with the answer printed in the marker; red 【聽力稿】 transcript,
      【題目中譯】/【中譯】, 【試題解析】... 故選【C】.
Every item has three options (pictures in 辨識句意). Writes question and
explanation images plus tools/bank/<year>_listening.json (answers and the
speaker-tagged transcripts gen_audio.py reads).

  python build_listening.py 112|113
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

SECTIONS = ('辨識句意', '基本問答', '言談理解')
# W/M: woman/man; M1, M2 (115 Q21: several people interviewed) are men;
# Anchor (a news anchor) gets the plain voice like a narrator
SPEAKER = re.compile(r'^(W\d?|M\d?|Q|Question|Anchor)\s*[:：]\s*')
VOICE = {'Question': 'Q', 'Anchor': 'N'}

FORMATS = {
    112: {
        'pdf': '112會考英文解析.pdf',
        'stop_at': '單一選擇題',
        'section': re.compile(r'^[一二三]\s*、\s*(辨識句意|基本問答|言談理解)'),
        'marker': re.compile(r'^(\d{1,2})\s*\.$'),
        'local_numbering': True,
        'answer': lambda t: re.findall(r'答案[:：]\(([A-C])\)', t),
        'transcript_start': '錄音稿',
    },
    113: {
        'pdf': '113會考英聽解析.pdf',
        'stop_at': None,
        'section': re.compile(r'^第[一二三]部分\s*[:：]\s*(辨識句意|基本問答|言談理解)'),
        'marker': re.compile(r'^[\(（]\s*([A-C])\s*[\)）]\s*第\s*(\d{1,2})\s*題$'),
        'local_numbering': False,
        # 故選【C】/ 唯一答案為【A】/ 故答案選【B】: the last 【X】 of 【試題解析】
        'answer': lambda t: re.findall(r'【([A-C])】', t.split('【試題解析】')[-1])[-1:],
        'transcript_start': '【聽力稿】',
    },
}
# 114, 115: separate 翰林 英聽解析卷 in the same layout as 113
for _y in (114, 115):
    FORMATS[_y] = dict(FORMATS[113], pdf=f'{_y}會考英聽解析.pdf')


def parse_transcript(text_lines):
    """['W: Hey, Ted.  What did', 'the teacher say?', 'M: ...'] ->
    [('W', 'Hey, Ted. What did the teacher say?'), ('M', ...)]"""
    segs = []
    for t in text_lines:
        t = t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
        m = SPEAKER.match(t)
        if m:
            segs.append([VOICE.get(m.group(1), m.group(1)[0]), t[m.end():]])
        elif segs:
            segs[-1][1] += ' ' + t
        else:
            segs.append(['N', t])       # single narrator line (辨識句意、基本問答)
    out = []
    for who, s in segs:
        s = re.sub(r'\s+', ' ', s).strip()
        s = re.sub(r"\s+'s\b", "'s", s)                                 # "girl 's head"
        s = re.sub(r'\((?:sound|sounds) of [^)]*\)', '', s).strip()      # stage directions
        s = re.sub(r'\[[^\]]*\]\s*', '', s).strip()                        # 114 Q21 "[singing]"
        if s:
            out.append((who, s))
    return out


def transcript_lines(expl_lines, start_tag):
    k = next((j for j, t in enumerate(expl_lines) if t.startswith(start_tag) or start_tag in t[:6]), None)
    if k is None:
        return None
    first = expl_lines[k].split(start_tag, 1)[1].lstrip(':：')
    out = [first] if first.strip() else []
    for t in expl_lines[k + 1:]:
        if t.startswith('【'):          # 113: 【題目中譯】/【中譯】 ends the transcript
            break
        out.append(t)
    return [t.strip() for t in out if t.strip()]


def main(year):
    fmt = FORMATS[year]
    pdf = os.path.join(DL, fmt['pdf'])
    doc, edoc, qdoc = fitz.open(pdf), fitz.open(pdf), fitz.open(pdf)
    rules = {'mid': doc[0].rect.width / 2}
    pieces, lines, _ = B.reflow(doc, rules, mask_docs=(edoc, qdoc))
    end = len(lines)
    if fmt['stop_at']:
        end = next(i for i, l in enumerate(lines) if fmt['stop_at'] in l.text)
    base = B.column_text_base(lines)

    sections, markers = [], []        # markers: (stream idx, section, local no, letter)
    sec, local, glob = None, 0, 0
    for i in range(end):
        l = lines[i]
        if l.red >= 0.5 or l.is_image:
            continue
        m = fmt['section'].match(l.text)
        if m:
            sections.append(i)
            sec, local = m.group(1), 0
            continue
        m = fmt['marker'].match(l.text)
        if not m or not sec or l.x0 - base[l.col] >= 12:
            continue
        if fmt['local_numbering'] and int(m.group(1)) == local + 1:
            local += 1
            markers.append((i, sec, local, ''))
        elif not fmt['local_numbering'] and int(m.group(2)) == glob + 1:
            glob += 1
            local += 1
            markers.append((i, sec, local, m.group(1)))

    events = sorted([i for i, _, _, _ in markers] + sections + [end])
    nxt = lambda i: next(e for e in events if e > i)
    questions, errors = [], []
    for n, (m, sec, local, letter) in enumerate(markers, start=1):
        stop = nxt(m)
        red = next((j for j in range(m + 1, stop) if lines[j].red >= 0.5), None)
        if red is None:
            errors.append(f'Q{n}: no red explanation')
            continue
        expl_lines = [lines[j].text for j in range(red, stop) if lines[j].red >= 0.5]
        am = fmt['answer'](''.join(expl_lines).replace(' ', ''))
        tl = transcript_lines(expl_lines, fmt['transcript_start'])
        if not am or not tl:
            errors.append(f'Q{n}: answer={bool(am)} transcript={bool(tl)}')
            continue
        if letter and letter != am[0]:
            errors.append(f'Q{n}: marker says {letter}, explanation says {am[0]}')
        questions.append({'qno': n, 'section': sec, 'local': local, 'marker': m, 'letter': letter,
                          'stem': (m, red), 'expl': (red, stop), 'answer': letter or am[0],
                          'transcript': parse_transcript(tl)})

    counts = {s: sum(1 for q in questions if q['section'] == s) for s in SECTIONS}
    if len(questions) != 21 or counts != {'辨識句意': 3, '基本問答': 8, '言談理解': 10}:
        errors.append(f'expected 3+8+10=21 questions, got {counts}')
    for q in questions:
        if not q['transcript'] or any(re.search(r'[一-鿿]', s) for _, s in q['transcript']):
            errors.append(f"Q{q['qno']}: transcript empty or contains Chinese: {q['transcript']}")
        if q['section'] == '言談理解' and not any(w == 'Q' for w, _ in q['transcript']):
            errors.append(f"Q{q['qno']}: 言談理解 transcript has no question line")
        # anything TTS would read out that is not speech: an unknown speaker
        # tag ("Anchor:", "M1:" before they were known) or a [stage direction]
        for _, s in q['transcript']:
            if re.search(r'(^|\s)[A-Z][A-Za-z]{0,7}\d?[:：]\S|[\[\]]', s):
                errors.append(f"Q{q['qno']}: speaker tag or [direction] left in the text: {s[:60]}")
    if errors:
        print('\n'.join(errors))
        sys.exit(1)

    # paint the printed answer letter out of the question images (113)
    B.mask_answer_letters(qdoc, lines, [B.Question(q['qno'], q['marker'], letter=q['letter'])
                                        for q in questions if q['letter']])
    B.whiten_red(qdoc, lines)

    qdir = os.path.join(PUBLIC, 'questions', 'listening', str(year))
    edir = os.path.join(PUBLIC, 'explanations', 'listening', str(year))
    for d in (qdir, edir):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    for q in questions:
        n = q['qno']
        B.stitch(B.render_region(qdoc, pieces, lines, q['stem'], end, DPI, lift=True), os.path.join(qdir, f'q{n:02d}.png'))
        B.stitch(B.render_region(edoc, pieces, lines, q['expl'], end, DPI), os.path.join(edir, f'e{n:02d}.png'))

    bank = {'year': year, 'subject': '英聽', 'count': len(questions),
            'answers': {q['qno']: q['answer'] for q in questions},
            'sections': {q['qno']: f"{q['section']} 第{q['local']}題" for q in questions},
            'transcripts': {q['qno']: q['transcript'] for q in questions}}
    with open(os.path.join(BANK_DIR, f'{year}_listening.json'), 'w', encoding='utf-8') as f:
        json.dump(bank, f, ensure_ascii=False, indent=1)
    print(f'ok: {year} {len(questions)} listening questions {counts}')


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 112)
