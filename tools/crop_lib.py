import fitz, re, os, shutil, unicodedata
from PIL import Image

GROUP_HDR_RE = re.compile(r'閱讀.{0,15}回答第?\s*(\d{1,3})\s*[^\d]{1,3}\s*(\d{1,3})\s*題')
GROUP_HDR_LOOSE_RE = re.compile(r'閱讀[^\d]{0,20}(\d{1,3})\s*[^\d]{1,3}\s*(\d{1,3})\s*題')
BRACKET_HDR_RE = re.compile(r'^[\(（]\s*(\d{1,3})\s*[-~～]\s*(\d{1,3})\s*[\)）]$')
QMARK_RE = re.compile(r'^(\d{1,3})\.(?:\s|$)')
QSTART_RE = re.compile(r'^[\(（]\s*([A-D]?)\s*[\)）]\s*(\d{1,3})\.?(?!\d)')
NUM_FIRST_MARKER_RE = re.compile(r'^(\d{1,3})\.\s*[\(（]\s*[A-D]?\s*[\)）]')
CHOSEN_RE = re.compile(r'(?:故(?:選|答案選|答案為)|答案)[\s:：]*[\(（【]?\s*([A-D])\s*[\)）】]?')
ANSWER_PREFIX_RE = re.compile(r'答案[:：]\s*(.+)')
PAIR_ABS_RE = re.compile(r'(\d{1,3})\.?\s*[\(（]\s*([A-D])\s*[\)）]')
PAIR_LOCAL_RE = re.compile(r'[\(（](\d{1,2})[\)）]\s*[\(（]\s*([A-D])\s*[\)）]')
SIMPLE_ANSWER_RE = re.compile(r'^[\(（]\s*([A-D])\s*[\)）]\s*$')
STANDALONE_NUM_FIRST_RE = re.compile(r'^(\d{1,3})\.\s*[\(（]\s*[\)）]')
STANDALONE_PAREN_FIRST_RE = re.compile(r'^[\(（]\s*[\)）]\s*(\d{1,3})\.')
GROUP_LOCAL_HDR_RE = re.compile(
    r'^\d{1,3}\.\s*閱讀.{0,30}[\(（]\s*1\s*[\)）]\s*[至~]\s*[\(（]?(\d{1,2})[\)）]?\s*題'
)
BARE_ORDINAL_RE = re.compile(r'^(\d{1,2})\.\s*$')
LOCAL_ITEM_RE = re.compile(r'^[\(（]\s*[\)）]\s*[\(（](\d{1,2})[\)）]')

# Publisher/official-release ad footers and page furniture. Different years
# use different wording for the same boilerplate, and missing a variant is
# dangerous: it leaves ad text (and therefore whole blank trailing pages) in
# the stream, which can massively over-extend the *last* unit in a document
# since its crop end falls back to "end of stream".
BOILERPLATE_RE = re.compile(
    r'^第\s*\d+\s*頁'
    r'|^請翻面繼續作答|^請翻頁繼續作答'
    r'|^會考考完看這裡|^翰林獨家統整'
    r'|^國三升高一看這裡'
    r'|^您未來順利銜接|^讓您未來順利銜接'
    r'|^免費觀看$|^歡迎分享$'
    r'|^www\.ehanlin\.com\.tw'
)

# Some 解析 files append genuine reference material after the last real
# question (a formula sheet, a chapter cross-reference table, a question-
# type breakdown) -- not an ad, so it must stay out of BOILERPLATE_RE, but
# it must never be absorbed into the *last* question's explanation crop
# (whose end otherwise falls back to "end of stream"). Once any of these
# section headers is seen, the stream is truncated right there.
APPENDIX_START_RE = re.compile(r'參考公式|題型分析|章節.{0,4}對應表|非選擇題')


def build_2col_stream(doc, boilerplate_re=None):
    mid_x = doc[0].rect.width / 2
    stream = []
    for pno in range(doc.page_count):
        page = doc[pno]
        d = page.get_text('dict')
        per_col = {0: [], 1: []}
        for block in d['blocks']:
            if 'lines' not in block:
                continue
            for line in block['lines']:
                text = ''.join(span['text'] for span in line['spans']).strip()
                if not text:
                    continue
                text = unicodedata.normalize('NFKC', text)
                if boilerplate_re and boilerplate_re.search(text):
                    continue
                bbox = line['bbox']
                col = 0 if bbox[0] < mid_x else 1
                per_col[col].append((bbox[1], bbox[3], text))
        for col in (0, 1):
            per_col[col].sort()
            for y0, y1, text in per_col[col]:
                stream.append((pno, col, y0, y1, text))
    for i, (_, _, _, _, text) in enumerate(stream):
        if APPENDIX_START_RE.search(text):
            stream = stream[:i]
            break
    return stream, mid_x, doc[0].rect.height, doc[0].rect.width


def render_stream_span(doc, stream, start_idx, end_idx, mid_x, page_h, page_w,
                        out_path, dpi=200, pad=6):
    start_page, start_col, start_y0 = stream[start_idx][0], stream[start_idx][1], stream[start_idx][2]
    segs = []
    cur_page, cur_col, cur_top = start_page, start_col, start_y0
    last_seen = (start_page, start_col, start_y0)
    for j in range(start_idx, end_idx):
        p, c, y0, y1, text = stream[j]
        if (p, c) != (cur_page, cur_col):
            segs.append((cur_page, cur_col, cur_top, last_seen[2]))
            cur_page, cur_col, cur_top = p, c, 0
        last_seen = (p, c, y1)
    segs.append((cur_page, cur_col, cur_top, last_seen[2]))

    piece_paths = []
    for k, (spno, scol, stop, sbottom) in enumerate(segs):
        page = doc[spno]
        x0 = 0 if scol == 0 else mid_x
        x1 = mid_x if scol == 0 else page_w
        top_pad = pad if k == 0 else 0
        bot_pad = pad if k == len(segs) - 1 else 0
        crop = fitz.Rect(x0, max(0, stop - top_pad), x1, min(page_h, sbottom + bot_pad))
        pix = page.get_pixmap(dpi=dpi, clip=crop)
        p = f'{out_path}._tmp_{k}.png'
        pix.save(p)
        piece_paths.append(p)

    if len(piece_paths) == 1:
        os.replace(piece_paths[0], out_path)
    else:
        imgs = [Image.open(p) for p in piece_paths]
        w = max(im.width for im in imgs)
        h = sum(im.height for im in imgs)
        combined = Image.new('RGB', (w, h), 'white')
        y = 0
        for im in imgs:
            combined.paste(im, (0, y))
            y += im.height
        combined.save(out_path)
        for p in piece_paths:
            os.remove(p)


def find_stream_idx(stream, needle, start=0):
    for idx in range(start, len(stream)):
        if needle in stream[idx][4]:
            return idx
    return None


# ---------------------------------------------------------------------------
# 題本 (question booklet) croppers
# ---------------------------------------------------------------------------

def crop_questions(pdf_path, out_dir, num_questions, first_page, last_page,
                    margin_x=(60, 76), footer_limit=780, dpi=200,
                    group_style='chinese'):
    """Single-column booklet (110/111 style)."""
    doc = fitz.open(pdf_path)
    os.makedirs(out_dir, exist_ok=True)

    pages_lines = {}
    for pno in range(first_page, last_page):
        page = doc[pno]
        d = page.get_text('dict')
        lines = []
        for block in d['blocks']:
            if 'lines' not in block:
                continue
            for line in block['lines']:
                text = ''.join(span['text'] for span in line['spans']).strip()
                if not text:
                    continue
                text = unicodedata.normalize('NFKC', text)
                bbox = line['bbox']
                if bbox[1] > footer_limit:
                    continue
                lines.append((bbox[0], bbox[1], bbox[3], text))
        lines.sort(key=lambda t: t[1])
        pages_lines[pno] = lines

    cutpoints = []
    seen_qnos = set()
    for pno, lines in pages_lines.items():
        for x0, y0, y1, text in lines:
            if group_style == 'chinese':
                gm = GROUP_HDR_RE.search(text)
            else:
                gm = BRACKET_HDR_RE.match(text)
            if gm:
                qstart, qend = int(gm.group(1)), int(gm.group(2))
                cutpoints.append((pno, y0, list(range(qstart, qend + 1))))
                continue
            m = QMARK_RE.match(text)
            if m and margin_x[0] <= x0 <= margin_x[1]:
                qno = int(m.group(1))
                if 1 <= qno <= num_questions and qno not in seen_qnos:
                    seen_qnos.add(qno)
                    cutpoints.append((pno, y0, [qno]))

    cutpoints.sort(key=lambda t: (t[0], t[1]))
    group_ranges = [cp[2] for cp in cutpoints if len(cp[2]) > 1]

    def in_any_group(qno):
        return any(qno in rng for rng in group_ranges)

    cutpoints = [cp for cp in cutpoints if len(cp[2]) > 1 or not in_any_group(cp[2][0])]
    cutpoints.sort(key=lambda t: (t[0], t[1]))

    page_h = doc[first_page].rect.height
    page_w = doc[first_page].rect.width

    def render_unit(start_page, start_y, end_page, end_y, out_path):
        pieces = []
        if start_page == end_page:
            pieces.append((start_page, start_y, end_y))
        else:
            pieces.append((start_page, start_y, footer_limit))
            for mid in range(start_page + 1, end_page):
                pieces.append((mid, 0, footer_limit))
            pieces.append((end_page, 0, end_y))

        imgs = []
        for pno, y0, y1 in pieces:
            page = doc[pno]
            crop = fitz.Rect(0, max(0, y0 - 4), page_w, min(page_h, y1))
            pix = page.get_pixmap(dpi=dpi, clip=crop)
            imgs.append(Image.frombytes('RGB', (pix.width, pix.height), pix.samples))

        if len(imgs) == 1:
            imgs[0].save(out_path)
        else:
            w = max(im.width for im in imgs)
            h = sum(im.height for im in imgs)
            combined = Image.new('RGB', (w, h), 'white')
            y = 0
            for im in imgs:
                combined.paste(im, (0, y))
                y += im.height
            combined.save(out_path)

    for i, (pno, y0, qnos) in enumerate(cutpoints):
        if i + 1 < len(cutpoints):
            end_page, end_y, _ = cutpoints[i + 1]
        else:
            end_page, end_y = pno, footer_limit
        for q in qnos:
            render_unit(pno, y0, end_page, end_y, f'{out_dir}/q{q:02d}.png')

    total_q = sum(len(c[2]) for c in cutpoints)
    print(f'[questions] units={len(cutpoints)} questions={total_q}')
    if total_q != num_questions:
        print(f'  !! expected {num_questions} questions, got {total_q}')
    return cutpoints


def crop_questions_2col_standalone(pdf_path, out_dir, num_questions, dpi=200,
                                    boilerplate_re=None):
    doc = fitz.open(pdf_path)
    os.makedirs(out_dir, exist_ok=True)
    stream, mid_x, page_h, page_w = build_2col_stream(doc, boilerplate_re)

    markers = []
    next_expected = 1
    for idx, (pno, col, y0, y1, text) in enumerate(stream):
        m = NUM_FIRST_MARKER_RE.match(text)
        if m and int(m.group(1)) == next_expected:
            markers.append((idx, next_expected))
            next_expected += 1

    for i, (idx, qno) in enumerate(markers):
        end_idx = markers[i + 1][0] if i + 1 < len(markers) else len(stream)
        render_stream_span(doc, stream, idx, end_idx, mid_x, page_h, page_w,
                            f'{out_dir}/q{qno:02d}.png', dpi=dpi)

    print(f'[questions-2col] found {len(markers)} of {num_questions} expected')
    return markers


def crop_questions_2col_grouped(pdf_path, out_dir, num_questions, dpi=200,
                                 boilerplate_re=None):
    doc = fitz.open(pdf_path)
    os.makedirs(out_dir, exist_ok=True)
    stream, mid_x, page_h, page_w = build_2col_stream(doc, boilerplate_re)

    cutpoints = []
    next_expected = 1
    for idx, (pno, col, y0, y1, text) in enumerate(stream):
        gm = GROUP_HDR_LOOSE_RE.search(text)
        if not gm and idx > 0:
            gm = GROUP_HDR_LOOSE_RE.search(stream[idx - 1][4] + text)
        if gm:
            qstart, qend = int(gm.group(1)), int(gm.group(2))
            if qstart == next_expected:
                cutpoints.append((idx, list(range(qstart, qend + 1))))
                next_expected = qend + 1
            continue
        m = STANDALONE_NUM_FIRST_RE.match(text) or STANDALONE_PAREN_FIRST_RE.match(text)
        if m:
            qno = int(m.group(1))
            if qno == next_expected:
                cutpoints.append((idx, [qno]))
                next_expected += 1

    for i, (idx, qnos) in enumerate(cutpoints):
        end_idx = cutpoints[i + 1][0] if i + 1 < len(cutpoints) else len(stream)
        for q in qnos:
            render_stream_span(doc, stream, idx, end_idx, mid_x, page_h, page_w,
                                f'{out_dir}/q{q:02d}.png', dpi=dpi)

    total = sum(len(c[1]) for c in cutpoints)
    print(f'[questions-2col-grouped] units={len(cutpoints)} questions={total} (expected {num_questions})')
    return cutpoints


def crop_questions_2col_localgroups(pdf_path, out_dir, num_standalone, dpi=200,
                                     boilerplate_re=None, stream_start=0):
    doc = fitz.open(pdf_path)
    os.makedirs(out_dir, exist_ok=True)
    stream, mid_x, page_h, page_w = build_2col_stream(doc, boilerplate_re)

    cutpoints = []
    next_expected = 1
    for idx in range(stream_start, len(stream)):
        pno, col, y0, y1, text = stream[idx]
        if next_expected <= num_standalone:
            m = STANDALONE_NUM_FIRST_RE.match(text) or STANDALONE_PAREN_FIRST_RE.match(text)
            if m and int(m.group(1)) == next_expected:
                cutpoints.append((idx, [next_expected]))
                next_expected += 1
        else:
            gm = GROUP_LOCAL_HDR_RE.match(text)
            if gm:
                k = int(gm.group(1))
                qnos = list(range(next_expected, next_expected + k))
                cutpoints.append((idx, qnos))
                next_expected += k

    for i, (idx, qnos) in enumerate(cutpoints):
        end_idx = cutpoints[i + 1][0] if i + 1 < len(cutpoints) else len(stream)
        for q in qnos:
            render_stream_span(doc, stream, idx, end_idx, mid_x, page_h, page_w,
                                f'{out_dir}/q{q:02d}.png', dpi=dpi)

    total = sum(len(c[1]) for c in cutpoints)
    print(f'[questions-2col-localgroups] units={len(cutpoints)} questions={total}')
    return cutpoints


def _bare_ordinal_starts(stream, stream_start, num_standalone, standalone_marker_match):
    next_expected = 1
    next_group_ordinal = 1
    starts = []
    group_start_idx = None
    group_qnos = []

    for idx in range(stream_start, len(stream)):
        text = stream[idx][4]
        if next_expected <= num_standalone:
            r = standalone_marker_match(text)
            if r:
                letter, qno = r
                if qno == next_expected:
                    starts.append((idx, [qno], letter))
                    next_expected += 1
            continue
        bm = BARE_ORDINAL_RE.match(text)
        if bm and int(bm.group(1)) == next_group_ordinal:
            if group_start_idx is not None and group_qnos:
                starts.append((group_start_idx, group_qnos, None))
            group_start_idx = idx
            group_qnos = []
            next_group_ordinal += 1
            continue
        lm = LOCAL_ITEM_RE.match(text)
        if lm and group_start_idx is not None:
            li = int(lm.group(1))
            if li == len(group_qnos) + 1:
                group_qnos.append(next_expected)
                next_expected += 1
    if group_start_idx is not None and group_qnos:
        starts.append((group_start_idx, group_qnos, None))
    return starts, next_expected


def crop_questions_2col_bareordinal(pdf_path, out_dir, num_standalone, dpi=200,
                                     boilerplate_re=None, section_marker=None):
    doc = fitz.open(pdf_path)
    os.makedirs(out_dir, exist_ok=True)
    stream, mid_x, page_h, page_w = build_2col_stream(doc, boilerplate_re)
    stream_start = find_stream_idx(stream, section_marker) if section_marker else 0
    if stream_start is None:
        stream_start = 0

    def match_standalone(text):
        m = STANDALONE_NUM_FIRST_RE.match(text) or STANDALONE_PAREN_FIRST_RE.match(text)
        return (None, int(m.group(1))) if m else None

    starts, total_expected = _bare_ordinal_starts(stream, stream_start, num_standalone, match_standalone)

    for i, (idx, qnos, _letter) in enumerate(starts):
        end_idx = starts[i + 1][0] if i + 1 < len(starts) else len(stream)
        for q in qnos:
            render_stream_span(doc, stream, idx, end_idx, mid_x, page_h, page_w,
                                f'{out_dir}/q{q:02d}.png', dpi=dpi)

    total = sum(len(s[1]) for s in starts)
    print(f'[questions-bareordinal] units={len(starts)} questions={total}')
    return starts


# ---------------------------------------------------------------------------
# 解析 (answer + explanation) croppers
# ---------------------------------------------------------------------------

def crop_explanations(pdf_path, out_dir, num_questions, dpi=200,
                       group_style='chinese', passage_tag=None):
    doc = fitz.open(pdf_path)
    os.makedirs(out_dir, exist_ok=True)
    stream, mid_x, page_h, page_w = build_2col_stream(doc, BOILERPLATE_RE)

    answers = {}
    qmarker_events = []
    group_events = []
    next_expected = 1
    pending = []
    prev_alone_matched = False

    for idx, (pno, col, y0, y1, text) in enumerate(stream):
        m = QSTART_RE.match(text)
        m2 = None if m else NUM_FIRST_MARKER_RE.match(text)
        if m or m2:
            letter, qno = (m.group(1), int(m.group(2))) if m else ('', int(m2.group(1)))
            if qno == next_expected:
                next_expected += 1
                qmarker_events.append((idx, qno))
                if letter:
                    answers[qno] = letter
                else:
                    pending.append(qno)
                continue
        if pending:
            am = ANSWER_PREFIX_RE.search(text)
            if am:
                rest = am.group(1)
                abs_pairs = [(int(n), l) for n, l in PAIR_ABS_RE.findall(rest) if int(n) in pending]
                if abs_pairs:
                    for n, l in abs_pairs:
                        answers[n] = l
                        pending.remove(n)
                else:
                    local_pairs = PAIR_LOCAL_RE.findall(rest)
                    if local_pairs:
                        for local_idx, l in local_pairs:
                            li = int(local_idx) - 1
                            if 0 <= li < len(pending):
                                answers[pending[li]] = l
                        pending = []
                    else:
                        sm = SIMPLE_ANSWER_RE.match(rest.strip())
                        if sm and len(pending) == 1:
                            answers[pending[0]] = sm.group(1)
                            pending = []
            else:
                cm = CHOSEN_RE.search(text)
                if cm and len(pending) == 1:
                    answers[pending[0]] = cm.group(1)
                    pending = []
        if group_style == 'chinese':
            alone = GROUP_HDR_RE.search(text)
            if alone:
                gm = alone
            elif not prev_alone_matched and idx > 0:
                gm = GROUP_HDR_RE.search(stream[idx - 1][4] + text)
            else:
                gm = None
            prev_alone_matched = bool(alone)
            if gm:
                group_events.append((idx, int(gm.group(1)), int(gm.group(2))))

    missing = sorted(set(range(1, num_questions + 1)) - set(answers))
    print(f'[explanations] answers found={len(answers)}', f'missing={missing}' if missing else '')

    grouped_qnos = set()
    if group_style == 'bracket' and passage_tag:
        # Locating each group's start via a *backward* scan from its first
        # question's own marker is fragile: 2-column reading order can place
        # the marker later in the stream than expected, letting the scan
        # walk past the true tag and start too early -- or (worse) leave the
        # previous group's end boundary too late, bleeding into the next
        # group's passage. Far more robust: every group has exactly one
        # "文章翻譯"-style tag, in the same order as `groups` itself, so
        # just locate all of them directly and use tag-to-next-tag as each
        # group's span.
        groups, tag_sub = passage_tag
        for a, b in groups:
            grouped_qnos.update(range(a, b + 1))
        unit_starts = []
        # Each group's true start is its "(N-M)" bracket header, which
        # precedes the reprinted English passage -- itself followed by the
        # "文章翻譯" tag and then the Chinese translation. Using the tag as
        # the start (as done previously) leaves the group's OWN passage in
        # the PRIOR unit's span and instead captures the NEXT group's
        # passage at the tail end of the current unit. Prefer the bracket
        # header when every group has exactly one, unambiguous match.
        hdr_matches = []
        for i, (_, _, _, _, t) in enumerate(stream):
            m = BRACKET_HDR_RE.match(t)
            if m:
                hdr_matches.append((i, int(m.group(1)), int(m.group(2))))
        if len(hdr_matches) == len(groups) and [(a, b) for _, a, b in hdr_matches] == list(groups):
            unit_starts = list(hdr_matches)
        else:
            tag_positions = [i for i, (_, _, _, _, t) in enumerate(stream) if tag_sub in t]
            if len(tag_positions) == len(groups):
                for (a, b), tag_idx in zip(groups, tag_positions):
                    unit_starts.append((tag_idx, a, b))
        if not unit_starts:
            print(f'  !! bracket headers/tags did not cleanly match {len(groups)} groups -- '
                  'falling back to per-question backward scan')
            for idx, qno in qmarker_events:
                grp = next(((a, b) for a, b in groups if a <= qno <= b), None)
                if grp and grp[0] == qno:
                    start_idx = idx
                    for j in range(idx - 1, -1, -1):
                        t = stream[j][4]
                        if tag_sub in t:
                            start_idx = j
                            break
                        if QSTART_RE.match(t):
                            break
                    unit_starts.append((start_idx, grp[0], grp[1]))
        for idx, qno in qmarker_events:
            if qno not in grouped_qnos:
                unit_starts.append((idx, qno, qno))
    else:
        for _, a, b in group_events:
            grouped_qnos.update(range(a, b + 1))
        unit_starts = list(group_events)
        for idx, qno in qmarker_events:
            if qno not in grouped_qnos:
                unit_starts.append((idx, qno, qno))

    unit_starts.sort(key=lambda t: t[0])
    units = []
    for i, (idx, a, b) in enumerate(unit_starts):
        end_idx = unit_starts[i + 1][0] if i + 1 < len(unit_starts) else len(stream)
        units.append((idx, end_idx, list(range(a, b + 1))))

    for start_idx, end_idx, qnos in units:
        combined_path = f'{out_dir}/e{qnos[0]:02d}.png'
        render_stream_span(doc, stream, start_idx, end_idx, mid_x, page_h, page_w, combined_path, dpi=dpi)
        for q in qnos[1:]:
            shutil.copyfile(combined_path, f'{out_dir}/e{q:02d}.png')

    print(f'[explanations] units={len(units)} questions={sum(len(u[2]) for u in units)}')
    return answers


def crop_explanations_localgroups(pdf_path, out_dir, num_standalone, dpi=200,
                                   stream_start=0):
    doc = fitz.open(pdf_path)
    os.makedirs(out_dir, exist_ok=True)
    stream, mid_x, page_h, page_w = build_2col_stream(doc, BOILERPLATE_RE)

    answers = {}
    next_expected = 1
    pending = []
    starts = []

    def try_resolve(text):
        nonlocal pending
        if not pending:
            return
        am = ANSWER_PREFIX_RE.search(text)
        if am:
            rest = am.group(1)
            if len(pending) == 1:
                sm = SIMPLE_ANSWER_RE.match(rest.strip())
                if sm:
                    answers[pending[0]] = sm.group(1)
                    pending = []
                    return
            local_pairs = PAIR_LOCAL_RE.findall(rest)
            if local_pairs:
                for local_idx, l in local_pairs:
                    li = int(local_idx) - 1
                    if 0 <= li < len(pending):
                        answers[pending[li]] = l
                pending = []
                return
            abs_pairs = [(int(n), l) for n, l in PAIR_ABS_RE.findall(rest) if int(n) in pending]
            if abs_pairs:
                for n, l in abs_pairs:
                    answers[n] = l
                    pending.remove(n)
                return
        elif len(pending) == 1:
            cm = CHOSEN_RE.search(text)
            if cm:
                answers[pending[0]] = cm.group(1)
                pending = []

    for idx in range(stream_start, len(stream)):
        pno, col, y0, y1, text = stream[idx]
        if next_expected <= num_standalone:
            m = QSTART_RE.match(text)
            m2 = None if m else NUM_FIRST_MARKER_RE.match(text)
            if m or m2:
                letter, qno = (m.group(1), int(m.group(2))) if m else ('', int(m2.group(1)))
                if qno == next_expected:
                    next_expected += 1
                    starts.append((idx, [qno]))
                    if letter:
                        answers[qno] = letter
                    else:
                        pending = [qno]
                    continue
            try_resolve(text)
        else:
            gm = GROUP_LOCAL_HDR_RE.match(text)
            if gm:
                k = int(gm.group(1))
                qnos = list(range(next_expected, next_expected + k))
                starts.append((idx, qnos))
                next_expected += k
                pending = list(qnos)
                continue
            try_resolve(text)

    missing = sorted(set(range(1, next_expected)) - set(answers))
    print(f'[explanations-localgroups] answers found={len(answers)}', f'missing={missing}' if missing else '')

    for i, (idx, qnos) in enumerate(starts):
        end_idx = starts[i + 1][0] if i + 1 < len(starts) else len(stream)
        combined_path = f'{out_dir}/e{qnos[0]:02d}.png'
        render_stream_span(doc, stream, idx, end_idx, mid_x, page_h, page_w, combined_path, dpi=dpi)
        for q in qnos[1:]:
            shutil.copyfile(combined_path, f'{out_dir}/e{q:02d}.png')

    print(f'[explanations-localgroups] units={len(starts)} questions={sum(len(s[1]) for s in starts)}')
    return answers


def crop_explanations_bareordinal(pdf_path, out_dir, num_standalone, dpi=200,
                                   section_marker=None):
    doc = fitz.open(pdf_path)
    os.makedirs(out_dir, exist_ok=True)
    stream, mid_x, page_h, page_w = build_2col_stream(doc, BOILERPLATE_RE)
    stream_start = find_stream_idx(stream, section_marker) if section_marker else 0
    if stream_start is None:
        stream_start = 0

    def match_standalone(text):
        m = QSTART_RE.match(text)
        m2 = None if m else NUM_FIRST_MARKER_RE.match(text)
        if m:
            return (m.group(1), int(m.group(2)))
        if m2:
            return ('', int(m2.group(1)))
        return None

    starts, total_expected = _bare_ordinal_starts(stream, stream_start, num_standalone, match_standalone)

    answers = {}
    for i, (idx, qnos, letter) in enumerate(starts):
        if letter:
            answers[qnos[0]] = letter
            continue
        end_idx = starts[i + 1][0] if i + 1 < len(starts) else len(stream)
        pending = list(qnos)
        for j in range(idx, end_idx):
            text = stream[j][4]
            am = ANSWER_PREFIX_RE.search(text)
            if not am:
                if len(pending) == 1:
                    cm = CHOSEN_RE.search(text)
                    if cm:
                        answers[pending[0]] = cm.group(1)
                        pending = []
                continue
            rest = am.group(1)
            if len(pending) == 1:
                sm = SIMPLE_ANSWER_RE.match(rest.strip())
                if sm:
                    answers[pending[0]] = sm.group(1)
                    pending = []
                    continue
            local_pairs = PAIR_LOCAL_RE.findall(rest)
            if local_pairs:
                for local_idx, l in local_pairs:
                    li = int(local_idx) - 1
                    if 0 <= li < len(pending):
                        answers[pending[li]] = l
                pending = []
                continue
            abs_pairs = [(int(n), l) for n, l in PAIR_ABS_RE.findall(rest) if int(n) in pending]
            for n, l in abs_pairs:
                answers[n] = l
                pending.remove(n)

    missing = sorted(set(range(1, total_expected)) - set(answers))
    print(f'[explanations-bareordinal] answers found={len(answers)}', f'missing={missing}' if missing else '')

    for i, (idx, qnos, _letter) in enumerate(starts):
        end_idx = starts[i + 1][0] if i + 1 < len(starts) else len(stream)
        combined_path = f'{out_dir}/e{qnos[0]:02d}.png'
        render_stream_span(doc, stream, idx, end_idx, mid_x, page_h, page_w, combined_path, dpi=dpi)
        for q in qnos[1:]:
            shutil.copyfile(combined_path, f'{out_dir}/e{q:02d}.png')

    print(f'[explanations-bareordinal] units={len(starts)} questions={sum(len(s[1]) for s in starts)}')
    return answers
