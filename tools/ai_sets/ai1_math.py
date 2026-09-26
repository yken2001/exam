"""AI-1 數學: build src/data/ai/ai1_math.json and its figures.

Every answer is *computed* here (exact fractions), not typed: an item gives
the correct option first plus distractors, the script checks the correct
option equals the computed value and that no distractor does, then places
the options so the answer letters are spread, and writes 「故選 (X)」 itself.

  python tools/ai_sets/ai1_math.py
"""
import json
import math
import os
from fractions import Fraction as F

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon

plt.rcParams['font.family'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(os.path.dirname(HERE))
FIG_DIR = os.path.join(APP, 'public', 'ai', '901', 'math')
OUT = os.path.join(APP, 'src', 'data', 'ai', 'ai1_math.json')
os.makedirs(FIG_DIR, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(FIG_DIR, name), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return f'ai/901/math/{name}'


def blank_axes(w=4.2, h=3.2):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


# ---------------------------------------------------------------- figures

def fig_line():
    fig, ax = plt.subplots(figsize=(3.6, 3.0))
    ax.set_aspect('equal')
    ax.set_xlim(-1.5, 5.5)
    ax.set_ylim(-1.5, 3.8)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.set_xticks(range(-1, 6))
    ax.set_yticks(range(-1, 4))
    ax.tick_params(labelsize=8)
    ax.grid(True, color='#dddddd', linewidth=0.6)
    xs = [-1, 5.2]
    ax.plot(xs, [2 - x / 2 for x in xs], color='black', linewidth=1.6)
    ax.plot([0, 4], [2, 0], 'o', color='black', markersize=4)
    ax.text(0.15, 2.15, '(0, 2)', fontsize=9)
    ax.text(3.7, 0.25, '(4, 0)', fontsize=9)
    ax.text(4.7, -0.7, 'L', fontsize=11, style='italic')
    ax.text(5.35, -0.35, 'x', fontsize=9, style='italic')
    ax.text(0.15, 3.55, 'y', fontsize=9, style='italic')
    return save(fig, 'f09.png')


def fig_triangle():
    fig, ax = blank_axes(4.4, 2.8)
    # drawn to the item's data: ∠B = 70°, ∠C = 180° − 50° − 70° = 60°
    B, C, D = (0, 0), (3.2, 0), (5.0, 0)
    tb, tc = math.tan(math.radians(70)), math.tan(math.radians(60))
    ax_ = C[0] * tc / (tb + tc)
    A = (ax_, ax_ * tb)
    ax.add_patch(Polygon([A, B, C], fill=False, linewidth=1.6))
    ax.plot([C[0], D[0]], [0, 0], color='black', linewidth=1.6)
    for p, name, dx, dy in ((A, 'A', -0.1, 0.12), (B, 'B', -0.3, -0.25), (C, 'C', -0.05, -0.32), (D, 'D', 0.05, -0.32)):
        ax.text(p[0] + dx, p[1] + dy, name, fontsize=12)
    ang = math.degrees(math.atan2(A[1] - C[1], A[0] - C[0]))
    ax.add_patch(Arc(C, 0.8, 0.8, theta1=0, theta2=ang, linewidth=1.2))
    ax.set_xlim(-0.5, 5.4)
    ax.set_ylim(-0.5, A[1] + 0.4)
    return save(fig, 'f14.png')


def fig_ladder():
    fig, ax = blank_axes(3.0, 3.4)
    ax.plot([0, 0], [0, 5.2], color='black', linewidth=2.2)          # wall
    ax.plot([-0.3, 2.6], [0, 0], color='black', linewidth=2.2)       # ground
    ax.plot([1.4, 0], [0, 4.8], color='#8a5a2b', linewidth=3)         # ladder
    ax.plot([0, 0.25, 0.25], [0.25, 0.25, 0], color='black', linewidth=1)
    ax.text(0.85, 2.6, '5 公尺', fontsize=10)
    ax.annotate('', xy=(0, -0.35), xytext=(1.4, -0.35), arrowprops=dict(arrowstyle='<->', linewidth=1))
    ax.text(0.35, -0.8, '1.4 公尺', fontsize=10)
    ax.text(-0.75, 2.4, '牆', fontsize=10)
    ax.text(-0.45, 4.7, '?', fontsize=12)
    ax.set_xlim(-1.0, 2.8)
    ax.set_ylim(-1.1, 5.4)
    return save(fig, 'f15.png')


def fig_circle():
    fig, ax = blank_axes(3.2, 3.2)
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, linewidth=1.6))
    pt = lambda deg: (math.cos(math.radians(deg)), math.sin(math.radians(deg)))
    A, B, C = pt(235), pt(305), pt(100)          # arc AB = 70°, as ∠AOB = 2 × 35°
    ax.plot([A[0], 0, B[0]], [A[1], 0, B[1]], color='black', linewidth=1.3)
    ax.plot([A[0], C[0], B[0]], [A[1], C[1], B[1]], color='black', linewidth=1.3)
    for p, name, dx, dy in ((A, 'A', -0.18, -0.12), (B, 'B', 0.06, -0.12), (C, 'C', -0.03, 0.07), ((0, 0), 'O', -0.05, 0.08)):
        ax.text(p[0] + dx, p[1] + dy, name, fontsize=12)
    ax.plot(0, 0, 'o', color='black', markersize=3)
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.3)
    return save(fig, 'f17.png')


def fig_parallel():
    fig, ax = blank_axes(4.2, 3.0)
    y1, y2 = 2.4, 0.6
    ax.plot([-0.2, 5.2], [y1, y1], color='black', linewidth=1.5)
    ax.plot([-0.2, 5.2], [y2, y2], color='black', linewidth=1.5)
    ax.text(5.3, y1 - 0.08, r'$L_1$', fontsize=12)
    ax.text(5.3, y2 - 0.08, r'$L_2$', fontsize=12)
    t = math.radians(65)                                  # transversal at 65°
    P = (3.0, y1)
    Q = (P[0] - (y1 - y2) / math.tan(t), y2)
    ext = 0.9
    ax.plot([Q[0] - ext * math.cos(t), P[0] + ext * math.cos(t)],
            [Q[1] - ext * math.sin(t), P[1] + ext * math.sin(t)], color='black', linewidth=1.5)
    # ∠1 at P: below L1, left of the transversal (from 180° to 245°)
    ax.add_patch(Arc(P, 0.7, 0.7, theta1=180, theta2=245, linewidth=1.2))
    ax.text(P[0] - 0.62, P[1] - 0.42, '1', fontsize=11)
    # ∠x at Q: above L2, left of the transversal (from 65° to 180°)
    ax.add_patch(Arc(Q, 0.7, 0.7, theta1=65, theta2=180, linewidth=1.2))
    ax.text(Q[0] - 0.42, Q[1] + 0.3, 'x', fontsize=11, style='italic')
    ax.set_xlim(-0.4, 5.7)
    ax.set_ylim(-0.3, 3.4)
    return save(fig, 'f18.png')


def fig_box():
    fig, ax = blank_axes(3.6, 2.8)
    l, w, h, d = 3.0, 1.2, 1.8, (0.9, 0.6)          # drawn sizes (not to scale)
    front = [(0, 0), (l, 0), (l, h), (0, h)]
    back = [(x + d[0], y + d[1]) for x, y in front]
    ax.add_patch(Polygon(front, fill=False, linewidth=1.5))
    for a, b in zip(front, back):
        ax.plot([a[0], b[0]], [a[1], b[1]], color='black', linewidth=1.5 if a != (0, 0) else 1, linestyle='-' if a != (0, 0) else '--')
    ax.plot([back[1][0], back[2][0], back[3][0]], [back[1][1], back[2][1], back[3][1]], color='black', linewidth=1.5)
    ax.plot([back[0][0], back[1][0]], [back[0][1], back[1][1]], color='black', linewidth=1, linestyle='--')
    ax.plot([back[0][0], back[3][0]], [back[0][1], back[3][1]], color='black', linewidth=1, linestyle='--')
    ax.text(l / 2 - 0.3, -0.35, '5 公分', fontsize=10)
    ax.text(l + 0.55, 0.05, '4 公分', fontsize=10, rotation=34)
    ax.text(-0.95, h / 2 - 0.1, '3 公分', fontsize=10)
    ax.set_xlim(-1.1, l + d[0] + 0.3)
    ax.set_ylim(-0.6, h + d[1] + 0.2)
    return save(fig, 'f23.png')


# ---------------------------------------------------------------- items
# each: stem, correct option, distractors, the computed value the correct
# option must equal (checked), explanation (without 故選), figure

def frac_str(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    s = '−' if x < 0 else ''
    return f'{s}{abs(x.numerator)}/{x.denominator}'


items = []


def item(stem, correct, distractors, explanation, figure=None, check=None):
    assert len(distractors) == 3 and correct not in distractors and len(set(distractors)) == 3
    if check is not None:
        ok, bad = check
        assert ok, f'computed value does not match the correct option: {stem[:30]}'
        assert not any(bad), f'a distractor equals the computed value: {stem[:30]}'
    items.append(dict(stem=stem, correct=correct, distractors=distractors, explanation=explanation, figure=figure))


# 1
v = (-3) * 4 - F(-18, 6)
item('計算 (−3)×4 − (−18)÷6 之值為何？', '−9', ['−15', '−5', '9'],
     '先乘除後加減：(−3)×4＝−12，(−18)÷6＝−3，所以 −12 − (−3)＝−12＋3＝−9。',
     check=(v == -9, [v == -15, v == -5, v == 9]))
# 2
v = F(3, 4) - F(5, 6) / F(5, 2)
wrong = (F(3, 4) - F(5, 6)) / F(5, 2)
item('計算 3/4 − 5/6 ÷ 5/2 之值為何？', '5/12', ['−1/30', '1/6', '7/12'],
     '先算除法：5/6 ÷ 5/2＝5/6 × 2/5＝1/3，再算 3/4 − 1/3＝9/12 − 4/12＝5/12。若由左往右先減再除，會得到 −1/30，這是錯誤的運算順序。',
     check=(v == F(5, 12), [wrong == v, v == F(1, 6), v == F(7, 12)]))
# 3
v = 0.0000075
item('人體一顆紅血球的直徑約為 0.0000075 公尺。若以科學記號表示，下列何者正確？',
     '7.5 × 10⁻⁶ 公尺', ['7.5 × 10⁻⁵ 公尺', '7.5 × 10⁻⁷ 公尺', '7.5 × 10⁻⁴ 公尺'],
     '0.0000075 的小數點要向右移 6 位才得到 7.5，所以 0.0000075＝7.5 × 10⁻⁶。',
     check=(abs(v - 7.5e-6) < 1e-15, [abs(v - x) < 1e-15 for x in (7.5e-5, 7.5e-7, 7.5e-4)]))
# 4
v = math.sqrt(48) - math.sqrt(12)
item('化簡 √48 − √12 的結果為何？', '2√3', ['6', '4√3', '6√3'],
     '√48＝√(16×3)＝4√3，√12＝√(4×3)＝2√3，所以 √48 − √12＝4√3 − 2√3＝2√3。注意 √48 − √12 不等於 √(48−12)＝6。',
     check=(abs(v - 2 * math.sqrt(3)) < 1e-12, [abs(v - x) < 1e-9 for x in (6, 4 * math.sqrt(3), 6 * math.sqrt(3))]))
# 5
v = F(2 ** 3) ** 2 / F(2) ** 4
item('計算 (2³)² ÷ 2⁴ 之值為何？', '4', ['16', '32', '1/4'],
     '(2³)²＝2⁶，2⁶ ÷ 2⁴＝2⁶⁻⁴＝2²＝4。',
     check=(v == 4, [v == 16, v == 32, v == F(1, 4)]))
# 6
x = F(8 + 6, 3 - 1)
item('解一元一次方程式 3(x − 2)＝x＋8，得 x＝？', '7', ['5', '1', '−1'],
     '3(x − 2)＝x＋8 → 3x − 6＝x＋8 → 2x＝14 → x＝7。驗算：3×(7−2)＝15，7＋8＝15。',
     check=(x == 7 and 3 * (x - 2) == x + 8, [3 * (5 - 2) == 5 + 8, 3 * (1 - 2) == 1 + 8, 3 * (-1 - 2) == -1 + 8]))
# 7
px, ny = 20, 30          # pen, notebook
item('文具店裡每支筆的價格都相同，每本筆記本的價格也都相同。小美買 2 支筆和 3 本筆記本共付 130 元；小華買 4 支筆和 1 本筆記本共付 110 元。請問一本筆記本多少元？',
     '30 元', ['20 元', '25 元', '35 元'],
     '設筆每支 x 元、筆記本每本 y 元：2x＋3y＝130，4x＋y＝110。由第二式得 y＝110 − 4x，代入第一式：2x＋3(110 − 4x)＝130 → −10x＝−200 → x＝20，y＝110 − 80＝30。所以筆記本一本 30 元（20 元是筆的價格）。',
     check=(2 * px + 3 * ny == 130 and 4 * px + ny == 110, [False, 2 * 25 + 3 * 25 == 130 and 4 * 25 + 25 == 110, False]))
# 8
v = 6 * 25000 / 100000
item('某張地圖的比例尺是 1：25000。地圖上兩地相距 6 公分，則兩地的實際距離是多少公里？', '1.5 公里', ['15 公里', '0.15 公里', '150 公里'],
     '實際距離＝6 × 25000＝150000 公分。1 公里＝100000 公分，所以 150000 公分＝1.5 公里。',
     check=(v == 1.5, [v == 15, v == 0.15, v == 150]))
# 9
f9 = fig_line()
chk = lambda a, b, c: a * 0 + b * 2 == c and a * 4 + b * 0 == c        # passes (0,2) and (4,0)
item('坐標平面上，直線 L 通過 (0, 2) 與 (4, 0) 兩點，如附圖所示。直線 L 的方程式為何？', 'x＋2y＝4', ['2x＋y＝4', 'x − 2y＝4', '2x − y＝−4'],
     '斜率＝(0 − 2)/(4 − 0)＝−1/2，y 截距為 2，所以 y＝−(1/2)x＋2，同乘 2 移項得 x＋2y＝4。驗算：(0, 2)：0＋4＝4；(4, 0)：4＋0＝4。',
     figure=f9, check=(chk(1, 2, 4), [chk(2, 1, 4), chk(1, -2, 4), chk(2, -1, -4)]))
# 10
roots = sorted(((5 + 1) // 2, (5 - 1) // 2), reverse=True)     # x²−5x+6=(x−2)(x−3)
a, b = roots
assert a * a - 5 * a + 6 == 0 and b * b - 5 * b + 6 == 0
v = a - 2 * b
item('若一元二次方程式 x² − 5x＋6＝0 的兩根為 a、b，且 a＞b，則 a − 2b 之值為何？', '−1', ['1', '−4', '7'],
     'x² − 5x＋6＝(x − 2)(x − 3)＝0，兩根為 3 和 2。因為 a＞b，所以 a＝3、b＝2，a − 2b＝3 − 4＝−1。若把 a、b 對調會得到 2 − 6＝−4。',
     check=(v == -1, [v == 1, v == -4, v == 7]))
# 11
poly = lambda t: t * t - 9 * t + 20
item('下列何者是多項式 x² − 9x＋20 的因式？', 'x − 4', ['x＋4', 'x − 2', 'x＋5'],
     'x² − 9x＋20 要找兩數相乘為 20、相加為 −9，即 −4 和 −5，所以 x² − 9x＋20＝(x − 4)(x − 5)，x − 4 是它的因式。',
     check=(poly(4) == 0, [poly(-4) == 0, poly(2) == 0, poly(-5) == 0]))
# 12
d = F(23 - 11, 7 - 3)
a1 = 11 - 2 * d
v = a1 + 19 * d
item('一個等差數列的第 3 項是 11，第 7 項是 23，則此數列的第 20 項是多少？', '62', ['59', '65', '68'],
     '第 3 項到第 7 項相差 4 個公差：23 − 11＝4d，d＝3。首項＝11 − 2×3＝5，第 20 項＝5＋19×3＝62。',
     check=(v == 62, [v == 59, v == 65, v == 68]))
# 13
v = sum(20 + 2 * k for k in range(15))
item('學校禮堂的第一排有 20 個座位，之後每一排都比前一排多 2 個座位，共有 15 排。這個禮堂共有多少個座位？', '510 個', ['480 個', '540 個', '328 個'],
     '各排座位數是首項 20、公差 2 的等差數列，第 15 排有 20＋14×2＝48 個。總和＝(20＋48)×15÷2＝510 個。',
     check=(v == 510, [v == 480, v == 540, v == 328]))
# 14
f14 = fig_triangle()
v = 50 + 70
item('如附圖，△ABC 中，∠A＝50°，∠B＝70°，延長 BC 到 D 點。則 ∠ACD 的度數為何？', '120°', ['60°', '110°', '130°'],
     '三角形的外角等於不相鄰的兩個內角和，所以 ∠ACD＝∠A＋∠B＝50°＋70°＝120°。（60° 是 ∠ACB 的度數。）',
     figure=f14, check=(v == 120, [v == 60, v == 110, v == 130]))
# 15
f15 = fig_ladder()
v = math.sqrt(5 ** 2 - 1.4 ** 2)
item('一支長 5 公尺的梯子斜靠在垂直的牆上，梯腳離牆 1.4 公尺，如附圖所示。梯子頂端離地面多少公尺？', '4.8 公尺', ['3.6 公尺', '4.6 公尺', '5.2 公尺'],
     '牆、地面和梯子形成直角三角形，梯子是斜邊。由畢氏定理，高度＝√(5² − 1.4²)＝√(25 − 1.96)＝√23.04＝4.8 公尺。',
     figure=f15, check=(abs(v - 4.8) < 1e-9, [abs(v - x) < 1e-9 for x in (3.6, 4.6, 5.2)]))
# 16
v = F(160, 120) * 9
item('同一時間在陽光下，身高 160 公分的小安影子長 120 公分，旗桿的影子長 9 公尺。旗桿高多少公尺？', '12 公尺', ['6.75 公尺', '10.5 公尺', '15 公尺'],
     '同一時間，物體的高度和影長成正比：160：120＝旗桿高：9，旗桿高＝9 × 160/120＝12 公尺。若寫成 120：160 會算出 6.75，比例放反了。',
     check=(v == 12, [v == F(27, 4), v == F(21, 2), v == 15]))
# 17
f17 = fig_circle()
v = 2 * 35
item('如附圖，A、B、C 三點在圓 O 上，且 ∠ACB＝35°。則 ∠AOB 的度數為何？', '70°', ['35°', '110°', '145°'],
     '∠AOB 是圓心角，∠ACB 是對同一弧 AB 的圓周角。圓心角是同弧所對圓周角的 2 倍，所以 ∠AOB＝2 × 35°＝70°。',
     figure=f17, check=(v == 70, [v == 35, v == 110, v == 145]))
# 18
f18 = fig_parallel()
v = 180 - 65
item('如附圖，直線 L₁ 與 L₂ 平行，一條直線與它們相交。若 ∠1＝65°，則 ∠x 的度數為何？', '115°', ['65°', '25°', '130°'],
     '∠1 和 ∠x 位在兩平行線之間、截線的同一側，是同側內角。兩平行線的同側內角互補，所以 ∠x＝180° − 65°＝115°。',
     figure=f18, check=(v == 115, [v == 65, v == 25, v == 130]))
# 19
vx = F(2, 2)
vy = vx * vx - 2 * vx - 3
item('二次函數 y＝x² − 2x − 3 的圖形頂點坐標為何？', '(1, −4)', ['(−1, −4)', '(1, 4)', '(−1, 0)'],
     '配方：y＝x² − 2x＋1 − 1 − 3＝(x − 1)² − 4，所以頂點坐標是 (1, −4)。',
     check=((vx, vy) == (1, -4), [(vx, vy) == (-1, -4), (vx, vy) == (1, 4), (vx, vy) == (-1, 0)]))
# 20
data = [45, 52, 38, 60, 52, 47, 55, 52, 41, 58]
s = sorted(data)
median = F(s[4] + s[5], 2)
mean = F(sum(data), len(data))
mode = max(set(data), key=data.count)
rng = max(data) - min(data)
item('下表是某班 10 位同學一分鐘跳繩的次數：\n| 座號 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |\n| 次數 | 45 | 52 | 38 | 60 | 52 | 47 | 55 | 52 | 41 | 58 |\n關於這筆資料，下列敘述何者正確？',
     '中位數比平均數大', ['眾數是 55 次', '平均數是 52 次', '全距是 20 次'],
     f'由小到大排列：38、41、45、47、52、52、52、55、58、60。中位數＝(52＋52)÷2＝52，平均數＝500÷10＝50，所以中位數比平均數大。眾數是出現最多次的 52；全距＝60 − 38＝22。',
     check=(median > mean, [mode == 55, mean == 52, rng == 20]))
# 21
v = F(3 + 2, 10)
item('袋中有 3 顆紅球、5 顆白球、2 顆黃球，每顆球被抽到的機會相等。從袋中任意抽出 1 顆球，抽到的不是白球的機率為何？', '1/2', ['3/10', '1/5', '7/10'],
     '不是白球的有紅球 3 顆和黃球 2 顆，共 5 顆，全部 10 顆，所以機率＝5/10＝1/2。',
     check=(v == F(1, 2), [v == F(3, 10), v == F(1, 5), v == F(7, 10)]))
# 22
outcomes = [(a, b) for a in 'HT' for b in 'HT']
v = F(sum(1 for a, b in outcomes if a != b), len(outcomes))
item('同時投擲兩枚公正的硬幣，出現「一枚正面、一枚反面」的機率為何？', '1/2', ['1/4', '1/3', '3/4'],
     '所有可能的結果有（正, 正）、（正, 反）、（反, 正）、（反, 反）4 種，機會相等。一正一反有（正, 反）和（反, 正）2 種，機率＝2/4＝1/2。常見的錯誤是把結果只算成 3 種而得 1/3。',
     check=(v == F(1, 2), [v == F(1, 4), v == F(1, 3), v == F(3, 4)]))
# 23
f23 = fig_box()
v = 2 * (5 * 4 + 5 * 3 + 4 * 3)
item('如附圖，一個長方體的長、寬、高分別是 5 公分、4 公分、3 公分。這個長方體的表面積是多少平方公分？', '94 平方公分', ['47 平方公分', '60 平方公分', '120 平方公分'],
     '長方體有 3 組相同的面：5×4＝20、5×3＝15、4×3＝12，表面積＝2×(20＋15＋12)＝94 平方公分。60 是體積（立方公分），47 只算了一半。',
     figure=f23, check=(v == 94, [v == 47, v == 60, v == 120]))
# 24, 25 (題組)
plan_a = lambda g: 199 + max(0, g - 5) * 30
plan_b = lambda g: 399
v24 = plan_a(9)
item('小明這個月用了 9 GB 的網路流量。若他選擇甲方案，這個月要付多少元？', '319 元', ['469 元', '199 元', '399 元'],
     '甲方案含 5 GB，超過的 9 − 5＝4 GB 每 GB 加收 30 元：199＋4×30＝319 元。若把 9 GB 全部乘以 30 會得到 469 元，是錯誤的。',
     check=(v24 == 319, [v24 == 469, v24 == 199, v24 == 399]))
v25 = next(g for g in range(0, 100) if plan_b(g) < plan_a(g))
item('若每月流量都以整數 GB 計算，每月至少要用多少 GB，選乙方案才會比甲方案便宜？', '12 GB', ['7 GB', '11 GB', '17 GB'],
     '甲方案付 199＋(用量 − 5)×30 元。用 11 GB 時甲付 199＋6×30＝379 元，比乙的 399 元便宜；用 12 GB 時甲付 199＋7×30＝409 元，比乙貴。所以至少用 12 GB，乙方案才比較便宜。（7 是只算了超出的 GB 數，忘了加上甲方案內含的 5 GB。）',
     check=(v25 == 12, [v25 == 7, v25 == 11, v25 == 17]))

assert len(items) == 25

# spread the answer letters: A 6, B 6, C 7, D 6, no letter three times in a row
TARGET = 'CADBACBDCABDACBDACDBCABDC'
assert len(TARGET) == 25 and all(TARGET.count(L) >= 6 for L in 'ABCD')
questions = []
for n, (it, letter) in enumerate(zip(items, TARGET), start=1):
    k = 'ABCD'.index(letter)
    opts = list(it['distractors'])
    opts.insert(k, it['correct'])
    questions.append({
        'qNo': n, 'stem': it['stem'], 'options': opts, 'answer': letter,
        'explanation': f"【解析】{it['explanation']}故選 ({letter})。",
        **({'figure': it['figure']} if it['figure'] else {}),
    })

data = {
    'set': 'AI-1', 'year': 901, 'subject': '數學', 'title': 'AI-1 數學模擬卷（選擇題）',
    'note': '由 AI 依會考數學科選擇題型與素養導向原則（生活情境、資料判讀）編寫，非會考真題；每題答案均由程式計算驗證（tools/ai_sets/ai1_math.py），附圖由程式依題目數據繪製。',
    'groups': [{
        'from': 24, 'to': 25,
        'passage': '某電信公司推出兩種手機網路方案：\n| 方案 | 月租費 | 內含流量 | 超過的部分 |\n| 甲 | 199 元 | 5 GB | 每 GB 加收 30 元 |\n| 乙 | 399 元 | 不限量 | 不另外收費 |\n請根據上表回答下列問題。',
    }],
    'items': questions,
}
if os.path.exists(OUT):                      # keep the verification record
    data['verification'] = json.load(open(OUT, encoding='utf-8')).get('verification', [])
json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', OUT, 'answers', ''.join(q['answer'] for q in questions))
