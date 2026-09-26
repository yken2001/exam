"""Answer-free booklet of an AI set, for the independent solvers.

  python ai_booklet.py ai1_math  <out.txt>

Writes passages, stems and options -- never answers or explanations. A
figure is listed by its absolute file path so the solver can open the image;
a 英聽 item lists its transcript (what the student hears) instead of a stem.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)


def booklet(name):
    d = json.load(open(os.path.join(APP, 'src', 'data', 'ai', name + '.json'), encoding='utf-8'))
    fig = lambda f: os.path.join(APP, 'public', f).replace(os.sep, '/')
    out = [f"{d['title']} -- {len(d['items'])} questions"]
    k = 3 if d['subject'] == '英聽' else 4
    for it in d['items']:
        n = it['qNo']
        for g in d['groups']:
            if g['from'] == n:
                out.append(f"\n===== Passage for questions {g['from']}-{g['to']} =====\n{g['passage']}")
                if g.get('figure'):
                    out.append(f"[Figure for this passage: open the image {fig(g['figure'])}]")
                out.append('')
        if d['subject'] == '英聽':
            heard = ' / '.join(f'{w}: {t}' for w, t in it['transcript'])
            out.append(f"{n}. (The student hears:) {heard}")
        else:
            out.append(f"{n}. {it['stem'] or f'(blank __{n}__ in the passage above)'}")
        if it.get('figure'):
            out.append(f"   [Figure: open the image {fig(it['figure'])}]")
        for L, o in zip('ABCD'[:k], it['options']):
            out.append(f"   ({L}) {o or '(see the picture ' + L + ' in the figure)'}")
    return '\n'.join(out) + '\n'


if __name__ == '__main__':
    open(sys.argv[2], 'w', encoding='utf-8').write(booklet(sys.argv[1]))
    print('written', sys.argv[2])
