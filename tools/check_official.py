"""Compare the question bank's answers with the official answer keys.

official_answers/<year>.txt holds the rows of 心測中心's 「選擇題參考答案一覽表」
(copied from the PDF text and checked against it with a SHA-256 of the rows).
Each row is: 題號, then the answer of every subject that still has a question
with that number, in the fixed column order 國文 英語閱讀 英語聽力 數學 社會
自然. Which columns a row holds therefore follows from each subject's
question count; a row with a different number of answers is an error.

  python check_official.py        exit code 1 on any difference
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COLUMNS = [('國文', 'chinese'), ('英文', 'english'), ('英聽', 'listening'),
           ('數學', 'math'), ('社會', 'social'), ('自然', 'science')]
LISTENING_COUNT = 21          # 110, 111: in the official key, not in the bank


def load_bank(year, en):
    path = os.path.join(HERE, 'bank', f'{year}_{en}.json')
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        return {int(k): v for k, v in json.load(f)['answers'].items()}


def main():
    problems = 0
    for name in sorted(os.listdir(os.path.join(HERE, 'official_answers'))):
        m = re.fullmatch(r'(\d{3})\.txt', name)
        if not m:
            continue
        year = int(m.group(1))
        banks = {zh: load_bank(year, en) for zh, en in COLUMNS}
        counts = {zh: len(b) if b else LISTENING_COUNT for zh, b in banks.items()}
        official = {zh: {} for zh, _ in COLUMNS}
        with open(os.path.join(HERE, 'official_answers', name), encoding='utf-8') as f:
            for line in f:
                if not re.fullmatch(r'\d{1,2}( [A-D])+', line.strip()):
                    continue
                n, *vals = line.split()
                n = int(n)
                cols = [zh for zh, _ in COLUMNS if counts[zh] >= n]
                if len(cols) != len(vals):
                    print(f'{year} 第{n}列: {len(vals)} 個答案，但依題數應有 {len(cols)} 科 {cols}')
                    problems += 1
                    continue
                for zh, v in zip(cols, vals):
                    official[zh][n] = v
        for zh, _ in COLUMNS:
            bank = banks[zh]
            if bank is None:
                print(f'{year}{zh}: 題庫沒有這一科（官方 {len(official[zh])} 題）')
                continue
            if sorted(official[zh]) != sorted(bank):
                print(f'{year}{zh}: 題數不同 官方 {len(official[zh])} 題 / 題庫 {len(bank)} 題')
                problems += 1
            diff = [f'Q{n} 官方{official[zh][n]} 題庫{bank[n]}'
                    for n in sorted(bank) if n in official[zh] and official[zh][n] != bank[n]]
            problems += len(diff)
            print(f'{year}{zh}: {len(bank)} 題, 與官方不同 {len(diff)} 題 {diff if diff else ""}')
    print('不一致總數:', problems)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
