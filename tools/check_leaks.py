"""Answer-leak check, independent of how build_bank.py cut the images.

For every question it finds the "(" and ")" of the question's marker on the
PDF page, renders the inside of the brackets from the stem document (the
PDF with the answer letters painted out, which the question images are cut
from) and requires it to be blank. It also renders the same spot from the
original PDF, to report how many questions really had a letter printed there.
A long horizontal rule running through the brackets (the bottom edge of a
題組 passage box) is not a letter and is ignored.

  python check_leaks.py        exit code 1 if any question leaks its answer
"""
import sys
import unicodedata

import fitz
import numpy as np

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import bank_lib as B
import build_bank as BB
import build_listening as BL


def ink(doc, pno, rect):
    pix = doc[pno].get_pixmap(dpi=150, clip=rect)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
    dark = a.min(axis=2) < 200
    rule_rows = dark.sum(axis=1) > 0.5 * dark.shape[1]      # a letter is far narrower
    return int(dark[~rule_rows].sum())


def brackets(page, m):
    """inside of the first "( )" on the marker line m, as a page rect"""
    cs = []
    for b in page.get_text('rawdict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                for c in s['chars']:
                    x0, y0, x1, y1 = c['bbox']
                    if y0 < m.y1 - 1 and y1 > m.y0 + 1 and m.x0 - 2 <= x0 <= m.x0 + 70:
                        cs.append((x0, unicodedata.normalize('NFKC', c['c']), c['bbox']))
    cs.sort()
    o = next((c for c in cs if c[1] == '('), None)
    cl = o and next((c for c in cs if c[1] == ')' and c[0] > o[0]), None)
    if not cl:
        return None
    return fitz.Rect(o[2][2] + 0.3, min(o[2][1], cl[2][1]), cl[2][0] - 0.3, max(o[2][3], cl[2][3]))


def check(name, doc, qdoc, lines, markers):
    bad, printed = [], 0
    for qno, mi in markers:
        m = lines[mi]
        r = brackets(doc[m.pno], m)
        if r is None:
            bad.append(f'Q{qno}: brackets not found')
            continue
        printed += ink(doc, m.pno, r) > 0
        k = ink(qdoc, m.pno, r)
        if k:
            bad.append(f'Q{qno}: {k} dark px inside the brackets')
    print(f'{name}: {len(markers)} 題, 原稿括號內有字 {printed} 題, 洩漏 {len(bad)} {bad if bad else ""}')
    return len(bad)


def main():
    leaks = 0
    for y in BB.YEARS:
        for s in BB.SUBJECTS:
            pdf = rf'{BB.DL}\{y}會考{s}解析.pdf'
            doc, edoc, qdoc = fitz.open(pdf), fitz.open(pdf), fitz.open(pdf)
            rules = dict(BB.RULES.get((y, s), {}))
            rules['mid'] = doc[0].rect.width / 2
            pieces, lines, _ = B.reflow(doc, rules, mask_docs=(edoc, qdoc))
            qs, groups, sections, start, end, notes = B.parse(lines, rules)
            B.compute_regions(lines, qs, groups, sections, end)
            B.extract_answers(lines, qs, groups)
            B.mask_answer_letters(qdoc, lines, qs)
            leaks += check(f'{y}{s}', doc, qdoc, lines, [(q.qno, q.marker) for q in qs])
    for y, fmt in BL.FORMATS.items():
        if fmt['local_numbering']:
            print(f'{y}英聽: 官方格式,題號旁沒有印答案(答案只在解析)')
            continue
        pdf = rf'{BB.DL}\{fmt["pdf"]}'
        doc, edoc, qdoc = fitz.open(pdf), fitz.open(pdf), fitz.open(pdf)
        pieces, lines, _ = B.reflow(doc, {'mid': doc[0].rect.width / 2}, mask_docs=(edoc, qdoc))
        ms = []
        for i, l in enumerate(lines):
            mm = fmt['marker'].match(l.text) if l.red < 0.5 and not l.is_image else None
            if mm and int(mm.group(2)) == len(ms) + 1:
                ms.append((len(ms) + 1, i, mm.group(1)))
        B.mask_answer_letters(qdoc, lines, [B.Question(q, i, letter=L) for q, i, L in ms])
        leaks += check(f'{y}英聽', doc, qdoc, lines, [(q, i) for q, i, _ in ms])
    print('洩漏總數:', leaks)
    return 1 if leaks else 0


if __name__ == '__main__':
    sys.exit(main())
