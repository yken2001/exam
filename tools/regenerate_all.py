import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crop_lib import (
    crop_questions, crop_explanations,
    crop_questions_2col_grouped, crop_questions_2col_standalone,
    crop_questions_2col_localgroups, crop_questions_2col_bareordinal,
    crop_explanations_localgroups, crop_explanations_bareordinal,
)

DL = r'C:\Users\Ken\Downloads'
OUT = r'C:\Users\Ken\claude_workspace\exam-app\public'  # absolute: immune to cwd mistakes


def qpath(year, subj):
    return rf'{DL}\{year}會考{subj}題本.pdf'


def apath(year, subj):
    return rf'{DL}\{year}會考{subj}解析.pdf'


results = {}  # (subj, year) -> answers dict

# ---- 110 & 111: single-column booklets ----
CONFIG_110_111 = {
    110: {
        '國文': dict(total=48, pages=15, group_style='chinese'),
        '英文': dict(total=41, pages=13, group_style='bracket'),
        '數學': dict(total=26, pages=13, group_style='chinese'),
        '社會': dict(total=63, pages=15, group_style='chinese'),
        '自然': dict(total=54, pages=15, group_style='chinese'),
    },
    111: {
        '國文': dict(total=42, pages=15, group_style='chinese'),
        '英文': dict(total=43, pages=14, group_style='bracket'),
        '數學': dict(total=25, pages=13, group_style='chinese'),
        '社會': dict(total=54, pages=15, group_style='chinese'),
        '自然': dict(total=50, pages=15, group_style='chinese'),
    },
}

ENGLISH_BRACKET_GROUPS = {
    110: [(15, 16), (17, 18), (19, 21), (22, 24), (25, 28), (29, 31), (32, 34), (35, 37), (38, 41)],
    111: [(21, 22), (23, 24), (25, 26), (27, 29), (30, 32), (33, 36), (37, 39), (40, 43)],
}

for year, subjects in CONFIG_110_111.items():
    for subj, cfg in subjects.items():
        print(f'\n===== {subj} {year} =====')
        qout = f'{OUT}/questions/{subj}/{year}'
        eout = f'{OUT}/explanations/{subj}/{year}'
        crop_questions(
            qpath(year, subj), qout, num_questions=cfg['total'],
            first_page=1, last_page=cfg['pages'], group_style=cfg['group_style'],
        )
        if cfg['group_style'] == 'bracket':
            answers = crop_explanations(
                apath(year, subj), eout, num_questions=cfg['total'], group_style='bracket',
                passage_tag=(ENGLISH_BRACKET_GROUPS[year], '文章翻譯'),
            )
        else:
            answers = crop_explanations(apath(year, subj), eout, num_questions=cfg['total'], group_style='chinese')
        results[(subj, year)] = answers

# ---- 112: 2-column official release ----
print('\n===== 國文 112 =====')
crop_questions_2col_grouped(qpath(112, '國文'), f'{OUT}/questions/國文/112', num_questions=42)
results[('國文', 112)] = crop_explanations(apath(112, '國文'), f'{OUT}/explanations/國文/112', num_questions=42, group_style='chinese')

print('\n===== 數學 112 =====')
crop_questions_2col_standalone(qpath(112, '數學'), f'{OUT}/questions/數學/112', num_questions=23)
results[('數學', 112)] = crop_explanations(apath(112, '數學'), f'{OUT}/explanations/數學/112', num_questions=23, group_style='chinese')

print('\n===== 自然 112 =====')
crop_questions_2col_grouped(qpath(112, '自然'), f'{OUT}/questions/自然/112', num_questions=50)
results[('自然', 112)] = crop_explanations(apath(112, '自然'), f'{OUT}/explanations/自然/112', num_questions=50, group_style='chinese')

print('\n===== 社會 112 =====')
crop_questions_2col_localgroups(qpath(112, '社會'), f'{OUT}/questions/社會/112', num_standalone=43)
results[('社會', 112)] = crop_explanations_localgroups(apath(112, '社會'), f'{OUT}/explanations/社會/112', num_standalone=43)

print('\n===== 英文 112 =====')
crop_questions_2col_bareordinal(qpath(112, '英文'), f'{OUT}/questions/英文/112', num_standalone=23, section_marker='單一選擇題')
results[('英文', 112)] = crop_explanations_bareordinal(apath(112, '英文'), f'{OUT}/explanations/英文/112', num_standalone=23, section_marker='單一選擇題')

with open(r'C:\Users\Ken\claude_workspace\regenerate_answers.json', 'w', encoding='utf-8') as f:
    json.dump({f'{s}-{y}': a for (s, y), a in results.items()}, f, ensure_ascii=False, indent=2)

print('\nDONE')
