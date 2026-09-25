"""Build the question bank from a single 解析 PDF.

Pipeline per PDF:
  1. reflow  -- drop page furniture (page-1 title block, per-column footer:
               page number / 請翻面 / ad / QR code, plus per-file rules), then
               split every page into left/right column "pieces" and read them
               in order: p1-left, p1-right, p2-left, ...
  2. parse   -- walk the reflowed text stream, find question markers and
               題組 headers with strict sequential numbering.
  3. regions -- a question's stem runs from its marker to the first red
               (explanation) line; its explanation runs from there to the
               next marker/header. 題組 passages are the black part between
               the header and the first item.
  4. render  -- crop each region piece by piece and stitch vertically. Stems
               are rendered from a copy of the PDF with the printed answer
               letter painted out, so "( C )3." becomes "(   )3.".
"""
import os
import re
import unicodedata
from dataclasses import dataclass, field

import fitz
import numpy as np
from PIL import Image

FOOTER_RE = re.compile(r'第\s*\d+\s*頁|請翻面|請翻頁|ehanlin|會考考完|翰林獨家|國三升高一|順利銜接|免費觀看|歡迎分享|試題結束')
TITLE_RE = re.compile(r'國中教育會考|解析卷|姓名|座號')
TITLE_WORDS = {'國文', '英語', '數學', '自然', '社會', '閱讀'}

# period after the number is optional (110英文 prints "( A )14 Nora:"); a
# bare numeric answer option like "(B) 3 公尺" is instead rejected by
# requiring the marker to sit at the column's left text edge
M_HANLIN = re.compile(r'^[\(（]\s*([A-D]?)\s*[\)）]\s*(\d{1,2})(?:\s*\.|\s+(?=\D))')
M_OFFICIAL = re.compile(r'^(\d{1,2})\s*\.\s*[\(（]\s*[\)）]')
M_ITEM = re.compile(r'^[\(（]\s*[\)）]\s*[\(（](\d)[\)）]')
G_RANGE = re.compile(r'回答第?\s*(\d{1,2})\s*[~〜～至\-]\s*(\d{1,2})\s*題')
G_BRACKET = re.compile(r'^[\(（]\s*(\d{1,2})\s*[-~～〜]\s*(\d{1,2})\s*[\)）]$')
G_LOCAL = re.compile(r'^(\d)\s*\.\s*.{0,4}閱讀.*回答第?\s*\((\d)\)\s*[至~〜～]\s*\((\d)\)\s*題')
G_BARE = re.compile(r'^(\d)\s*\.$')
# "一、單題(1~55題)" / "第二部分:題組(第15-41題)" -- but not experiment steps
# like "一、將胡蘿蔔磨成泥狀" inside a question stem
SECTION_RE = re.compile(r'^([一二三四五六七八九]\s*、|第[一二三四]部分).{0,6}(題組|單題|選擇題|非選)')
END_RE = re.compile(r'非選擇題')

ANS_LOCAL_RE = re.compile(r'\((\d)\)\s*\(([A-D])\)')
ANS_ABS_RE = re.compile(r'(\d{1,2})\s*\.?\s*\(([A-D])\)')
ANS_SINGLE_RE = re.compile(r'(?:故選|答案選|答案為|答案[:：]|故答案為|應選)\s*[【\(（]?\s*([A-D])\s*[】\)）]?')


def is_red(color):
    r, g, b = (color >> 16) & 255, (color >> 8) & 255, color & 255
    return r > 150 and g < 110 and b < 110


def norm(s):
    return unicodedata.normalize('NFKC', s).strip()


@dataclass
class Piece:
    pno: int
    col: int
    x0: float
    x1: float
    top: float
    bottom: float


@dataclass
class Line:
    piece: int
    pno: int
    col: int
    x0: float
    y0: float
    x1: float
    y1: float
    text: str
    red: float
    is_image: bool = False


@dataclass
class Question:
    qno: int
    marker: int              # stream index of marker line
    letter: str = ''         # letter printed in the marker, if any
    letter_line: int = -1    # stream index of a separately drawn answer letter
    group: int = -1          # index into groups
    local: int = 0           # 1-based item number inside a local-numbered group
    stem: tuple = None       # (start, end) stream indices
    expl: tuple = None
    answer: str = ''
    expl_letters: list = field(default_factory=list)


@dataclass
class Group:
    header: int
    qnos: list = field(default_factory=list)
    pre_black: tuple = None
    pre_expl: tuple = None


# ---------------------------------------------------------------- reflow

def _page_lines(page):
    out = []
    for b in page.get_text('dict')['blocks']:
        if 'lines' not in b:
            continue
        for l in b['lines']:
            t = norm(''.join(s['text'] for s in l['spans']))
            if not t:
                continue
            n = sum(len(s['text'].strip()) for s in l['spans']) or 1
            nr = sum(len(s['text'].strip()) for s in l['spans'] if is_red(s['color']))
            out.append((l['bbox'], t, nr / n))
    return out


def reflow(doc, rules, mask_docs=()):
    """Split pages into column pieces. Footer furniture (page number,
    請翻面繼續作答, ad text, QR code, their boxes) is painted white in every
    doc of `mask_docs` rather than cropped away: the page number sits at the
    same height as the last lines of the left column on some pages, so no
    single cut line works for both columns."""
    W, H = doc[0].rect.width, doc[0].rect.height
    mid = W / 2
    pages = list(range(len(doc)))
    if rules.get('drop_last_page'):
        pages = pages[:-1]
    pieces, lines, warnings = [], [], []

    for pno in pages:
        page = doc[pno]
        plines = _page_lines(page)
        is_last = pno == pages[-1]

        top = 0.0
        if pno == 0:
            hb = [bb[3] for bb, t, _ in plines
                  if bb[1] < 125 and (TITLE_RE.search(t) or t.replace(' ', '') in TITLE_WORDS)]
            # the title block may also be one full-width image (113自然)
            hb += [img['bbox'][3] for img in page.get_image_info()
                   if img['bbox'][1] < 60 and img['bbox'][2] - img['bbox'][0] > W * 0.6]
            top = max(hb) + 1.0 if hb else 0.0
            # the title image can overlap the first content line by a hair
            # (115英聽: image to y=92, "第一部分:辨識句意" from y=90): never
            # cut a line that starts inside the header and ends below it
            straddle = [bb[1] for bb, t, _ in plines if bb[1] < top and bb[3] > top + 3]
            if straddle:
                top = min(straddle) - 0.5

        footer = []
        content = []
        for bb, t, red in plines:
            cx = (bb[0] + bb[2]) / 2
            is_pnum = re.fullmatch(r'\d{1,2}', t) and bb[1] > H * 0.9 and abs(cx - mid) < 25
            if bb[1] > H * 0.85 and (FOOTER_RE.search(t) or is_pnum):
                footer.append(fitz.Rect(bb))
            else:
                content.append((bb, t, red))
        ftop = min((r.y0 for r in footer), default=H)
        images = []
        for img in page.get_image_info():
            r = fitz.Rect(img['bbox'])
            if r.y0 >= ftop - 15 and r.width < 100 and r.height < 100 and r.x0 > W * 0.75:
                footer.append(r)                       # QR code (far right)
            elif pno == 0 and r.y0 < 60 and r.width > W * 0.6:
                continue                               # the title image itself
            elif r.y1 > top + 1:
                images.append(r)
        # only drawings that touch a footer element (the box around
        # 請翻面繼續作答) -- NOT any thin line at that height: fraction bars in
        # the left column's last formula sit at the same y as the ad
        near = [fitz.Rect(r.x0 - 6, r.y0 - 6, r.x1 + 6, r.y1 + 6) for r in footer]
        for d in page.get_drawings():
            r = d['rect']     # may be zero-height (a single line), so no Rect.intersects
            if r.height < 40 and any(r.x0 <= n.x1 and r.x1 >= n.x0 and r.y0 <= n.y1 and r.y1 >= n.y0
                                     for n in near):
                footer.append(r)
        # never paint over body text: e.g. a "故選【A】。" whose glyph box
        # touches the top of the ad box -- push the mask below it instead.
        # (images are left alone: where a figure's bbox reaches the page
        # number it is only the figure's blank padding under the number)
        kept = []
        for r in footer:
            over = [bb for bb, _, _ in content
                    if bb[0] < r.x1 and bb[2] > r.x0 and bb[1] < r.y1 and bb[3] > r.y0]
            if over:
                y0 = max(bb[3] for bb in over) + 0.3
                if y0 >= r.y1:
                    continue
                r = fitz.Rect(r.x0, y0, r.x1, r.y1)
            kept.append(r)
        footer = kept
        for md in mask_docs:
            for r in footer:
                md[pno].draw_rect(fitz.Rect(r.x0 - 1, r.y0 - 1, r.x1 + 1, r.y1 + 1),
                                  color=None, fill=(1, 1, 1), overlay=True)

        bottom = H - 2
        if is_last and rules.get('cut_last_page_at'):
            for bb, t, _ in plines:
                if rules['cut_last_page_at'] in t:
                    bottom = bb[1] - 2
                    break

        for col, (cx0, cx1) in enumerate(((0, mid - 1.5), (mid + 1.5, W))):
            if is_last and rules.get('drop_last_page_col') == col:
                continue
            pieces.append(Piece(pno, col, cx0, cx1, top, bottom))
            pi = len(pieces) - 1
            mine = []
            for bb, t, red in content:
                if (0 if bb[0] < mid else 1) == col and bb[1] >= top - 0.5 and bb[3] <= bottom + 0.5:
                    mine.append(Line(pi, pno, col, bb[0], bb[1], bb[2], bb[3], t, red))
            for r in images:
                if (0 if r.x0 < mid else 1) == col and r.y0 >= top - 0.5 and r.y1 <= bottom + 0.5:
                    mine.append(Line(pi, pno, col, r.x0, r.y0, r.x1, r.y1, '', 0.0, is_image=True))
            mine.sort(key=lambda l: (round(l.y0, 1), l.x0))
            lines.extend(mine)

    # crop both columns with the same small margin before their text edge, so
    # content stitched across a column break stays left-aligned
    # (the margin covers the furthest-left element of either column, e.g. a
    # stray 試題解析 line that starts left of the usual edge)
    base = column_text_base(lines)
    overhang = max(base[c] - min(l.x0 for l in lines if l.col == c) for c in (0, 1))
    margin = max(overhang, 0) + 4
    for p in pieces:
        if p.col == 0:
            p.x0 = max(0.0, base[0] - margin)
        else:
            p.x0 = max(mid + 1.5, base[1] - margin)
            p.x1 = W - 2
    return pieces, lines, warnings


def column_text_base(lines):
    """Left text edge of each column: the smallest x0 that at least 5 lines
    start at (markers and 試題解析 lines start there; options are indented)."""
    base = {}
    for c in (0, 1):
        counts = {}
        for l in lines:
            if l.col == c and l.text:
                counts[round(l.x0)] = counts.get(round(l.x0), 0) + 1
        base[c] = min(x for x, n in counts.items() if n >= 5)
    return base


def save_reflowed_pdf(doc, pieces, path):
    out = fitz.open()
    for p in pieces:
        clip = fitz.Rect(p.x0, p.top, p.x1, p.bottom)
        page = out.new_page(width=clip.width, height=clip.height)
        page.show_pdf_page(page.rect, doc, p.pno, clip=clip)
    out.save(path, garbage=3, deflate=True)
    out.close()


# ---------------------------------------------------------------- parse

def parse(lines, rules):
    start, end = 0, len(lines)
    if rules.get('start_after'):
        for i, l in enumerate(lines):
            if rules['start_after'] in l.text:
                start = i + 1
                break
    for i in range(start, len(lines)):
        if END_RE.search(lines[i].text) and lines[i].red < 0.5:
            end = i
            break

    questions, groups, sections, notes = [], [], [], []
    next_q = 1
    local = None        # {'group': gi, 'k': next local index, 'count': K or None}
    in_group_section = False
    bare_next = 1

    # markers start exactly at the column's text edge; answer options are
    # indented well past it
    col_base = column_text_base(lines)

    for i in range(start, end):
        l = lines[i]
        t = l.text
        if l.red >= 0.5 or l.is_image:
            continue
        indent = l.x0 - col_base[l.col]

        if SECTION_RE.match(t):
            sections.append(i)
            in_group_section = '題組' in t
            local = None
            continue

        m = G_LOCAL.match(t)
        if m:
            groups.append(Group(i))
            local = {'group': len(groups) - 1, 'k': 1, 'count': int(m.group(3))}
            continue

        m = G_BARE.match(t)
        if m and in_group_section and rules.get('bare_groups') and int(m.group(1)) == bare_next \
                and indent < 12:
            groups.append(Group(i))
            local = {'group': len(groups) - 1, 'k': 1, 'count': None}
            bare_next += 1
            continue

        m = G_BRACKET.match(t)
        if m and int(m.group(1)) == next_q:
            groups.append(Group(i))
            local = None
            continue

        m = G_RANGE.search(t)
        if m and int(m.group(1)) == next_q and ('閱讀' in t or (i > 0 and '閱讀' in lines[i - 1].text)):
            h = i - 1 if '閱讀' not in t and lines[i - 1].piece == l.piece else i
            groups.append(Group(h))
            local = None
            continue

        m = M_ITEM.match(t)
        if m and local is not None and int(m.group(1)) == local['k'] and indent < 22:
            questions.append(Question(next_q, i, group=local['group'], local=local['k']))
            groups[local['group']].qnos.append(next_q)
            next_q += 1
            local['k'] += 1
            if local['count'] and local['k'] > local['count']:
                local = None
            continue

        # a blank "( )43." can't be a numeric answer option, so 112's slightly
        # indented 題組 items are allowed more indent than lettered markers
        m = M_HANLIN.match(t)
        if m and int(m.group(2)) == next_q and indent < (12 if m.group(1) else 22):
            questions.append(Question(next_q, i, letter=m.group(1)))
            next_q += 1
            continue

        m = M_OFFICIAL.match(t)
        if m and int(m.group(1)) == next_q and indent < 25:
            questions.append(Question(next_q, i))
            next_q += 1
            continue

    # 110英文: no "(15-16)" headers; each 題組 has one 【文章翻譯】 tag, preceded
    # by the passage (an image). The group starts where that black run begins.
    tag = rules.get('tag_groups')
    if tag:
        marker_idx = {q.marker for q in questions}
        tags = [i for i in range(start, end) if tag in lines[i].text and lines[i].red >= 0.5]
        for t_idx in tags:
            h = t_idx
            while h - 1 >= start and lines[h - 1].red < 0.5 and h - 1 not in marker_idx \
                    and h - 1 not in sections:
                h -= 1
            groups.append(Group(h))
        groups.sort(key=lambda g: g.header)
        heads = [g.header for g in groups] + [end]
        for gi, g in enumerate(groups):
            for q in questions:
                if heads[gi] < q.marker < heads[gi + 1]:
                    q.group = gi
                    g.qnos.append(q.qno)

    # attach absolute-numbered questions to the group header they follow
    for gi, g in enumerate(groups):
        if g.qnos:
            continue
        rng = None
        for j in range(g.header, min(g.header + 3, len(lines))):
            mm = G_RANGE.search(lines[j].text) or G_BRACKET.match(lines[j].text)
            if mm:
                rng = (int(mm.group(1)), int(mm.group(2)))
                break
        if rng and rng[1] < rng[0]:
            # misprinted range, e.g. 113社會 "回答第52至41題": take every
            # question up to the next 題組 header / section instead
            stop = min([h.header for h in groups if h.header > g.header] +
                       [s for s in sections if s > g.header] + [end])
            members = [q for q in questions if g.header < q.marker < stop]
            notes.append(f'group header {lines[g.header].text!r} has an inverted range; '
                         f'took Q{members[0].qno}-Q{members[-1].qno} up to the next header')
            rng = (members[0].qno, members[-1].qno)
        if rng:
            for q in questions:
                if rng[0] <= q.qno <= rng[1]:
                    q.group = gi
                    g.qnos.append(q.qno)

    # 113數學: the marker's text is a blank "(     ) 1." and the red answer
    # letter is a separate one-letter line drawn inside the parentheses. It
    # is the answer (not the start of the explanation), and must be painted
    # out of the question image like any printed letter.
    for q in questions:
        m = lines[q.marker]
        # the letter can sit a hair above the marker text and sort before it;
        # match by vertical overlap, not by top edge: a superscript on the
        # marker's line (113數學 Q15 "10^a") pulls the line's top up by 8pt
        for j in sorted(range(max(start, q.marker - 4), min(q.marker + 5, end)), key=lambda j: abs(j - q.marker)):
            if j == q.marker:
                continue
            l = lines[j]
            if l.piece == m.piece and l.red >= 0.5 and re.fullmatch(r'[A-D]', l.text) \
                    and l.y0 < m.y1 - 2 and l.y1 > m.y0 + 2 and m.x0 <= l.x0 <= m.x0 + 30:
                if q.letter and q.letter != l.text:
                    notes.append(f'Q{q.qno}: marker text says {q.letter}, red letter says {l.text}')
                q.letter = q.letter or l.text
                q.letter_line = j
                l.red = 0.0
                break

    marker_idx = {q.marker for q in questions}

    def black_run_before(i):
        """First index of the unbroken run of black (non-red) elements
        right before line i -- stops at red text, a marker or a section."""
        h = i
        while h - 1 >= start and lines[h - 1].red < 0.5 and h - 1 not in marker_idx \
                and h - 1 not in sections:
            h -= 1
        return h

    # a header can be the tail of a sentence that starts on the line before
    # (113國文 "…主角古阿明是 / 茶農家庭的小學生。請閱讀並回答36〜37題:").
    # Only pull in text lines tight above it -- not e.g. a figure that ends
    # the previous question's explanation (111英文 Q22's postcard).
    for g in groups:
        if rules.get('tag_groups'):
            continue
        h = g.header
        while h - 1 >= start:
            prev, cur = lines[h - 1], lines[h]
            if prev.is_image or prev.red >= 0.5 or h - 1 in marker_idx or h - 1 in sections \
                    or prev.piece != cur.piece or cur.y0 - prev.y1 > 8 or abs(prev.x0 - cur.x0) > 30:
                break
            h -= 1
        g.header = h

    # 113自然 prints no 題組 header at all: the passage (black text and
    # figures) sits between one explanation and the next marker. From the
    # first such passage on, every question belongs to the most recent one.
    if rules.get('headerless_groups'):
        current = None
        for q in questions:
            m = lines[q.marker]
            h = black_run_before(q.marker)
            # inline figures on the marker's own row sort just before it
            # ("( D )25. 圖(十四)為[圖]…") -- they are stem, not a passage
            run = [l for l in lines[h:q.marker] if not (l.piece == m.piece and l.y1 > m.y0 + 1)]
            if run and (sum(len(l.text) for l in run) >= 20 or any(l.is_image for l in run)):
                groups.append(Group(h))
                current = len(groups) - 1
            if current is not None:
                q.group = current
                groups[current].qnos.append(q.qno)

    groups.sort(key=lambda g: g.header)
    order = {id(g): k for k, g in enumerate(groups)}
    by_qno = {n: g for g in groups for n in g.qnos}
    for q in questions:
        q.group = order[id(by_qno[q.qno])] if q.qno in by_qno else -1

    # an element on the marker's own row can start a hair above the marker
    # text and so sort before it (115社會 Q41: the 表(六) picture beside the
    # stem is 2.5pt higher). It belongs to this question, not to the end of
    # the previous explanation: move the marker in front of it.
    protected = {q.marker for q in questions} | {g.header for g in groups} | set(sections)
    for q in questions:
        m = q.marker
        k = m
        while k - 1 > start and k - 1 not in protected:
            l, ml = lines[k - 1], lines[m]
            if not (l.piece == ml.piece and l.red < 0.5 and l.y0 >= ml.y0 - 8 and l.y1 > ml.y0 + 2):
                break
            k -= 1
        if k == m:
            continue
        lines.insert(k, lines.pop(m))

        def shift(i, k=k, m=m):
            return k if i == m else i + 1 if k <= i < m else i
        for o in questions:
            o.marker = shift(o.marker)
            if o.letter_line >= 0:
                o.letter_line = shift(o.letter_line)
        for g in groups:
            g.header = shift(g.header)
        sections[:] = [shift(i) for i in sections]
        protected = {o.marker for o in questions} | {g.header for g in groups} | set(sections)
        notes.append(f'Q{q.qno}: {m - k} element(s) on the marker row sorted before it; moved into the question')

    return questions, groups, sections, start, end, notes


# ---------------------------------------------------------------- regions

def compute_regions(lines, questions, groups, sections, end):
    events = sorted([q.marker for q in questions] + [g.header for g in groups] + sections + [end])

    def next_event(i):
        for e in events:
            if e > i:
                return e
        return end

    def first_red(a, b):
        for j in range(a, b):
            if lines[j].red >= 0.5:
                return j
        return None

    qby = {q.qno: q for q in questions}
    errors = []
    for q in questions:
        nxt = next_event(q.marker)
        if q.group >= 0:
            g = groups[q.group]
            members = {qby[n].marker for n in g.qnos}
            unit_end = next((e for e in events if e > q.marker and e not in members), end)
        else:
            unit_end = nxt
        r = first_red(q.marker + 1, unit_end)
        if r is None:
            errors.append(f'Q{q.qno}: no explanation (red) line found')
            q.stem = (q.marker, nxt)
            continue
        q.stem = (q.marker, min(nxt, r))
        q.expl = (r, next_event(r))

    for g in groups:
        if not g.qnos:
            continue
        m1 = qby[g.qnos[0]].marker
        r = first_red(g.header, m1)
        g.pre_black = (g.header, r if r is not None else m1)
        if r is not None:
            g.pre_expl = (r, m1)
    return errors


def extract_answers(lines, questions, groups):
    notes = []
    for q in questions:
        if not q.expl:
            continue
        a, b = q.expl
        text = ''.join(lines[j].text for j in range(a, b) if lines[j].red >= 0.5).replace(' ', '')
        found = []
        # 112 題組 give one combined line for the whole group:
        #   答案:(1)(C);(2)(D)   or   答案:32(B);33(C)
        # (a 題組 numbered 41-42 may still write its answers as (1)(B);(2)(D),
        # so local pairs are matched by the item's position in its group)
        head = ''
        if text.startswith('答案'):
            head = text.split('解析')[0]
        if head:
            abs_pairs = {int(n): ltr for n, ltr in ANS_ABS_RE.findall(head)}
            loc_pairs = {int(k): ltr for k, ltr in ANS_LOCAL_RE.findall(head)}
            pos = q.local or (groups[q.group].qnos.index(q.qno) + 1 if q.group >= 0 else 0)
            if q.qno in abs_pairs:
                found = [abs_pairs[q.qno]]
            elif pos and pos in loc_pairs:
                found = [loc_pairs[pos]]
            elif abs_pairs or loc_pairs:
                notes.append(f'Q{q.qno}: combined answer line {head!r} does not list this question')
                continue
        if not found:
            found = ANS_SINGLE_RE.findall(text)
        q.expl_letters = found
        if q.letter:
            q.answer = q.letter
            if found and any(f != q.letter for f in found):
                notes.append(f'Q{q.qno}: marker says {q.letter}, explanation text says {found}')
            elif not found:
                notes.append(f'Q{q.qno}: marker {q.letter}, no confirming answer text in explanation')
        else:
            if not found:
                notes.append(f'Q{q.qno}: NO ANSWER FOUND')
            else:
                q.answer = found[0]
                if len(set(found)) > 1:
                    notes.append(f'Q{q.qno}: several answer letters in explanation: {found} (took {found[0]})')
    return notes


# ---------------------------------------------------------------- render

def _trim(im, pad=6):
    """Drop blank rows above/below the content (ignores a 4px side margin so
    a stray column rule at the edge doesn't count as content)."""
    w, h = im.size
    ink = im.convert('L').crop((4, 0, w - 4, h)).point(lambda v: 255 if v < 243 else 0)
    bbox = ink.getbbox()
    if bbox is None:
        return None
    return im.crop((0, max(0, bbox[1] - pad), w, min(h, bbox[3] + pad)))


def _drop_top_sliver(im, max_h=4):
    """A region starts with a question/explanation line, never with a band
    only a few pixels tall: such a band is a glyph of the line above (e.g. the
    tall 【】 brackets, a red underline) poking out of its text box. Cut it
    off -- unless it is a black rule, i.e. the bottom edge of a 題組 passage
    box, which belongs to the picture."""
    rgb = np.asarray(im.convert('RGB')).astype(int)[:, 4:-4]
    g = rgb.min(axis=2) < 243
    rows = g.any(axis=1)
    if not rows[:max_h + 1].any():
        return im
    first_blank = next((y for y in range(rows.argmax(), min(len(rows), max_h + 2)) if not rows[y]), None)
    if first_blank is None or not rows[first_blank:].any():
        return im
    band = rgb[:first_blank]
    red = ((band[..., 0] > 150) & (band[..., 1] < 110) & (band[..., 2] < 110)).any()
    rule = (g[:first_blank].sum(axis=1) > 0.3 * g.shape[1]).any()
    if rule and not red:
        return im
    return im.crop((0, first_blank, im.width, im.height))


def whiten_red(qdoc, lines):
    """Paint every red (explanation) line out of the stem document. Stems
    never contain red lines, so this only removes explanations -- and with
    them any chance of a red sliver at the edge of a question image."""
    for l in lines:
        if l.red >= 0.5 and not l.is_image:
            qdoc[l.pno].draw_rect(fitz.Rect(l.x0 - 0.5, l.y0 - 0.5, l.x1 + 0.5, l.y1 + 0.5),
                                  color=None, fill=(1, 1, 1), overlay=True)


def render_region(doc, pieces, lines, region, end, dpi, lift=False):
    a, b = region
    if a >= b:
        return []
    pa = lines[a].piece
    # a little headroom above the first line, but never into the line above
    # it (that would leave a sliver of the previous region's last line)
    # (with tight leading the line above's box can overlap this one's -- then
    # start where the two boxes meet, never more than 0.5pt into this line)
    top = lines[a].y0
    y_start = top - 3
    above = [l.y1 for l in lines[max(0, a - 40):a] if l.piece == pa and l.y0 < top - 2]
    if above:
        y_start = max(y_start, min(max(above), top + 0.5))
    # lift (stems, from the red-whitened document): an element of this
    # region that starts above its first line -- a picture beside the stem
    # whose caption sits higher than the marker (115社會 Q43 表(七)) -- is
    # included up to its top, but never into black content above it
    if lift:
        ext = [l.y0 for l in lines[a:b] if l.piece == pa and l.y0 < top - 0.5]
        if ext:
            black = [l.y1 for l in lines[max(0, a - 40):a]
                     if l.piece == pa and l.red < 0.5 and l.y0 < min(ext) - 2]
            y_start = min(y_start, max([min(ext) - 1] + black))
    if b < len(lines):
        pb, y_end = lines[b].piece, lines[b].y0 - 1.5
    else:
        pb, y_end = lines[b - 1].piece, pieces[lines[b - 1].piece].bottom
    out = []
    for pi in range(pa, pb + 1):
        p = pieces[pi]
        ys = max(p.top, y_start) if pi == pa else p.top
        ye = min(p.bottom, y_end) if pi == pb else p.bottom
        if ye - ys < 2:
            continue
        pix = doc[p.pno].get_pixmap(dpi=dpi, clip=fitz.Rect(p.x0, ys, p.x1, ye))
        im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        if pi == pa:
            im = _drop_top_sliver(im)
        im = _trim(im)
        if im is not None:
            out.append(im)
    return out


def stitch(images, path):
    images = [im for im in images if im is not None]
    if not images:
        raise ValueError(f'nothing to render for {path}')
    w = max(im.width for im in images)
    h = sum(im.height for im in images)
    canvas = Image.new('RGB', (w, h), 'white')
    y = 0
    for im in images:
        canvas.paste(im, (0, y))
        y += im.height
    canvas.save(path)
    return canvas.size


def mask_answer_letters(qdoc, lines, questions):
    """Paint the printed answer letter of '( X )N.' markers white."""
    for q in questions:
        if not q.letter:
            continue
        if q.letter_line >= 0:        # drawn as its own line (113數學)
            r = lines[q.letter_line]
            qdoc[r.pno].draw_rect(fitz.Rect(r.x0 - 0.5, r.y0 - 0.5, r.x1 + 0.5, r.y1 + 0.5),
                                  color=None, fill=(1, 1, 1), overlay=True)
            continue
        l = lines[q.marker]
        page = qdoc[l.pno]
        done = False
        for b in page.get_text('rawdict')['blocks']:
            if 'lines' not in b or done:
                continue
            for rl in b['lines']:
                bb = rl['bbox']
                if abs(bb[1] - l.y0) > 1 or abs(bb[0] - l.x0) > 1:
                    continue
                chars = [c for s in rl['spans'] for c in s['chars']]
                seen_paren = False
                for c in chars:
                    ch = unicodedata.normalize('NFKC', c['c'])
                    if ch in '(（':
                        seen_paren = True
                    elif seen_paren and ch in 'ABCD':
                        r = fitz.Rect(c['bbox'])
                        page.draw_rect(fitz.Rect(r.x0 - 0.5, r.y0 - 0.5, r.x1 + 0.5, r.y1 + 0.5),
                                       color=None, fill=(1, 1, 1), overlay=True)
                        done = True
                        break
                    elif seen_paren and ch in ')）':
                        break
                if done:
                    break
        if not done:
            raise RuntimeError(f'Q{q.qno}: could not locate answer letter to mask')
