"""AI-2 數學（進階）: build src/data/ai/ai2_math.json and its figures.

Every answer is computed here with exact arithmetic (fractions.Fraction or
integers) and passed through check=(ok, [bad...]); the builder places the
options, writes the letters into the explanation and appends 「故選」.
Each item is tagged with its design level (# L2 .. # L5, see SPEC_AI2_AI3.md).

  PYTHONIOENCODING=utf-8 python tools/ai_sets/ai2_math.py
"""
import math
import os
import sys
from fractions import Fraction as F
from itertools import product

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon, Rectangle, Circle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SetBuilder, spread_target  # noqa: E402

plt.rcParams['font.family'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False

TOPICS = [
    '數與式、因式分解、根號估算',
    '一次方程式與不等式建模（表格、收費規則）',
    '一次函數與二次函數圖形判讀',
    '等差數列與級數',
    '幾何：摺紙、相似形、圓與切線、表面最短路徑、外心',
    '統計（四分位數）與機率',
    '時事：2026 FIFA 世界盃賽制（48 隊、12 組每組 4 隊、各組前 2 名與 8 個最佳第三名晉級 32 強、共 104 場、2026/6/11–7/19、加拿大墨西哥美國合辦）: https://en.wikipedia.org/wiki/2026_FIFA_World_Cup',
    '時事：2025 大阪・關西世博會期 2025/4/13–10/13、總入場人次 29,017,924（一般入場 25,578,986）: https://en.wikipedia.org/wiki/Expo_2025',
    '時事：大阪世博「大屋根環」內徑約 615 m、外徑約 675 m、寬約 30 m、全周約 2,025 m（在寬度中心 15 m 處量）、建築面積 61,035.55 m²、金氏世界紀錄最大木造建築: https://kyodonewsprwire.jp/release/202503045110',
    '時事：115 年（2026）起每月最低工資 29,500 元、每小時 196 元（114 年為 28,590 元、190 元）: https://www.mol.gov.tw/1607/1632/1633/84947/post',
]

b = SetBuilder('ai2_math', '數學', year=902, set_name='AI-2', title='AI-2 數學模擬卷（進階）',
               note='由 AI 依會考數學科選擇題型編寫（非會考真題），難度定位「進階」：多為兩到三步推理、讀表格與規則建模、圖形判讀，並以 2025–2026 年真實時事（世界盃、大阪世博、最低工資）為素材。每題答案均由程式以精確分數計算驗證（tools/ai_sets/ai2_math.py），附圖依題目數據繪製。',
               target=spread_target(25, 4, 902), difficulty='進階', topics=TOPICS)


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


# ====================================================================== items

# 1  # L3
cands1 = [n for n in range(1, 2000) if n % 6 == 5 and n % 4 == 3]
jia1 = all(n % 12 == 11 for n in cands1)
yi1 = all((n + 1) % 24 == 0 for n in cands1)
b.item('已知正整數 n 除以 6 的餘數是 5，除以 4 的餘數是 3。甲、乙兩人提出以下看法：\n【甲】n 除以 12 的餘數一定是 11\n【乙】n＋1 一定是 24 的倍數\n對於甲、乙兩人的看法，下列判斷何者正確？',
       '甲正確，乙錯誤', ['甲、乙皆正確', '甲錯誤，乙正確', '甲、乙皆錯誤'],
       '【解析】n 除以 6 餘 5，表示 n＋1 是 6 的倍數；n 除以 4 餘 3，表示 n＋1 是 4 的倍數。所以 n＋1 是 6 與 4 的公倍數，也就是 12 的倍數'
       '（6 與 4 的最小公倍數是 12，不是 6×4＝24），n＋1＝12k，n＝12k − 1＝12(k − 1)＋11，除以 12 餘 11，甲正確。'
       '例如 n＝11：11÷6 餘 5、11÷4 餘 3，但 n＋1＝12 不是 24 的倍數，乙錯誤。'
       '({d0}) 與 ({d1}) 是把「同時是 6 和 4 的倍數」誤當成「是 6×4＝24 的倍數」，但 6 與 4 有公因數 2；({d2}) 是沒有發現 n＋1 同時是 6 與 4 的倍數。',
       check=(jia1 and not yi1, [jia1 and yi1, (not jia1) and yi1, (not jia1) and (not yi1)]))

# 2  # L3
ks = sorted({p + q for p in range(-30, 31) for q in range(-30, 31) if p * q == -24})
b.item('若 x²＋kx − 24 可以因式分解成 (x＋p)(x＋q)，其中 k、p、q 都是整數，則 k 共有幾種可能的值？',
       f'{len(ks)} 種', ['4 種', '16 種', '6 種'],
       '【解析】(x＋p)(x＋q)＝x²＋(p＋q)x＋pq，所以 pq＝−24、k＝p＋q。pq＝−24 時 p、q 一正一負，'
       'p、q 兩數可能是 1 與 −24、−1 與 24、2 與 −12、−2 與 12、3 與 −8、−3 與 8、4 與 −6、−4 與 6，'
       'k 分別是 −23、23、−10、10、−5、5、−2、2，共 8 種。'
       '({d0}) 是只算了 k＞0 的情形；({d1}) 是把 (p, q) 與 (q, p) 當成不同的分解，但它們的 k 相同；({d2}) 是漏了 1 與 24 這一組因數。',
       check=(len(ks) == 8, [len(ks) == 4, len(ks) == 16, len(ks) == 6]))

# 3  # L3
lo, hi = F(725, 100) ** 2, F(735, 100) ** 2
ns = [n for n in range(1, 200) if lo <= n < hi]
ns_wrong = [n for n in range(1, 200) if F(73, 10) ** 2 <= n < F(74, 10) ** 2]
b.item('小宜用計算機算出正整數 n 的平方根，並把結果四捨五入到小數點後第一位，得到 7.3。符合這個條件的正整數 n 共有幾個？',
       '2 個', ['1 個', '3 個', '4 個'],
       '【解析】√n 四捨五入到小數第一位是 7.3，表示 7.25 ≤ √n＜7.35，平方得 52.5625 ≤ n＜54.0225，所以 n＝53 或 54，共 2 個。'
       '({d0}) 是誤以為 7.3 ≤ √n＜7.4（即 53.29 ≤ n＜54.76，只有 54）；({d1}) 是把 52 也算進去，但 √52≈7.21，四捨五入是 7.2；({d2}) 是把 52 到 55 都算入，55 的平方根約 7.42，四捨五入是 7.4。',
       check=(len(ns) == 2 and ns == [53, 54], [len(ns) == 1, len(ns) == 3, len(ns) == 4]))
assert ns_wrong == [54]

# 4  # L3  (current events: Expo 2025)
from datetime import date
days = (date(2025, 10, 13) - date(2025, 4, 13)).days + 1
total, paid = 29017924, 25578986


def sci2(x):
    """a × 10ⁿ with a rounded to 2 decimals (half up), as text"""
    x = F(x)
    n = 0
    while x >= 10:
        x /= 10
        n += 1
    a2 = math.floor(x * 100 + F(1, 2))
    sup = str(n).translate(str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹'))
    return f'{a2 // 100}.{a2 % 100:02d} × 10{sup}'


avg = F(total, days)
b.item('2025 年日本大阪・關西世界博覽會的會期從 4 月 13 日開幕到 10 月 13 日閉幕（開幕日與閉幕日都算在會期內）。'
       '大會公布的總入場人次為 29,017,924，其中一般入場 25,578,986 人次。若以「總入場人次 ÷ 會期天數」計算平均每天的入場人次，'
       '並以科學記號表示（係數四捨五入到小數點後第二位），結果為何？',
       sci2(avg), [sci2(F(total, days - 1)), sci2(F(paid, days)), '1.58 × 10⁴'],
       f'【解析】會期天數：4 月 13 日～30 日有 18 天，5～9 月有 31＋30＋31＋31＋30＝153 天，10 月 1 日～13 日有 13 天，共 18＋153＋13＝{days} 天（頭尾兩天都要算）。'
       f'平均每天＝29,017,924 ÷ {days}≈157,706，以科學記號表示約為 1.58 × 10⁵。'
       '({d0}) 是天數用「10 月 13 日 − 4 月 13 日」算成 183 天，少算了一天；({d1}) 是誤用一般入場人次 25,578,986；({d2}) 是 157,706 的位數數錯，10 的次方少了 1。',
       check=(days == 184 and sci2(avg) == '1.58 × 10⁵',
              [sci2(F(total, days - 1)) == sci2(avg), sci2(F(paid, days)) == sci2(avg), sci2(avg) == '1.58 × 10⁴']))


# 5  # L4  (current events: Grand Ring)
def fig_ring():
    fig, ax = blank(4.2, 4.2)
    R, r = 337.5, 307.5
    ax.add_patch(Circle((0, 0), R, facecolor='#d9c3a0', edgecolor='black', linewidth=1.2))
    ax.add_patch(Circle((0, 0), r, facecolor='white', edgecolor='black', linewidth=1.2))
    ax.add_patch(Circle((0, 0), 322.5, fill=False, edgecolor='#555555', linewidth=0.8, linestyle='--'))
    ax.plot(0, 0, 'o', color='black', markersize=3)
    # inner diameter (horizontal)
    ax.annotate('', xy=(-r, 0), xytext=(r, 0), arrowprops=dict(arrowstyle='<->', linewidth=1))
    ax.text(0, 18, '內徑 615 公尺', ha='center', fontsize=10)
    # outer diameter (vertical-ish)
    t = math.radians(65)
    ax.annotate('', xy=(R * math.cos(t), R * math.sin(t)), xytext=(-R * math.cos(t), -R * math.sin(t)),
                arrowprops=dict(arrowstyle='<->', linewidth=1, color='#1f4e79'))
    ax.text(70, -120, '外徑 675 公尺', fontsize=10, color='#1f4e79')
    ax.text(-140, -250, '虛線：寬度中心的圓', fontsize=8.5, color='#555555')
    ax.set_xlim(-360, 360)
    ax.set_ylim(-360, 360)
    return b.save_fig(fig, 'q05_ring.png')


Rr, rr = F(675, 2), F(615, 2)
area_over_pi = Rr * Rr - rr * rr
opts5 = {'mid': F(645) * 30, 'outer': F(675) * 30, 'inner': F(615) * 30, 'w60': F(645) * 60}
b.item('2025 大阪世博的地標「大屋根環」是一座環狀木造建築，官方資料：內徑約 615 公尺、外徑約 675 公尺、寬約 30 公尺。'
       '若把它的俯視圖看成兩個同心圓之間的圓環（如附圖），則這個圓環的面積等於下列哪一個長方形的面積？',
       '寬 30 公尺，長等於「直徑 645 公尺的圓」的周長',
       ['寬 30 公尺，長等於「直徑 675 公尺的圓」的周長', '寬 30 公尺，長等於「直徑 615 公尺的圓」的周長', '寬 60 公尺，長等於「直徑 645 公尺的圓」的周長'],
       '【解析】外圓半徑 337.5、內圓半徑 307.5，圓環面積＝π×337.5² − π×307.5²＝π×(337.5＋307.5)×(337.5 − 307.5)＝π×645×30＝(645π)×30。'
       '645π 正是直徑 645 公尺（寬度正中間）那個圓的周長，所以圓環面積等於「寬 30、長為中間圓周長」的長方形面積。官方說全周約 2,025 公尺，就是在寬度中心量的：645π≈2,026。'
       '({d0}) 用外圓周長會多算（外側較長）；({d1}) 用內圓周長會少算；({d2}) 把寬度誤當成兩直徑的差 675 − 615＝60，其實寬度是半徑差 30。',
       figure=fig_ring(),
       check=(opts5['mid'] == area_over_pi, [opts5[k] == area_over_pi for k in ('outer', 'inner', 'w60')]))

# 6  # L3  (current events: minimum wage)
need = math.ceil(F(29500, 196))
b.item('勞動部公告：自 115 年 1 月 1 日起，每月最低工資由 28,590 元調整為 29,500 元，每小時最低工資由 190 元調整為 196 元。'
       '某位按時計酬的工讀生（虛構情境）在 115 年以每小時 196 元計薪，若他一個月的薪資要不低於每月最低工資 29,500 元，這個月至少要工作幾小時（以整數小時計）？',
       f'{need} 小時', ['150 小時', '156 小時', '155 小時'],
       '【解析】設工作 h 小時：196h ≥ 29,500，h ≥ 29,500 ÷ 196≈150.5，h 取整數，所以至少 151 小時（150 小時只有 29,400 元，不夠；151 小時是 29,596 元）。'
       '({d0}) 是把 150.5 無條件捨去，但 150 小時的薪資不到 29,500 元；({d1}) 與 ({d2}) 是誤用舊的時薪 190 元（29,500 ÷ 190≈155.3），題目說的是 115 年的新時薪。',
       check=(need == 151 and 196 * need >= 29500 and 196 * (need - 1) < 29500,
              [need == 150, need == math.ceil(F(29500, 190)), need == 155]))

# 7  # L4
from itertools import combinations
rec = [((3, 2), 155), ((2, 3), 170), ((1, 2), 105), ((2, 1), 95)]
sols = {}
for i, j in combinations(range(4), 2):
    (a1, b1), c1 = rec[i]
    (a2, b2), c2 = rec[j]
    det = a1 * b2 - a2 * b1
    t_, b_ = F(c1 * b2 - c2 * b1, det), F(a1 * c2 - a2 * c1, det)
    sols[(i, j)] = (t_, b_, sum(1 for (x, y), c in rec if x * t_ + y * b_ != c))
good = {(t_, b_) for t_, b_, w in sols.values() if w == 1}
assert len(good) == 1
t7, b7 = good.pop()
v7 = t7 + 4 * b7
alt = lambda i, j: sols[(i, j)][0] + 4 * sols[(i, j)][1]
b.item('某早餐店（虛構情境）每杯紅茶價格相同、每個麵包價格也相同。下表是四張收據，店員說其中恰有一張的金額打錯了，其餘三張都正確：\n'
       '| 收據 | 紅茶 | 麵包 | 金額 |\n| 第一張 | 3 杯 | 2 個 | 155 元 |\n| 第二張 | 2 杯 | 3 個 | 170 元 |\n| 第三張 | 1 杯 | 2 個 | 105 元 |\n| 第四張 | 2 杯 | 1 個 | 95 元 |\n'
       '若買 1 杯紅茶和 4 個麵包，正確的金額是多少元？',
       f'{fs(v7)} 元', [f'{fs(alt(0, 3))} 元', f'{float(alt(1, 3)):g} 元', f'{fs(alt(2, 3))} 元'],
       '【解析】任取兩張收據可解出一組價格，再用另外兩張檢驗：正確的價格必須讓「恰好一張」不符合。'
       '由第一、二張：3t＋2b＝155、2t＋3b＝170，得紅茶 t＝25、麵包 b＝40；檢驗第三張 25＋80＝105 符合，第四張 50＋40＝90≠95 不符合，恰好一張錯，所以第四張打錯了。'
       '1 杯紅茶＋4 個麵包＝25＋160＝185 元。'
       '其他選項都是誤信了第四張：({d0}) 由第一、四張解出 t＝35、b＝25，但這樣第二張（145 元）與第三張（85 元）都不符，變成兩張錯；'
       '({d1}) 由第二、四張解出 t＝28.75、b＝37.5，第一、三張都不符；({d2}) 由第三、四張解出 t＝85/3、b＝115/3，第一、二張都不符。',
       check=(v7 == 185 and (t7, b7) == (25, 40), [alt(0, 3) == v7, alt(1, 3) == v7, alt(2, 3) == v7]))
assert (alt(0, 3), alt(1, 3), alt(2, 3)) == (135, F(715, 4), F(545, 3))

# 8  # L4
shopA = lambda n: F(3, 2) * n if n < 200 else F(6, 5) * n
shopB = lambda n: 120 + F(4, 5) * n
cheaperB = [n for n in range(1, 1000) if shopB(n) < shopA(n)]
b.item('小芸（虛構情境）要印同一份講義，兩家影印店的收費如下：\n| 店家 | 收費方式 |\n| 甲店 | 每張 1.5 元；一次印 200 張以上（含 200 張），全部改為每張 1.2 元 |\n| 乙店 | 先付會員費 120 元，之後每張 0.8 元 |\n'
       '若她一次印下列張數，哪一種張數選乙店會比甲店便宜？',
       '180 張', ['250 張', '300 張', '160 張'],
       '【解析】不到 200 張時，甲店 1.5n、乙店 120＋0.8n，乙便宜要 0.7n＞120，n＞171.4，所以 172～199 張選乙便宜；'
       '200 張以上甲店變成 1.2n，乙便宜要 0.4n＞120，n＞300，所以要 301 張以上乙才又便宜。'
       '180 張：甲 270 元、乙 264 元，乙便宜。({d0}) 250 張：甲 300 元、乙 320 元，甲便宜；({d1}) 300 張：兩家都是 360 元，一樣貴，不是「便宜」；({d2}) 160 張：甲 240 元、乙 248 元，甲便宜。'
       '這題的陷阱是忽略「滿 200 張全部降價」，以為張數越多乙一定越划算。',
       check=(180 in cheaperB, [250 in cheaperB, 300 in cheaperB, 160 in cheaperB]))


# 9  # L3
def fig_garden():
    fig, ax = blank(4.4, 3.0)
    W, H, x = 20, 12, 2
    ax.add_patch(Rectangle((0, 0), W, H, facecolor='#cfe8c4', edgecolor='black', linewidth=1.4))
    ax.add_patch(Rectangle((7, 0), x, H, facecolor='#e8dcc0', edgecolor='black', linewidth=1))
    ax.add_patch(Rectangle((0, 7.5), W, x, facecolor='#e8dcc0', edgecolor='black', linewidth=1))
    ax.annotate('', xy=(0, -1.0), xytext=(W, -1.0), arrowprops=dict(arrowstyle='<->', linewidth=1))
    ax.text(W / 2, -2.3, '20 公尺', ha='center', fontsize=10)
    ax.annotate('', xy=(-1.0, 0), xytext=(-1.0, H), arrowprops=dict(arrowstyle='<->', linewidth=1))
    ax.text(-1.6, H / 2, '12 公尺', ha='right', va='center', fontsize=10)
    ax.text(8, 12.5, 'x', ha='center', fontsize=11, style='italic')
    ax.text(20.6, 8.5, 'x', va='center', fontsize=11, style='italic')
    ax.text(3.5, 3.5, '花', fontsize=10, ha='center')
    ax.text(14.5, 3.5, '花', fontsize=10, ha='center')
    ax.text(3.5, 10.6, '花', fontsize=10, ha='center')
    ax.text(14.5, 10.6, '花', fontsize=10, ha='center')
    ax.set_xlim(-6, 22)
    ax.set_ylim(-3, 13.5)
    return b.save_fig(fig, 'q09_garden.png')


# (20 − x)(12 − x) = 180 -> x² − 32x + 60 = 0
roots = [x for x in range(0, 40) if (20 - x) * (12 - x) == 180]
assert roots == [2, 30]
xv = [r for r in roots if r < 12][0]
b.item('如附圖，一塊長 20 公尺、寬 12 公尺的長方形花圃中，要鋪兩條互相垂直、寬度都是 x 公尺的步道（步道分別與花圃的邊平行），'
       '剩下的部分種花。若種花的面積是 180 平方公尺，則 x＝？',
       '2', ['30', '15/8', '3'],
       '【解析】把四塊種花區拼在一起，恰好是一個長 (20 − x)、寬 (12 − x) 的長方形，所以 (20 − x)(12 − x)＝180，'
       '展開得 x² − 32x＋60＝0，(x − 2)(x − 30)＝0，x＝2 或 30。步道寬不能超過花圃的寬 12 公尺，所以 x＝2。'
       '({d0}) 是沒有檢查答案是否合理；({d1}) 是用 240 − 20x − 12x＝180 計算，忘了兩條步道交叉的那一塊被扣了兩次；({d2}) 代入檢驗：(20 − 3)(12 − 3)＝153≠180。',
       figure=fig_garden(),
       check=(xv == 2, [30 == xv, F(15, 8) == xv, 3 == xv]))
assert (240 - 32 * F(15, 8)) == 180


# 10  # L3
def fig_tanks():
    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    ax.plot([0, 30], [120, 0], color='#1f4e79', linewidth=1.8)
    ax.plot([0, 25], [20, 120], color='#c0392b', linewidth=1.8)
    for (px, py) in ((0, 120), (10, 80)):
        ax.plot(px, py, 'o', color='#1f4e79', markersize=4)
    for (px, py) in ((0, 20), (5, 40)):
        ax.plot(px, py, 'o', color='#c0392b', markersize=4)
    ax.text(10.6, 82, '(10, 80)', fontsize=9, color='#1f4e79')
    ax.text(5.6, 34, '(5, 40)', fontsize=9, color='#c0392b')
    ax.text(27.5, 16, '甲', fontsize=11, color='#1f4e79')
    ax.text(21, 112, '乙', fontsize=11, color='#c0392b')
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 130)
    ax.set_xticks(range(0, 31, 5))
    ax.set_yticks(range(0, 121, 20))
    ax.grid(True, color='#dddddd', linewidth=0.6)
    ax.set_xlabel('時間（分鐘）', fontsize=9)
    ax.set_ylabel('水量（公升）', fontsize=9)
    ax.tick_params(labelsize=8)
    return b.save_fig(fig, 'q10_tanks.png')


ta = lambda t: 120 + F(80 - 120, 10) * t
tb = lambda t: 20 + F(40 - 20, 5) * t
teq = F(120 - 20, 4 + 4)
b.item('甲、乙兩個水桶同時開始改變水量：甲桶以固定速率排水，乙桶以固定速率注水。附圖是兩桶水量（公升）與時間（分鐘）的關係圖，'
       '圖上標出了 (10, 80) 與 (5, 40) 兩點。兩桶水量相同時是第幾分鐘？當時水量是多少公升？',
       '第 12.5 分鐘，70 公升', ['第 12.5 分鐘，60 公升', '第 10 分鐘，80 公升', '第 15 分鐘，60 公升'],
       '【解析】甲：10 分鐘從 120 降到 80，每分鐘減少 4 公升，y＝120 − 4t；乙：5 分鐘從 20 升到 40，每分鐘增加 4 公升，y＝20＋4t。'
       '120 − 4t＝20＋4t，t＝12.5，水量＝120 − 50＝70 公升。'
       '({d0}) 時間對，但水量誤取 0 與 120 的中點 60；({d1}) 是直接拿圖上標出的甲桶點 (10, 80)，那時乙桶只有 60 公升；({d2}) 第 15 分鐘甲 60 公升、乙 80 公升，並不相同。',
       figure=fig_tanks(),
       check=(ta(teq) == tb(teq) == 70 and teq == F(25, 2),
              [ta(teq) == 60, ta(10) == tb(10), ta(15) == tb(15)]))

# 11  # L4
xs = [0, 1, 2, 3]
ys = [F(1), F(12, 5), F(17, 5), F(4)]
# solve y = ax² + bx + c from the first three points
c0 = ys[0]
# a + b = y1 − c, 4a + 2b = y2 − c
aa = ((ys[2] - c0) - 2 * (ys[1] - c0)) / 2
bq = (ys[1] - c0) - aa
f11 = lambda x: aa * x * x + bq * x + c0
assert f11(3) == ys[3] and aa < 0
xv = -bq / (2 * aa)
vmax = f11(xv)
b.item('公園噴水池的一道水柱，從噴口射出後的高度 y（公尺）是水平距離 x（公尺）的二次函數。工程人員測得以下數據：\n'
       '| 水平距離 x | 0 | 1 | 2 | 3 |\n| 高度 y | 1 | 2.4 | 3.4 | 4.0 |\n這道水柱的最高點離地面多少公尺？',
       '4.2 公尺', ['4.0 公尺', '4.6 公尺', '4.4 公尺'],
       '【解析】高度每次增加 1.4、1.0、0.6，差每次少 0.4（二次函數等距取點時，相鄰差會等差變化），所以接著增加 0.2、再來 −0.2……'
       '因此 x＝4 時 y＝4.2 是最高點，之後開始下降（x＝5 時又回到 4.0，與 x＝3 對稱）。'
       '也可以設 y＝ax²＋bx＋1，代入兩點解出 y＝−0.2x²＋1.6x＋1＝−0.2(x − 4)²＋4.2。'
       '({d0}) 是以為表中最大的數就是最高點；({d1}) 是以為每次都再增加 0.6（當成一次函數）；({d2}) 是把「差的變化量 0.4」誤當成下一次的增加量（4.0＋0.4）。',
       check=(vmax == F(21, 5) and xv == 4, [vmax == 4, vmax == F(23, 5), vmax == F(22, 5)]))

# 12  # L3
a1, d = F(2), F(1, 2)
S = lambda n: n * (2 * a1 + (n - 1) * d) / 2
n12 = next(n for n in range(1, 100) if S(n) > 100)
an = a1 + (n12 - 1) * d
b.item('阿哲（虛構情境）為了準備路跑開始練習：第 1 天跑 2 公里，之後每天都比前一天多跑 0.5 公里。'
       '他在第幾天跑完時，累計的總里程第一次超過 100 公里？那一天他跑了幾公里？',
       f'第 {n12} 天，{float(an):g} 公里', [f'第 {n12} 天，{float(an + d):g} 公里', f'第 {n12 - 1} 天，{float(an - d):g} 公里', f'第 {n12 + 1} 天，{float(an + d):g} 公里'],
       '【解析】每天里程是首項 2、公差 0.5 的等差數列，前 n 天總和 Sₙ＝n[2×2＋(n − 1)×0.5]÷2。'
       'S₁₆＝16×(4＋7.5)÷2＝92（還沒超過），S₁₇＝17×(4＋8)÷2＝102（超過 100），所以是第 17 天；第 17 天跑 2＋16×0.5＝10 公里。'
       '({d0}) 是把第 n 天的里程寫成 2＋0.5n（公差的個數應是 n − 1）；({d1}) 第 16 天累計只有 92 公里；({d2}) 第 18 天已經不是「第一次」超過。',
       check=((n12, an) == (17, 10), [(n12, an) == (n12, an + d), (n12, an) == (n12 - 1, an - d), (n12, an) == (n12 + 1, an + d)]))
assert S(16) == 92 and S(17) == 102


# 13  # L4
def reflect(P, A, B):
    (px, py), (ax_, ay), (bx, by) = P, A, B
    dx, dy = bx - ax_, by - ay
    t = ((px - ax_) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    fx, fy = ax_ + t * dx, ay + t * dy
    return (2 * fx - px, 2 * fy - py)


def fig_fold():
    fig, ax = blank(4.4, 2.8)
    A, B, C, D = (0, 0), (8, 0), (8, 4), (0, 4)
    E, Fp = (5, 0), (3, 4)
    B2 = reflect(B, E, Fp)
    ax.add_patch(Polygon([A, E, Fp, D], fill=False, linewidth=1.5))
    ax.add_patch(Polygon([E, B, C, Fp], fill=False, linewidth=1, linestyle=':', edgecolor='#888888'))
    ax.add_patch(Polygon([E, B2, A, Fp], facecolor='#f2e6c9', edgecolor='black', linewidth=1.5, alpha=0.9))
    ax.plot([E[0], Fp[0]], [E[1], Fp[1]], color='black', linewidth=1.5, linestyle='--')
    for p, s, dx, dy in ((A, 'A(C)', -0.9, -0.45), (B, 'B', 0.1, -0.4), (C, 'C', 0.1, 0.1), (D, 'D', -0.4, 0.1),
                         (E, 'E', -0.1, -0.5), (Fp, 'F', -0.1, 0.15), (B2, "B'", -0.2, -0.6)):
        ax.text(p[0] + dx, p[1] + dy, s, fontsize=11)
    ax.set_xlim(-1.2, 9)
    ax.set_ylim(min(-1.3, B2[1] - 0.8), 4.7)
    return b.save_fig(fig, 'q13_fold.png')


# E on AB with AE = EC: x² = (8 − x)² + 4²
AE = F(64 + 16, 16)
AC2 = 8 * 8 + 4 * 4
EF2 = 4 * (AE * AE - F(AC2, 4))      # EF = 2·√(AE² − (AC/2)²)
b.item('如附圖，長方形紙片 ABCD 中，AB＝8、BC＝4。將紙片沿 EF 摺疊，使 C 點與 A 點重合，B 點落在 B\'，其中 E 在 AB 上、F 在 CD 上。摺痕 EF 的長度為何？',
       '2√5', ['√5', '5', '4√5'],
       '【解析】摺疊後 EC 與 EA 重合，所以 EA＝EC。設 AE＝x，則 EB＝8 − x，在直角△EBC 中 x²＝(8 − x)²＋4²，得 x＝5。'
       '摺痕 EF 是 AC 的垂直平分線，AC＝√(8²＋4²)＝4√5，AC 中點 O 到 A 的距離是 2√5，EO＝√(5² − (2√5)²)＝√5，再由對稱 FO＝EO，所以 EF＝2√5。'
       '({d0}) 只算了一半 EO；({d1}) 是 AE 的長；({d2}) 是對角線 AC 的長，摺痕並不等於對角線。',
       figure=fig_fold(),
       check=(AE == 5 and EF2 == 20, [EF2 == 5, EF2 == 25, EF2 == 80]))


# 14  # L4
def fig_squares():
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.9))
    s1 = F(60 * 80, 140)
    c, h = 100, F(60 * 80, 100)
    s2 = c * h / (c + h)
    for ax in axes:
        ax.set_aspect('equal')
        ax.axis('off')
        ax.add_patch(Polygon([(0, 0), (80, 0), (0, 60)], fill=False, linewidth=1.5))
        ax.text(40, -7, '80 公分', ha='center', fontsize=9)
        ax.text(-4, 30, '60 公分', ha='right', va='center', fontsize=9)
        ax.set_xlim(-22, 85)
        ax.set_ylim(-14, 64)
    s = float(s1)
    axes[0].add_patch(Rectangle((0, 0), s, s, facecolor='#cfe2f3', edgecolor='black', linewidth=1.2))
    axes[0].text(40, 56, '（甲）', fontsize=10)
    # square on the hypotenuse 3x + 4y = 240: the opposite side lies on 3x + 4y = 240 − 5s
    s = float(s2)
    k = 240 - 5 * s
    P4, P3 = (k / 3, 0.0), (0.0, k / 4)                 # on the two legs
    P1 = (P4[0] + 0.6 * s, P4[1] + 0.8 * s)             # pushed onto the hypotenuse
    P2 = (P3[0] + 0.6 * s, P3[1] + 0.8 * s)
    for P in (P1, P2):
        assert abs(3 * P[0] + 4 * P[1] - 240) < 1e-9
    axes[1].add_patch(Polygon([P1, P2, P3, P4], facecolor='#cfe2f3', edgecolor='black', linewidth=1.2))
    axes[1].text(40, 56, '（乙）', fontsize=10)
    return b.save_fig(fig, 'q14_squares.png')


s1 = F(60 * 80, 60 + 80)                     # corner square: s/60 + s/80 = 1
hyp, alt = 100, F(60 * 80, 100)
s2 = hyp * alt / (hyp + alt)                 # square on hypotenuse
best = max(s1, s2)
b.item('木工師傅有一塊直角三角形木板，兩股長分別是 60 公分與 80 公分。他想從木板上切下一塊最大的正方形，考慮兩種放法（如附圖）：'
       '（甲）正方形的一個角放在直角處，兩邊貼著兩股；（乙）正方形的一邊貼著斜邊。兩種放法中，較大的正方形邊長為多少公分？',
       fs(best) + ' 公分', [fs(s2) + ' 公分', '30 公分', '40 公分'],
       '【解析】（甲）設邊長 s，正方形上方剩下的小直角三角形與原三角形相似：(60 − s)/60＝s/80，得 140s＝4800，s＝240/7≈34.3。'
       '（乙）斜邊 100，斜邊上的高＝60×80÷100＝48。正方形與直角頂點之間的小三角形（底是正方形的一邊 s、高是 48 − s）與原三角形相似，對應「底：高」相同：s/100＝(48 − s)/48，得 s＝4800/148＝1200/37≈32.4。'
       '比較後（甲）較大，邊長 240/7 公分。'
       '({d0}) 是（乙）的結果，比較小；({d1}) 是把正方形邊長誤當成較短股的一半；({d2}) 是較長股的一半，這樣的正方形放不進三角形（40/60＋40/80＞1）。',
       figure=fig_squares(),
       check=(best == F(240, 7) and s1 > s2, [s2 == best, best == 30, best == 40]))


# 15  # L4
def fig_tangent():
    fig, ax = blank(4.6, 2.9)
    th = math.radians(56)
    O, A, B = (0, 0), (-1, 0), (1, 0)
    C = (math.cos(th), math.sin(th))
    P = (1 / math.cos(th), 0)
    ax.add_patch(Circle(O, 1, fill=False, linewidth=1.5))
    ax.plot([A[0], P[0] + 0.15], [0, 0], color='black', linewidth=1.3)
    ax.plot([A[0], C[0]], [A[1], C[1]], color='black', linewidth=1.3)
    ax.plot([O[0], C[0]], [O[1], C[1]], color='black', linewidth=1.0)
    ext = 0.35
    d = (P[0] - C[0], P[1] - C[1])
    L = math.hypot(*d)
    ax.plot([C[0] - d[0] / L * ext, P[0]], [C[1] - d[1] / L * ext, P[1]], color='black', linewidth=1.3)
    ax.add_patch(Arc(P, 0.5, 0.5, theta1=180 - 34, theta2=180, linewidth=1.1))
    ax.text(P[0] - 0.42, 0.05, '34°', fontsize=9)
    for p, s, dx, dy in ((A, 'A', -0.17, -0.05), (B, 'B', 0.02, -0.15), (C, 'C', 0.0, 0.07), (O, 'O', -0.05, -0.16), (P, 'P', 0.03, -0.15)):
        ax.text(p[0] + dx, p[1] + dy, s, fontsize=11)
    ax.plot(0, 0, 'o', color='black', markersize=3)
    ax.set_xlim(-1.25, P[0] + 0.3)
    ax.set_ylim(-1.1, 1.15)
    return b.save_fig(fig, 'q15_tangent.png')


angP = 34
angCOB = 90 - angP                 # OC ⊥ PC
angCAB = F(angCOB, 2)
b.item('如附圖，AB 是圓 O 的直徑，C 是圓上一點，過 C 的切線與 AB 的延長線交於 P 點。若 ∠P＝34°，則 ∠CAB 的度數為何？',
       '28°', ['56°', '34°', '62°'],
       '【解析】切線垂直於過切點的半徑，所以 ∠OCP＝90°。在△OCP 中，∠COP＝180° − 90° − 34°＝56°。'
       '∠CAB 是弧 CB 所對的圓周角，∠COB（即 ∠COP）是同弧所對的圓心角，所以 ∠CAB＝56°÷2＝28°。'
       '({d0}) 是圓心角 ∠COB，忘了除以 2；({d1}) 是誤以為 ∠CAB＝∠P；({d2}) 是 90° − 28°，是 ∠ABC 的度數（AB 為直徑，∠ACB＝90°）。',
       figure=fig_tangent(),
       check=(angCAB == 28, [angCAB == 56, angCAB == 34, angCAB == 62]))


# 16  # L4
def fig_box():
    fig, ax = blank(4.2, 3.0)
    l, w, h = 5.0, 4.0, 3.0
    k = (0.55, 0.42)                     # oblique depth direction per unit of width
    dxy = (w * k[0], w * k[1])
    A, B, C, D = (0, 0), (l, 0), (l + dxy[0], dxy[1]), (dxy[0], dxy[1])
    up = lambda p: (p[0], p[1] + h)
    E, Fp, G, H = up(A), up(B), up(C), up(D)
    ax.add_patch(Polygon([E, Fp, G, H], facecolor='#f6e7a8', edgecolor='none'))
    ax.text((E[0] + G[0]) / 2, (E[1] + G[1]) / 2 - 0.1, '頂面（有膠水）', ha='center', fontsize=8.5)
    solid = [(A, B), (B, C), (E, Fp), (Fp, G), (G, H), (H, E), (A, E), (B, Fp), (C, G)]
    dashed = [(A, D), (D, C), (D, H)]
    for p, q in solid:
        ax.plot([p[0], q[0]], [p[1], q[1]], color='black', linewidth=1.5)
    for p, q in dashed:
        ax.plot([p[0], q[0]], [p[1], q[1]], color='black', linewidth=1, linestyle='--')
    ax.plot([-1.2, l + dxy[0] + 0.6], [-0.05, -0.05], color='#888888', linewidth=0.8)
    ax.plot(*A, 'o', color='#c0392b', markersize=5)
    ax.plot(*G, 'o', color='#c0392b', markersize=5)
    ax.text(A[0] - 0.35, A[1] - 0.45, 'A', fontsize=12)
    ax.text(G[0] + 0.1, G[1] + 0.05, 'G', fontsize=12)
    ax.text(l / 2, -0.55, '5 公分', ha='center', fontsize=9)
    ax.text(l + dxy[0] / 2 + 0.15, dxy[1] / 2 - 0.3, '4 公分', fontsize=9)
    ax.text(-0.25, h / 2, '3 公分', ha='right', fontsize=9)
    ax.set_xlim(-1.4, l + dxy[0] + 0.7)
    ax.set_ylim(-0.9, h + dxy[1] + 0.4)
    return b.save_fig(fig, 'q16_box.png')


l, w, h = 5, 4, 3
# all two-face unfoldings from A (bottom-front-left) to G (top-back-right); faces used in each
unfold = {('front', 'top'): (l ** 2 + (h + w) ** 2), ('left', 'top'): (w ** 2 + (h + l) ** 2),
          ('front', 'right'): ((l + w) ** 2 + h ** 2), ('left', 'back'): ((w + l) ** 2 + h ** 2),
          ('bottom', 'back'): (l ** 2 + (w + h) ** 2), ('bottom', 'right'): (w ** 2 + (l + h) ** 2)}
allowed = [v for faces, v in unfold.items() if 'top' not in faces and 'bottom' not in faces]
shortest = min(allowed)
free = min(unfold.values())
b.item('如附圖，一個長方體紙盒的長、寬、高分別是 5 公分、4 公分、3 公分，平放在桌上（螞蟻不能爬到盒子底面）。盒子的頂面剛塗了膠水，螞蟻也不能經過頂面。'
       '一隻螞蟻從頂點 A 沿著盒子的表面爬到頂點 G，牠爬行的最短路徑長是多少公分？',
       f'√{shortest} 公分', [f'√{free} 公分', '√80 公分', '√50 公分'],
       '【解析】底面貼著桌子、頂面有膠水，螞蟻只能在四個側面上爬。G 是頂面的一個角，也在後面與右側面上，所以可以只走側面到達。'
       '把「前面＋右側面」（或「左側面＋後面」）展開成一個長 5＋4＝9、高 3 的長方形，A 與 G 是這個長方形的對角，最短路徑＝√(9²＋3²)＝√90。'
       '({d0}) √74 是經過頂面的走法（前面＋頂面展開，√[5²＋(3＋4)²]），在沒有限制時最短，但本題頂面不能走；'
       '({d1}) √80 是「左側面＋頂面」的走法，也經過頂面；({d2}) √50 是長方體的對角線 √(5²＋4²＋3²)，穿過盒子內部，螞蟻爬不到。',
       figure=fig_box(),
       check=(shortest == 90 and free == 74, [shortest == free, shortest == 80, shortest == 50]))

# 17  # L4
# 甲 apex, 乙丙 base 8, legs 5: height 3. O on the axis at signed height y above the base midpoint: 16 + y² = (3 − y)²
y17 = F(9 - 16, 6)
R17 = 3 - y17
outside = y17 < 0
assert 16 + y17 ** 2 == R17 ** 2 and 5 * 5 + 5 * 5 < 8 * 8           # obtuse at 甲
r17 = F(2 * (8 * 3 // 2), 5 + 5 + 8)                                  # inradius = 2·area / perimeter
b.item('甲、乙、丙三個村莊之間的直線距離：甲村到乙村 5 公里、甲村到丙村 5 公里、乙村到丙村 8 公里。鄉公所要蓋一座水塔，使它到三個村莊的距離都相等。'
       '關於這座水塔，下列敘述何者正確？',
       f'到每村 {fs(R17)} 公里，位在三村連成的三角形外部',
       [f'到每村 {fs(R17)} 公里，位在三村連成的三角形內部', '到每村 4 公里，位在乙丙兩村連線的中點', f'到每村 {fs(r17)} 公里，位在三村連成的三角形內部'],
       '【解析】到三個頂點距離相等的點是外心，在乙丙的垂直平分線上，也就是過甲且垂直乙丙的對稱軸上。乙丙中點 M 到甲的距離＝√(5² − 4²)＝3。'
       '設外心 O 在 M「往甲的方向」的距離為 y（y＜0 表示在另一側），則 O 到乙村的距離平方＝4²＋y²、O 到甲村的距離＝3 − y，兩者相等得 16＋y²＝9 − 6y＋y²，y＝−7/6，'
       '所以 O 在乙丙連線的另一側（三角形外部），到每村 3＋7/6＝25/6 公里。這是因為 5²＋5²＜8²，∠甲是鈍角，鈍角三角形的外心在外部。'
       '({d0}) 距離對，但鈍角三角形的外心不在內部；({d1}) 是把「直角三角形外心在斜邊中點」套用到這個三角形，但中點到甲村只有 3 公里，不等於 4 公里；'
       '({d2}) 是內切圓半徑（面積 12×2÷周長 18），那是到三「邊」距離相等的內心。',
       check=(outside and R17 == F(25, 6), [not outside, R17 == 4, R17 == r17]))

# 18  # L3
def quartiles(xs):
    s = sorted(xs)
    n = len(s)

    def med(t):
        m = len(t)
        return F(t[m // 2]) if m % 2 else F(t[m // 2 - 1] + t[m // 2], 2)
    lower, upper = s[:n // 2], s[(n + 1) // 2:]
    return med(lower), med(s), med(upper)


data18 = [9, 3, 12, 6, 18, 8, 6, 11, 5, 14, 10, 6]
q1, q2, q3 = quartiles(data18)
mean18 = F(sum(data18), len(data18))
data18b = sorted(data18)[:-1]
_, q2b, _ = quartiles(data18b)
b.item('某班（虛構情境）調查 12 位同學一週的課外閱讀時數（小時），結果如下：\n| 座號 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |\n| 時數 | 9 | 3 | 12 | 6 | 18 | 8 | 6 | 11 | 5 | 14 | 10 | 6 |\n'
       '關於這筆資料，下列敘述何者正確？',
       '平均數大於中位數', ['第三四分位數是 12 小時', '四分位距是 15 小時', '刪去最大值 18 後，中位數不變'],
       '【解析】由小到大：3、5、6、6、6、8、9、10、11、12、14、18。平均數＝108÷12＝9，中位數＝(8＋9)÷2＝8.5，所以平均數大於中位數。'
       '({d0}) 後半 6 筆是 9、10、11、12、14、18，第三四分位數是其中位數 (11＋12)÷2＝11.5，不是 12；'
       '({d1}) 第一四分位數＝(6＋6)÷2＝6，四分位距＝11.5 − 6＝5.5，15 是全距 18 − 3；'
       '({d2}) 刪去 18 後剩 11 筆，中位數變成第 6 筆的 8，改變了。',
       check=(mean18 > q2, [q3 == 12, q3 - q1 == 15, q2b == q2]))
assert (q1, q2, q3) == (6, F(17, 2), F(23, 2)) and mean18 == 9

# 19  # L3
rolls = [(i, j) for i in range(1, 7) for j in range(1, 7)]
P_ = lambda cond: F(sum(1 for r in rolls if cond(*r)), 36)
jia19 = P_(lambda i, j: i == 6 or j == 6) == F(1, 3)
yi19 = P_(lambda i, j: i == j) == P_(lambda i, j: i + j == 7)
b.item('同時擲兩顆公正的骰子。甲、乙兩人提出以下看法：\n【甲】至少有一顆骰子出現 6 點的機率是 1/3\n【乙】兩顆骰子點數相同的機率，等於兩顆骰子點數和為 7 的機率\n對於甲、乙兩人的看法，下列判斷何者正確？',
       '甲錯誤，乙正確', ['甲、乙皆正確', '甲正確，乙錯誤', '甲、乙皆錯誤'],
       '【解析】兩顆骰子共有 6×6＝36 種結果，機會相等。'
       '甲：至少一顆 6 點的有 (6,1)～(6,6) 6 種、(1,6)～(5,6) 5 種，共 11 種（(6,6) 只能算一次），機率 11/36，不是 1/3＝12/36，甲錯誤。'
       '乙：點數相同有 (1,1)～(6,6) 6 種；點數和為 7 有 (1,6)、(2,5)、(3,4)、(4,3)、(5,2)、(6,1) 6 種，兩者機率都是 6/36，乙正確。'
       '({d0}) 與 ({d1}) 是把甲算成 1/6＋1/6＝1/3，重複計算了 (6,6)；({d2}) 是把點數和為 7 只算成 3 種（忽略 (1,6) 與 (6,1) 是不同結果）。',
       check=((not jia19) and yi19, [jia19 and yi19, jia19 and not yi19, (not jia19) and (not yi19)]))

# 20  # L4
base, depth0, edge = 40 * 30, 12, 20
water = base * depth0
h_new = F(water, base - edge * edge)
assert h_new < edge                       # the cube is not fully under water
rise = h_new - depth0
b.item('一個長方體水箱，內部底面長 40 公分、寬 30 公分，裡面的水深 12 公分。把一個邊長 20 公分的正立方體鐵塊平放到水箱底部（水沒有溢出），'
       '水面會上升多少公分？',
       f'{fs(rise)} 公分', ['20/3 公分', '18 公分', '10 公分'],
       '【解析】鐵塊高 20 公分，比原來的水深高，要先判斷會不會被淹沒。放入後水只能占「水箱底面 − 鐵塊底面」＝1200 − 400＝800 平方公分的底面積，'
       '水量 1200×12＝14400 立方公分不變，新水深＝14400÷800＝18 公分＜20 公分，鐵塊沒有被淹沒，所以水面上升 18 − 12＝6 公分。'
       '({d0}) 是以為鐵塊完全沉入水中，用鐵塊體積 8000÷1200 計算；({d1}) 是新的水深，不是上升的高度；({d2}) 是用鐵塊整個體積 8000 除以 800，但鐵塊在水面以上的部分沒有排開水。',
       check=(rise == 6, [rise == F(20, 3), rise == 18, rise == 10]))

# 21-22  題組: public bike fees (fictional)
b.group(21, 22, '某市公共自行車（虛構情境）的租借收費規則如下：\n'
        '| 單次租借的使用時間 | 費率 |\n| 2 小時以內（含 2 小時）的部分 | 每 30 分鐘 10 元 |\n| 超過 2 小時到 4 小時（含）的部分 | 每 30 分鐘 20 元 |\n| 超過 4 小時的部分 | 每 30 分鐘 40 元 |\n'
        '說明：使用時間以 30 分鐘為一個計費單位，不足 30 分鐘以 30 分鐘計；登記為會員者，每次租借的第一個 30 分鐘免費（其餘照上表計算）。')


def bike(minutes, member=True):
    n = -(-minutes // 30)
    rate = lambda k: 10 if k <= 4 else (20 if k <= 8 else 40)
    return sum(rate(k) for k in range(2 if member else 1, n + 1))


v21 = bike(160)
wrong_all10 = 10 * (-(-160 // 30) - 1)
wrong_free_expensive = 10 * 4 + 20 * 1          # free block taken out of the 20-yuan part
# 21  # L3
b.item('會員小柏（虛構情境）某次租借騎了 2 小時 40 分鐘，他這次要付多少元？',
       f'{v21} 元', [f'{bike(160, member=False)} 元', f'{wrong_all10} 元', f'{wrong_free_expensive} 元'],
       '【解析】2 小時 40 分鐘＝160 分鐘，不足 30 分鐘以 30 分鐘計，共 6 個計費單位。前 4 個單位在 2 小時以內，每個 10 元，但第 1 個免費，付 3×10＝30 元；'
       '第 5、6 個單位在 2～4 小時之間，每個 20 元，付 40 元。合計 70 元。'
       '({d0}) 是忘了會員第一個 30 分鐘免費；({d1}) 是全部都用每 30 分鐘 10 元計算，沒注意超過 2 小時的費率較高；({d2}) 是把免費的 30 分鐘扣在較貴的時段，但免費的是「第一個」30 分鐘。',
       check=(v21 == 70, [bike(160, member=False) == v21, wrong_all10 == v21, wrong_free_expensive == v21]))

# 22  # L4
c22 = {'4 小時 20 分鐘': 260, '4 小時': 240, '4 小時 40 分鐘': 280, '7 小時 45 分鐘': 465}
b.item('會員小芳（虛構情境）某次租借付了 150 元。她這次騎乘的時間可能是下列何者？',
       '4 小時 20 分鐘', ['4 小時', '4 小時 40 分鐘', '7 小時 45 分鐘'],
       '【解析】會員騎滿 4 小時（8 個單位）要付：前 2 小時 3×10＝30 元（第 1 個免費）＋2～4 小時 4×20＝80 元＝110 元。'
       '150 − 110＝40 元，正好是超過 4 小時後的 1 個單位，所以共 9 個單位，騎乘時間超過 4 小時、不超過 4 小時 30 分鐘，4 小時 20 分鐘符合。'
       '({d0}) 4 小時只要 110 元；({d1}) 4 小時 40 分鐘是 10 個單位，要 190 元；({d2}) 是把 150 元全部用每 30 分鐘 10 元回推（15 個單位再加免費 1 個），忽略了費率會隨時間提高，7 小時 45 分鐘其實要 430 元。',
       check=(bike(c22['4 小時 20 分鐘']) == 150, [bike(c22[k]) == 150 for k in ('4 小時', '4 小時 40 分鐘', '7 小時 45 分鐘')]))
assert bike(240) == 110 and bike(280) == 190 and bike(465) == 430

# 23-25  題組: 2026 FIFA World Cup format (real)
b.group(23, 25, '2026 年國際足總世界盃（FIFA World Cup）於 2026 年 6 月 11 日至 7 月 19 日由加拿大、墨西哥、美國三國合辦，參賽隊伍首度由 32 隊擴大為 48 隊。賽制如下：\n'
        '1. 小組賽：48 隊分成 12 組，每組 4 隊進行單循環（同組每兩隊都比賽一場）。每場勝隊得 3 分、敗隊得 0 分，若平手兩隊各得 1 分。\n'
        '2. 各組依積分排出第 1～4 名（積分相同時再依對戰成績、淨勝球等規則排名）。各組前 2 名，加上 12 個小組第 3 名中成績最好的 8 隊，共 32 隊晉級。\n'
        '3. 32 強起為單淘汰賽（每場一定分出勝負，敗隊淘汰），直到冠軍戰；另外，四強賽的兩支敗隊再比賽一場爭奪季軍。')

# 23  # L3
group_games = 12 * (4 * 3 // 2)
ko = 32 - 1 + 1
total23 = group_games + ko
b.item('依上述賽制，這屆世界盃全部共有幾場比賽？',
       f'{total23} 場', ['103 場', '105 場', '176 場'],
       '【解析】小組賽每組 4 隊兩兩比賽 1 場，共 4×3÷2＝6 場，12 組共 72 場。單淘汰賽每場淘汰 1 隊，32 隊要淘汰到只剩冠軍，須淘汰 31 隊，共 31 場，再加季軍戰 1 場，共 32 場。'
       '全部 72＋32＝104 場。'
       '({d0}) 是忘了季軍戰；({d1}) 是把淘汰賽算成 32 場再加季軍戰（32 隊只需淘汰 31 隊）；({d2}) 是把小組賽算成每隊 3 場 × 48 隊＝144 場，每場被兩隊各算一次而重複計算。',
       check=(total23 == 104, [total23 == 103, total23 == 105, total23 == 144 + 32]))

# all outcomes of one group: 6 matches, each W / D / L for the first-listed team
matches = [(i, j) for i in range(4) for j in range(i + 1, 4)]
tables = []
for res in product((0, 1, 2), repeat=6):
    pts = [0] * 4
    for (i, j), r in zip(matches, res):
        if r == 0:
            pts[i] += 3
        elif r == 2:
            pts[j] += 3
        else:
            pts[i] += 1
            pts[j] += 1
    tables.append(sorted(pts, reverse=True))
third_max = max(t[2] for t in tables)
second_min = min(t[1] for t in tables)

# 24  # L4
b.item('在某一組的小組賽中，排名第 3 的隊伍，積分最多可能是幾分？',
       f'{third_max} 分', ['4 分', '7 分', '5 分'],
       '【解析】6 場比賽中，每場分出勝負時兩隊共得 3 分，平手時共得 2 分，所以一組 4 隊的積分總和最多 6×3＝18 分。'
       '若第 3 名有 7 分以上，則第 1、2 名也都至少 7 分，三隊合計至少 21 分＞18，不可能。6 分則做得到：例如 A 勝 B、B 勝 C、C 勝 A，三隊又都贏 D，則 A、B、C 都是 6 分，依淨勝球排名，第 3 名仍有 6 分。'
       '所以最多 6 分。({d0}) 是以為第 3 名只能「一勝一和」；({d1}) 忽略了全組積分總和的限制；({d2}) 是 1 勝 2 和的積分，但 6 分也做得到，5 分並不是最多。',
       check=(third_max == 6, [third_max == 4, third_max == 7, third_max == 5]))

# 25  # L5
b.item('在某一組的小組賽中，排名第 2 的隊伍，積分最少可能是幾分？',
       f'{second_min} 分', ['3 分', '1 分', '0 分'],
       '【解析】除了第 1 名以外的三隊，彼此之間還有 3 場比賽，這 3 場至少產生 3×2＝6 分（全部平手時最少）。若第 2 名只有 1 分以下，則第 2、3、4 名三隊合計最多 3 分，'
       '但他們彼此的 3 場就至少產生 6 分，矛盾，所以第 2 名至少 2 分。2 分做得到：甲隊贏其他三隊得 9 分，乙、丙、丁彼此三場都平手，各得 2 分，第 2 名就是 2 分。'
       '({d0}) 是想到「6 場全部平手，每隊 3 分」的情形，但那不是最少；({d1}) 與 ({d2}) 會使第 2～4 名三隊合計不到 6 分，與他們彼此的三場比賽至少產生 6 分矛盾。',
       check=(second_min == 2, [second_min == 3, second_min == 1, second_min == 0]))

b.write()
