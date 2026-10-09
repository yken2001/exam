"""Shared builder for the AI-made practice sets (AI-2 onward).

An item is written with its correct option first and its distractors after
it; the builder places the options so the answer letters follow TARGET (an
even spread chosen per set), and writes the explanation's letters itself:

  {c}            -> the correct option's letter
  {d0} {d1} {d2} -> the letters of the distractors, in the order given

and appends 「故選 (X)。」. So an explanation can discuss every option by
letter and still always agree with where the options ended up. A numeric item
passes check=(ok, [bad...]): ok must be True (the correct option equals the
computed value) and every bad False (no distractor equals it).

  b = SetBuilder('ai2_math', '數學', year=902, set_name='AI-2', title=..., note=..., target='CADB...')
  b.group(24, 25, passage)                 # 題組: passage shared by items 24-25
  b.item(stem, correct, [d0, d1, d2], explanation, figure=None, check=None)
  b.write()                                # src/data/ai/ai2_math.json
"""
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(os.path.dirname(HERE))
DATA_DIR = os.path.join(APP, 'src', 'data', 'ai')
PUBLIC = os.path.join(APP, 'public')

EN = {'國文': 'chinese', '英文': 'english', '英聽': 'listening', '數學': 'math', '自然': 'science', '社會': 'social'}


class SetBuilder:
    def __init__(self, name, subject, year, set_name, title, note, target, difficulty='', topics=()):
        self.name, self.subject, self.year = name, subject, year
        self.set_name, self.title, self.note = set_name, title, note
        self.difficulty, self.topics = difficulty, list(topics)
        self.k = 3 if subject == '英聽' else 4
        self.letters = 'ABCD'[:self.k]
        assert all(L in self.letters for L in target), 'TARGET has a letter beyond the options'
        self.target = target
        self.groups, self.items = [], []
        self.fig_dir = os.path.join(PUBLIC, 'ai', str(year), EN[subject])
        os.makedirs(self.fig_dir, exist_ok=True)

    # ---------------------------------------------------------------- figures
    def fig_path(self, filename):
        """(absolute path to save to, path the question refers to)"""
        return os.path.join(self.fig_dir, filename), f'ai/{self.year}/{EN[self.subject]}/{filename}'

    def save_fig(self, fig, filename):
        import matplotlib.pyplot as plt
        abs_path, rel = self.fig_path(filename)
        fig.savefig(abs_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        return rel

    # ---------------------------------------------------------------- items
    def next_letter(self):
        return self.target[len(self.items)]

    def arrange(self, correct, distractors):
        """options in display order for the NEXT item (for picture items whose
        panels must be drawn in the final order)"""
        opts = list(distractors)
        opts.insert(self.letters.index(self.next_letter()), correct)
        return opts

    def group(self, frm, to, passage, translation=None, figure=None):
        g = {'from': frm, 'to': to, 'passage': passage}
        if translation:
            g['translation'] = translation
        if figure:
            g['figure'] = figure
        self.groups.append(g)

    def item(self, stem, correct, distractors, explanation, figure=None, check=None, transcript=None, picture=False):
        n = len(self.items) + 1
        assert len(distractors) == self.k - 1, f'Q{n}: needs {self.k - 1} distractors'
        if not picture:
            assert correct not in distractors and len(set(distractors)) == len(distractors), f'Q{n}: duplicate options'
        if check is not None:
            ok, bad = check
            assert ok, f'Q{n}: computed value does not match the correct option'
            assert not any(bad), f'Q{n}: a distractor equals the computed value'
        letter = self.next_letter()
        opts = [''] * self.k if picture else self.arrange(correct, distractors)
        # letters of the distractors, in the order they were given
        others = [L for L in self.letters if L != letter]
        expl = explanation.replace('{c}', letter)
        for i, L in enumerate(others):
            expl = expl.replace('{d%d}' % i, L)
        assert '{c}' not in expl and '{d' not in expl, f'Q{n}: unreplaced placeholder'
        q = {'qNo': n, 'stem': stem, 'options': opts, 'answer': letter,
             'explanation': f'{expl}故選 ({letter})。'}
        if figure:
            q['figure'] = figure
        if transcript:
            q['transcript'] = [list(x) for x in transcript]
        self.items.append(q)
        return letter

    # ---------------------------------------------------------------- output
    def write(self):
        n = len(self.items)
        assert len(self.target) == n, f'TARGET has {len(self.target)} letters for {n} items'
        spread = Counter(self.target)
        assert max(spread.values()) - min(spread.get(L, 0) for L in self.letters) <= 2, f'uneven TARGET {spread}'
        out = os.path.join(DATA_DIR, self.name + '.json')
        data = {'set': self.set_name, 'year': self.year, 'subject': self.subject, 'title': self.title,
                'difficulty': self.difficulty, 'note': self.note, 'topics': self.topics,
                'groups': self.groups, 'items': self.items}
        if os.path.exists(out):                       # keep the verification record
            data['verification'] = json.load(open(out, encoding='utf-8')).get('verification', [])
        json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('written', out, 'answers', ''.join(q['answer'] for q in self.items), dict(sorted(spread.items())))
        return out


def spread_target(n, k=4, seed=0):
    """an answer-letter sequence of length n, letters as even as possible and
    never the same letter three times in a row (deterministic for a seed)"""
    import random
    letters = 'ABCD'[:k]
    rnd = random.Random(seed)
    while True:
        seq = list((letters * (n // k + 1))[:n])
        rnd.shuffle(seq)
        s = ''.join(seq)
        if not any(L * 3 in s for L in letters):
            return s
