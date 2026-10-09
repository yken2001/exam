"""AI-4 英聽（會考水準）: build src/data/ai/ai4_listening.json and the pictures of part 1.

Parts as in the real test: 辨識句意 1-3 (three pictures, drawn here), 基本問答
4-11, 言談理解 12-21. Each item is written with its correct option first;
SetBuilder places the options by TARGET, and a picture item's panels are drawn
in that final order (b.arrange). Level tags (# L1..L4) follow SPEC_AI2_AI3.md
(AI-4: about L1 10%, L2 40%, L3 40%, L4 10%, mean about 2.5, as in 會考 114-115).
  PYTHONIOENCODING=utf-8 python tools/ai_sets/ai4_listening.py
  python tools/gen_audio.py ai4
"""
import os
import sys

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle, Wedge

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SetBuilder, spread_target

plt.rcParams['font.family'] = 'Microsoft JhengHei'

TOPICS = [
    'Netflix 動畫電影 KPop Demon Hunters（2025/6 上線）成為 Netflix 史上觀看次數最多的電影：https://www.koreajoongangdaily.com/entertainment/kpop-demon-hunters-becomes-most-watched-film-on-netflix-with-236-million-views/12114967',
    '主題曲 "Golden"（HUNTR/X）2025 年登上 Billboard Hot 100 第一名，2026/2/1 獲葛萊美最佳影視歌曲獎，為第一首得到葛萊美獎的 K-pop 歌曲：https://au.variety.com/2026/music/global/kpop-demons-hunters-grammy-win-32586/',
    '撐竿跳 Armand Duplantis 2025/9/15 在東京世界田徑錦標賽跳過 6.30 公尺，第 14 次刷新世界紀錄並衛冕：https://www.news4jax.com/sports/2025/09/15/duplantis-breaks-pole-vault-world-record-for-14th-time-to-capture-third-world-championship-title/',
    'Labubu 熱潮（2025）：香港藝術家龍家昇（Kasing Lung）創作，泡泡瑪特（Pop Mart）以盲盒販售，打開才知道是哪一款，各地排隊搶購：https://www.nbcnews.com/pop-culture/pop-culture-news/labubu-craze-viral-lines-pop-mart-stores-rcna203213',
    '2026 台灣燈會在嘉義（3/3–3/15），2026 為馬年，但主燈「光沐－世界的阿里山」以阿里山神木為意象、高約 21 公尺、每半小時展演；馬年元素在小提燈「喔熊馬抵嘉」（熊騎木馬）：https://www.ctee.com.tw/news/20260109701141-430104',
    '2026 年農曆新年為 2/17，進入馬年：https://www.canada.ca/en/department-national-defence/maple-leaf/defence/2026/02/year-horse-lunar-new-year-2026.html',
    '對話中的人物、班級出遊、診所留言、電影票價、捷運公園站／湖站與河濱自行車道新聞皆為虛構情境',
]

b = SetBuilder('ai4_listening', '英聽', year=904, set_name='AI-4', title='AI-4 英語（聽力）模擬卷（會考水準）',
               note='由 AI 依心測中心英語聽力架構（辨識句意 3 題、基本問答 8 題、言談理解 10 題，三選一）編寫，非會考真題；'
                    '難度比照近年會考（平均約 2.5 級）：對話與廣播長度和會考相當，含計畫改變、言外之意、慣用語、簡單金額計算，'
                    '誘答選項多用錄音中出現過的字詞或別的細節。第一部分的圖片由程式繪製（tools/ai_sets/ai4_listening.py），語音以錄音稿合成（非會考原音）。',
               target=spread_target(21, 3, 904), difficulty='會考水準', topics=TOPICS)


# ------------------------------------------------------------ drawing helpers
def frame(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.add_patch(Rectangle((0.01, 0.01), 0.98, 0.98, fill=False, linewidth=1, edgecolor='#999999'))


def panels(draws, name):
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.2))
    for ax, label, draw in zip(axes, 'ABC', draws):
        frame(ax)
        draw(ax)
        ax.text(0.5, -0.08, f'({label})', ha='center', fontsize=13)
    return b.save_fig(fig, name)


def apple(ax, x, y):
    ax.add_patch(Circle((x, y), 0.065, facecolor='#d62828', edgecolor='#7a1010', linewidth=1.2, zorder=3))
    ax.plot([x, x + 0.01], [y + 0.06, y + 0.10], color='#5a3a1a', linewidth=2, zorder=4)
    ax.add_patch(Ellipse((x + 0.035, y + 0.085), 0.045, 0.022, angle=25, color='#2e8b3a', zorder=4))


def banana(ax, x, y):
    """a crescent: thick in the middle, pointed at both ends"""
    import numpy as np
    R = 0.10
    a = np.radians(np.linspace(202, 338, 40))
    outer = [(x + R * np.cos(t), y + R + R * np.sin(t)) for t in a]
    lift = 0.032 * np.sin(np.linspace(0, np.pi, len(a)))
    inner = [(px, py + h) for (px, py), h in zip(outer[::-1], lift[::-1])]
    ax.add_patch(Polygon(outer + inner, closed=True, facecolor='#f7d117', edgecolor='#a88a00', linewidth=1.3, zorder=3))
    ax.add_patch(Circle(outer[0], 0.012, color='#5a3a1a', zorder=4))


def fruit_plate(apples, bananas):
    """a plate with apples (back row) and bananas (front row) on it"""
    def draw(ax):
        ax.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96, color='#f4efe6'))
        ax.add_patch(Ellipse((0.5, 0.42), 0.88, 0.62, facecolor='white', edgecolor='#888888', linewidth=2, zorder=1))
        ax.add_patch(Ellipse((0.5, 0.42), 0.70, 0.46, fill=False, edgecolor='#cccccc', linewidth=1, zorder=2))
        xs = [0.5] if apples == 1 else [0.5 + (k - (apples - 1) / 2) * 0.16 for k in range(apples)]
        for x in xs:
            apple(ax, x, 0.55)
        xs = [0.5] if bananas == 1 else [0.5 + (k - (bananas - 1) / 2) * 0.25 for k in range(bananas)]
        for x in xs:
            banana(ax, x, 0.22)
    return draw


def chair(ax, x0):
    c = '#8a5a2b'
    ax.add_patch(Rectangle((x0, 0.40), 0.24, 0.04, color=c))           # seat
    ax.add_patch(Rectangle((x0, 0.44), 0.035, 0.36, color=c))          # back
    ax.add_patch(Rectangle((x0, 0.12), 0.03, 0.28, color=c))
    ax.add_patch(Rectangle((x0 + 0.21, 0.12), 0.03, 0.28, color=c))


def table(ax, x0):
    c = '#6b4a2b'
    ax.add_patch(Rectangle((x0, 0.52), 0.44, 0.05, color=c))          # top
    ax.add_patch(Rectangle((x0 + 0.03, 0.12), 0.035, 0.40, color=c))
    ax.add_patch(Rectangle((x0 + 0.375, 0.12), 0.035, 0.40, color=c))


def cat(ax, x, y):
    """a sleeping cat lying on y, centred at x"""
    col = '#f0a040'
    ax.add_patch(Ellipse((x, y + 0.05), 0.17, 0.10, facecolor=col, edgecolor='#8a5010', linewidth=1.2, zorder=5))
    ax.add_patch(Circle((x + 0.085, y + 0.075), 0.045, facecolor=col, edgecolor='#8a5010', linewidth=1.2, zorder=6))
    for dx in (0.06, 0.105):
        ax.add_patch(Polygon([(x + dx - 0.02, y + 0.105), (x + dx + 0.02, y + 0.105), (x + dx, y + 0.145)],
                             facecolor=col, edgecolor='#8a5010', linewidth=1.0, zorder=6))
    for dx in (0.068, 0.102):                                           # closed eyes
        ax.plot([dx + x - 0.01, dx + x + 0.01], [y + 0.075, y + 0.075], color='black', linewidth=1.2, zorder=7)
    ax.plot([x - 0.08, x - 0.11, x - 0.06], [y + 0.04, y + 0.01, y + 0.005], color='#8a5010', linewidth=3, zorder=4)
    ax.text(x + 0.13, y + 0.17, 'z z', fontsize=8, style='italic', zorder=7)


def ball(ax, x, y):
    ax.add_patch(Circle((x, y + 0.045), 0.045, facecolor='#2e86de', edgecolor='#123d6b', linewidth=1.2, zorder=5))
    ax.plot([x - 0.045, x + 0.045], [y + 0.045, y + 0.045], color='white', linewidth=2, zorder=6)


def room(cat_at, ball_at):
    """chair on the left, table on the right; cat_at / ball_at: 'on chair', 'under table', 'on table'"""
    spots = {'on chair': (0.13, 0.44), 'under table': (0.74, 0.12), 'on table': (0.74, 0.57)}

    def draw(ax):
        ax.add_patch(Rectangle((0.02, 0.02), 0.96, 0.10, color='#d9c7a7'))   # floor
        chair(ax, 0.06)
        table(ax, 0.52)
        cx, cy = spots[cat_at]
        cat(ax, cx, cy)
        bx, by = {'on chair': (0.19, 0.44), 'under table': (0.70, 0.12), 'on table': (0.74, 0.57)}[ball_at]
        ball(ax, bx, by)
    return draw


def sign(rows):
    """a museum opening-hours sign; rows: [(day, hours), ...]"""
    def draw(ax):
        ax.add_patch(Rectangle((0.08, 0.06), 0.84, 0.88, facecolor='#fffdf5', edgecolor='#2c3e50', linewidth=2.5))
        ax.add_patch(Rectangle((0.08, 0.78), 0.84, 0.16, color='#2c3e50'))
        ax.text(0.5, 0.86, 'CITY MUSEUM', ha='center', va='center', fontsize=10, color='white', weight='bold')
        ax.text(0.5, 0.72, 'Opening Hours', ha='center', va='center', fontsize=8, style='italic')
        for k, (day, hours) in enumerate(rows):
            y = 0.58 - 0.13 * k
            ax.text(0.14, y, day, ha='left', va='center', fontsize=8.5, weight='bold')
            ax.text(0.88, y, hours, ha='right', va='center', fontsize=8.5,
                    color='#c0392b' if hours == 'Closed' else 'black', weight='bold' if hours == 'Closed' else 'normal')
            ax.plot([0.13, 0.87], [y - 0.065, y - 0.065], color='#dddddd', linewidth=0.8)
    return draw


FULL, EARLY = '9 a.m. - 5 p.m.', '9 a.m. - 4 p.m.'


# ------------------------------------------------------------ item helpers
def heard(transcript):
    lines = []
    for w, t in transcript:
        lines.append(t if w == 'N' else ('Question: ' + t if w == 'Q' else f'{w}: {t}'))
    return '\n'.join(lines)


def picture(sentence, correct, distractors, name, zh, why):
    fig = panels(b.arrange(correct, distractors), name)
    b.item('', None, [None, None], f'【聽力稿】{sentence}\n【中譯】{zh}\n【解析】{why}', figure=fig,
           transcript=[['N', sentence]], picture=True)


def text(transcript, correct, distractors, zh, why, check=None):
    b.item('', correct, distractors, f'【聽力稿】{heard(transcript)}\n【中譯】{zh}\n【解析】{why}',
           transcript=transcript, check=check)


# ============================================================ 第一部分：辨識句意
# Q1  L1  counting: three apples and two bananas
picture('There are three apples and two bananas on the plate.',
        fruit_plate(3, 2), [fruit_plate(2, 3), fruit_plate(3, 3)], 'q01.png',
        '盤子上有三顆蘋果和兩根香蕉。',
        '要同時符合「三顆蘋果」和「兩根香蕉」。({c}) 三顆蘋果、兩根香蕉，完全符合；'
        '({d0}) 兩顆蘋果、三根香蕉，數量剛好顛倒；({d1}) 蘋果是三顆，但香蕉有三根。')

# Q2  L2  two positions: on the chair / under the table
picture('The cat is sleeping on the chair, and the ball is under the table.',
        room('on chair', 'under table'), [room('under table', 'on chair'), room('on chair', 'on table')], 'q02.png',
        '貓在椅子上睡覺，球在桌子底下。',
        '要同時符合兩個位置：貓「在椅子上」（on the chair），球「在桌子下」（under the table）。'
        '({c}) 貓睡在椅子上、球在桌子底下；({d0}) 貓和球的位置顛倒了，貓在桌子底下、球在椅子上；'
        '({d1}) 貓雖然在椅子上，但球在桌子「上面」，不是桌子底下。')

# Q3  L3  sign: closed on Mondays + closes early (at four) on Saturdays
picture("The museum is closed on Mondays, and on Saturdays, it closes early, at four o'clock.",
        sign([('MON', 'Closed'), ('TUE - FRI', FULL), ('SAT', EARLY), ('SUN', FULL)]),
        [sign([('MON', 'Closed'), ('TUE - FRI', EARLY), ('SAT', FULL), ('SUN', FULL)]),
         sign([('MON', FULL), ('TUE - FRI', FULL), ('SAT', EARLY), ('SUN', 'Closed')])], 'q03.png',
        '博物館星期一休館，星期六比較早關門，四點就關。',
        '兩個條件：星期一休館（closed on Mondays）；星期六提早在四點關門，其他開館日是五點關。'
        '({c}) 星期一 Closed，星期六 9 a.m.–4 p.m.，其他日子到 5 p.m.，完全符合；'
        '({d0}) 星期一休館沒錯，但四點關門的是星期二到五，星期六反而開到五點；'
        '({d1}) 星期六四點關門沒錯，但休館的是星期日，星期一有開。')

# ============================================================ 第二部分：基本問答
# Q4  L1  What time ...? -> a clock time
text([['N', 'What time does your piano lesson start?']],
     'At four thirty.', ['For about an hour.', "At my teacher's house."],
     '你的鋼琴課幾點開始？',
     'What time 問「幾點」，要回答時間點。({c})「四點半」正確。'
     '({d0}) 回答「上多久」（How long 的答案）；({d1}) 回答「在哪裡上」（Where 的答案）。')

# Q5  L2  turn down = make it quieter
text([['N', "Could you turn down the TV a little? I'm trying to study."]],
     "Sorry. I didn't know it was so loud.",
     ['Sure. Which channel do you want to watch?', 'Yes, I studied for the test last night.'],
     '你可以把電視（音量）關小聲一點嗎？我正在讀書。',
     'turn down 是「把音量調小」，對方在讀書，嫌電視太吵。({c})「抱歉，我不知道這麼大聲」適當回應。'
     '({d0}) 對方是要讀書，不是要看電視、選頻道；({d1}) 用了聽到的 study，說的卻是自己昨晚讀書，答非所問。')

# Q6  L2  current event: KPop Demon Hunters (Netflix, 2025) and its song "Golden"
text([['N', 'Have you seen KPop Demon Hunters yet? Everyone in my class is talking about it.']],
     'Yes, twice. The songs are great.',
     ["No, I've never been to Korea.", "Yes, they're talking too loudly."],
     '你看過《KPop 獵魔女團》（KPop Demon Hunters）了嗎？我們班上每個人都在討論它。',
     '對方問你「有沒有看過」這部片。({c})「看過兩次了，歌很好聽」回答了有看過。'
     '({d0}) 只抓到 KPop 聯想到韓國，說的是沒去過韓國，答非所問；({d1}) 用了聽到的 talking，說的卻是別人講話太大聲。'
     '（KPop Demon Hunters 是 2025 年 6 月在 Netflix 上線的動畫電影，成為 Netflix 史上觀看次數最多的電影，主題曲〈Golden〉登上美國 Billboard 單曲榜第一名，並在 2026 年 2 月得到葛萊美獎。）')

# Q7  L2  Do you need anything? -> ask for something
text([['N', "I'm going to the convenience store. Do you need anything?"]],
     'Yes. Could you get me a bottle of milk?',
     ["Yes, it's open twenty-four hours a day.", "Sorry, it's not convenient for me today."],
     '我要去便利商店，你需要什麼東西嗎？',
     '對方問你要不要幫你買東西。({c})「要，可以幫我買一瓶牛奶嗎？」回答了需要什麼。'
     '({d0}) 說的是商店的營業時間，沒有回答需不需要東西；({d1}) 用了和 convenience 很像的 convenient（方便的），答非所問。')

# Q8  L2  stay up late -> a reason
text([['N', 'You look tired. Did you stay up late again last night?']],
     'Yes. I watched a baseball game until midnight.',
     ["No, I'm usually late for school.", "Sure. Let's stay up and study together."],
     '你看起來很累。你昨晚又熬夜了嗎？',
     'stay up late 是「熬夜」。({c})「對，我看棒球比賽看到半夜」說明了熬夜的原因。'
     '({d0}) 用了聽到的 late，說的卻是上學常遲到，答非所問；({d1}) 對方問的是昨晚的事，這句卻是邀對方一起熬夜讀書。')

# Q9  L3  a helpful answer in question form
text([['N', "I can't find my glasses anywhere. Have you seen them?"]],
     "Aren't they on your head?",
     ['Yes, I can see the words clearly now.', 'They look really nice on you.'],
     '我到處都找不到我的眼鏡，你有看到嗎？',
     '({c})「不就在你頭上嗎？」用反問句告訴對方眼鏡在哪裡，是很自然的回應。'
     '({d0}) 說的是自己現在看得很清楚，跟幫對方找眼鏡無關；({d1}) 對方正找不到眼鏡、沒有戴著，稱讚「戴起來很好看」不合理。')

# Q10  L2  apology for being late -> accept it
text([['N', "I'm sorry I'm late. The bus didn't come for thirty minutes."]],
     "That's OK. The movie hasn't started yet.",
     ['Great. You should take the bus more often.', "Don't worry. I'll be there in thirty minutes."],
     '抱歉我遲到了。公車三十分鐘都沒來。',
     '對方為遲到道歉。({c})「沒關係，電影還沒開始」接受了道歉。'
     '({d0}) 公車害對方遲到，卻說「太好了，你應該多搭公車」，不合理；'
     '({d1}) 對方已經到了，你卻說自己三十分鐘後才到，用了聽到的 thirty minutes 卻答非所問。')

# Q11  L3  current event: Duplantis' pole vault world record (Tokyo, Sept 2025); "broke" a record, not a bone
text([['N', 'Duplantis broke the pole vault world record again in Tokyo. He jumped six point three meters!']],
     "Amazing! I can't even imagine jumping that high.",
     ['Oh no! Is he badly hurt?', 'How many meters did he swim?'],
     'Duplantis（杜普蘭提斯）在東京又打破了撐竿跳世界紀錄，他跳過了 6.3 公尺！',
     'break a record 是「打破紀錄」，是好消息。({c})「太厲害了！我連想像跳那麼高都沒辦法」適當回應。'
     '({d0}) 把 broke 誤解成「摔斷（骨頭）」，以為他受傷了；({d1}) 撐竿跳是「跳」的項目，對方說的是 jumped，不是游泳。'
     '（2025 年 9 月 15 日，瑞典的 Armand Duplantis 在東京世界田徑錦標賽跳過 6.30 公尺，第 14 次刷新撐竿跳世界紀錄。）')

# ============================================================ 第三部分：言談理解
# Q12  L2  plan B if it rains (the gym is the trap from "last time")
t = [['M', "Hi, everyone. Ms. Chen just told me about tomorrow's class trip. We'll meet at the school gate at eight. "
           "If it's sunny, we'll go to the zoo as planned. If it rains, we won't stay in the school gym like last time. "
           "We'll go to the science museum instead. Either way, please bring your own lunch and a water bottle."],
     ['Q', 'Where will the class go if it rains tomorrow?']]
text(t, 'To the science museum.', ['To the zoo.', 'To the school gym.'],
     '嗨，各位。陳老師剛剛告訴我明天班級出遊的事。我們八點在校門口集合。如果天氣晴朗，就照原定計畫去動物園。'
     '如果下雨，我們不會像上次一樣待在學校體育館，而是改去科學博物館。不管去哪裡，都請自己帶午餐和水壺。'
     '問題：如果明天下雨，全班會去哪裡？',
     '男生說下雨時「改去科學博物館」（We\'ll go to the science museum instead）。'
     '({d0}) 動物園是晴天時的計畫；({d1}) 待在體育館是「上次」的做法，這次說了不會（won\'t）待在體育館。')

# Q13  L3  current event: Labubu blind boxes; infer what she will do
t = [['W', 'Look! I finally got a Labubu. I waited in line for two hours this morning.'],
     ['M', "That little monster toy? Why is everyone so crazy about it?"],
     ['W', "It's cute, and it comes in a blind box. You don't know which one you'll get until you open it."],
     ['M', 'So which one did you want?'],
     ['W', 'The pink one. But I got the green one again. Now I have two green ones.'],
     ['M', "Didn't your friend Amy say she wanted a green one? And she has two pink ones, right?"],
     ['W', "You're right! I'll call her right now."],
     ['Q', 'What will the girl most likely do?']]
text(t, 'Trade one of her green Labubus for one of Amy\'s pink ones.',
     ['Wait in line again to buy another blind box.', 'Give the pink Labubu to the boy.'],
     '女：你看！我終於買到 Labubu 了，我今天早上排了兩個小時的隊。男：那個小怪獸玩偶？為什麼大家都那麼瘋它？'
     '女：它很可愛，而且是裝在盲盒裡賣的，不打開就不知道會拿到哪一款。男：那妳想要哪一款？'
     '女：粉紅色的。可是我又拿到綠色的了，現在我有兩個綠色的。男：妳朋友 Amy 不是說她想要綠色的嗎？而且她有兩個粉紅色的，對吧？'
     '女：對耶！我現在就打電話給她。問題：女孩最可能會做什麼？',
     '女孩多了一個綠色的、想要粉紅色的；Amy 想要綠色的、多了一個粉紅色的。男孩一提醒，女孩就說要馬上打給 Amy，'
     '可見她要用多的綠色 Labubu 跟 Amy 交換粉紅色的。'
     '({d0}) 排隊兩小時是她今天早上做過的事，她並沒有說要再去排隊；({d1}) 她根本還沒有粉紅色的，也沒有說要送男孩東西。'
     '（Labubu 是香港藝術家龍家昇創作、泡泡瑪特以盲盒販售的玩偶，2025 年在各地掀起排隊搶購熱潮。）')

# Q14  L3  current event: 2026 Taiwan Lantern Festival in Chiayi; Year of the Horse but the main lantern is a tree
t = [['W', 'Did you go to the Taiwan Lantern Festival in Chiayi this March?'],
     ['M', 'Yes, I went with my family on the last weekend. It was really crowded.'],
     ['W', "Was the main lantern a horse? It's the Year of the Horse."],
     ['M', "That's what I thought, too. But it wasn't. It looked like a giant tree from Alishan, about twenty meters tall."],
     ['W', 'A tree? How interesting!'],
     ['M', 'Every half hour, it had a light show. The horse was on the small hand lanterns. They looked like a bear riding a wooden horse.'],
     ['Q', 'What did the main lantern look like?']]
text(t, 'A tall tree.', ['A horse.', 'A bear riding a horse.'],
     '女：你今年三月有去嘉義的台灣燈會嗎？男：有，我最後一個週末跟家人去的，人超多。女：主燈是馬嗎？今年是馬年。'
     '男：我本來也這麼以為，但不是。它看起來像一棵阿里山的巨大神木，大約二十公尺高。女：一棵樹？真有趣！'
     '男：每半小時它會有一場燈光秀。馬出現在小提燈上，小提燈是一隻熊騎著木馬的樣子。問題：主燈看起來是什麼樣子？',
     '男子說主燈「不是馬」，而是「看起來像一棵阿里山的巨大神木」。'
     '({d0}) 馬是女子的猜測，男子說「但不是」；({d1}) 熊騎木馬是「小提燈」的樣子，不是主燈。'
     '（2026 年 2 月 17 日起是馬年；2026 台灣燈會 3 月 3 日至 15 日在嘉義舉行，主燈「光沐－世界的阿里山」以阿里山神木為意象，高約 21 公尺。）')

# Q15  L3  voicemail: appointment moved; Wednesday is only the call-back deadline
t = [['W', "Hello, this is Doctor Lin's office calling for Kevin Wang. Your appointment is on Thursday at four thirty. "
           "But Doctor Lin has to go to a meeting at the hospital on Thursday afternoon. Can you come on Friday at the same time instead? "
           "If Friday is not good for you, please call us back before Wednesday, and we'll find another time for you. Thank you."],
     ['Q', 'When does the woman ask Kevin to come?']]
text(t, 'On Friday at four thirty.', ['On Thursday at four thirty.', 'On Wednesday at four thirty.'],
     '您好，這裡是林醫師診所，找王凱文。您原本預約的是星期四四點半，但林醫師星期四下午要去醫院開會。您可以改成星期五同一個時間來嗎？'
     '如果星期五不方便，請在星期三以前回電，我們會幫您另外找時間。謝謝。問題：這位女士請凱文什麼時候來？',
     '原本是星期四四點半，因為醫師要開會，改成「星期五同一個時間」（Friday at the same time），也就是星期五四點半。'
     '({d0}) 星期四是原本的預約時間，醫師那天下午不在；({d1}) 星期三是「回電」的期限，不是看診的日子。')

# Q16  L3  attitude now vs. at first (current event: "Golden" won a Grammy in Feb 2026)
t = [['M', "Can you please stop singing that song? You've been singing it all morning."],
     ['W', "You mean Golden? I can't help it. It's the song from KPop Demon Hunters."],
     ['M', "I know. I've watched the movie with you three times. At first, I loved the song, too."],
     ['W', 'It even won a Grammy in February. It was the first K-pop song to win one!'],
     ['M', "Good for them. But if I hear it one more time today, I'm going to wear earplugs."],
     ['Q', 'How does the man feel about the song now?']]
text(t, 'He is tired of hearing it.',
     ['He likes it as much as he did at first.', 'He hopes it will win a Grammy.'],
     '男：妳可以不要再唱那首歌了嗎？妳已經唱了一整個早上。女：你是說〈Golden〉？我忍不住嘛，它是《KPop 獵魔女團》的歌。'
     '男：我知道，我已經陪妳看了三次那部電影。一開始我也很喜歡那首歌。女：它二月還得了葛萊美獎，是第一首得獎的 K-pop 歌曲！'
     '男：恭喜他們。但如果今天再讓我聽到一次，我就要戴耳塞了。問題：男子現在對這首歌有什麼感覺？',
     '男子請女子別再唱，還說再聽到一次就要戴耳塞，可見他現在已經聽膩了。'
     '({d0}) 他只是「一開始」很喜歡，現在不是；({d1}) 女子說這首歌「已經」在二月得到葛萊美獎，不是還希望它得獎。'
     '（〈Golden〉於 2026 年 2 月 1 日獲葛萊美最佳影視歌曲獎，是第一首得到葛萊美獎的 K-pop 歌曲。）')

# Q17  L4  price: student price only with a card; the brother forgot his
ticket, off = 300, 50
pay = (ticket - off) + ticket + ticket
both_students = 2 * (ticket - off) + ticket
no_discount = 3 * ticket
t = [['W', "Three tickets for the seven o'clock show, please. One for me, one for my brother, and one for my mom."],
     ['M', 'Tickets are three hundred dollars each, and students get fifty dollars off. Are you and your brother students?'],
     ['W', 'Yes. Here is my student card. Oh no, my brother left his card at home. Is that OK?'],
     ['M', "I'm sorry. Without a student card, I can't give him the student price."],
     ['W', "I see. That's fine."],
     ['Q', 'How much will the woman pay for the three tickets?']]
text(t, f'{pay} dollars.', [f'{both_students} dollars.', f'{no_discount} dollars.'],
     '女：請給我七點那場的三張票，我一張、我弟弟一張、我媽媽一張。男：票一張三百元，學生折五十元。妳和妳弟弟是學生嗎？'
     '女：是的，這是我的學生證。喔不，我弟弟把學生證忘在家裡了，這樣可以嗎？男：很抱歉，沒有學生證，我不能算他學生價。'
     '女：我知道了，沒關係。問題：女子三張票要付多少錢？',
     f'只有女子出示學生證，可以折五十元：300－50＝250 元；弟弟沒帶學生證、媽媽不是學生，各 300 元。'
     f'合計 250＋300＋300＝{pay} 元。'
     f'({{d0}}) {both_students} 元是把弟弟也算成學生價，但他沒帶學生證；({{d1}}) {no_discount} 元是三張都沒有折扣，忘了女子有學生證。',
     check=(pay == 850, [both_students == pay, no_discount == pay]))

# Q18  L3  idiom inferred from context: "My lips are sealed"
t = [['W', "I'm planning a surprise party for Mom's fiftieth birthday next Sunday."],
     ['M', "That's a great idea! Does Dad know about it?"],
     ['W', "Not yet. You know Dad. He can never keep a secret. I'll tell him the day before the party."],
     ['M', "Smart. And don't worry about me. My lips are sealed."],
     ['W', 'Thanks. Can you help me pick up the cake on Sunday morning?'],
     ['M', 'Sure, no problem.'],
     ['Q', 'What does the man mean when he says "My lips are sealed"?']]
text(t, "He won't tell anyone about the party.",
     ["His mouth hurts, so he can't eat any cake.", 'He will tell Dad about the party the day before.'],
     '女：我正在計畫下星期天幫媽媽辦五十歲生日的驚喜派對。男：好主意！爸爸知道嗎？'
     '女：還不知道。你也知道爸爸，他從來守不住秘密。我會在派對前一天才告訴他。男：聰明。還有，妳不用擔心我，我的嘴巴是封起來的。'
     '女：謝謝。你可以星期天早上幫我去拿蛋糕嗎？男：當然，沒問題。問題：男子說 "My lips are sealed" 是什麼意思？',
     '前面在談「守不住秘密」的爸爸，男子接著說「不用擔心我，我的嘴巴是封起來的」，意思是他會守住秘密、不會說出去。'
     '({d0}) 只照字面理解成嘴巴有問題，而且他還答應去拿蛋糕；({d1}) 派對前一天告訴爸爸的是「女子」的計畫，不是男子要做的事。')

# Q19  L4  announcement: which rule applies at 11 a.m.; the bus leaves from Lake Station
t = [['N', 'Attention, please. This Saturday, from ten in the morning to four in the afternoon, Blue Line trains will not stop at Park Station '
           'because of repair work. Riders going to Park Station can get off at Lake Station, one stop before Park Station, '
           'and take a free bus from Exit Two. The bus leaves every ten minutes. After four o\'clock, trains will stop at Park Station as usual. Thank you.'],
     ['Q', 'Mia wants to go to Park Station at eleven on Saturday morning. What should she do?']]
text(t, 'Get off at Lake Station and take the free bus.',
     ['Take the Blue Line to Park Station as usual.', 'Wait for the free bus at Exit Two of Park Station.'],
     '請注意。本星期六上午十點到下午四點，因為維修工程，藍線列車不停靠公園站。要到公園站的旅客，可以在公園站前一站的湖站下車，'
     '從二號出口搭免費公車，公車每十分鐘一班。四點以後，列車照常停靠公園站。謝謝。'
     '問題：Mia 星期六早上十一點要去公園站，她應該怎麼做？',
     '十一點在「十點到四點」之間，列車不停公園站，所以要在前一站湖站下車，從二號出口搭免費公車。'
     '({d0}) 照常搭到公園站是四點以後才可以；({d1}) 免費公車是從「湖站」的二號出口出發，不是公園站。')

# Q20  L2  plan changes twice; the final choice
t = [['M', "Grandpa's birthday is this Friday. What should we give him?"],
     ['W', 'How about a new watch? His old one is broken.'],
     ['M', 'Mom already bought him one last week.'],
     ['W', 'Oh. Then what about a book? He loves reading.'],
     ['M', "His eyes aren't very good these days. He can't read for long."],
     ['W', 'Hmm. He always says he misses the old days. Why don\'t we make him a photo album of our family?'],
     ['M', "Great idea. I'll look for the old photos tonight."],
     ['Q', 'What will they give Grandpa?']]
text(t, 'A photo album.', ['A new watch.', 'A book.'],
     '男：爺爺的生日是這個星期五，我們要送他什麼？女：送一支新手錶如何？他的舊手錶壞了。男：媽媽上星期已經買一支給他了。'
     '女：喔，那送一本書呢？他很愛看書。男：他最近眼睛不太好，沒辦法看太久。'
     '女：嗯……他常說很懷念以前的日子。我們何不做一本全家人的相簿送他？男：好主意，我今晚就去找舊照片。問題：他們要送爺爺什麼？',
     '手錶和書都被男生否決了，最後兩人同意做一本家庭相簿，男生還說今晚就去找舊照片。'
     '({d0}) 媽媽上星期已經買了手錶給爺爺；({d1}) 爺爺最近眼睛不好，不能看書太久。')

# Q21  L3  three opinions: all for the plan ("costs too much" is what *some people* say)
t = [['N', "Good evening. Next on the news, River City will build a new bike path along the river. It will open next spring. "
           "Let's hear what people think."],
     ['M', 'I ride my bike to work every day. Right now, I have to ride next to cars and buses. The new path will make my trip much safer.'],
     ['W', "Some people say it costs too much money. But I think it's worth it. My kids can finally ride their bikes on weekends, and I won't need to worry."],
     ['M', "I don't even have a bike, but I walk my dog by the river every morning. A nicer riverside is good news for everyone."],
     ['Q', 'What do these three people think of the new bike path?']]
text(t, 'They think it is a good plan.',
     ['They think it costs too much money.', 'They think only people who ride bikes will like it.'],
     '晚安。下一則新聞，河城（虛構城市）將沿著河邊興建一條新的自行車道，明年春天啟用。我們來聽聽民眾怎麼說。'
     '男一：我每天騎腳踏車上班，現在得在汽車和公車旁邊騎，新車道會讓我通勤安全很多。'
     '女：有人說花太多錢了，但我覺得很值得。我的孩子週末終於可以騎腳踏車，我也不用擔心了。'
     '男二：我連腳踏車都沒有，但我每天早上都在河邊遛狗。河邊變得更好，對每個人都是好消息。'
     '問題：這三個人對新的自行車道有什麼看法？',
     '三個人都支持：第一位覺得通勤更安全，第二位覺得值得、孩子可以安心騎車，第三位雖然不騎車也認為是好消息。'
     '({d0})「花太多錢」是「有些人」的說法，女子接著說 But I think it\'s worth it，表示她不同意；'
     '({d1}) 第三位沒有腳踏車，卻也覺得是好消息，所以不是只有騎車的人會喜歡。')

assert len(b.items) == 21
b.write()
