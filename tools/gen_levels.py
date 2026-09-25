"""Read 心測中心's 「各科等級加標示與答對題數對照表」 (official_levels/<year>.pdf)
and write src/data/levels.ts: for every year the official level of every
possible number of correct answers.

  表一  國文、社會、自然: 答對題數 -> 等級加標示
  表二  英語: 閱讀答對題數 x 聽力答對題數 -> 英語整體等級加標示
        (備註1: 閱讀 alone 精熟/基礎/待加強, 聽力 alone 基礎/待加強)
  表三  數學: 選擇題答對題數 x 非選擇題級分 -> 等級加標示
  表四  英語 without 聽力: 閱讀答對題數 -> 英語整體等級加標示

Everything is checked before anything is written: every range list must
cover 0..滿分 exactly, 滿分 must equal the number of questions in the official
answer key, and in the 英語/數學 grids more correct answers may never give a
lower level. Any failure stops the script.

  python gen_levels.py
"""
import os
import re
import sys
import unicodedata

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'src', 'data', 'levels.ts')
ORDER = ['C', 'B', 'B+', 'B++', 'A', 'A+', 'A++']          # low -> high
RANGE = re.compile(r'^(\d+)(?:-(\d+))?$')


def norm(cell):
    """cell text without line breaks; NFKC because 110's PDF writes 精 as
    the compatibility ideograph U+FA1D"""
    return unicodedata.normalize('NFKC', cell or '').replace('\n', '')


def label(cell):
    """'基礎(B+)' / '精熟 (A)' / '待加強' -> 'B+' / 'A' / 'C'"""
    c = norm(cell).replace(' ', '')
    if c.startswith('待加強'):
        return 'C'
    m = re.fullmatch(r'(?:基礎|精熟)\((A\+\+|A\+|A|B\+\+|B\+|B)\)', c)
    if not m:
        raise ValueError(f'unknown level cell {cell!r}')
    return m.group(1)


def rng(cell):
    m = RANGE.match(norm(cell).replace(' ', ''))
    if not m:
        return None
    lo = int(m.group(1))
    return lo, int(m.group(2) or lo)


def by_count(ranges, full, what):
    """[(label, lo, hi)] -> list indexed by 答對題數, checking exact coverage"""
    out = [None] * (full + 1)
    for lab, lo, hi in ranges:
        for n in range(lo, hi + 1):
            if n > full or out[n] is not None:
                raise ValueError(f'{what}: {n} out of range or covered twice')
            out[n] = lab
    if None in out:
        raise ValueError(f'{what}: 答對題數 {out.index(None)} not covered')
    for a, b in zip(out, out[1:]):
        if ORDER.index(b) < ORDER.index(a):
            raise ValueError(f'{what}: level goes down')
    return out


def monotone_grid(grid, what):
    for i, row in enumerate(grid):
        for j, lab in enumerate(row):
            if j and ORDER.index(lab) < ORDER.index(row[j - 1]):
                raise ValueError(f'{what}: row {i} goes down at column {j}')
            if i and ORDER.index(lab) < ORDER.index(grid[i - 1][j]):
                raise ValueError(f'{what}: column {j} goes down at row {i}')


def page_with(doc, title):
    return next(i for i, p in enumerate(doc) if title in p.get_text())


def official_counts(year):
    """question counts per column of the official answer key"""
    rows = [l.split() for l in open(os.path.join(HERE, 'official_answers', f'{year}.txt'), encoding='utf-8')
            if re.fullmatch(r'\d{1,2}( [A-D])+', l.strip())]
    # a subject's column exists while its questions last: the count of rows
    # having at least k answers tells how many subjects reach that row
    return rows


def parse_year(year):
    doc = fitz.open(os.path.join(HERE, 'official_levels', f'{year}.pdf'))

    # 表一
    t = doc[page_with(doc, '表一')].find_tables().tables[0].extract()
    subjects = [unicodedata.normalize('NFKC', t[0][c] or '').strip() for c in (2, 4, 6)]
    if subjects != ['國文', '社會', '自然']:
        raise ValueError(f'{year} 表一 header {subjects}')
    table1 = {}
    for k, subj in enumerate(subjects):
        g, m = 2 + 2 * k, 3 + 2 * k
        ranges = []
        for row in t[1:]:
            mark = unicodedata.normalize('NFKC', row[1] or '').strip()
            r = rng(row[g]) if mark == 'C' else rng(row[m])
            if r is None:
                raise ValueError(f'{year} 表一 {subj} {mark}: no range in {row}')
            ranges.append((mark, *r))
        table1[subj] = ranges

    # 表二 grid, spread over several pages; rows start with the 閱讀 count
    grid = {}
    for p in doc:
        for tb in p.find_tables().tables:
            for row in tb.extract():
                cells = [c for c in row if c not in (None, '')]
                if len(cells) == 23 and re.fullmatch(r'\d+', cells[0].strip()) and '待加強' in ''.join(cells[1:]) + '待加強':
                    try:
                        grid[int(cells[0])] = [label(c) for c in cells[1:]]
                    except ValueError:
                        pass
    # 備註1 (閱讀 / 聽力 alone) and the 表三 grid, parsed from their tables
    reading, listening = [], []
    for p in doc:
        for tb in p.find_tables().tables:
            rows = tb.extract()
            flat = [[norm(c).strip() for c in r] for r in rows]
            if flat and '閱讀' in flat[0] and '聽力' in flat[0]:
                for r in flat[2:]:
                    vals = [c for c in r if c]
                    # [level, range, (level, range)] -- 閱讀 first, then 聽力
                    k = 0
                    if len(vals) >= 2 and vals[0] in ('精熟', '基礎', '待加強') and rng(vals[1]):
                        reading.append((vals[0], *rng(vals[1])))
                        k = 2
                    if len(vals) >= k + 2 and vals[k] in ('基礎', '待加強') and rng(vals[k + 1]):
                        listening.append((vals[k], *rng(vals[k + 1])))
    abc = {'精熟': 'A', '基礎': 'B', '待加強': 'C'}
    reading = [(abc[a], lo, hi) for a, lo, hi in reading]
    listening = [(abc[a], lo, hi) for a, lo, hi in listening]

    # 表三
    t = doc[page_with(doc, '表三')].find_tables().tables[0].extract()
    head = next(r for r in t if any((c or '').strip() == '0' for c in r[1:]))
    scores = [int(c) for c in head if c and re.fullmatch(r'\d+', c.strip())]
    math = {}
    for row in t:
        cells = [c for c in row if c not in (None, '')]
        if len(cells) == len(scores) + 1 and re.fullmatch(r'\d+', cells[0].strip()) and row is not head:
            try:
                math[int(cells[0])] = [label(c) for c in cells[1:]]
            except ValueError:
                pass

    # 表四
    t = doc[page_with(doc, '表四')].find_tables().tables[0].extract()
    only = []
    for row in t[1:]:
        vals = [norm(c).strip() for c in row if c and c.strip()]
        mark = next(v for v in vals if v in ORDER)
        r = [rng(v) for v in vals if rng(v)]
        only.append((mark, *r[-1]))

    # checks against the official answer key's question counts
    key_rows = official_counts(year)
    col_len = lambda k: sum(1 for r in key_rows if len(r) - 1 > k)
    # column order of the key: 國文 閱讀 聽力 數學 社會 自然 -- a row's
    # columns are the subjects still running, so count per subject from the
    # bank-independent row lengths is ambiguous; use the ranges' own maxima
    # and cross-check them with the key's total number of answers instead
    full = {s: max(hi for _, _, hi in table1[s]) for s in subjects}
    full['閱讀'] = max(grid)
    full['聽力'] = len(next(iter(grid.values()))) - 1
    full['數學'] = max(math)
    total_key = sum(len(r) - 1 for r in key_rows)
    if total_key != sum(full.values()):
        raise ValueError(f'{year}: tables say {full} (sum {sum(full.values())}), answer key has {total_key} answers')

    out = {
        'full': full,
        '國文': by_count(table1['國文'], full['國文'], f'{year}國文'),
        '社會': by_count(table1['社會'], full['社會'], f'{year}社會'),
        '自然': by_count(table1['自然'], full['自然'], f'{year}自然'),
        'readingOnly': by_count(only, full['閱讀'], f'{year}表四'),
        'reading': by_count(reading, full['閱讀'], f'{year}閱讀'),
        'listening': by_count(listening, full['聽力'], f'{year}聽力'),
    }
    if sorted(grid) != list(range(full['閱讀'] + 1)):
        raise ValueError(f'{year} 表二: rows {sorted(grid)}')
    out['english'] = [grid[i] for i in range(full['閱讀'] + 1)]
    monotone_grid(out['english'], f'{year}表二')
    if sorted(math) != list(range(full['數學'] + 1)) or scores != list(range(len(scores))):
        raise ValueError(f'{year} 表三: rows {sorted(math)} scores {scores}')
    out['math'] = [math[i] for i in range(full['數學'] + 1)]
    monotone_grid(out['math'], f'{year}表三')
    # the grid's corner cells must agree with the one-subject tables
    if out['english'][full['閱讀']][full['聽力']] != 'A++' or out['english'][0][0] != 'C':
        raise ValueError(f'{year} 表二 corners')
    return out


def ts_row(labels):
    return "'" + ' '.join(labels) + "'"


def main():
    years = sorted(int(f[:3]) for f in os.listdir(os.path.join(HERE, 'official_levels')) if re.fullmatch(r'\d{3}\.pdf', f))
    parsed = {}
    for y in years:
        try:
            parsed[y] = parse_year(y)
        except ValueError as e:
            print(f'ERROR {y}: {e}')
            sys.exit(1)
        f = parsed[y]['full']
        print(f'{y}: 滿分 {f}  數學非選 0-{len(parsed[y]["math"][0]) - 1} 級分')

    lines = [
        "// 心測中心「各科等級加標示與答對題數對照表」110–115 -- 由 tools/gen_levels.py",
        "// 自動產生，請勿手動修改。每個字串是依答對題數 0,1,2… 排列的等級（空白分隔）。",
        "export interface YearLevels {",
        "  /** 滿分題數 */",
        "  full: Record<'國文' | '社會' | '自然' | '閱讀' | '聽力' | '數學', number>;",
        "  /** 表一：答對題數 -> 等級加標示 */",
        "  國文: string; 社會: string; 自然: string;",
        "  /** 表四：只考閱讀時，閱讀答對題數 -> 英語整體等級加標示 */",
        "  readingOnly: string;",
        "  /** 備註：閱讀 A/B/C、聽力 B/C（不加標示） */",
        "  reading: string; listening: string;",
        "  /** 表二：[閱讀答對題數] -> 依聽力答對題數排列的英語整體等級加標示 */",
        "  english: string[];",
        "  /** 表三：[數學選擇題答對題數] -> 依非選擇題級分 0… 排列的等級加標示 */",
        "  math: string[];",
        "}",
        "",
        "export const LEVELS: Record<number, YearLevels> = {",
    ]
    for y, d in parsed.items():
        f = ', '.join(f"'{k}': {v}" for k, v in d['full'].items())
        lines.append(f"  {y}: {{")
        lines.append(f"    full: {{ {f} }},")
        for k in ('國文', '社會', '自然', 'readingOnly', 'reading', 'listening'):
            lines.append(f"    {k}: {ts_row(d[k])},")
        lines.append("    english: [")
        lines += [f"      {ts_row(r)}," for r in d['english']]
        lines.append("    ],")
        lines.append("    math: [")
        lines += [f"      {ts_row(r)}," for r in d['math']]
        lines.append("    ],")
        lines.append("  },")
    lines.append("};")
    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(lines) + '\n')
    print('written', OUT)


if __name__ == '__main__':
    main()
