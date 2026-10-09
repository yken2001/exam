"""AI-4 數學（會考水準）: build src/data/ai/ai4_math.json and its figures.

A mock paper pitched like a real recent 會考 math paper (mean level ≈ 2.5):
25 multiple-choice items, 2 題組, short computations mixed with graph,
table and rule-reading items. Every answer is computed here with exact
arithmetic (fractions.Fraction or integers) and passed through
check=(ok, [bad...]); the builder places the options, writes the letters into
the explanation and appends 「故選」. Each item is tagged with its design level
(# L1 .. # L4, see SPEC_AI2_AI3.md).

  PYTHONIOENCODING=utf-8 python tools/ai_sets/ai4_math.py
"""
import math
import os
import sys
from fractions import Fraction as F
from itertools import product

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Polygon

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SetBuilder, spread_target  # noqa: E402

plt.rcParams['font.family'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False

TOPICS = [
    '數與式：整數四則、根式、科學記號、因式分解、乘法公式、最大公因數與最小公倍數',
    '方程式：二元一次聯立、一元二次方程式、不等式（團體票方案）',
    '函數：一次函數圖形平移、二次函數圖形性質',
    '數列：等差數列（紀錄進程）、等比數列',
    '幾何：正多邊形內角、相似形比例尺、外心、平行四邊形與角平分線、切線與圓內接四邊形、平行線截比與面積、角柱表面積',
    '統計與機率：中位數、平均數、成長率、取球機率',
    '時事：航海家 1 號預計 2026 年 11 月中旬左右（EarthSky 推算為 11/18）成為第一個距地球 1 光日（約 259 億公里）的人造物體: https://earthsky.org/space/voyager-1-1-light-day-from-earth-november-17-18-2026/',
    '時事：淡江大橋 2026/5/12 通車，主橋長 920 m、主跨 450 m、橋塔高約 211 m，世界最長單塔不對稱斜張橋: https://zh.wikipedia.org/wiki/淡江大橋 ；通車日: https://www.twreporter.org/a/photo-danjiang-bridge-opening',
    '時事：杜普蘭蒂斯（Mondo Duplantis）撐竿跳世界紀錄進程，6.17 m（2020/2/8）到 6.31 m（2026/3/12 烏普薩拉，第 15 次），之前紀錄為 Lavillenie 6.16 m（2014）: https://en.wikipedia.org/wiki/Men%27s_pole_vault_world_record_progression',
    '時事：同上，第 15 次世界紀錄 6.31 m 報導: https://www.philstar.com/sports/2026/03/13/2514027/duplantis-clears-631m-set-15th-pole-vault-world-record',
    '時事：2025 年中職上半季 180 場、場均 9,373 人；各隊主場場均：中信兄弟 12,415、味全龍 10,168、富邦悍將 10,288（2024 年 7,307）、統一獅 7,793、樂天桃猿 8,317、台鋼雄鷹 7,255（中央社）: https://www.cna.com.tw/news/aspt/202507045002.aspx',
]

b = SetBuilder('ai4_math', '數學', year=904, set_name='AI-4', title='AI-4 數學模擬卷（會考水準）',
               note='由 AI 依會考數學科選擇題型編寫（非會考真題），難度定位「會考水準」：題數、題型與難度分布比照近年會考，'
                    '有基本計算，也有圖形判讀、規則閱讀與兩到三步的幾何推理，並以 2025–2026 年真實時事（航海家 1 號、淡江大橋、撐竿跳世界紀錄、中職觀眾人數）為素材。'
                    '每題答案均由程式以精確分數計算驗證（tools/ai_sets/ai4_math.py），附圖依題目數據繪製。',
               target=spread_target(25, 4, 904), difficulty='會考水準', topics=TOPICS)


def fs(x):
    """exact number as text: 7, −3, 15/8"""
    x = F(x)
    s = '−' if x < 0 else ''
    x = abs(x)
    return f'{s}{x.numerator}' if x.denominator == 1 else f'{s}{x.numerator}/{x.denominator}'


def blank(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def pmul(p, q):
    """polynomials as coefficient lists, constant term first"""
    r = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, c in enumerate(q):
            r[i + j] += a * c
    return r


def padd(p, q, s=1):
    n = max(len(p), len(q))
    p, q = p + [0] * (n - len(p)), q + [0] * (n - len(q))
    return [a + s * c for a, c in zip(p, q)]


def area(*P):
    s = 0
    for (x1, y1), (x2, y2) in zip(P, P[1:] + P[:1]):
        s += x1 * y2 - x2 * y1
    return abs(F(s)) / 2


def angle_deg(V, P, Q):
    a = (P[0] - V[0], P[1] - V[1])
    c = (Q[0] - V[0], Q[1] - V[1])
    cosv = (a[0] * c[0] + a[1] * c[1]) / (math.hypot(*a) * math.hypot(*c))
    return math.degrees(math.acos(max(-1.0, min(1.0, cosv))))


# ====================================================================== items

# 1  # L1
v1 = F(-3) ** 2 - F(4 * -2, -8)
m_sign = F(-3) ** 2 + F(4 * -2, -8)            # −(−8)÷(−8) 的正負號弄錯
m_order = (F(-3) ** 2 - 4 * 2) / -8            # 先減再除：(9 − 8)÷(−8)
m_sq = -9 - F(4 * -2, -8)                      # (−3)² 算成 −9
b.item('計算 (−3)² − 4 × (−2) ÷ (−8) 之值為何？', fs(v1), [fs(m_sign), fs(m_order), fs(m_sq)],
       '【解析】先算乘方與乘除，再算加減：(−3)²＝9，4 × (−2) ÷ (−8)＝(−8) ÷ (−8)＝1，所以原式＝9 − 1＝8。'
       '({d0}) 是把 (−8) ÷ (−8) 的結果算成 −1（負負得正弄錯）；({d1}) 是先算 9 − 4×2 再除以 −8，違反「先乘除後加減」；({d2}) 是把 (−3)² 誤算成 −9。',
       check=(v1 == 8, [m_sign == v1, m_order == v1, m_sq == v1]))

# 2  # L1
sols2 = [(x, y) for x in range(-20, 21) for y in range(-20, 21) if x + 3 * y == 7 and 2 * x - y == -7]
x2, y2 = sols2[0]
b.item('解二元一次聯立方程式 { x＋3y＝7，2x − y＝−7 }，得 x 值為何？', fs(x2), [fs(-x2), fs(y2), fs(-y2)],
       '【解析】由第二式得 y＝2x＋7，代入第一式：x＋3(2x＋7)＝7，7x＋21＝7，x＝−2，再代回得 y＝3。'
       '({d0}) 是移項時正負號弄錯；({d1}) 是 y 的值，題目問的是 x；({d2}) 是 y 的值又把正負號弄錯。',
       check=(len(sols2) == 1 and x2 == -2, [-x2 == x2, y2 == x2, -y2 == x2]))

# 3  # L2
# (√50 − √8)×√2 : √50 = 5√2, √8 = 2√2 -> 3√2 × √2 = 6 ; represent a√b as (a, b)
# compare squares: (a√b)² = a²·b, so distinct options have distinct squares
sq3 = ((5 - 2) ** 2 * 2) * 2                    # ((5√2 − 2√2)·√2)² = (3√2)²·2 = 36
sq_wrong = [2 * 2 * 21, 3 * 3 * 2, 6 * 6 * 2]   # 2√21 (√42·√2 = √84), 3√2, 6√2
assert 50 - 8 == 42 and 42 * 2 == 84 == 4 * 21
b.item('計算 (√50 − √8) × √2 的結果為何？', '6', ['2√21', '3√2', '6√2'],
       '【解析】√50＝5√2，√8＝2√2，所以 √50 − √8＝3√2，再乘以 √2：3√2 × √2＝3 × 2＝6。'
       '({d0}) 是誤以為 √50 − √8＝√42，再乘 √2 得 √84＝2√21（根號不能這樣相減）；({d1}) 是只算到 √50 − √8＝3√2，忘了乘以 √2；({d2}) 是把 √2 × √2 算成 2√2。',
       check=(sq3 == 6 * 6, [w == sq3 for w in sq_wrong]))


# 4  # L2  (current events: Voyager 1)
def sci(x):
    """exact a × 10ⁿ text (1 ≤ a < 10, a written exactly)"""
    x = F(x)
    n = 0
    while x >= 10:
        x /= 10
        n += 1
    while x < 1:
        x *= 10
        n -= 1
    sup = str(n).translate(str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹'))
    a = f'{float(x):g}'
    return f'{a} × 10{sup}'


c_kms = 3 * 10 ** 5
day = 24 * 60 * 60
lday = c_kms * day
b.item('美國 NASA 於 1977 年發射的太空探測器「航海家 1 號」持續飛離太陽系，預計在 2026 年 11 月中旬左右，'
       '成為史上第一個與地球距離達到「1 光日」的人造物體。1 光日是指光在 1 天之內行進的距離。'
       '若光速以每秒 3 × 10⁵ 公里計算，1 光日約為多少公里？',
       sci(lday), [sci(lday // 10), sci(c_kms * 24 * 60), sci(c_kms * 3600)],
       '【解析】1 天＝24 × 60 × 60＝86400 秒＝8.64 × 10⁴ 秒，1 光日＝3 × 10⁵ × 8.64 × 10⁴＝25.92 × 10⁹＝2.592 × 10¹⁰ 公里'
       '（NASA 公布的數字約 259 億公里，兩者相符）。'
       '({d0}) 是把 25.92 × 10⁹ 化成科學記號時，次方弄錯少了 1（係數變小，次方應該變大）；({d1}) 是只換算到「分鐘」（3 × 10⁵ × 24 × 60），但光速是每「秒」；({d2}) 是只乘了 1 小時的 3600 秒，那是 1 光時。',
       check=(lday == 25920000000 and sci(lday) == '2.592 × 10¹⁰',
              [lday // 10 == lday, c_kms * 24 * 60 == lday, c_kms * 3600 == lday]))

# 5  # L2
target5 = [-15, -1, 6]                          # 6x² − x − 15
pairs5 = [(a, c) for a in range(-20, 21) for c in range(-20, 21) if pmul([a, 2], [c, 3]) == target5]
a5, c5 = pairs5[0]
b.item('若多項式 6x² − x − 15 可因式分解成 (2x＋a)(3x＋b)，其中 a、b 為整數，則 a＋b 之值為何？',
       fs(a5 + c5), [fs(-(a5 + c5)), fs(a5 - c5), fs(c5 - a5)],
       '【解析】(2x＋a)(3x＋b)＝6x²＋(2b＋3a)x＋ab。要 ab＝−15 且 2b＋3a＝−1，試得 a＝3、b＝−5：2×(−5)＋3×3＝−1。'
       '所以 6x² − x − 15＝(2x＋3)(3x − 5)，a＋b＝3＋(−5)＝−2。'
       '({d0}) 來自 (2x − 3)(3x＋5)，展開一次項是＋x，正負號相反；({d1}) 是 a − b 的值；({d2}) 是 b − a 的值，題目問的是兩數的和。',
       check=(pairs5 == [(3, -5)], [-(a5 + c5) == a5 + c5, a5 - c5 == a5 + c5, c5 - a5 == a5 + c5]))
assert pmul([-5, 2], [3, 3]) == [-15, -9, 6]

# 6  # L2
p6 = padd(pmul([-3, 2], [-3, 2]), pmul([1, 1], [-1, 1]), -1)        # (2x−3)² − (x+1)(x−1)


def ptext(p):
    c, bx, a = (p + [0, 0, 0])[:3]
    s = f'{a}x²' if a != 1 else 'x²'
    if bx:
        s += f' − {-bx}x' if bx < 0 else f'＋{bx}x'
    if c:
        s += f' − {-c}' if c < 0 else f'＋{c}'
    return s


w6a = padd(pmul([-3, 2], [-3, 2]), [1, 0, 1], -1)                   # −(x²−1) 寫成 −x² − 1
w6b = padd([9, -6, 4], [-1, 0, 1], -1)                              # 中間項只算 −6x
w6c = padd([-9, 0, 4], [-1, 0, 1], -1)                              # (2x−3)² 誤為 4x² − 9
b.item('化簡 (2x − 3)² − (x＋1)(x − 1) 的結果為何？', ptext(p6), [ptext(w6a), ptext(w6b), ptext(w6c)],
       '【解析】(2x − 3)²＝4x² − 12x＋9，(x＋1)(x − 1)＝x² − 1，相減時括號前是負號，每一項都要變號：'
       '4x² − 12x＋9 − x²＋1＝3x² − 12x＋10。'
       '({d0}) 是去括號時 −(x² − 1) 只變了第一項的號，寫成 −x² − 1；({d1}) 是 (2x − 3)² 的中間項漏乘 2，算成 −6x；({d2}) 是誤以為 (2x − 3)²＝4x² − 9。',
       check=(p6 == [10, -12, 3], [w6a == p6, w6b == p6, w6c == p6]))
assert ptext(p6) == '3x² − 12x＋10' and ptext(w6c) == '3x² − 8'

# 7  # L3
pairs7 = [(a, c) for a in range(1, 200) for c in range(a, 200) if math.gcd(a, c) == 6 and a * c // math.gcd(a, c) == 72]
jia7 = any(a + c == 42 for a, c in pairs7)            # 甲：a＋b 可能是 42
yi7 = all(72 in (a, c) for a, c in pairs7)            # 乙：一定有一數是 72
key7 = {(True, True): '甲、乙皆正確', (False, False): '甲、乙皆錯誤', (True, False): '甲正確，乙錯誤', (False, True): '甲錯誤，乙正確'}
ans7 = key7[(jia7, yi7)]
b.item('已知 a、b 皆為正整數，且 a、b 兩數的最大公因數為 6、最小公倍數為 72。關於 a、b 兩數，甲、乙兩人提出看法如下：\n'
       '甲：a＋b 可能是 42\n乙：a、b 兩數中一定有一個數是 72\n對於甲、乙兩人的看法，下列判斷何者正確？',
       ans7, [v for v in key7.values() if v != ans7],
       '【解析】設 a＝6m、b＝6n，m、n 互質，最小公倍數 6mn＝72，得 mn＝12。m、n 互質的組合只有 1 與 12、3 與 4，'
       '所以 a、b 是 6 與 72，或 18 與 24。18＋24＝42，甲正確；18 與 24 都不是 72，乙錯誤。'
       '誤以為「最小公倍數一定是其中一數」或漏掉 3 與 4 這組的人，會判斷乙正確。({d0})、({d1})、({d2}) 都與上面的判斷不符。',
       check=(ans7 == '甲正確，乙錯誤' and sorted(pairs7) == [(6, 72), (18, 24)], [False, False, False]))

# 8  # L2
a8 = [a for a in range(-20, 21) if 2 * 2 + a * 2 - 10 == 0][0]
roots8 = [x for x in range(-50, 51) if x * x + a8 * x - 10 == 0]
other8 = [r for r in roots8 if r != 2][0]
b.item('已知 x＝2 是一元二次方程式 x²＋ax − 10＝0 的一個解，則此方程式的另一個解為何？',
       fs(other8), [fs(-other8), fs(a8), fs(-a8)],
       '【解析】把 x＝2 代入：4＋2a − 10＝0，a＝3。方程式為 x²＋3x − 10＝0，(x＋5)(x − 2)＝0，所以另一個解是 x＝−5。'
       '({d0}) 是因式分解成 (x − 5)(x＋2)，正負號放反了（代入 x＝2 檢查就會發現不合）；({d1}) 是 a 的值，不是方程式的解；({d2}) 是把 −a 誤當成另一個解。',
       check=(a8 == 3 and roots8 == [-5, 2], [-other8 == other8, a8 == other8, -a8 == other8]))

# 9  # L3
full9, group9 = 250, 250 * F(8, 10)
cost_group = 30 * group9
n9 = next(n for n in range(1, 31) if full9 * n > cost_group)
n9_wrong = next(n for n in range(1, 31) if full9 * n > 30 * (250 - 80))
b.item('某遊樂園（虛構情境）的門票規定如下：\n| 票種 | 價格 |\n| 全票 | 每張 250 元 |\n| 團體票 | 一次購買 30 張以上（含 30 張），每張打八折 |\n'
       '一支 n 人的隊伍（n＜30）可以每人各買一張全票，也可以直接買 30 張團體票（多出來的票不使用）。'
       '這支隊伍至少要有幾人，直接買 30 張團體票的總價才會比每人各買一張全票便宜？',
       f'{n9} 人', [f'{n9 - 1} 人', f'{n9_wrong} 人', '30 人'],
       '【解析】團體票每張 250 × 0.8＝200 元，30 張共 6000 元。n 人各買全票要 250n 元，要比較便宜須 250n＞6000，n＞24，所以至少 25 人。'
       '({d0}) 24 人時兩種買法都是 6000 元，一樣貴，並不是「比較便宜」；({d1}) 是把「打八折」誤當成每張少 80 元（170 × 30＝5100，n＞20.4）；'
       '({d2}) 是以為人數要滿 30 人才能用團體票，忽略了可以多買幾張。',
       check=(n9 == 25, [n9 - 1 == n9, n9_wrong == n9, 30 == n9]))
assert n9_wrong == 21 and full9 * 24 == cost_group


# 10  # L3
def fig_line():
    fig, ax = plt.subplots(figsize=(3.8, 3.2))
    xs = [-1, 5.2]
    ax.plot(xs, [3 - 0.75 * x for x in xs], color='black', linewidth=1.6)
    ax.axhline(0, color='black', linewidth=0.9)
    ax.axvline(0, color='black', linewidth=0.9)
    for p, s, dx, dy in (((0, 3), '(0, 3)', 0.2, 0.15), ((4, 0), '(4, 0)', 0.05, 0.3)):
        ax.plot(*p, 'o', color='black', markersize=4)
        ax.text(p[0] + dx, p[1] + dy, s, fontsize=10)
    ax.text(4.6, -1.15, 'L', fontsize=12, style='italic')
    ax.text(5.6, -0.45, 'x', fontsize=11, style='italic')
    ax.text(-0.45, 4.6, 'y', fontsize=11, style='italic')
    ax.text(-0.45, -0.45, 'O', fontsize=10)
    ax.set_xlim(-1.2, 6)
    ax.set_ylim(-1.5, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    return b.save_fig(fig, 'q10_line.png')


m10, k10 = F(-3, 4), F(3)
k10b = k10 + 3                                     # 向上平移 3
xint = -k10b / m10
area10 = xint * k10b / 2
w10a = (4 + 3) * k10b / 2                          # 以為 x 截距也加 3
w10b = 4 * k10b / 2                                # 只改了 y 截距
w10c = xint * k10b                                 # 忘了除以 2
b.item('如附圖，坐標平面上的直線 L 通過 (0, 3) 與 (4, 0) 兩點。將直線 L 向上平移 3 個單位後得到直線 M，'
       '則直線 M 與 x 軸、y 軸所圍成的三角形面積為何？',
       fs(area10), [fs(w10a), fs(w10b), fs(w10c)],
       '【解析】L 的斜率＝(0 − 3) ÷ (4 − 0)＝−3/4，L：y＝−(3/4)x＋3。向上平移 3 個單位，斜率不變、y 截距加 3，M：y＝−(3/4)x＋6。'
       '令 y＝0 得 x＝8，所以 M 與兩軸交於 (8, 0)、(0, 6)，面積＝8 × 6 ÷ 2＝24。'
       '({d0}) 是以為 x 截距也跟著加 3 變成 7，但向上平移時 x 截距會依斜率改變；({d1}) 是只改了 y 截距、x 截距仍用 4；({d2}) 是三角形面積忘了除以 2。',
       figure=fig_line(),
       check=(area10 == 24 and xint == 8, [w10a == area10, w10b == area10, w10c == area10]))

# 11  # L3
f11 = lambda x: -2 * (x - 3) ** 2 + 8
ymax11 = 8                                          # vertex (3, 8), opens downward
jia11 = ymax11 >= 9                                 # 甲：圖形上有一點的 y 坐標為 9
roots11 = [x for x in range(-20, 21) if f11(x) == 0]
yi11 = len(roots11) == 2 and roots11[1] - roots11[0] == 4   # 乙：與 x 軸兩交點距離為 4
key11 = {(True, True): '甲、乙皆正確', (False, False): '甲、乙皆錯誤', (True, False): '甲正確，乙錯誤', (False, True): '甲錯誤，乙正確'}
ans11 = key11[(jia11, yi11)]
b.item('已知坐標平面上有二次函數 y＝−2(x − 3)²＋8 的圖形，甲、乙兩人提出以下看法：\n'
       '【甲】此函數圖形上某個點的 y 坐標為 9\n【乙】此函數圖形與 x 軸的兩個交點，彼此的距離為 4\n對於甲、乙兩人的看法，下列判斷何者正確？',
       ans11, [v for v in key11.values() if v != ans11],
       '【解析】y＝−2(x − 3)²＋8 的圖形開口向下，頂點 (3, 8) 是最高點，所以 y 坐標最大是 8，不可能是 9，甲錯誤。'
       '令 y＝0：(x − 3)²＝4，x − 3＝±2，x＝1 或 5，兩交點 (1, 0)、(5, 0) 的距離是 4，乙正確。'
       '若把頂點看成最低點（忽略 x² 前的負號），會誤判甲正確；若把 (x − 3)²＝4 解成 x − 3＝4、只得到一個交點，會誤判乙錯誤。({d0})、({d1})、({d2}) 都與上面的判斷不符。',
       check=(ans11 == '甲錯誤，乙正確' and roots11 == [1, 5] and max(f11(F(x, 10)) for x in range(-100, 101)) == 8,
              [False, False, False]))

# 12-13  題組: Duplantis pole vault world records (real)
recs = [('2020/2/8', 617), ('2020/2/15', 618), ('2022/3/7', 619), ('2022/3/20', 620), ('2022/7/24', 621),
        ('2023/2/25', 622), ('2023/9/17', 623), ('2024/4/20', 624), ('2024/8/5', 625), ('2024/8/25', 626),
        ('2025/2/28', 627), ('2025/6/15', 628), ('2025/8/12', 629), ('2025/9/15', 630), ('2026/3/12', 631)]
assert all(h == 616 + n for n, (_, h) in enumerate(recs, 1))
rows = '\n'.join(f'| {n} | {d} | {h / 100:.2f} |' for n, (d, h) in enumerate(recs, 1))
b.group(12, 13, '瑞典撐竿跳選手杜普蘭蒂斯（Mondo Duplantis）在 2020 年 2 月第一次打破男子撐竿跳世界紀錄，在他之前的世界紀錄是 2014 年創下的 6.16 公尺。'
        '此後他一再刷新自己的紀錄，2025 年 9 月在東京世界田徑錦標賽跳過 6.30 公尺，2026 年 3 月 12 日又在瑞典跳過 6.31 公尺，創下他個人第 15 次世界紀錄。'
        '下表是他歷次創下的世界紀錄：\n| 第幾次 | 日期 | 高度（公尺） |\n' + rows)

# 12  # L2
b.item('若以 n 表示「第 n 次」、h 表示該次世界紀錄的高度（公尺），則表中每一筆資料的 n 與 h 都符合下列哪一個關係式？',
       'h＝0.01n＋6.16', ['h＝0.01n＋6.17', 'h＝0.01n＋6.15', 'h＝0.1n＋6.16'],
       '【解析】每次紀錄都比前一次高 1 公分＝0.01 公尺，第 1 次是 6.17，所以 h＝6.17＋0.01(n − 1)＝0.01n＋6.16（n＝0 時正好是之前的紀錄 6.16 公尺）。'
       '代入檢查：n＝15 時 h＝0.15＋6.16＝6.31，正確。'
       '({d0}) 是把首項 6.17 直接當常數項，n＝1 時會得到 6.18；({d1}) n＝1 時得 6.16，少了 1 公分；({d2}) 是把 1 公分誤換算成 0.1 公尺。',
       check=(all(F(h, 100) == F(1, 100) * n + F(616, 100) for n, (_, h) in enumerate(recs, 1)),
              [all(F(h, 100) == F(1, 100) * n + F(617, 100) for n, (_, h) in enumerate(recs, 1)),
               all(F(h, 100) == F(1, 100) * n + F(615, 100) for n, (_, h) in enumerate(recs, 1)),
               all(F(h, 100) == F(1, 10) * n + F(616, 100) for n, (_, h) in enumerate(recs, 1))]))

# 13  # L3
by_year = {}
for d, h in recs:
    by_year.setdefault(int(d[:4]), []).append(h)
best_year = max(by_year, key=lambda y: len(by_year[y]))
assert [y for y in by_year if len(by_year[y]) == len(by_year[best_year])] == [best_year]
prev_end = max(h for d, h in recs if int(d[:4]) < best_year)
gain = max(by_year[best_year]) - prev_end
gain_wrong = max(by_year[best_year]) - min(by_year[best_year])
g2024 = max(by_year[2024]) - max(by_year[2023])
g2022 = max(by_year[2022]) - max(by_year[2020])
b.item('哪一個年度他創下世界紀錄的次數最多？那一年他總共把世界紀錄提高了幾公分？',
       f'{best_year} 年，{gain} 公分', [f'{best_year} 年，{gain_wrong} 公分', f'2024 年，{g2024} 公分', f'2022 年，{g2022} 公分'],
       '【解析】依年度數次數：2020 年 2 次、2022 年 3 次、2023 年 2 次、2024 年 3 次、2025 年 4 次、2026 年（到 3 月）1 次，2025 年最多。'
       '2025 年開始時的世界紀錄是 2024 年底的 6.26 公尺，2025 年底是 6.30 公尺，所以那一年提高了 4 公分。'
       '({d0}) 是用該年第一筆 6.27 去減，但 6.27 本身已經比原紀錄高了 1 公分；({d1}) 與 ({d2}) 的 2024 年、2022 年各只有 3 次，不是最多。',
       check=((best_year, gain) == (2025, 4), [gain_wrong == gain, (2024, g2024) == (best_year, gain), (2022, g2022) == (best_year, gain)]))
assert gain_wrong == 3 and g2024 == 3 and g2022 == 3

# 14  # L2
r3 = F(-48, 6)
r14 = [r for r in range(-10, 11) if r ** 3 == r3][0]
a1 = F(6, r14)
seq14 = [a1 * r14 ** k for k in range(6)]
b.item('一個等比數列的第 2 項是 6，第 5 項是 −48，則此數列的第 4 項為何？',
       fs(seq14[3]), [fs(-seq14[3]), fs(seq14[2]), fs(seq14[5])],
       '【解析】第 5 項 ÷ 第 2 項＝r³＝−48 ÷ 6＝−8，所以公比 r＝−2。第 3 項＝6 × (−2)＝−12，第 4 項＝(−12) × (−2)＝24（也可用第 5 項 ÷ r＝−48 ÷ (−2)＝24）。'
       '({d0}) 是把公比誤算成 2（忽略 −8 的負號），再由第 5 項 −48 ÷ 2 得 −24；({d1}) 是第 3 項；({d2}) 是第 6 項。',
       check=(r14 == -2 and seq14[1] == 6 and seq14[4] == -48 and seq14[3] == 24,
              [-seq14[3] == seq14[3], seq14[2] == seq14[3], seq14[5] == seq14[3]]))

# 15  # L1
n15 = 12
int15 = F(180 * (n15 - 2), n15)
b.item('一個正十二邊形的每一個內角是多少度？',
       f'{fs(int15)}°', [f'{fs(F(360, n15))}°', '165°', f'{fs(F(180 * 8, 10))}°'],
       '【解析】正 n 邊形的內角和是 180°×(n − 2)，正十二邊形的內角和＝180°×10＝1800°，每個內角＝1800° ÷ 12＝150°（或用外角：360° ÷ 12＝30°，內角＝180° − 30°＝150°）。'
       '({d0}) 是每一個外角的度數；({d1}) 是把內角和誤算成 180°×11＝1980°（多算了一個三角形）；({d2}) 是正十邊形的內角。',
       check=(int15 == 150, [F(360, n15) == int15, F(180 * 11, 12) == int15, F(180 * 8, 10) == int15]))

# 16  # L2  (current events: Danjiang Bridge)
span_m, tower_m, main_m, model_cm = 450, 211, 920, 90
scale16 = F(model_cm, span_m * 100)
tower_model = tower_m * 100 * scale16
w16a = tower_m * F(model_cm, span_m * 1000) * 100     # 1 公尺誤換成 1000 公分
w16b = tower_m * scale16 * 1000                       # 換算時多乘 10
w16c = tower_m * 100 * F(model_cm, main_m * 100)      # 誤用主橋長 920 公尺
b.item('2026 年 5 月 12 日通車的淡江大橋，是全世界主跨最長的「單塔不對稱斜張橋」。它的主橋長 920 公尺，其中主跨長 450 公尺，主橋塔高約 211 公尺。'
       '某校美術社（虛構情境）依實物等比例縮小製作模型，模型中主跨的長度為 90 公分。依此比例，模型中的主橋塔應高多少公分？',
       f'{float(tower_model):g} 公分', [f'{float(w16a):g} 公分', f'{float(w16b):g} 公分', f'約 {float(w16c):.1f} 公分'],
       '【解析】450 公尺＝45000 公分，模型與實物的比例＝90：45000＝1：500。主橋塔 211 公尺＝21100 公分，模型高＝21100 ÷ 500＝42.2 公分。'
       '({d0}) 是把主跨 450 公尺誤換算成 450000 公分（多乘了 10），比例尺變成 1：5000，21100 ÷ 5000＝4.22；({d1}) 是把橋塔高 211 公尺誤換算成 211000 公分（多乘了 10），211000 ÷ 500＝422；'
       '({d2}) 是誤把模型的 90 公分對應到「主橋長 920 公尺」，但題目說 90 公分是主跨的長度，主跨是 450 公尺。',
       check=(tower_model == F(422, 10) and scale16 == F(1, 500),
              [w16a == tower_model, w16b == tower_model, w16c == tower_model]))
assert float(w16a) == 4.22 and float(w16b) == 422


# 17  # L3
def fig_circum():
    fig, ax = blank(3.6, 3.6)
    th = lambda d: (math.cos(math.radians(d)), math.sin(math.radians(d)))
    B, C, A = th(200), th(340), th(245)
    O = (0.0, 0.0)
    ax.add_patch(Circle(O, 1, fill=False, linewidth=1.0, linestyle='--', edgecolor='#666666'))
    ax.add_patch(Polygon([A, B, C], fill=False, linewidth=1.6))
    ax.plot([B[0], O[0], C[0]], [B[1], O[1], C[1]], color='black', linewidth=1.0)
    ax.plot(0, 0, 'o', color='black', markersize=3)
    for p, s, dx, dy in ((A, 'A', -0.05, -0.17), (B, 'B', -0.17, -0.03), (C, 'C', 0.05, -0.03), (O, 'O', -0.04, 0.07)):
        ax.text(p[0] + dx, p[1] + dy, s, fontsize=12)
    assert abs(angle_deg(A, B, C) - 110) < 1e-6 and abs(angle_deg(O, B, C) - 140) < 1e-6
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    return b.save_fig(fig, 'q17_circumcenter.png')


A17 = 110
BOC17 = 2 * (180 - A17)            # A obtuse: A on the minor arc BC, the major arc BC is 2·∠A
b.item('如附圖，△ABC 中，∠A＝110°，O 點為△ABC 的外心（虛線為△ABC 的外接圓）。∠BOC 的度數為何？',
       f'{BOC17}°', ['145°', f'{180 - A17}°', f'{A17}°'],
       '【解析】外心是外接圓的圓心。∠A＝110° 是鈍角，A 在劣弧 BC 上，∠A 所對的是優弧 BC，所以優弧 BC＝2 × 110°＝220°，'
       '劣弧 BC＝360° − 220°＝140°，∠BOC 是劣弧 BC 所對的圓心角，等於 140°（外心 O 在三角形外部）。'
       '({d0}) 是把外心當成內心，用 90°＋110°÷2＝145° 計算；({d1}) 是 180° − 110°，那是優弧上一點所對的圓周角；({d2}) 是誤以為圓心角等於 ∠A。',
       figure=fig_circum(),
       check=(BOC17 == 140, [145 == BOC17, 180 - A17 == BOC17, A17 == BOC17]))


# 18  # L3
def fig_para():
    fig, ax = blank(4.2, 2.4)
    s3 = math.sqrt(3)
    B, C = (0, 0), (10, 0)
    A = (3.5, 3.5 * s3)
    D = (A[0] + 10, A[1])
    E = (7, 0)
    ax.add_patch(Polygon([A, B, C, D], fill=False, linewidth=1.6))
    ax.plot([A[0], E[0]], [A[1], E[1]], color='black', linewidth=1.3)
    for p, s, dx, dy in ((A, 'A', -0.5, 0.15), (B, 'B', -0.6, -0.4), (C, 'C', 0.15, -0.4), (D, 'D', 0.15, 0.1), (E, 'E', -0.15, -0.75)):
        ax.text(p[0] + dx, p[1] + dy, s, fontsize=12)
    assert abs(angle_deg(A, B, E) - angle_deg(A, E, D)) < 1e-9
    ax.set_xlim(-1, 14.5)
    ax.set_ylim(-1, 7)
    return b.save_fig(fig, 'q18_parallelogram.png')


BE18, EC18 = 7, 3
AB18 = BE18                       # ∠BAE = ∠EAD = ∠AEB  ->  AB = BE
BC18 = BE18 + EC18
per18 = 2 * (AB18 + BC18)
b.item('如附圖，平行四邊形 ABCD 中，AE 平分 ∠BAD，且與 BC 交於 E 點。若 BE＝7，EC＝3，則平行四邊形 ABCD 的周長為何？',
       str(per18), [str(2 * (EC18 + BC18)), str(4 * BC18), str(2 * (BE18 + BE18))],
       '【解析】AD // BC，所以 ∠EAD＝∠AEB（內錯角）；又 AE 平分 ∠BAD，∠BAE＝∠EAD，因此 ∠BAE＝∠AEB，△ABE 是等腰三角形，AB＝BE＝7。'
       'BC＝7＋3＝10，周長＝2 × (7＋10)＝34。'
       '({d0}) 是誤以為 AB＝EC＝3；({d1}) 是把四邊都當成 10（平行四邊形不一定是菱形）；({d2}) 是把 BC 也當成 7，漏了 EC。',
       figure=fig_para(),
       check=(per18 == 34, [2 * (EC18 + BC18) == per18, 4 * BC18 == per18, 2 * (BE18 + BE18) == per18]))


# 19  # L4
def fig_tangents():
    fig, ax = blank(4.4, 2.8)
    half = math.radians(65)                       # ∠AOP = 65° so ∠APB = 50°
    O = (0.0, 0.0)
    A, Bp = (math.cos(half), math.sin(half)), (math.cos(half), -math.sin(half))
    P = (1 / math.cos(half), 0.0)
    C = (math.cos(math.radians(18)), math.sin(math.radians(18)))
    ax.add_patch(Circle(O, 1, fill=False, linewidth=1.5))
    ax.plot([A[0], P[0], Bp[0]], [A[1], P[1], Bp[1]], color='black', linewidth=1.4)
    ax.plot([A[0], C[0], Bp[0]], [A[1], C[1], Bp[1]], color='black', linewidth=1.2)
    ax.plot(0, 0, 'o', color='black', markersize=3)
    ax.add_patch(Arc(P, 0.55, 0.55, theta1=180 - 25, theta2=180 + 25, linewidth=1.0))
    ax.text(P[0] - 0.55, -0.07, '50°', fontsize=9)
    for p, s, dx, dy in ((A, 'A', -0.02, 0.07), (Bp, 'B', -0.02, -0.2), (C, 'C', 0.05, 0.0), (O, 'O', -0.06, -0.2), (P, 'P', 0.05, -0.05)):
        ax.text(p[0] + dx, p[1] + dy, s, fontsize=12)
    assert abs(angle_deg(P, A, Bp) - 50) < 1e-6 and abs(angle_deg(C, A, Bp) - 115) < 1e-6
    ax.set_xlim(-1.15, P[0] + 0.35)
    ax.set_ylim(-1.15, 1.15)
    return b.save_fig(fig, 'q19_tangents.png')


P19 = 50
AOB19 = 180 - P19                 # OA ⊥ PA, OB ⊥ PB
ACB19 = 180 - F(AOB19, 2)         # C on the minor arc AB: ACB + (major-arc inscribed angle) = 180
b.item('如附圖，PA、PB 分別與圓 O 相切於 A、B 兩點，C 點在劣弧 AB 上。若 ∠P＝50°，則 ∠ACB 的度數為何？',
       f'{fs(ACB19)}°', [f'{fs(F(AOB19, 2))}°', f'{AOB19}°', f'{P19}°'],
       '【解析】切線垂直於過切點的半徑，∠OAP＝∠OBP＝90°，四邊形 OAPB 的內角和 360°，所以 ∠AOB＝360° − 90° − 90° − 50°＝130°，劣弧 AB＝130°。'
       'C 在劣弧 AB 上，∠ACB 所對的是優弧 AB＝360° − 130°＝230°，所以 ∠ACB＝230° ÷ 2＝115°'
       '（也可以在優弧上取一點 D，∠ADB＝65°，圓內接四邊形 ADBC 對角互補，∠ACB＝180° − 65°＝115°）。'
       '({d0}) 是 C 在優弧上時的答案，但圖中 C 在劣弧上；({d1}) 是圓心角 ∠AOB；({d2}) 是誤以為 ∠ACB＝∠P。',
       figure=fig_tangents(),
       check=(ACB19 == 115, [F(AOB19, 2) == ACB19, AOB19 == ACB19, P19 == ACB19]))


# 20  # L4
def tri20(fx):
    A, B, C = (F(2), F(10)), (F(0), F(0)), (F(20), F(0))
    t = F(2, 5)                                       # AD : AB = 2 : 5
    D = (A[0] + t * (B[0] - A[0]), A[1] + t * (B[1] - A[1]))
    E = (A[0] + t * (C[0] - A[0]), A[1] + t * (C[1] - A[1]))
    Fp = (F(fx), F(0))
    return A, B, C, D, E, Fp


A, B_, C, D, E, Fp = tri20(13)
assert area(A, B_, C) == 100
areas20 = {area(*tri20(fx)[3:]) for fx in (0, 3, 13, 20)}      # same for every F on BC
v20 = areas20.pop()
assert not areas20
w20a = area(A, D, E)                     # △ADE
w20b = 100 * F(3, 5) ** 2                # 用 (3/5)² 計算
w20c = 100 * F(3, 5) / 2                 # 只用了高的比


def fig_dist():
    fig, ax = blank(4.2, 2.4)
    pts = {k: (float(p[0]), float(p[1])) for k, p in zip('ABCDEF', tri20(13))}
    ax.add_patch(Polygon([pts['A'], pts['B'], pts['C']], fill=False, linewidth=1.6))
    ax.add_patch(Polygon([pts['D'], pts['E'], pts['F']], facecolor='#d9d9d9', edgecolor='black', linewidth=1.2))
    for k, dx, dy in (('A', -0.3, 0.4), ('B', -1.0, -0.6), ('C', 0.3, -0.6), ('D', -1.1, 0.0), ('E', 0.3, 0.1), ('F', -0.3, -1.4)):
        ax.text(pts[k][0] + dx, pts[k][1] + dy, k, fontsize=12)
    ax.set_xlim(-1.5, 21.5)
    ax.set_ylim(-1.8, 11)
    return b.save_fig(fig, 'q20_parallel.png')


b.item('如附圖，△ABC 的面積為 100，D、E 兩點分別在 AB、AC 上，且 DE // BC，AD：DB＝2：3。若 F 為 BC 上任意一點，則△DEF（灰色部分）的面積為何？',
       fs(v20), [fs(w20a), fs(w20b), fs(w20c)],
       '【解析】DE // BC，所以△ADE ~ △ABC，DE：BC＝AD：AB＝2：5。設△ABC 中 BC 上的高為 h，則 A 到 DE 的距離是 (2/5)h，DE 與 BC 之間的距離是 (3/5)h。'
       '△DEF 以 DE 為底，F 在 BC 上，所以高就是 DE 與 BC 之間的距離 (3/5)h，面積＝½ × (2/5)BC × (3/5)h＝(6/25) × (½ × BC × h)＝(6/25) × 100＝24，與 F 的位置無關。'
       '({d0}) 是△ADE 的面積 (2/5)² × 100＝16，△DEF 的高不是 A 到 DE 的距離；({d1}) 是誤用 (3/5)² × 100；({d2}) 是只乘了高的比 3/5 再除以 2，忘了底 DE 也只有 BC 的 2/5。',
       figure=fig_dist(),
       check=(v20 == 24, [w20a == v20, w20b == v20, w20c == v20]))
assert w20a == 16 and w20b == 36 and w20c == 30


# 21  # L2
def fig_prism():
    fig, ax = blank(4.0, 2.8)
    k = (0.55, 0.38)
    depth = 12 * 0.42
    off = (depth * k[0] / 0.55 * 0.55, depth * k[1] / 0.55 * 0.55)
    P, Q, R = (0, 0), (8, 0), (0, 6)
    sh = lambda p: (p[0] + off[0] * 1.6, p[1] + off[1] * 1.6)
    P2, Q2, R2 = sh(P), sh(Q), sh(R)
    ax.add_patch(Polygon([P, Q, R], fill=False, linewidth=1.6))
    for a_, b2 in ((Q, Q2), (R, R2), (Q2, R2)):
        ax.plot([a_[0], b2[0]], [a_[1], b2[1]], color='black', linewidth=1.6)
    for a_, b2 in ((P, P2), (P2, Q2), (P2, R2)):
        ax.plot([a_[0], b2[0]], [a_[1], b2[1]], color='black', linewidth=1.0, linestyle='--')
    ax.plot([0, 0.6, 0.6], [0.6, 0.6, 0], color='black', linewidth=0.8)
    ax.text(4, -0.9, '8', fontsize=11, ha='center')
    ax.text(-0.7, 3, '6', fontsize=11, va='center')
    mid = ((Q[0] + Q2[0]) / 2, (Q[1] + Q2[1]) / 2)
    ax.text(mid[0] + 0.3, mid[1] - 0.6, '12', fontsize=11)
    ax.set_xlim(-1.5, Q2[0] + 1.5)
    ax.set_ylim(-1.4, R2[1] + 0.6)
    return b.save_fig(fig, 'q21_prism.png')


l1, l2, hh = 6, 8, 12
hyp21 = math.isqrt(l1 * l1 + l2 * l2)
assert hyp21 * hyp21 == l1 * l1 + l2 * l2
base21 = F(l1 * l2, 2)
lat21 = (l1 + l2 + hyp21) * hh
sa21 = 2 * base21 + lat21
b.item('如附圖，一個直角柱的底面是直角三角形，兩股長分別為 6 公分、8 公分，柱高為 12 公分。這個直角柱的表面積是多少平方公分？',
       fs(sa21), [fs(base21 + lat21), fs(lat21), fs(2 * base21 + (l1 + l2) * hh)],
       '【解析】底面直角三角形的斜邊＝√(6²＋8²)＝10，底面積＝6 × 8 ÷ 2＝24。側面積＝底面周長 × 高＝(6＋8＋10) × 12＝288。'
       '表面積＝2 × 24＋288＝336 平方公分。'
       '({d0}) 是只算了一個底面；({d1}) 只算了側面積；({d2}) 是漏算了斜邊那一個側面（只用 6＋8 乘以高）。',
       figure=fig_prism(),
       check=(sa21 == 336, [base21 + lat21 == sa21, lat21 == sa21, 2 * base21 + (l1 + l2) * hh == sa21]))

# 22  # L3
bag1 = ['紅'] + ['白'] * 2
bag2 = ['紅'] * 2 + ['白']
outs = list(product(bag1, bag2))
p22 = F(sum(a == c for a, c in outs), len(outs))
p_rr = F(sum(a == c == '紅' for a, c in outs), len(outs))
b.item('甲袋中有 1 顆紅球、2 顆白球，乙袋中有 2 顆紅球、1 顆白球，每顆球除顏色外都相同。從甲、乙兩袋中各任意抽出 1 顆球，抽出的兩顆球顏色相同的機率為何？',
       fs(p22), [fs(1 - p22), '1/2', fs(p_rr)],
       '【解析】甲袋 3 顆、乙袋 3 顆，各抽 1 顆共有 3 × 3＝9 種等可能的結果。兩顆都是紅色：1 × 2＝2 種；兩顆都是白色：2 × 1＝2 種，'
       '所以顏色相同的機率＝(2＋2)/9＝4/9。'
       '({d0}) 是顏色「不同」的機率；({d1}) 是以為只有「相同」與「不同」兩種結果，所以各占一半，但這兩種結果發生的可能性並不相等；({d2}) 只算了兩顆都是紅色的情形。',
       check=(p22 == F(4, 9), [1 - p22 == p22, F(1, 2) == p22, p_rr == p22]))

# 23-25  題組: CPBL 2025 first-half attendance (real)
teams = [('中信兄弟', 12415), ('味全龍', 10168), ('富邦悍將', 10288), ('統一7-ELEVEn獅', 7793), ('樂天桃猿', 8317), ('台鋼雄鷹', 7255)]
att = [v for _, v in teams]
b.group(23, 25, '中華職棒 2025 年上半季共進行 180 場例行賽，觀眾人數創下新高，平均每場有 9,373 人進場。'
        '下表是中央社報導的六隊主場「平均每場觀眾人數」（簡稱場均）。其中富邦悍將 2024 年的主場場均為 7,307 人。\n'
        '| 球隊 | 中信兄弟 | 味全龍 | 富邦悍將 | 統一7-ELEVEn獅 | 樂天桃猿 | 台鋼雄鷹 |\n'
        '| 主場場均（人） | 12,415 | 10,168 | 10,288 | 7,793 | 8,317 | 7,255 |')


def median(xs):
    s = sorted(xs)
    n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


def num(x):
    x = F(x)
    return f'{x.numerator:,}' if x.denominator == 1 else f'{float(x):,.1f}'


# 23  # L2
med23 = median(att)
mean23 = F(sum(att), len(att))
unsorted_mid = F(att[2] + att[3], 2)
b.item('表中六隊主場場均的中位數是多少人？',
       f'{num(med23)} 人', [f'{num(unsorted_mid)} 人', f'{num(mean23.__round__())} 人', f'{num(sorted(att)[3])} 人'],
       '【解析】由小到大排列：7,255、7,793、8,317、10,168、10,288、12,415。共 6 個數，中位數是第 3、4 個數的平均：(8,317＋10,168) ÷ 2＝9,242.5 人。'
       '({d0}) 是沒有先排序，直接取表中第 3、4 個數（富邦與統一）平均；({d1}) 是六隊的平均數 56,236 ÷ 6≈9,373，不是中位數；({d2}) 是只取了排序後的第 4 個數。',
       check=(med23 == F(18485, 2), [unsorted_mid == med23, F(round(mean23)) == med23, sorted(att)[3] == med23]))

# 24  # L3
home_games = 180 // len(teams)
total24 = home_games * sum(att)
to_wan = lambda x: f'約 {float(F(x, 10000)):.0f} 萬'
b.item('假設上半季的 180 場比賽平均分配給六隊當主場（每隊主場場數相同），依表中數據估計，上半季全部比賽的觀眾總人次約為多少？',
       to_wan(total24) + '人次', [to_wan(2 * total24) + '人次', to_wan(180 * sum(att)) + '人次', to_wan(home_games * 9373) + '人次'],
       f'【解析】每隊主場 180 ÷ 6＝30 場，每一場比賽只屬於一個主場球隊。總人次＝30 × (12,415＋10,168＋10,288＋7,793＋8,317＋7,255)＝30 × 56,236＝{total24:,}≈169 萬'
       '（和「180 場 × 平均每場 9,373 人≈169 萬」一致）。'
       '({d0}) 是以為每隊比賽 60 場，用 60 × 56,236，但每場比賽有主、客兩隊，這樣每場都被算了兩次；({d1}) 是用 180 場乘以六隊場均的總和，每場只會有一個主場球隊的觀眾數，不能把六隊加起來再乘全部場數；'
       '({d2}) 是 30 × 9,373≈28 萬，只算了 30 場，那只是「一隊」的主場場數。',
       check=(to_wan(total24) == '約 169 萬' and to_wan(180 * 9373) == '約 169 萬',
              [to_wan(2 * total24) == to_wan(total24), to_wan(180 * sum(att)) == to_wan(total24), to_wan(home_games * 9373) == to_wan(total24)]))
assert total24 == 1687080

# 25  # L4
fubon_growth = F(10288 - 7307, 7307)
s_true = fubon_growth > F(40, 100)                                       # 富邦成長超過 40%
s_half = sum(v > 9373 for v in att) > len(att) / 2                       # 超過一半的隊伍高於 9,373
s_ctbc = F(12415 - 7255, 7255) >= F(75, 100)                             # 中信比台鋼多 75% 以上
s_mean = mean23 < med23                                                  # 平均數小於中位數
b.item('根據上表與文中資料，下列敘述何者正確？',
       '富邦悍將的主場場均，2025 年上半季比 2024 年成長超過 40%',
       ['主場場均高於 9,373 人的隊伍超過六隊的一半', '中信兄弟的主場場均比台鋼雄鷹多了 75% 以上', '六隊主場場均的平均數小於中位數'],
       '【解析】富邦：(10,288 − 7,307) ÷ 7,307＝2,981 ÷ 7,307≈0.408，成長約 40.8%，超過 40%，正確。'
       '({d0}) 高於 9,373 人的只有中信、味全、富邦 3 隊，恰好是一半，不是「超過一半」；'
       '({d1}) (12,415 − 7,255) ÷ 7,255＝5,160 ÷ 7,255≈0.711，只多了約 71%，不到 75%；'
       '({d2}) 平均數 56,236 ÷ 6≈9,372.7，中位數 9,242.5，平均數大於中位數。'
       '注意成長率要除以「原來的」7,307，若誤除以 10,288 會得到約 29%，而誤判富邦沒有超過 40%。',
       check=(s_true, [s_half, s_ctbc, s_mean]))
assert sum(v > 9373 for v in att) == 3 and F(2981, 10288) < F(30, 100)

b.write()
