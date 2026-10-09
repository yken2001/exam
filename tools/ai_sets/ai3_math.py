"""AI-3 數學（挑戰）: build src/data/ai/ai3_math.json and its figures.

Every answer is computed here with exact arithmetic (fractions.Fraction or
integers) and passed through check=(ok, [bad...]); the builder places the
options, writes the letters into the explanation and appends 「故選」.
Each item is tagged with its design level (# L3 .. # L5, see SPEC_AI2_AI3.md).

  PYTHONIOENCODING=utf-8 python tools/ai_sets/ai3_math.py
"""
import math
import os
import sys
from fractions import Fraction as F

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SetBuilder, spread_target  # noqa: E402

plt.rcParams['font.family'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False

TOPICS = [
    '數論與無理數的推理（反例）',
    '等差級數、等比數列建模',
    '二次函數最佳化（含限制條件）、拋物線隧道',
    '幾何：面積比、摺紙、圓內接四邊形、對稱求最短路徑、內心與外心、傾斜容器',
    '統計（四分位距）與機率',
    '規則閱讀與決策（票價方案、積分與比序）',
    '時事：2026 世界棒球經典賽（20 隊、4 組各 5 隊、各組前 2 名晉級八強、共 47 場；C 組東京巨蛋，日本 4 勝，韓國、澳洲、中華皆 2 勝 2 敗）: https://en.wikipedia.org/wiki/2026_World_Baseball_Classic',
    '時事：WBC C 組比分（中華 0：3 澳洲、中華 5：4 韓國（延長 10 局）、韓國 7：2 澳洲）與「同勝隊間失分 ÷ 防守出局數」比序（韓國 7/57、澳洲與中華 7/54）: https://en.wikipedia.org/wiki/2026_World_Baseball_Classic_Pool_C',
    '時事：韓國須至少贏 5 分且失分不超過 2 分才能晉級: https://www.koreajoongangdaily.com/sports/everything-had-to-go-just-right-for-korea-to-advance-to-wbc-knockout-stage-amazingly-it-did/12520933',
    '時事：Artemis II 於 2026/4/1 發射，4 名太空人，飛越月球背面時距月面最近約 6,545 公里，最遠距地 406,771 公里: https://en.wikipedia.org/wiki/Artemis_II',
    '月球直徑約 3,474 公里、地月平均距離約 384,400 公里: https://en.wikipedia.org/wiki/Moon ；地球平均半徑約 6,371 公里: https://en.wikipedia.org/wiki/Earth_radius',
    '時事：2026 米蘭－科爾蒂納冬奧共 116 個項目，獎牌榜前六名（挪威 18/12/11、美國 12/12/9、荷蘭 10/7/3、義大利 10/6/14、德國 8/10/8、法國 8/9/6）: https://en.wikipedia.org/wiki/2026_Winter_Olympics_medal_table',
    '時事：臺灣出生數 2016 年 208,440 人、2025 年 107,812 人（中央社引內政部）: https://www.cna.com.tw/news/acn/202601090280.aspx',
    '時事：臺灣 2024 年出生數 134,856 人（內政部 2025/1/10 公布）: https://www.mirrormedia.mg/story/20250110edi055',
]

b = SetBuilder('ai3_math', '數學', year=903, set_name='AI-3', title='AI-3 數學模擬卷（挑戰）',
               note='由 AI 依會考數學科選擇題型編寫（非會考真題），難度定位「挑戰」：接近會考最難一級，多為三步以上推理、長規則閱讀與決策、需要想通轉折的幾何與函數題，並以 2025–2026 年真實時事（世界棒球經典賽、Artemis II、米蘭冬奧、臺灣出生數）為素材。每題答案均由程式以精確分數計算驗證（tools/ai_sets/ai3_math.py），附圖依題目數據繪製。',
               target=spread_target(25, 4, 903), difficulty='挑戰', topics=TOPICS)


def fs(x):
    x = F(x)
    s = '−' if x < 0 else ''
    x = abs(x)
    return f'{s}{x.numerator}' if x.denominator == 1 else f'{s}{x.numerator}/{x.denominator}'


def blank(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def area(*P):
    s = 0
    for (x1, y1), (x2, y2) in zip(P, P[1:] + P[:1]):
        s += x1 * y2 - x2 * y1
    return abs(F(s)) / 2


def intersect(P1, P2, P3, P4):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = P1, P2, P3, P4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    t = F(num) / den if isinstance(num, (int, F)) and isinstance(den, (int, F)) else num / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


# ====================================================================== items

# 1  # L4
pairs = [(a, bq) for a in range(1, 1014) for bq in range(1, a) if a * a - bq * bq == 2025]
ndiv = sum(1 for d in range(1, 2026) if 2025 % d == 0)
b.item('若 a、b 都是正整數，且 a² − b²＝2025，則這樣的數對 (a, b) 共有幾組？',
       f'{len(pairs)} 組', ['8 組', f'{ndiv} 組', '14 組'],
       '【解析】a² − b²＝(a＋b)(a − b)＝2025＝3⁴×5²。設 a − b＝m、a＋b＝n，則 m×n＝2025、m＜n，且 m、n 同為奇數時 a＝(m＋n)/2、b＝(n − m)/2 都是整數。'
       '2025 的因數有 (4＋1)(2＋1)＝15 個，都是奇數；配成 m×n 且 m＜n 的有 (15 − 1)÷2＝7 組（m＝n＝45 時 b＝0，不是正整數，不算）。'
       '這 7 組是 (1,2025)、(3,675)、(5,405)、(9,225)、(15,135)、(25,81)、(27,75)。'
       '({d0}) 是把 m＝n＝45（b＝0）也算進去；({d1}) 是直接拿因數個數 15；({d2}) 是把 (m, n) 和 (n, m) 當成不同兩組，但 a − b 一定比 a＋b 小。',
       check=(len(pairs) == 7, [len(pairs) == 8, len(pairs) == ndiv, len(pairs) == 14]))
assert (53, 28) in pairs and ndiv == 15


# 2  # L5
class R2:
    """p + q√2 with rational p, q (exact)"""
    def __init__(self, p, q=0):
        self.p, self.q = F(p), F(q)

    def __add__(self, o):
        return R2(self.p + o.p, self.q + o.q)

    def __sub__(self, o):
        return R2(self.p - o.p, self.q - o.q)

    def __mul__(self, o):
        return R2(self.p * o.p + 2 * self.q * o.q, self.p * o.q + self.q * o.p)

    def __truediv__(self, o):
        den = o.p * o.p - 2 * o.q * o.q
        return self * R2(o.p / den, -o.q / den)

    def rational(self):
        return self.q == 0


s2 = R2(0, 1)
ms2 = R2(0, -1)
# counterexamples: both members rational although a, b are irrational
cx_sum_prod = (s2 + ms2).rational() and (s2 * ms2).rational()          # a=√2, b=−√2
cx_squares = True                                                       # a=√2, b=√3: a²=2, b²=3
assert (s2 * s2).rational() and math.isqrt(3) ** 2 != 3                 # √3 is irrational, (√3)²=3
cx_prod_quot = (s2 * s2).rational() and (s2 / s2).rational()            # a=b=√2
# the true statement: (a+b)+(a−b)=2a, so a+b and a−b cannot both be rational
b.item('已知 a、b 都是無理數。下列哪一個敘述「一定」正確？',
       '「a＋b」與「a − b」中，至少有一個是無理數',
       ['「a＋b」與「a×b」中，至少有一個是無理數', '「a²」與「b²」中，至少有一個是無理數', '「a×b」與「a÷b」中，至少有一個是無理數'],
       '【解析】若 a＋b 與 a − b 都是有理數，則兩者相加 (a＋b)＋(a − b)＝2a 也是有理數，a 就是有理數，與 a 是無理數矛盾，所以兩者至少有一個是無理數，一定正確。'
       '其他三個都能舉出反例：({d0}) 取 a＝√2、b＝−√2，a＋b＝0、a×b＝−2 都是有理數；'
       '({d1}) 取 a＝√2、b＝√3，a²＝2、b²＝3 都是有理數；({d2}) 取 a＝b＝√2，a×b＝2、a÷b＝1 都是有理數。',
       check=(True, [not cx_sum_prod, not cx_squares, not cx_prod_quot]))

# 3  # L5
a3 = 29
# S10 = S20  ->  10a + 45d = 20a + 190d  ->  d = −10a / 145
d3 = F(-10 * a3, 145)
S3 = lambda n: n * (2 * a3 + (n - 1) * d3) / 2
assert S3(10) == S3(20) and d3 == -2
best_n = max(range(1, 60), key=S3)
v3 = S3(best_n)
b.item('一個等差數列的首項是 29，且它的前 10 項和等於前 20 項和。在此數列的「前 n 項和」之中（n＝1, 2, 3, ……），最大的值是多少？',
       fs(v3), [fs(S3(14)), fs(S3(10)), fs(2 * v3)],
       '【解析】前 10 項和＝前 20 項和，表示第 11 項到第 20 項的和是 0。這 10 項的和＝(第 11 項＋第 20 項)×10÷2＝0，'
       '所以第 11 項＋第 20 項＝0，即 (29＋10d)＋(29＋19d)＝0，公差 d＝−2，第 n 項＝31 − 2n。'
       '第 15 項＝1＞0，第 16 項＝−1＜0，所以加到第 15 項時和最大：S₁₅＝15×(29＋1)÷2＝225。'
       '（也可看成 Sₙ＝−n²＋30n，因 S₁₀＝S₂₀，圖形的對稱軸是 n＝15。）'
       '({d0}) 是 S₁₄（也等於 S₁₆）＝224，差了一項；({d1}) 是 S₁₀＝S₂₀＝200，誤以為和在第 10 項或第 20 項時最大；({d2}) 是用公式時忘了除以 2。',
       check=(best_n == 15 and v3 == 225, [v3 == S3(14), v3 == S3(10), v3 == 450]))
assert S3(14) == S3(16) == 224 and S3(10) == 200

# 4  # L4  (current events: births)
b16, b24, b25 = 208440, 134856, 107812
r = F(b25, b24)
quarter = F(b16, 4)
k_geo = next(k for k in range(1, 50) if b25 * r ** k < quarter)
k_lin = next(k for k in range(1, 50) if b25 - (b24 - b25) * k < quarter)
k_q25 = next(k for k in range(1, 50) if b25 * r ** k < F(b25, 4))
yr = lambda k: f'{2025 + k} 年'
b.item('內政部統計臺灣的出生數如下表：\n| 年 | 2016 | 2024 | 2025 |\n| 出生數（人） | 208,440 | 134,856 | 107,812 |\n'
       '某研究小組（虛構情境）建立一個「假設模型」：2025 年以後，每一年的出生數都是前一年的 r 倍，r 等於 2025 年出生數 ÷ 2024 年出生數。'
       '依此模型，哪一年的出生數會第一次少於 2016 年出生數的四分之一？',
       yr(k_geo), [yr(k_lin), yr(k_q25), yr(k_geo + 1)],
       '【解析】2016 年的四分之一＝208,440÷4＝52,110。r＝107,812÷134,856≈0.7995，每過一年乘以 r：'
       '2026 年≈86,192、2027 年≈68,907、2028 年≈55,089（仍多於 52,110）、2029 年≈44,041（少於 52,110），所以是 2029 年。'
       '({d0}) 是改用「每年減少相同人數 27,044」的等差模型（2028 年 26,680），不是題目的等比模型；'
       '({d1}) 是把四分之一的基準弄成 2025 年（107,812÷4），而不是 2016 年；({d2}) 是多算了一年（2029 年就已經少於 52,110）。',
       check=(yr(k_geo) == '2029 年', [yr(k_lin) == yr(k_geo), yr(k_q25) == yr(k_geo), yr(k_geo + 1) == yr(k_geo)]))
assert (k_geo, k_lin, k_q25) == (4, 3, 7)
assert b25 * r ** 3 > quarter > b25 * r ** 4

# 5  # L4
pairs5 = [(a, c) for a in range(1, 10) for c in range(1, 10) if a != c]
cond5 = [(a, c) for a, c in pairs5 if a > c]
mult5 = [(a, c) for a, c in cond5 if (10 * a + c) % 4 == 0]
p5 = F(len(mult5), len(cond5))
p5_all = F(len(mult5), len(pairs5))
p5_no_cond = F(sum(1 for a, c in pairs5 if (10 * a + c) % 4 == 0), len(cond5))
b.item('有 9 張數字卡，分別寫著 1～9。小明從中任意抽出 2 張（不放回），第一張當十位數字、第二張當個位數字，組成一個二位數。'
       '他看了一眼後說：「十位數字比個位數字大。」在這個條件下，這個二位數是 4 的倍數的機率為何？',
       fs(p5), [fs(p5_all), fs(p5_no_cond), '1/4'],
       '【解析】已知十位數字比個位數字大，可能的結果只剩：從 1～9 任取兩個不同數字、大的當十位，共 9×8÷2＝36 種，機會相等。'
       '其中是 4 的倍數的有 32、52、64、72、76、84、92、96，共 8 個（12、16、24、28、36、48、56、68 雖然也是 4 的倍數，但十位比個位小，不符合條件）。機率＝8/36＝2/9。'
       '({d0}) 是分母仍用全部的 9×8＝72 種，沒有把已知條件納入；({d1}) 是分子用了全部 16 個 4 的倍數，沒有排除十位比個位小的；'
       '({d2}) 是以為「每 4 個整數有 1 個 4 的倍數」。',
       check=(p5 == F(2, 9), [p5 == p5_all, p5 == p5_no_cond, p5 == F(1, 4)]))
assert len(mult5) == 8 and (p5_all, p5_no_cond) == (F(1, 9), F(4, 9))

# 6  # L5
def fig_tunnel():
    fig, ax = blank(4.8, 3.0)
    xs = [x / 20 for x in range(-160, 161)]
    ax.plot(xs, [8 - x * x / 8 for x in xs], color='black', linewidth=1.6)
    ax.plot([-9.5, 9.5], [0, 0], color='black', linewidth=1.6)
    ax.plot([0, 0], [0, 8], color='#888888', linewidth=1, linestyle='--')
    ax.text(0.15, 8.2, '中線', fontsize=8, color='#555555')
    ax.annotate('', xy=(-8, -0.8), xytext=(8, -0.8), arrowprops=dict(arrowstyle='<->', linewidth=1))
    ax.text(0, -1.7, '16 公尺', ha='center', fontsize=9)
    # measurement 2 m from the right wall: height 3.5 m
    ax.plot([6, 6], [0, 3.5], color='#1f4e79', linewidth=1.2)
    ax.annotate('', xy=(6, 0.5), xytext=(8, 0.5), arrowprops=dict(arrowstyle='<->', linewidth=0.8, color='#1f4e79'))
    ax.text(7, 0.75, '2', ha='center', fontsize=8.5, color='#1f4e79')
    ax.text(5.8, 1.8, '3.5', ha='right', fontsize=8.5, color='#1f4e79')
    ax.text(3.0, 2.5, '右側車道', ha='center', fontsize=8.5, color='#555555')
    ax.set_xlim(-9.8, 9.8)
    ax.set_ylim(-2.2, 8.8)
    return b.save_fig(fig, 'q06_tunnel.png')


# y = a(64 − x²) through (6, 3.5)
a6 = F(7, 2) / (64 - 36)
yt = lambda x: a6 * (64 - x * x)
assert yt(0) == 8
clear = F(1, 2)
# the truck occupies [s, s + 3] with 1 ≤ s ≤ 5; the roof must clear the tunnel over the whole width
best_h = max(min(yt(F(s, 100) + F(k, 100)) for k in range(0, 301)) - clear for s in range(100, 501))
mid_h = yt(F(4) + F(3, 2)) - clear                     # truck centred in the lane (2.5 to 5.5)
b.item('某隧道的截面是拋物線形（如附圖），兩側牆腳相距 16 公尺，路面中央畫有中線。工程人員在距離右側牆腳水平 2 公尺處，量得隧道頂部離地面 3.5 公尺。'
       '一輛寬 3 公尺、車頂為水平的貨車要在右側車道通過，車身必須與中線至少保持 1 公尺，而且車頂與隧道頂部之間在鉛直方向至少要留 0.5 公尺。'
       '這輛貨車的高度最多可以是多少公尺？',
       f'{float(best_h):g} 公尺', ['6 公尺', '7.375 公尺', '約 3.72 公尺'],
       '【解析】以地面中點為原點，兩牆腳是 (−8, 0)、(8, 0)，設 y＝a(64 − x²)。距右牆腳 2 公尺處 x＝6，3.5＝a(64 − 36)，a＝1/8，y＝8 − x²/8（最高 8 公尺）。'
       '隧道越往外越低，貨車應盡量靠中線行駛：車身左側在 x＝1、右側在 x＝4，限制車高的是右側 x＝4 處的高度 8 − 2＝6，再留 0.5 公尺，車高最多 5.5 公尺。'
       '({d0}) 是忘了保留 0.5 公尺；({d1}) 是用車身左側 x＝1 的高度計算，但右側的隧道比較低，會撞到；'
       '({d2}) 是讓貨車走在車道正中央（x＝2.5 到 5.5），右側只有 8 − 5.5²/8≈4.22 公尺高，這不是最好的行駛位置。',
       figure=fig_tunnel(),
       check=(best_h == F(11, 2), [best_h == 6, best_h == yt(1) - clear, f'約 {float(mid_h):.2f} 公尺' == f'{float(best_h):g} 公尺']))
assert f'{float(mid_h):.2f}' == '3.72' and yt(1) - clear == F(59, 8)

# 7  # L5
def fig_incenter():
    fig, ax = blank(4.2, 3.4)
    A, B, C = (5, 12), (0, 0), (14, 0)
    I = (6, 4)
    D = (5 * 4 / 12, 4.0)                         # on AB at height 4 (AB from (0,0) to (5,12))
    E = (5 + 9 * (12 - 4) / 12, 4.0)              # on AC: from (5,12) to (14,0)
    ax.add_patch(Polygon([A, B, C], fill=False, linewidth=1.5))
    ax.plot([D[0], E[0]], [D[1], E[1]], color='black', linewidth=1.3)
    ax.plot(*I, 'o', color='black', markersize=3.5)
    for p, s, dx, dy in ((A, 'A', -0.3, 0.4), (B, 'B', -0.9, -0.7), (C, 'C', 0.3, -0.7), (D, 'D', -1.0, 0.0),
                         (E, 'E', 0.35, 0.0), (I, 'I', -0.2, -1.1)):
        ax.text(p[0] + dx, p[1] + dy, s, fontsize=11)
    ax.text(1.2, 7, '13', fontsize=10)
    ax.text(10.2, 7, '15', fontsize=10)
    ax.text(7, -1.3, '14', fontsize=10, ha='center')
    ax.set_xlim(-1.5, 15.5)
    ax.set_ylim(-2, 13.2)
    return b.save_fig(fig, 'q07_incenter.png')


a7, b7_, c7 = 14, 15, 13                     # BC, CA, AB
x7 = F(c7 ** 2 - b7_ ** 2 + a7 ** 2, 2 * a7)  # BH, foot of the altitude from A
h7 = 12
assert x7 == 5 and x7 ** 2 + h7 ** 2 == c7 ** 2 and (a7 - x7) ** 2 + h7 ** 2 == b7_ ** 2
area7 = F(a7 * h7, 2)
r7 = 2 * area7 / (a7 + b7_ + c7)
DE = a7 * (h7 - r7) / h7
b.item('如附圖，△ABC 中，AB＝13、AC＝15、BC＝14，I 是△ABC 的內心。過 I 作一直線平行 BC，分別交 AB、AC 於 D、E 兩點。DE 的長度為何？',
       fs(DE), ['7', '14/3', '8'],
       '【解析】作 A 到 BC 的高 AH，設 BH＝x：13² − x²＝15² − (14 − x)²，得 x＝5，AH＝√(13² − 5²)＝12，△ABC 面積＝14×12÷2＝84。'
       '內心到三邊的距離都是內切圓半徑 r，把△ABC 分成△IBC、△ICA、△IAB 三塊：84＝r×(13＋14＋15)÷2，r＝4。'
       'DE∥BC 且 DE 與 BC 的距離是 r＝4，所以 A 到 DE 的距離是 12 − 4＝8。△ADE 與△ABC 相似，DE：BC＝8：12，DE＝14×2/3＝28/3。'
       '({d0}) 是誤以為 DE 是中位線（I 不一定在高的中點）；({d1}) 是把相似比用成 r：AH＝4：12；({d2}) 是把 A 到 DE 的距離 8 當成 DE 的長。',
       figure=fig_incenter(),
       check=(DE == F(28, 3) and r7 == 4, [DE == 7, DE == F(14, 3), DE == 8]))

# 8  # L5
def fig_cevian():
    fig, ax = blank(4.2, 3.0)
    A, B, C = (2.2, 4.0), (0, 0), (6.0, 0)
    D = (B[0] + 2 / 3 * (C[0] - B[0]), 0)
    E = ((A[0] + D[0]) / 2, (A[1] + D[1]) / 2)
    Fp = tuple(float(v) for v in intersect(B, E, A, C))
    ax.add_patch(Polygon([A, B, C], fill=False, linewidth=1.5))
    ax.add_patch(Polygon([E, D, C, Fp], facecolor='#cfe2f3', edgecolor='none'))
    ax.plot([A[0], D[0]], [A[1], D[1]], color='black', linewidth=1.3)
    ax.plot([B[0], Fp[0]], [B[1], Fp[1]], color='black', linewidth=1.3)
    for p, s, dx, dy in ((A, 'A', -0.1, 0.15), (B, 'B', -0.35, -0.3), (C, 'C', 0.1, -0.3), (D, 'D', -0.1, -0.4),
                         (E, 'E', 0.15, 0.0), (Fp, 'F', 0.12, 0.05)):
        ax.text(p[0] + dx, p[1] + dy, s, fontsize=11)
    ax.set_xlim(-0.6, 6.6)
    ax.set_ylim(-0.6, 4.5)
    return b.save_fig(fig, 'q08_cevian.png')


A8, B8, C8 = (F(11, 5), F(4)), (F(0), F(0)), (F(6), F(0))
D8 = (B8[0] + F(2, 3) * (C8[0] - B8[0]), F(0))
E8 = ((A8[0] + D8[0]) / 2, (A8[1] + D8[1]) / 2)
F8 = intersect(B8, E8, A8, C8)
scale = F(60) / area(A8, B8, C8)
quad = area(E8, D8, C8, F8) * scale
ratio_AF = (F8[0] - A8[0]) / (C8[0] - A8[0])            # AF / AC
b.item('如附圖，△ABC 的面積是 60。D 在 BC 上且 BD：DC＝2：1，E 是 AD 的中點，直線 BE 與 AC 交於 F 點。四邊形 EDCF（著色部分）的面積為何？',
       fs(quad), ['15', '50/3', '40/3'],
       '【解析】先求 AF：FC。過 D 作 DG∥BF 交 AC 於 G。在△CBF 中，DG∥BF，所以 CG：GF＝CD：DB＝1：2；在△ADG 中，E 是 AD 中點且 EF∥DG，所以 F 是 AG 中點，AF＝FG。'
       '設 CG＝k，則 GF＝2k、AF＝2k，AF：FC＝2k：3k＝2：3。'
       '△ADC 的面積＝60×1/3＝20（DC 是 BC 的 1/3）。△AEF 與△ADC 共用 ∠A，面積比＝(AE/AD)×(AF/AC)＝1/2×2/5＝1/5，所以△AEF＝4，四邊形 EDCF＝20 − 4＝16。'
       '({d0}) 是誤以為 F 也是 AC 的中點（AF：FC＝1：1，△AEF＝5）；({d1}) 是誤用 AF：FC＝1：2（△AEF＝10/3）；({d2}) 是誤用 AF：FC＝2：1（△AEF＝20/3）。',
       figure=fig_cevian(),
       check=(quad == 16 and ratio_AF == F(2, 5), [quad == 15, quad == F(50, 3), quad == F(40, 3)]))


# 9  # L4
def fig_squarefold():
    fig, ax = blank(3.8, 3.8)
    A, B, C, D = (0, 12), (12, 12), (12, 0), (0, 0)
    M, E, Fp = (6, 0), (0, 4.5), (12, 10.5)

    def refl(P):
        (px, py), (ax_, ay), (bx, by) = P, E, Fp
        dx, dy = bx - ax_, by - ay
        t = ((px - ax_) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
        return (2 * (ax_ + t * dx) - px, 2 * (ay + t * dy) - py)
    B2 = refl(B)
    ax.add_patch(Polygon([E, Fp, C, D], fill=False, linewidth=1.5))
    ax.add_patch(Polygon([A, B, Fp, E], fill=False, linewidth=1, linestyle=':', edgecolor='#888888'))
    ax.add_patch(Polygon([E, Fp, B2, M], facecolor='#f2e6c9', edgecolor='black', linewidth=1.5, alpha=0.9))
    ax.plot([E[0], Fp[0]], [E[1], Fp[1]], color='black', linewidth=1.5, linestyle='--')
    for p, s, dx, dy in ((A, 'A', -0.9, 0.2), (B, 'B', 0.3, 0.2), (C, 'C', 0.3, -0.6), (D, 'D', -0.9, -0.6),
                         (M, 'M', -0.3, -1.0), (E, 'E', -1.0, -0.2), (Fp, 'F', -1.1, 0.3), (B2, "B'", 0.25, -0.3)):
        ax.text(p[0] + dx, p[1] + dy, s, fontsize=11)
    ax.set_xlim(-1.5, 14)
    ax.set_ylim(-1.5, 13.5)
    return b.save_fig(fig, 'q09_squarefold.png')


side = 12
# E on AD: EA = EM ; with D=(0,0), A=(0,12), M=(6,0): (12−y)² = 36 + y²
yE = F(144 - 36, 24)
# F on BC (x=12): FA = FM: 144 + (y−12)² = 36 + y²
yF = F(144 + 144 - 36, 24)
EF2 = 12 ** 2 + (yF - yE) ** 2
AM2 = 6 ** 2 + 12 ** 2
b.item('如附圖，正方形紙片 ABCD 的邊長為 12，M 是 CD 的中點。將紙片摺疊，使 A 點落在 M 點上，摺痕 EF 的兩端 E、F 分別在 AD、BC 上。摺痕 EF 的長度為何？',
       '6√5', ['3√5', '12', '15/2'],
       '【解析】摺痕 EF 是 AM 的垂直平分線。設 DE＝y，則 EA＝12 − y，EM²＝y²＋6²，由 EA＝EM 得 (12 − y)²＝y²＋36，y＝4.5；'
       '同理設 CF＝z，FA²＝12²＋(12 − z)²、FM²＝6²＋z²，得 z＝10.5。E、F 的高度差 10.5 − 4.5＝6，水平距離 12，EF＝√(12²＋6²)＝6√5。'
       '（另解：正方形中，一條連接一組對邊的線段若垂直於另一條連接另一組對邊的線段，兩者等長，所以 EF＝AM＝√(12²＋6²)＝6√5。）'
       '({d0}) 是 AM 的一半；({d1}) 是誤以為摺痕和邊一樣長（水平方向的長度）；({d2}) 是 AE 的長 12 − 4.5＝7.5。',
       figure=fig_squarefold(),
       check=(EF2 == 180 and EF2 == AM2, [EF2 == 45, EF2 == 144, EF2 == F(225, 4)]))
assert yE == F(9, 2) and yF == F(21, 2)


# 10  # L5
def fig_cyclic():
    fig, ax = blank(3.6, 3.6)
    ang = {'A': 90, 'B': 170, 'C': 310, 'D': 10}
    P = {k: (math.cos(math.radians(v)), math.sin(math.radians(v))) for k, v in ang.items()}
    ax.add_patch(Circle((0, 0), 1, fill=False, linewidth=1.5))
    ax.add_patch(Polygon([P['A'], P['B'], P['C'], P['D']], fill=False, linewidth=1.4))
    ax.plot([P['A'][0], P['C'][0]], [P['A'][1], P['C'][1]], color='black', linewidth=1.2)
    ax.plot([P['B'][0], P['D'][0]], [P['B'][1], P['D'][1]], color='black', linewidth=1.2)
    E = tuple(float(v) for v in intersect(P['A'], P['C'], P['B'], P['D']))
    off = {'A': (-0.05, 0.07), 'B': (-0.16, -0.02), 'C': (0.0, -0.15), 'D': (0.05, -0.02)}
    for k, (dx, dy) in off.items():
        ax.text(P[k][0] + dx, P[k][1] + dy, k, fontsize=12)
    ax.text(E[0] - 0.17, E[1] - 0.17, 'E', fontsize=12)
    # equal-length ticks on AB and AD
    for Q in (P['B'], P['D']):
        mx, my = (P['A'][0] + Q[0]) / 2, (P['A'][1] + Q[1]) / 2
        dx, dy = Q[0] - P['A'][0], Q[1] - P['A'][1]
        L = math.hypot(dx, dy)
        nx, ny = -dy / L * 0.05, dx / L * 0.05
        ax.plot([mx - nx, mx + nx], [my - ny, my + ny], color='black', linewidth=1.3)
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    return b.save_fig(fig, 'q10_cyclic.png')


AEB_given, CBD = 70, 30
ACB = AEB_given - CBD            # exterior angle of △EBC
ACD = ACB                        # AB = AD: equal chords subtend equal inscribed angles
BCD = ACB + ACD
BAD = 180 - BCD                  # cyclic quadrilateral
# cross-check with arcs (drawn figure): arc AB = arc AD = 80, arc CD = 60, arc BC = 140
arcAB = 2 * ACB
arcBC = 360 - 2 * arcAB - 2 * CBD
assert arcAB == 80 and arcBC == 140
assert (arcAB + 2 * CBD) / 2 == AEB_given and (arcBC + 2 * CBD) / 2 == BAD
b.item('如附圖，四邊形 ABCD 的四個頂點都在同一個圓上，AB＝AD，對角線 AC 與 BD 交於 E 點。若 ∠AEB＝70°、∠CBD＝30°，則 ∠BAD 的度數為何？',
       f'{BAD}°', ['80°', '110°', '140°'],
       '【解析】∠AEB 是△EBC 的外角：∠AEB＝∠EBC＋∠ECB，所以 ∠ACB＝70° − 30°＝40°。'
       'AB＝AD，等弦所對的圓周角相等，∠ACD＝∠ACB＝40°（AC 平分 ∠BCD），∠BCD＝80°。圓內接四邊形對角互補，∠BAD＝180° − 80°＝100°。'
       '({d0}) 是 ∠BCD，忘了要求的是它的對角；({d1}) 是 180° − 70°，把 ∠BAD 誤當成 ∠AEB 的補角；({d2}) 是 2×70°，把 ∠AEB 誤當成圓周角再換成圓心角。',
       figure=fig_cyclic(),
       check=(BAD == 100, [BAD == 80, BAD == 110, BAD == 140]))


# 11  # L5
def fig_river():
    fig, ax = blank(4.6, 2.9)
    ax.add_patch(Rectangle((-1.5, -1.0), 9.5, 1.0, facecolor='#d6eaf8', edgecolor='none'))
    ax.plot([-1.5, 8], [0, 0], color='#1f4e79', linewidth=1.6)
    ax.text(7.0, -0.65, '河', fontsize=10, color='#1f4e79')
    A, B = (0, 3), (6, 5)
    for p, s in ((A, '甲村'), (B, '乙村')):
        ax.plot(*p, 'o', color='black', markersize=5)
        ax.text(p[0] + 0.2, p[1] + 0.1, s, fontsize=10)
        ax.plot([p[0], p[0]], [0, p[1]], color='#888888', linewidth=1, linestyle='--')
    ax.text(-0.25, 1.4, '3 公里', ha='right', fontsize=9)
    ax.text(6.2, 2.4, '5 公里', fontsize=9)
    ax.annotate('', xy=(0, -0.35), xytext=(6, -0.35), arrowprops=dict(arrowstyle='<->', linewidth=1))
    ax.text(3, -0.85, '6 公里', ha='center', fontsize=9)
    ax.text(-0.2, 0.15, 'H', fontsize=10, ha='right')
    ax.text(6.1, 0.15, 'K', fontsize=10)
    ax.set_xlim(-1.6, 8.2)
    ax.set_ylim(-1.1, 5.7)
    return b.save_fig(fig, 'q11_river.png')


# plan 1: shortest total pipe (reflect 甲 across the bank); plan 2: P equidistant from both villages
x1 = F(6 * 3, 3 + 5)
x2 = F(36 + 25 - 9, 12)                          # x² + 9 = (6 − x)² + 25
assert x2 ** 2 + 9 == (6 - x2) ** 2 + 25
gap = x2 - x1
tot = lambda x: math.sqrt(x * x + 9) + math.sqrt((6 - x) ** 2 + 25)
assert abs(tot(float(x1)) - 10) < 1e-12 and all(tot(float(x1)) < tot(k / 100) + 1e-12 for k in range(0, 601))
b.item('如附圖，甲、乙兩村在一條筆直河岸的同一側，甲村到河岸的距離是 3 公里，乙村到河岸的距離是 5 公里，H、K 分別是兩村在河岸上的垂足，HK＝6 公里。'
       '自來水公司要在河岸上設一個抽水站 P，再分別鋪設直線水管到兩村，提出兩個方案：'
       '方案一：P 的位置使兩條水管的總長最短；方案二：P 的位置使 P 到兩村的距離相等。兩個方案中 P 的位置相距多少公里？',
       f'{fs(gap)} 公里', [f'{fs(3 - x1)} 公里', f'{fs(x2 - F(15, 4))} 公里', f'{fs(x2 - 3)} 公里'],
       '【解析】方案一：作甲村對河岸的對稱點甲′，P甲＋P乙＝P甲′＋P乙 ≥ 甲′乙，P 在甲′乙與河岸的交點時最短。兩個直角三角形相似，HP：PK＝3：5，HP＝6×3/8＝9/4。'
       '方案二：設 HP＝x，P 到甲村的距離平方＝x²＋3²，P 到乙村的距離平方＝(6 − x)²＋5²，兩者相等：x²＋9＝x² − 12x＋61，x＝13/3。'
       '兩個 P 都在 H 的同一側，相距 13/3 − 9/4＝25/12 公里。'
       '({d0}) 是把方案二的 P 誤取為 HK 的中點 3（算成 3 − 9/4），但兩村到河岸的距離不同，中點到兩村並不等距；'
       '({d1}) 是方案一的比例弄反（HP：PK＝5：3，HP＝15/4）；({d2}) 是把方案一的 P 誤取為 HK 中點（13/3 − 3）。',
       figure=fig_river(),
       check=(gap == F(25, 12), [gap == 3 - x1, gap == x2 - F(15, 4), gap == x2 - 3]))
assert (3 - x1, x2 - F(15, 4), x2 - 3) == (F(3, 4), F(7, 12), F(4, 3))


# 12  # L5
def fig_tilt():
    fig, ax = blank(4.4, 3.2)
    L, H, bw = 30, 40, 15
    phi = math.atan2(40, 15)                      # rotate so that QR becomes horizontal
    rot = lambda p: (p[0] * math.cos(phi) - p[1] * math.sin(phi), p[0] * math.sin(phi) + p[1] * math.cos(phi))
    P, Bt, Ct, Q = rot((0, 0)), rot((L, 0)), rot((L, H)), rot((0, H))
    R = rot((bw, 0))
    ax.plot([-45, 25], [0, 0], color='#555555', linewidth=1.2)
    ax.add_patch(Polygon([P, R, Q], facecolor='#9fc5e8', edgecolor='none'))
    ax.plot([Q[0], P[0], Bt[0], Ct[0]], [Q[1], P[1], Bt[1], Ct[1]], color='black', linewidth=1.8)
    ax.plot([Q[0], R[0]], [Q[1], R[1]], color='#1f4e79', linewidth=1.2)
    ax.text(P[0] + 1.0, P[1] + 0.8, 'P', fontsize=11)
    ax.text(Q[0] - 3.5, Q[1] + 0.5, 'Q', fontsize=11)
    ax.text(R[0] - 3.5, R[1] - 4.0, 'R', fontsize=11)
    ax.text(Bt[0] + 1.0, Bt[1] - 1.0, 'B', fontsize=11)
    ax.text(-10, -4.5, '側面圖：PQ＝40，PB＝30（單位：公分）', fontsize=9, ha='center')
    ax.text((Q[0] + R[0]) / 2 - 3, Q[1] + 1.2, '水面', fontsize=9, color='#1f4e79')
    ax.set_xlim(-45, 25)
    ax.set_ylim(-7, 46)
    return b.save_fig(fig, 'q12_tilt.png')


Lt, Wt, Ht, d0 = 30, 20, 40, 10
vol = Lt * Wt * d0
# trapezoid case would need the other wall's water height 2·d0 − Ht < 0, so the water is a triangle
assert 2 * d0 - Ht < 0
base12 = F(2 * vol, Ht * Wt)
b.item('一個無蓋的長方體玻璃容器，內部長 30 公分、寬 20 公分、高 40 公分，平放在桌上時水深 10 公分。'
       '現在以容器底面一條長 20 公分的邊 P 為轉軸，慢慢把容器向這一側傾斜（轉軸始終貼著桌面），直到水面恰好碰到這一側容器口的邊緣 Q 為止（如附圖，為傾斜後的側面圖）。'
       '此時水面與容器底面的交線 R 和轉軸 P 的距離 PR 是多少公分？',
       f'{fs(base12)} 公分', ['30 公分', '15/2 公分', '10 公分'],
       '【解析】水量＝30×20×10＝6000 立方公分。若水面還蓋滿整個底面，側面看是梯形，一側水深 40、另一側水深 h，'
       '則 (40＋h)×30÷2×20＝6000，h＝−20＜0，不可能，所以底面只被蓋住一部分，側面的水是直角三角形 PQR（∠P＝90°，PQ＝40）。'
       '40×PR÷2×20＝6000，PR＝15 公分。'
       '({d0}) 是以為水還蓋滿整個底面；({d1}) 是三角形面積忘了除以 2；({d2}) 是以為傾斜後 PR 仍等於原來的水深。',
       figure=fig_tilt(),
       check=(base12 == 15, [base12 == 30, base12 == F(15, 2), base12 == 10]))

# 13  # L5
table13 = [(50, 200), (55, 190), (60, 180), (65, 170)]
kq = F(table13[1][1] - table13[0][1], table13[1][0] - table13[0][0])     # −2
q0 = table13[0][1] - kq * table13[0][0]                                 # 300
assert all(q == q0 + kq * p for p, q in table13)
CAP = 100
sold = lambda p: min(q0 + kq * p, CAP)
profit = lambda p: (p - 30) * sold(p)
best_p = max(range(30, 151), key=profit)
assert sorted(range(30, 151), key=profit)[-2] != best_p and profit(best_p) > max(profit(p) for p in range(30, 151) if p != best_p)
free_p = max(range(30, 151), key=lambda p: (p - 30) * (q0 + kq * p))     # ignoring the cap
opt13 = lambda p, v: f'每份 {p} 元，每天利潤 {v} 元'
b.item('某攤販（虛構情境）賣每份成本 30 元的炒麵。他記錄了不同售價時一天「想買的人數」：\n| 售價（元） | 50 | 55 | 60 | 65 |\n| 想買的份數 | 200 | 190 | 180 | 170 |\n'
       '假設想買的份數與售價的關係一直維持表中的規律（售價每提高 1 元，想買的份數就減少相同的數量），售價為整數元。但他每天最多只能準備 100 份炒麵，賣完就收攤。'
       '售價訂為多少時，一天的利潤最大？最大利潤是多少？',
       opt13(best_p, profit(best_p)),
       [opt13(free_p, (free_p - 30) * (q0 + kq * free_p)), opt13(free_p, profit(free_p)), opt13(75, profit(75))],
       '【解析】想買的份數 q＝300 − 2p（每提高 5 元少 10 份，即每提高 1 元少 2 份），實際賣出的份數是 q 與 100 中較小的那個。'
       '(1) 售價 p ≤ 100 時，q ≥ 100，每天都賣完 100 份，利潤＝100(p − 30)，p 越大越多，p＝100 時 7000 元。'
       '(2) 售價 p ≥ 100 時，q ≤ 100，利潤＝(p − 30)(300 − 2p)＝−2(p − 90)²＋7200，頂點 p＝90 不在這個範圍內，p 越大利潤越小，所以也是 p＝100 時最大，(70)(100)＝7000 元。'
       '因此售價 100 元，最大利潤 7000 元。'
       '({d0}) 是忽略每天只能準備 100 份，直接用頂點 p＝90（那時有 120 人想買，但只能賣 100 份）；({d1}) 售價 90 元時實際只賣 100 份，利潤 6000 元，不是最大；'
       '({d2}) 是用「營收 p(300 − 2p) 最大」的售價 75 元，賣 100 份只賺 4500 元。',
       check=(best_p == 100 and profit(best_p) == 7000 and free_p == 90,
              [(free_p, 7200) == (best_p, profit(best_p)), (free_p, profit(free_p)) == (best_p, profit(best_p)), (75, profit(75)) == (best_p, profit(best_p))]))
assert profit(90) == 6000 and profit(75) == 4500

# 14  # L5
def fig_fence():
    fig, ax = blank(4.4, 2.8)
    ax.plot([0, 18], [6, 6], color='black', linewidth=4)
    ax.text(9, 6.4, '牆（長 18 公尺）', ha='center', fontsize=9)
    Lw, Wd = 12, 5
    x0 = 3
    ax.plot([x0, x0, x0 + Lw, x0 + Lw], [6, 6 - Wd, 6 - Wd, 6], color='#1f4e79', linewidth=1.6)
    ax.plot([x0 + 5, x0 + 7], [6 - Wd, 6 - Wd], color='white', linewidth=2.6)
    ax.plot([x0 + 5, x0 + 5], [6 - Wd - 0.35, 6 - Wd + 0.35], color='#1f4e79', linewidth=1)
    ax.plot([x0 + 7, x0 + 7], [6 - Wd - 0.35, 6 - Wd + 0.35], color='#1f4e79', linewidth=1)
    ax.text(x0 + 6, 6 - Wd - 1.0, '門 2 公尺', ha='center', fontsize=9)
    ax.text(x0 + Lw / 2, 6 - Wd / 2, '菜園', ha='center', fontsize=10)
    ax.set_xlim(-1.5, 19.5)
    ax.set_ylim(-0.6, 7.2)
    return b.save_fig(fig, 'q14_fence.png')


def fence_best(total, wall, gate):
    best = None
    for k in range(1, 4000):
        Wd = F(k, 100)
        Lw = total + gate - 2 * Wd
        if Lw <= gate or (wall is not None and Lw > wall):
            continue
        v = Wd * Lw
        if best is None or v > best:
            best = v
    return best


v14 = fence_best(40, 18, 2)
b.item('農場要用總長 40 公尺的圍籬圍出一塊長方形菜園，菜園的一邊靠著一面長 18 公尺的牆（靠牆的那一邊不用圍籬，且不能超出牆的長度），'
       '另外三邊用圍籬圍起來，並在與牆平行的那一邊留一個寬 2 公尺的門（門的部分不用圍籬），如附圖。菜園的面積最大是多少平方公尺？',
       f'{fs(v14)} 平方公尺', ['441/2 平方公尺', '200 平方公尺', '198 平方公尺'],
       '【解析】設垂直於牆的邊長為 x，與牆平行的邊長為 y。圍籬用在兩個 x 和扣掉門的 y：2x＋(y − 2)＝40，y＝42 − 2x。'
       '面積＝x(42 − 2x)＝−2(x − 10.5)²＋220.5，頂點在 x＝10.5，但那時 y＝21 超過牆長 18，不可行。'
       '限制 y ≤ 18 即 x ≥ 12，在 x ≥ 12 的範圍內面積隨 x 增大而變小，所以 x＝12、y＝18 時最大，面積 12×18＝216 平方公尺。'
       '({d0}) 是只看頂點、忽略牆長只有 18 公尺；({d1}) 是忘了門與牆長的條件，用 y＝40 − 2x 的頂點；({d2}) 是考慮了牆長卻忘了門不用圍籬（y＝40 − 2x ≤ 18，x＝11 時 11×18）。',
       figure=fig_fence(),
       check=(v14 == 216, [v14 == F(441, 2), v14 == 200, v14 == 198]))
assert fence_best(40, None, 2) == F(441, 2) and fence_best(40, None, 0) == 200 and fence_best(40, 18, 0) == 198


# 15  # L5
def fig_travel():
    fig, ax = plt.subplots(figsize=(4.8, 3.2))
    # time in hours after 8:00
    ax.plot([0, 1, 1.5, 2.5], [0, 4, 4, 8], color='#1f4e79', linewidth=1.8)
    ax.plot([0.5, 1.5], [12, 0], color='#c0392b', linewidth=1.8)
    ax.text(2.3, 8.5, '甲', fontsize=11, color='#1f4e79')
    ax.text(0.62, 11.6, '乙', fontsize=11, color='#c0392b')
    ax.set_xlim(0, 2.6)
    ax.set_ylim(0, 13)
    ax.set_xticks([0, 0.5, 1, 1.5, 2, 2.5])
    ax.set_xticklabels(['8:00', '8:30', '9:00', '9:30', '10:00', '10:30'])
    ax.set_yticks(range(0, 13, 2))
    ax.grid(True, color='#dddddd', linewidth=0.6)
    ax.set_xlabel('時刻', fontsize=9)
    ax.set_ylabel('與 A 地的距離（公里）', fontsize=9)
    ax.tick_params(labelsize=8)
    return b.save_fig(fig, 'q15_travel.png')


# 甲: 4 km/h, rests 9:00–9:30 at 4 km; 乙: from B (12 km) at 8:30, 12 km/h, reaches A at 9:30, then back at 12 km/h
def jia(t):
    return 4 * t if t <= 1 else (F(4) if t <= F(3, 2) else 4 + 4 * (t - F(3, 2)))


def yi(t):
    return 12 - 12 * (t - F(1, 2)) if t <= F(3, 2) else 12 * (t - F(3, 2))


cuts = [F(1, 2), F(1), F(3, 2), F(5, 2)]
hits = set()
for t0, t1 in zip(cuts, cuts[1:]):
    e0, e1 = yi(t0) - jia(t0), yi(t1) - jia(t1)          # linear on each piece
    for target in (2, -2):
        if e0 != e1 and min(e0, e1) <= target <= max(e0, e1):
            hits.add(t0 + (target - e0) / (e1 - e0) * (t1 - t0))
hits = sorted(hits)


def clock(t):
    m = 8 * 60 + t * 60
    assert m.denominator == 1
    m = int(m)
    return f'{m // 60}:{m % 60:02d}'


assert [clock(t) for t in hits] == ['9:00', '9:20', '9:45', '10:15']
b.item('A、B 兩地相距 12 公里。附圖是甲、乙兩人某天上午離 A 地的距離與時刻的關係圖：甲從 A 地出發步行前往 B 地，途中休息了一段時間；乙騎自行車從 B 地出發前往 A 地。'
       '乙到達 A 地後，立刻以原來的速率掉頭往 B 地方向騎，而甲則一直依圖中休息後的速率繼續走。從 8:30 到 10:30，兩人恰好相距 2 公里的時刻共有幾個？',
       f'{len(hits)} 個', ['3 個', '2 個', '5 個'],
       '【解析】由圖：甲每小時走 4 公里，9:00～9:30 在 4 公里處休息，之後每小時 4 公里；乙 8:30 從 12 公里處出發，每小時 12 公里，9:30 到 A 後掉頭。分段看兩人的距離：'
       '(1) 8:30～9:00 兩人相向，距離由 10 公里每小時減少 16 公里，9:00 時恰為 2 公里（甲在 4、乙在 6）。'
       '(2) 9:00～9:30 甲休息，乙繼續往 A，9:10 兩人相遇，之後乙越離越遠，9:20 時乙在 2 公里處，又相距 2 公里；9:30 相距 4 公里。'
       '(3) 9:30 以後乙掉頭追甲，距離每小時縮小 8 公里，9:45 相距 2 公里，10:00 追上；之後乙超前，10:15 又相距 2 公里，10:30 相距 4 公里。'
       '共 9:00、9:20、9:45、10:15 四個時刻。'
       '({d0}) 多半是漏了 9:20（以為甲休息時兩人不會再拉開）或漏了 10:15（以為追上後就結束）；({d1}) 只算了兩人「接近」時的 9:00 與 9:45；'
       '({d2}) 是把 9:00 算了兩次（它同時是第一段的終點和第二段的起點）。',
       figure=fig_travel(),
       check=(len(hits) == 4, [len(hits) == 3, len(hits) == 2, len(hits) == 5]))


# 16  # L5
def stats(xs):
    s = sorted(xs)
    n = len(s)
    med = lambda t: F(t[len(t) // 2]) if len(t) % 2 else F(t[len(t) // 2 - 1] + t[len(t) // 2], 2)
    q1, q2, q3 = med(s[:n // 2]), med(s), med(s[(n + 1) // 2:])
    return {'mean': F(sum(s), n), 'median': q2, 'iqr': q3 - q1, 'range': s[-1] - s[0]}


old16 = [72, 35, 86, 61, 90, 58, 75, 98, 64, 80, 55, 70, 82, 68, 78]
new16 = [85 if x == 35 else x for x in old16]
before, after = stats(old16), stats(new16)
same = [k for k in before if before[k] == after[k]]
names = {'mean': '平均數', 'median': '中位數', 'iqr': '四分位距', 'range': '全距'}
b.item('某班（虛構情境）15 位同學的數學小考成績登記如下：\n'
       '| 座號 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |\n'
       '| 成績 | 72 | 35 | 86 | 61 | 90 | 58 | 75 | 98 | 64 | 80 | 55 | 70 | 82 | 68 | 78 |\n'
       '後來發現 2 號同學的成績應為 85 分，被誤登記成 35 分。更正後，下列哪一個統計量與更正前相同？'
       '（四分位數的求法：資料由小到大排列，中位數以下的資料的中位數為第一四分位數，中位數以上的資料的中位數為第三四分位數。）',
       '四分位距', ['平均數', '中位數', '全距'],
       '【解析】更正前由小到大：35、55、58、61、64、68、70、72、75、78、80、82、86、90、98，中位數 72，第一四分位數＝前 7 筆的中位數 61，第三四分位數＝後 7 筆的中位數 82，四分位距 21，全距 98 − 35＝63。'
       '更正後：55、58、61、64、68、70、72、75、78、80、82、85、86、90、98，中位數 75，第一四分位數 64，第三四分位數 85，四分位距仍是 85 − 64＝21，全距變成 98 − 55＝43。'
       '雖然兩個四分位數都改變了，但它們都恰好增加 3，差不變。'
       '({d0}) 總分增加 50，平均數增加 50/15；({d1}) 85 移到中位數的上方，中位數由 72 變成 75；({d2}) 最小值由 35 變成 55，全距變小。',
       check=(same == ['iqr'], ['mean' in same, 'median' in same, 'range' in same]))
assert before['iqr'] == 21 and after['median'] == 75 and after['range'] == 43

# 17  # L5  (current events: Artemis II)
dm, de, dist, alt = 3470, 12740, 384400, 6545
to_moon = alt + F(dm, 2)
to_earth = to_moon + dist
ratio17 = (F(dm) / to_moon) / (F(de) / to_earth)
wrong_surface = (F(dm) / alt) / (F(de) / (alt + dist))
wrong_dist = to_earth / to_moon
wrong_diam = F(dm, de)


def about(x):
    x = F(x)
    return f'約 {round(float(x))} 倍' if x >= 1 else f'約 {float(x):.2f} 倍'


b.item('2026 年 4 月，美國 NASA 的 Artemis II 任務載著 4 名太空人繞過月球，飛越月球背面時與月球表面最近的距離約 6,545 公里。'
       '已知月球直徑約 3,470 公里，地球直徑約 12,740 公里；地球中心到月球中心的距離以平均值約 384,400 公里估算。'
       '看一個遠方的球體時，它「看起來的大小」可以用這個方法比較：在眼睛前方固定距離處放一片透明板，球體直徑在板上投影的長度，與「球體直徑 ÷ 球體中心到眼睛的距離」成正比（相似三角形）。'
       '假設在最接近月球時，太空船、月球中心、地球中心恰好在同一直線上（太空船在月球外側）。從太空船上看，月球看起來的大小約是地球看起來大小的幾倍？',
       about(ratio17), [about(wrong_surface), about(wrong_dist), about(wrong_diam)],
       '【解析】太空船到月球中心＝6,545＋3,470÷2＝8,280 公里；到地球中心＝8,280＋384,400＝392,680 公里。'
       '月球的投影長度與 3,470÷8,280 成正比，地球的與 12,740÷392,680 成正比，兩者相比＝(3,470÷8,280)÷(12,740÷392,680)≈0.419÷0.0324≈12.9，約 13 倍，所以月球會把地球完全擋住。'
       '({d0}) 是把太空船到月面的 6,545 公里當成到月球中心的距離（沒有加上月球半徑）；({d1}) 只比較了距離 392,680÷8,280，忘了兩個球的大小不同；'
       '({d2}) 只比較了直徑 3,470÷12,740，忘了距離的影響。',
       check=(about(ratio17) == '約 13 倍',
              [about(wrong_surface) == about(ratio17), about(wrong_dist) == about(ratio17), about(wrong_diam) == about(ratio17)]))
assert (about(wrong_surface), about(wrong_dist), about(wrong_diam)) == ('約 16 倍', '約 47 倍', '約 0.27 倍')

# 18  # L4  (current events: Winter Olympics medal table)
medals = [('挪威', 18, 12, 11), ('美國', 12, 12, 9), ('荷蘭', 10, 7, 3), ('義大利', 10, 6, 14), ('德國', 8, 10, 8), ('法國', 8, 9, 6)]
official = [m[0] for m in medals]
assert official == [m[0] for m in sorted(medals, key=lambda m: (-m[1], -m[2], -m[3]))]


def ned_strictly_third(x):
    pts = {m[0]: x * m[1] + 2 * m[2] + m[3] for m in medals}
    above = sum(1 for k in pts if pts[k] > pts['荷蘭'])
    tied = sum(1 for k in pts if k != '荷蘭' and pts[k] == pts['荷蘭'])
    return above == 2 and tied == 0


possible = [x for x in range(3, 2001) if ned_strictly_third(x)]
x_ger = next(x for x in range(3, 100) if 10 * x + 17 > 8 * x + 28)     # only compared with 德國
x_fra = next(x for x in range(3, 100) if 10 * x + 17 > 8 * x + 24)     # only compared with 法國
b.item('2026 年米蘭－科爾蒂納冬季奧運共有 116 個比賽項目。下表是官方獎牌榜的前六名（官方排名：先比金牌數，相同再比銀牌數，再比銅牌數）：\n'
       '| 官方排名 | 國家 | 金 | 銀 | 銅 | 總數 |\n'
       + ''.join(f'| {i + 1} | {m[0]} | {m[1]} | {m[2]} | {m[3]} | {sum(m[1:])} |\n' for i, m in enumerate(medals))
       + '若只就這六國，改用「金牌 x 分、銀牌 2 分、銅牌 1 分」（x 是大於 2 的整數）的積分由高到低排名。要讓荷蘭的積分排在這六國的第 3 名（只低於兩國、且不與他國同分），x 最小是多少？',
       '無論 x 是多少，荷蘭都不可能排在第 3 名',
       [f'x 最小是 {x_ger}', f'x 最小是 {x_fra}', 'x 最小是 10'],
       '【解析】荷蘭的積分 10x＋2×7＋3＝10x＋17，義大利的積分 10x＋2×6＋14＝10x＋26。兩國金牌數相同，x 不論多大，金牌部分都一樣多，'
       '義大利永遠比荷蘭多 9 分；挪威（18 金）與美國（12 金、12 銀、9 銅，積分 12x＋33）也一定比荷蘭高。所以荷蘭前面至少有挪威、美國、義大利三國，不可能排第 3 名。'
       '({d0}) 只和德國比較（10x＋17＞8x＋28，x＞5.5），忘了義大利；({d1}) 只和法國比較（10x＋17＞8x＋24，x＞3.5）；'
       '({d2}) 是以為 x 只要大於兩國銀、銅積分的差 9 就能反超，但兩國金牌一樣多，提高 x 並不會拉開差距。',
       check=(possible == [], [ned_strictly_third(x_ger), ned_strictly_third(x_fra), ned_strictly_third(10)]))
assert (x_ger, x_fra) == (6, 4)

# 19-20  題組: swimming pool plans (fictional)
b.group(19, 20, '某市立游泳館（虛構情境）的收費方案如下：\n'
        '| 方案 | 收費 | 說明 |\n'
        '| 單次票 | 每次 120 元 | 每次入場購買 |\n'
        '| 十次券 | 每本 1000 元 | 每本可入場 10 次，一年內有效，可買多本，也可與單次票搭配使用 |\n'
        '| 季卡 | 2400 元 | 啟用後連續 3 個月內不限次數入場 |\n'
        '| 年度會員 | 年費 600 元 | 一年內每次入場只要再付 60 元 |\n'
        '各方案都只能自己使用。')


def best_pack(n):
    """cheapest mix of 10-visit books and single tickets for n visits"""
    return min(1000 * k + 120 * max(0, n - 10 * k) for k in range(0, n // 10 + 2))


member = lambda n: 600 + 60 * n
n19 = next(n for n in range(1, 200) if member(n) < best_pack(n))
assert all(member(n) < best_pack(n) for n in range(n19, 200))
n19_cont = next(n for n in range(1, 200) if member(n) < 100 * n)          # 10-visit book as 100 元/次
n19_single = next(n for n in range(1, 200) if member(n) < 120 * n)
# 19  # L4
b.item('小安一年內預計去游泳 n 次。若只比較「年度會員」與「十次券和單次票的最省搭配」兩種做法，n 最少要是多少，年度會員才會比另一種做法省錢（而且次數再多也都是會員較省）？',
       f'{n19} 次', [f'{n19_cont} 次', f'{n19_single} 次', '13 次'],
       '【解析】十次券＋單次票的最省搭配：10 次 1000 元，超過 10 次的部分若不到 9 次就用單次票（9 次單次票 1080 元已超過一本十次券）。'
       '13 次：1000＋3×120＝1360 元，會員 600＋13×60＝1380 元，還是十次券省；14 次：1000＋4×120＝1480 元，會員 600＋840＝1440 元，會員較省，'
       '之後會員每次只多 60 元、另一種做法平均每次至少多 100 元，會員一直比較省。所以 n 至少 14。'
       '({d0}) 是把十次券看成每次 100 元連續計算（600＋60n＜100n，n＞15），忽略剩下的次數要用較貴的單次票；({d1}) 只和單次票比較；({d2}) 13 次時十次券搭配單次票仍便宜 20 元。',
       check=(n19 == 14, [n19 == n19_cont, n19 == n19_single, n19 == 13]))
assert (n19_cont, n19_single) == (16, 11) and best_pack(13) == 1360 and member(13) == 1380

# 20  # L5
def others(n):
    return min(best_pack(n), member(n))


k20 = next(k for k in range(1, 100) if 2400 < others(3 * k))
k_vs_pack = next(k for k in range(1, 100) if 2400 < best_pack(3 * k))
k_vs_single = next(k for k in range(1, 100) if 2400 < 120 * 3 * k)
b.item('小傑一年中只在 6、7、8 月去游泳（季卡可以涵蓋這 3 個月），每個月都去 k 次。若要「買季卡」比其他任何做法（任何方案或搭配）都省錢，k 最小是多少？',
       f'{k20}', ['10', f'{k_vs_pack}', f'{k_vs_single}'],
       '【解析】3 個月共 3k 次。季卡 2400 元固定。'
       '與年度會員比：600＋60×3k＞2400，k＞10，k＝10 時兩者都是 2400 元，一樣貴，季卡沒有比較省，所以 k 至少 11。'
       '與十次券搭配比：k＝11 時 33 次要 3000＋3×120＝3360 元，季卡較省；單次票更貴。所以 k 最小是 11。'
       '({d0}) 是 k＝10 時季卡與會員同價，並不是「比較省」；({d1}) 只和十次券比較（k＝8 時 24 次要 2480 元）而忘了年度會員；({d2}) 只和單次票比較（360k＞2400）。',
       check=(k20 == 11, [k20 == 10, k20 == k_vs_pack, k20 == k_vs_single]))
assert member(30) == 2400 and (k_vs_pack, k_vs_single) == (8, 7)

# 21-22  題組: admission points with tie-breaks (fictional)
LV = {'A++': 7, 'A+': 6, 'A': 5, 'B++': 4, 'B+': 3, 'B': 2, 'C': 1}
WR = {6: F(1), 5: F(4, 5), 4: F(3, 5), 3: F(2, 5)}
b.group(21, 22, '某區（虛構情境）免試入學的會考積分與比序規則如下：\n'
        '1. 國文、英語、數學、自然、社會五科依等級換算點數：A++ 7 點、A+ 6 點、A 5 點、B++ 4 點、B+ 3 點、B 2 點、C 1 點。\n'
        '2. 寫作測驗：6 級分 1 分、5 級分 0.8 分、4 級分 0.6 分、3 級分以下 0.4 分。\n'
        '3. 總積分＝五科點數總和＋寫作分數，總積分高者排在前面。\n'
        '4. 總積分相同時，依序比較：(1) 五科中 A++ 的科數，多者在前；(2) 數學點數，高者在前；(3) 國文點數，高者在前；仍相同則抽籤。\n'
        '下表是四位同學的成績：\n'
        '| 學生 | 國文 | 英語 | 數學 | 自然 | 社會 | 寫作 |\n'
        '| 甲 | A++ | A+ | A+ | A | A++ | 5 級分 |\n'
        '| 乙 | A+ | A++ | A++ | A+ | A | 5 級分 |\n'
        '| 丙 | A++ | A++ | B++ | A++ | A+ | 5 級分 |\n'
        '| 丁 | A+ | A+ | A++ | A+ | A+ | 6 級分 |')
studs = {'甲': (['A++', 'A+', 'A+', 'A', 'A++'], 5), '乙': (['A+', 'A++', 'A++', 'A+', 'A'], 5),
         '丙': (['A++', 'A++', 'B++', 'A++', 'A+'], 5), '丁': (['A+', 'A+', 'A++', 'A+', 'A+'], 6)}


def key(st, use_writing=True, math_first=False):
    lv, w = st
    pts_ = sum(LV[x] for x in lv) + (WR[w] if use_writing else 0)
    app = sum(1 for x in lv if x == 'A++')
    mth, chi = LV[lv[2]], LV[lv[0]]
    return (-pts_, -mth, -app, -chi) if math_first else (-pts_, -app, -mth, -chi)


order = ''.join(sorted(studs, key=lambda k: key(studs[k])))
order_nowrite = ''.join(sorted(studs, key=lambda k: key(studs[k], use_writing=False)))
order_math_first = ''.join(sorted(studs, key=lambda k: key(studs[k], math_first=True)))
order_reverse = ''.join(sorted(studs, key=lambda k: key(studs[k])[:1] + (-LV[studs[k][0][0]], -LV[studs[k][0][2]], key(studs[k])[1])))
# 21  # L4
b.item('依上述規則，四位同學由前到後的排序為何？',
       '、'.join(order), ['、'.join(order_reverse), '、'.join(order_nowrite), '、'.join(order_math_first)],
       '【解析】總積分：甲 7＋6＋6＋5＋7＝31，加寫作 0.8 得 31.8；乙 6＋7＋7＋6＋5＝31，31.8；丙 7＋7＋4＋7＋6＝31，31.8；丁 6＋6＋7＋6＋6＝31，加寫作 1 得 32.0。'
       '丁總積分最高排第一（比序只在總積分相同時才用）。甲、乙、丙同為 31.8：A++ 科數丙 3 科、甲 2 科、乙 2 科，丙在前；甲乙再比數學，乙 A++（7 點）＞甲 A+（6 點），乙在前。'
       '所以是丁、丙、乙、甲。'
       '({d0}) 是把比序的順序倒過來，從 (3) 國文開始比（甲、丙國文 A++ 在前，再比數學甲在丙前）；({d1}) 是忘了加寫作分數，四人五科都是 31 點，全部進入比序；({d2}) 是把比序 (1)(2) 的順序弄反，先比數學。',
       check=(order == '丁丙乙甲', [order_reverse == order, order_nowrite == order, order_math_first == order]))
assert (order_reverse, order_nowrite, order_math_first) == ('丁甲丙乙', '丙乙甲丁', '丁乙甲丙')


# 22  # L5
def wu(mlv, w):
    return (['A++', 'A+', mlv, 'A+', 'A'], w)


def between(st):
    """after 丙 and before 乙 in the ranking"""
    return key(studs['丙']) < key(st) < key(studs['乙'])


opts22 = {('A++', 5): '數學 A++，寫作 5 級分', ('A++', 6): '數學 A++，寫作 6 級分',
          ('A+', 6): '數學 A+，寫作 6 級分', ('A++', 4): '數學 A++，寫作 4 級分'}
ok22 = [k for k in opts22 if between(wu(*k))]
assert ok22 == [('A++', 5)]
b.item('另一位同學戊的國文 A++、英語 A+、自然 A+、社會 A，數學等級與寫作級分都還沒公布。後來戊和上表四人一起排序，結果戊恰好排在丙之後、乙之前。'
       '戊的數學等級與寫作級分可能是下列何者？',
       opts22[('A++', 5)], [opts22[('A++', 6)], opts22[('A+', 6)], opts22[('A++', 4)]],
       '【解析】戊其他四科 7＋6＋6＋5＝24 點。乙、丙的總積分都是 31.8，丙 A++ 3 科排在乙前面。戊要在丙之後、乙之前，總積分只能也是 31.8，再靠比序夾在中間。'
       '數學 A++、寫作 5 級分：24＋7＋0.8＝31.8。和丙比：A++ 科數戊 2 科（國文、數學）＜丙 3 科，戊在丙之後；和乙比：A++ 都是 2 科、數學都是 7 點，國文戊 A++＞乙 A+，戊在乙之前，符合。'
       '({d0}) 總積分 32.0，高於丙，會排在丙之前（甚至在丁之前，因為和丁同分時 A++ 科數 2＞1）；'
       '({d1}) 總積分 24＋6＋1＝31.0，低於乙；({d2}) 總積分 24＋7＋0.6＝31.6，也低於乙。',
       check=(between(wu('A++', 5)), [between(wu('A++', 6)), between(wu('A+', 6)), between(wu('A++', 4))]))

# 23-25  題組: 2026 World Baseball Classic Pool C (real)
b.group(23, 25, '2026 年 3 月舉行的第六屆世界棒球經典賽（WBC）共 20 隊參賽，分成 4 組、每組 5 隊進行單循環（同組每兩隊比賽一場），'
        '各組前 2 名晉級八強，之後進行單淘汰賽（八強賽、四強賽、冠軍賽，沒有季軍戰）。\n'
        '在東京巨蛋進行的 C 組由日本、韓國、澳洲、中華、捷克組成：日本 4 戰全勝；韓國、澳洲、中華都是 2 勝 2 敗，必須比序決定誰拿到第 2 名。'
        '大會規則：同勝敗的球隊，只計算它們「彼此之間」的比賽，比較「失分 ÷ 防守出局數」，比值越小排名越前（若仍相同，再比較自責分，本題不需用到）。三隊彼此的比賽結果如下：\n'
        '| 日期 | 對戰 | 比分 | 該場各隊的防守出局數 |\n'
        '| 3 月 5 日 | 中華 vs 澳洲 | 中華 0：3 澳洲 | 中華 24、澳洲 27 |\n'
        '| 3 月 8 日 | 中華 vs 韓國 | 中華 5：4 韓國（延長 10 局） | 中華 30、韓國 30 |\n'
        '| 3 月 9 日 | 韓國 vs 澳洲 | 韓國 7：2 澳洲 | 韓國 27、澳洲 27 |\n'
        '（某隊的「失分」是對手在該場得到的分數。）')

# 23  # L3
games = 4 * (5 * 4 // 2) + 4 + 2 + 1
b.item('依上述賽制，整屆比賽（含分組賽與淘汰賽）共有幾場？',
       f'{games} 場', ['48 場', '55 場', '87 場'],
       '【解析】每組 5 隊單循環：5×4÷2＝10 場，4 組共 40 場。淘汰賽：八強賽 4 場、四強賽 2 場、冠軍賽 1 場，共 7 場（8 隊淘汰到剩冠軍要淘汰 7 隊）。全部 40＋7＝47 場。'
       '({d0}) 是多算了季軍戰，但題目說沒有季軍戰；({d1}) 是把八強賽算成 8 場（8 隊兩兩一場只有 4 場）；({d2}) 是把每組算成 5×4＝20 場，每場被兩隊各算了一次。',
       check=(games == 47, [games == 48, games == 40 + 8 + 4 + 2 + 1, games == 80 + 7]))

# allowed runs and defensive outs among the tied teams
G = [('中華', 0, '澳洲', 3, 24, 27), ('中華', 5, '韓國', 4, 30, 30), ('韓國', 7, '澳洲', 2, 27, 27)]


def rates(games_):
    ra, outs = {}, {}
    for t1, r1, t2, r2, o1, o2 in games_:
        ra[t1] = ra.get(t1, 0) + r2
        ra[t2] = ra.get(t2, 0) + r1
        outs[t1] = outs.get(t1, 0) + o1
        outs[t2] = outs.get(t2, 0) + o2
    return {k: F(ra[k], outs[k]) for k in ra}


R = rates(G)
assert R == {'韓國': F(7, 57), '澳洲': F(7, 54), '中華': F(7, 54)}
s_true = R['韓國'] < R['澳洲'] == R['中華']
s_strict = R['韓國'] < R['澳洲'] < R['中華']
s_all_equal = R['韓國'] == R['澳洲'] == R['中華']
s_kor_tpe = R['韓國'] == R['中華'] < R['澳洲']
R_misread = dict(R, 中華=F(3 + 5, 54))            # 中華 counting its own 5 runs as runs allowed
assert R_misread['韓國'] < R_misread['澳洲'] < R_misread['中華']
# 24  # L4
b.item('依上表計算三隊的「失分 ÷ 防守出局數」，下列敘述何者正確？',
       '韓國的比值最小，澳洲與中華的比值相同', ['韓國的比值最小，澳洲次之，中華最大', '三隊的比值都相同', '韓國與中華的比值相同，都比澳洲小'],
       '【解析】韓國：失分 5（對中華）＋2（對澳洲）＝7，出局數 30＋27＝57，比值 7/57；澳洲：失分 0＋7＝7，出局數 27＋27＝54，比值 7/54；'
       '中華：失分 3＋4＝7，出局數 24＋30＝54，比值 7/54。三隊失分都是 7，韓國防守出局數最多，比值最小，排第 2 晉級八強；澳洲與中華同為 7/54（之後再以自責分比序）。'
       '({d0}) 是把中華對韓國那場自己的得分 5 誤當成失分（3＋5＝8，比值 8/54）；'
       '({d1}) 是只比失分（都是 7 分），忽略出局數；({d2}) 是沒看表中的出局數，以為打 9 局就是 27 個出局數，把中華算成 27＋30＝57（中華對澳洲那場只防守 24 個出局數，因為主隊澳洲領先，9 局下半不用打）。',
       check=(s_true, [s_strict, s_all_equal, s_kor_tpe]))

# 25  # L5
need = None
for k in range(3, 30):                      # 韓國 k : 2 澳洲, both sides 27 outs
    Rk = rates([G[0], G[1], ('韓國', k, '澳洲', 2, 27, 27)])
    if Rk['韓國'] < Rk['澳洲'] and Rk['韓國'] < Rk['中華']:
        need = k
        break
b.item('回到 3 月 9 日韓國與澳洲比賽開打之前（前兩場結果如上表）。假設這場打滿 9 局、雙方的防守出局數都是 27，且澳洲得 2 分。'
       '韓國至少要得幾分，才能依此規則確定排在澳洲與中華的前面？',
       f'{need} 分', ['3 分', '6 分', '8 分'],
       '【解析】設韓國得 k 分（k ≥ 3 才會贏球，三隊才會同為 2 勝 2 敗）。韓國比值＝(5＋2)/(30＋27)＝7/57；中華比值＝7/54，不受這場影響；'
       '澳洲比值＝(0＋k)/(27＋27)＝k/54。韓國要比澳洲小：7/57＜k/54，k＞54×7/57≈6.63，所以 k 至少 7（7/57 也小於中華的 7/54）。'
       '實際比賽韓國正好以 7：2 獲勝而晉級。'
       '({d0}) 是以為只要贏球就好，但 3：2 時澳洲比值 3/54 比韓國小；({d1}) 是把 6.63 四捨五入成 6 以下，k＝6 時澳洲 6/54≈0.111 仍比韓國 7/57≈0.123 小；'
       '({d2}) 8 分當然也可以，但不是「至少」。',
       check=(need == 7, [need == 3, need == 6, need == 8]))

b.write()
