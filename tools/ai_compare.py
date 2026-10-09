"""Compare an independent solver's answers (and difficulty ratings) with an AI set.

The solver replies one line per item:
  Q12: C | L4 | OK
  Q13: B | L3 | FLAG: two options fit ...

  python ai_compare.py ai2_math solver_reply.txt

prints every item where the solver's answer differs from the answer key or
that it flagged, then the mean rated difficulty and the level counts.
Exit code 1 if any answer differs.
"""
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
LINE = re.compile(r'^\s*Q(\d+)\s*:\s*([A-D])\s*\|\s*L\s*([1-5])\s*\|\s*(OK|FLAG\s*:?.*)$', re.I)


def main(name, reply_path):
    d = json.load(open(os.path.join(os.path.dirname(HERE), 'src', 'data', 'ai', name + '.json'), encoding='utf-8'))
    key = {i['qNo']: i['answer'] for i in d['items']}
    got, levels, flags = {}, {}, {}
    for line in open(reply_path, encoding='utf-8'):
        m = LINE.match(line.strip())
        if m:
            n = int(m.group(1))
            got[n], levels[n] = m.group(2).upper(), int(m.group(3))
            if m.group(4).upper().startswith('FLAG'):
                flags[n] = m.group(4)
    missing = sorted(set(key) - set(got))
    wrong = sorted(n for n in got if n in key and got[n] != key[n])
    print(f'{name}: {len(got)}/{len(key)} answered, {len(key) - len(wrong) - len(missing)} agree with the key')
    for n in missing:
        print(f'  Q{n}: no answer in the reply')
    for n in wrong:
        print(f'  Q{n}: key {key[n]}, solver {got[n]}' + (f' | {flags[n]}' if n in flags else ''))
    for n in sorted(set(flags) - set(wrong)):
        print(f'  Q{n}: (agrees) {flags[n]}')
    if levels:
        c = Counter(levels.values())
        mean = sum(levels.values()) / len(levels)
        print(f'  rated difficulty: mean {mean:.2f}  ' + '  '.join(f'L{k}={c.get(k, 0)}' for k in range(1, 6)))
    return 1 if wrong or missing else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
