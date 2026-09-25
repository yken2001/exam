"""Rebuild the whole question bank from the 15 解析 PDFs.

  python build_bank.py            parse + render + write everything
  python build_bank.py --dry      parse only, print the verification report
  python build_bank.py 110 自然    limit to one PDF (combine with --dry)
"""
import json
import os
import re
import shutil
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_lib as B

HERE = os.path.dirname(os.path.abspath(__file__))
DL = os.path.join(HERE, 'source_pdfs')      # the 15 解析 PDFs (not in git)
APP = os.path.dirname(HERE)
PUBLIC = os.path.join(APP, 'public')
BANK_DIR = os.path.join(HERE, 'bank')
REFLOW_DIR = os.path.join(HERE, 'reflowed')
DPI = 150

SUBJECTS = ['國文', '英文', '數學', '自然', '社會']
YEARS = [110, 111, 112]
SUBJ_EN = {'國文': 'chinese', '英文': 'english', '數學': 'math', '自然': 'science', '社會': 'social'}

# per-file page furniture that the generic header/footer rules don't cover
RULES = {
    (110, '國文'): {'drop_last_page_col': 1},          # right half = 題型分析
    (110, '英文'): {'tag_groups': '文章翻譯'},          # 題組 have no "(15-16)" header
    (110, '數學'): {'cut_last_page_at': '對應表'},       # 章節對應表 on the last page
    (111, '國文'): {'drop_last_page': True},
    (111, '數學'): {'drop_last_page': True},
    (112, '英文'): {'start_after': '單一選擇題', 'bare_groups': True},  # skip the listening part
}

# multiple-choice question counts of each paper (cross-checked against the
# "(第1~54題)"-style ranges printed in the PDFs where they exist)
EXPECTED = {
    (110, '國文'): 48, (111, '國文'): 42, (112, '國文'): 42,
    (110, '英文'): 41, (111, '英文'): 43, (112, '英文'): 43,
    (110, '數學'): 26, (111, '數學'): 25, (112, '數學'): 25,
    (110, '自然'): 54, (111, '自然'): 50, (112, '自然'): 50,
    (110, '社會'): 63, (111, '社會'): 54, (112, '社會'): 54,
}

RANGE_IN_HEADER = re.compile(r'(\d{1,2})\s*[~〜～\-]\s*(\d{1,2})\s*題')


def build(year, subj, render=True):
    pdf = rf'{DL}\{year}會考{subj}解析.pdf'
    rules = dict(RULES.get((year, subj), {}))
    doc = fitz.open(pdf)
    rules['mid'] = doc[0].rect.width / 2
    edoc = fitz.open(pdf)      # explanations + 備查 PDF (footer painted out)
    qdoc = fitz.open(pdf)      # stems (footer and printed answer letters painted out)

    pieces, lines, warnings = B.reflow(doc, rules, mask_docs=(edoc, qdoc) if render else ())
    questions, groups, sections, start, end = B.parse(lines, rules)
    errors = B.compute_regions(lines, questions, groups, sections, end)
    notes = B.extract_answers(lines, questions, groups)

    expected = EXPECTED[(year, subj)]
    stated = [int(m.group(2)) for i in sections for m in RANGE_IN_HEADER.finditer(lines[i].text)]
    if len(questions) != expected:
        errors.append(f'found {len(questions)} questions, expected {expected}')
    if stated and max(stated) != expected:
        errors.append(f'section headers state up to Q{max(stated)}, expected {expected}')
    for q in questions:
        if not q.answer:
            errors.append(f'Q{q.qno}: no answer')
        if q.stem:
            stem_text = ''.join(lines[j].text for j in range(*q.stem)).replace(' ', '')
            if re.search(r'故選|答案[:：]|試題解析', stem_text):
                errors.append(f'Q{q.qno}: stem region contains explanation text')
            if q.group < 0 and not re.search(r'\(D\)|（D）', stem_text):
                notes.append(f'Q{q.qno}: no "(D)" option text in stem region (check image options)')

    result = {
        'year': year, 'subject': subj, 'count': len(questions),
        'answers': {q.qno: q.answer for q in questions},
        'groups': [[g.qnos[0], g.qnos[-1]] for g in groups if len(g.qnos) > 1],
        'warnings': warnings, 'errors': errors, 'notes': notes,
    }

    if render and not errors:
        en = SUBJ_EN[subj]
        os.makedirs(REFLOW_DIR, exist_ok=True)
        B.save_reflowed_pdf(edoc, pieces, os.path.join(REFLOW_DIR, f'{year}_{en}_解析重組.pdf'))

        qdir = os.path.join(PUBLIC, 'questions', en, str(year))
        edir = os.path.join(PUBLIC, 'explanations', en, str(year))
        for d in (qdir, edir):
            shutil.rmtree(d, ignore_errors=True)
            os.makedirs(d)

        B.mask_answer_letters(qdoc, lines, questions)
        qby = {q.qno: q for q in questions}
        sizes = {}
        question_file, explanation_file = {}, {}

        # one image per 題組 (passage + every item's stem), shared by its items
        for g in groups:
            if not g.qnos:
                continue
            parts = B.render_region(qdoc, pieces, lines, g.pre_black, end, DPI)
            for n in g.qnos:
                parts += B.render_region(qdoc, pieces, lines, qby[n].stem, end, DPI)
            name = f'q{g.qnos[0]:02d}'
            sizes[name] = B.stitch(parts, os.path.join(qdir, name + '.png'))
            for n in g.qnos:
                question_file[n] = g.qnos[0]

        rendered = {}      # explanation region -> qno whose file holds it
        for q in questions:
            if q.group < 0:
                name = f'q{q.qno:02d}'
                sizes[name] = B.stitch(B.render_region(qdoc, pieces, lines, q.stem, end, DPI),
                                       os.path.join(qdir, name + '.png'))
                question_file[q.qno] = q.qno
            pre = None
            if q.group >= 0 and groups[q.group].qnos[0] == q.qno:
                pre = groups[q.group].pre_expl
            key = (pre, q.expl)
            if key in rendered:          # 112 題組: one combined 答案/解析 block
                explanation_file[q.qno] = rendered[key]
                continue
            parts = B.render_region(edoc, pieces, lines, pre, end, DPI) if pre else []
            parts += B.render_region(edoc, pieces, lines, q.expl, end, DPI)
            name = f'e{q.qno:02d}'
            sizes[name] = B.stitch(parts, os.path.join(edir, name + '.png'))
            rendered[key] = q.qno
            explanation_file[q.qno] = q.qno
        result['sizes'] = sizes
        result['question_file'] = question_file
        result['explanation_file'] = explanation_file

    if render and not errors:      # --dry must not clobber the file gen_ts.py reads
        os.makedirs(BANK_DIR, exist_ok=True)
        with open(os.path.join(BANK_DIR, f'{year}_{SUBJ_EN[subj]}.json'), 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=1)
    return result


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    render = '--dry' not in sys.argv
    combos = [(y, s) for y in YEARS for s in SUBJECTS]
    if args:
        combos = [(int(args[0]), args[1])]
    report = []
    for y, s in combos:
        r = build(y, s, render=render)
        report.append(f'===== {y} {s}: {r["count"]} questions, groups={r["groups"]}')
        for k in ('errors', 'warnings', 'notes'):
            for msg in r[k]:
                report.append(f'  [{k[:-1]}] {msg}')
    with open(os.path.join(HERE, 'build_report.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(report) + '\n')
    print('\n'.join(report).encode('cp950', 'replace').decode('cp950'))


if __name__ == '__main__':
    main()
