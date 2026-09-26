"""Consistency check of the AI-made practice sets (src/data/ai/*.json).

Whether each answer is *right* is checked by independent solvers (see the
set's "verification" record); this script checks that the file itself is
consistent, so an edit cannot leave it half-changed:
  - qNo 1..N without gaps, 4 options each (英聽 3), answer among them
  - every figure file exists under public/; a 英聽 item has a transcript,
    and a picture item (empty option texts) has a figure
  - 題組 ranges inside 1..N and not overlapping; every item of a range exists
  - a cloze item (empty stem) has its __n__ blank in its group's passage,
    and every __n__ in a passage is an item of that group
  - each explanation ends with 「故選 (X)」 and X is the answer
  - the answer letters are spread over A-D (none more than 40%)

  python check_ai_set.py        exit code 1 on any problem
"""
import glob
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
AI_DIR = os.path.join(os.path.dirname(HERE), 'src', 'data', 'ai')
PUBLIC = os.path.join(os.path.dirname(HERE), 'public')


def check(path):
    d = json.load(open(path, encoding='utf-8'))
    errs = []
    items = d['items']
    n = len(items)
    if [i['qNo'] for i in items] != list(range(1, n + 1)):
        errs.append('qNo is not 1..N in order')
    by = {i['qNo']: i for i in items}
    listening = d['subject'] == '英聽'
    k = 3 if listening else 4
    letters = 'ABCD'[:k]
    for i in items:
        q = i['qNo']
        opts = i['options']
        pictures = not any(o.strip() for o in opts)
        if len(opts) != k or (not pictures and not all(o.strip() for o in opts)):
            errs.append(f'Q{q}: needs {k} options (all texts, or all empty for a picture item)')
        if pictures and not i.get('figure'):
            errs.append(f'Q{q}: picture options but no figure')
        if i['answer'] not in letters or len(i['answer']) != 1:
            errs.append(f'Q{q}: answer {i["answer"]!r}')
        if listening and not i.get('transcript'):
            errs.append(f'Q{q}: 英聽 item without transcript')
        for f in [i.get('figure')] + [g.get('figure') for g in d['groups'] if g['from'] <= q <= g['to']]:
            if f and not os.path.exists(os.path.join(PUBLIC, f)):
                errs.append(f'Q{q}: figure {f} missing')
        m = re.findall(r'故選\s*[（(]\s*([A-D])\s*[)）]', i['explanation'])
        if not m:
            errs.append(f'Q{q}: explanation has no 故選 (X)')
        elif m[-1] != i['answer']:
            errs.append(f'Q{q}: explanation says 故選 ({m[-1]}) but answer is {i["answer"]}')
    covered = set()
    for g in d['groups']:
        rng = set(range(g['from'], g['to'] + 1))
        if g['from'] < 1 or g['to'] > n or g['from'] >= g['to']:
            errs.append(f'group {g["from"]}-{g["to"]}: bad range')
        if rng & covered:
            errs.append(f'group {g["from"]}-{g["to"]}: overlaps another group')
        covered |= rng
        blanks = {int(b) for b in re.findall(r'__(\d+)__', g['passage'])}
        if not blanks <= rng:
            errs.append(f'group {g["from"]}-{g["to"]}: blanks {sorted(blanks - rng)} outside the group')
        for q in rng:
            if q in by and not by[q]['stem'] and not listening and q not in blanks:
                errs.append(f'Q{q}: cloze item without __{q}__ in its passage')
    for i in items:
        if not i['stem'] and not listening and i['qNo'] not in covered:
            errs.append(f'Q{i["qNo"]}: empty stem outside a group')
    spread = Counter(i['answer'] for i in items)
    if max(spread.values()) > 0.4 * n:
        errs.append(f'answers not spread: {dict(spread)}')
    print(f'{os.path.basename(path)}: {n} 題, 題組 {len(d["groups"])} 組, 答案分布 {dict(sorted(spread.items()))}, 問題 {len(errs)}')
    for e in errs:
        print('  ', e)
    return len(errs)


if __name__ == '__main__':
    sys.exit(1 if sum(check(p) for p in sorted(glob.glob(os.path.join(AI_DIR, '*.json')))) else 0)
