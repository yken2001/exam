"""AI-3 英聽（挑戰）: build src/data/ai/ai3_listening.json and the pictures of part 1.

Parts as in the real test: 辨識句意 1-3 (three pictures, drawn here), 基本問答
4-11, 言談理解 12-21. Each item is written with its correct option first;
SetBuilder places the options by TARGET, and a picture item's panels are drawn
in that final order (b.arrange). Level tags (# L4..L5) follow SPEC_AI2_AI3.md.

Second version (after blind solvers rated the first one ~2.4-2.9): the
difficulty comes from listening, not vocabulary -- pictures that need two or
three details combined (and a little arithmetic), responses where a later
detail overrides an earlier one or the real meaning is unsaid (unreal
conditionals, reproach, understatement, indirect requests), and long
conversations or announcements where plans change several times, a speaker
corrects herself, the attitude is never stated, or several rules must be
applied together.
  PYTHONIOENCODING=utf-8 python tools/ai_sets/ai3_listening.py
  python tools/gen_audio.py ai3
"""
import math
import os
import sys

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SetBuilder, spread_target

plt.rcParams['font.family'] = 'Microsoft JhengHei'

TOPICS = [
    '2026 世界棒球經典賽（2026/3/5–3/17）：委內瑞拉 3/17 在邁阿密以 3:2 擊敗美國，首度奪冠；八強賽淘汰衛冕的日本：https://en.wikipedia.org/wiki/2026_World_Baseball_Classic',
    'NASA Artemis II：2026/4/1 發射的試飛任務，四名太空人（含加拿大籍 Jeremy Hansen）繞月飛行、未登月，飛得比以往任何人（含阿波羅太空人）都遠，4/10（美國時間；臺灣為 4/11）在太平洋濺落：https://www.cp24.com/news/world/2026/04/10/canadian-jeremy-hansen-artemis-ii-crew-to-splash-down-after-historic-moon-trip/',
    '2026 FIFA 世界盃（6/11–7/19，48 隊、104 場）：7/19 冠軍戰西班牙延長賽第 106 分鐘進球、1:0 擊敗衛冕的阿根廷：https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_final',
    '2026/8/12 日全食：全食帶經西班牙北部（含 Zaragoza），馬德里與巴塞隆納剛好在全食帶外；西班牙的全食發生在日落前不到一小時、太陽很低，各地全食都不到兩分鐘：https://en.wikipedia.org/wiki/Solar_eclipse_of_August_12,_2026',
    '2026 愛知–名古屋亞運：2026/9/19–10/4，部分選手住在郵輪上：https://en.wikipedia.org/wiki/2026_Asian_Games',
    '對話中的人物（李老師擔任亞運志工等）、旅行經過、商店、票價、動物園場次、課程與通話內容皆為虛構情境',
]

b = SetBuilder('ai3_listening', '英聽', year=903, set_name='AI-3', title='AI-3 英語（聽力）模擬卷（挑戰）',
               note='由 AI 依心測中心英語聽力架構（辨識句意 3 題、基本問答 8 題、言談理解 10 題，三選一）編寫，非會考真題；'
                    '難度為「挑戰」（接近會考最難一級）：圖片要結合兩三個條件並稍作推算；回應要聽出沒有說出口的意思（與事實相反的假設、責備、反話、委婉請託），'
                    '或注意後面的話推翻了前面的話；長對話與廣播中計畫多次改變、說話者自我更正、態度要自己推斷、需同時套用多項規定或計算，'
                    '誘答選項多用錄音中出現過的字詞或別人、別的時間的細節。第一部分的圖片由程式繪製（tools/ai_sets/ai3_listening.py），語音以錄音稿合成（非會考原音）。',
               target=spread_target(21, 3, 903), difficulty='挑戰', topics=TOPICS)


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


def clock(ax, cx, cy, r, h, m):
    ax.add_patch(Circle((cx, cy), r, facecolor='white', edgecolor='black', linewidth=2))
    for k in range(60):
        a = math.radians(90 - 6 * k)
        r0 = 0.88 * r if k % 5 == 0 else 0.93 * r
        ax.plot([cx + r0 * math.cos(a), cx + 0.98 * r * math.cos(a)], [cy + r0 * math.sin(a), cy + 0.98 * r * math.sin(a)],
                color='black', linewidth=1.2 if k % 5 == 0 else 0.4)
    for k in range(1, 13):
        a = math.radians(90 - 30 * k)
        ax.text(cx + 0.74 * r * math.cos(a), cy + 0.74 * r * math.sin(a), str(k), ha='center', va='center', fontsize=7.5)
    ha = math.radians(90 - 30 * ((h % 12) + m / 60))
    ma = math.radians(90 - 6 * m)
    ax.plot([cx, cx + 0.45 * r * math.cos(ha)], [cy, cy + 0.45 * r * math.sin(ha)], color='black', linewidth=3.6, solid_capstyle='round')
    ax.plot([cx, cx + 0.72 * r * math.cos(ma)], [cy, cy + 0.72 * r * math.sin(ma)], color='black', linewidth=1.8, solid_capstyle='round')
    ax.add_patch(Circle((cx, cy), 0.012, color='black'))


def wall_and_watch(wall, watch):
    """wall clock (h, m) on the wall, a digital wrist watch showing watch (h, m)"""
    def draw(ax):
        ax.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96, color='#f4efe6'))
        clock(ax, 0.36, 0.62, 0.29, *wall)
        ax.add_patch(Rectangle((0.70, 0.04), 0.14, 0.40, color='#555555'))                 # strap
        ax.add_patch(Rectangle((0.62, 0.15), 0.30, 0.18, facecolor='#222222', edgecolor='#999999', linewidth=2))
        ax.text(0.77, 0.24, f'{watch[0]}:{watch[1]:02d}', ha='center', va='center',
                fontsize=13, color='#7CFC00', family='monospace', weight='bold')
    return draw


BOOK_COLORS = ['#2e86de', '#27ae60', '#8e44ad', '#e67e22', '#16a085', '#7f8c8d']


def shelf(top):
    """a two-level shelf; top: items left to right on the top shelf
    ('D' dictionary, 'C' clock, 'b' an ordinary book); the bottom shelf is the same in every panel"""
    def draw(ax):
        ax.add_patch(Rectangle((0.06, 0.06), 0.88, 0.88, facecolor='#f6ead7', edgecolor='#7a4e1f', linewidth=3))
        for y in (0.50, 0.06):
            ax.add_patch(Rectangle((0.06, y), 0.88, 0.035, color='#7a4e1f'))
        x, nb = 0.12, 0
        for it in top:
            if it == 'D':
                ax.add_patch(Rectangle((x, 0.535), 0.12, 0.33, facecolor='#c0392b', edgecolor='#7b241c', linewidth=1.2))
                ax.text(x + 0.06, 0.70, 'DICTIONARY', rotation=90, ha='center', va='center', fontsize=5.6, color='white', weight='bold')
                x += 0.13
            elif it == 'C':
                ax.add_patch(Rectangle((x + 0.055, 0.535), 0.03, 0.04, color='#555555'))
                ax.add_patch(Circle((x + 0.07, 0.65), 0.075, facecolor='white', edgecolor='black', linewidth=1.6))
                ax.plot([x + 0.07, x + 0.07], [0.65, 0.70], color='black', linewidth=1.2)
                ax.plot([x + 0.07, x + 0.105], [0.65, 0.65], color='black', linewidth=2)
                x += 0.16
            else:
                ax.add_patch(Rectangle((x, 0.535), 0.055, 0.26, facecolor=BOOK_COLORS[nb % 6], edgecolor='#333333', linewidth=0.8))
                nb += 1
                x += 0.065
        for k, c in enumerate(['#f1c40f', '#2e86de', '#e67e22', '#7f8c8d', '#27ae60']):    # bottom shelf: books and a plant
            ax.add_patch(Rectangle((0.12 + 0.065 * k, 0.095), 0.055, 0.25, facecolor=c, edgecolor='#333333', linewidth=0.8))
        ax.add_patch(Rectangle((0.66, 0.095), 0.12, 0.10, color='#a0522d'))
        for dx, dy in ((-0.04, 0.25), (0.0, 0.29), (0.04, 0.25)):
            ax.add_patch(Circle((0.72 + dx, dy), 0.045, color='#2e8b3a'))
    return draw


def bars(jan, feb, mar):
    def draw(ax):
        y0, scale = 0.2, 0.065                     # value v -> y0 + v*scale  (0..10)
        for v in range(0, 11, 2):
            y = y0 + v * scale
            ax.plot([0.16, 0.95], [y, y], color='#dddddd' if v else 'black', linewidth=0.8 if v else 1.4, zorder=1)
            ax.text(0.13, y, str(v), ha='right', va='center', fontsize=7)
        ax.plot([0.16, 0.16], [y0, y0 + 10 * scale], color='black', linewidth=1.4)
        for k, (lab, v) in enumerate((('Jan.', jan), ('Feb.', feb), ('Mar.', mar))):
            x = 0.30 + 0.25 * k
            ax.add_patch(Rectangle((x - 0.07, y0), 0.14, v * scale, color='#2e86de', zorder=2))
            ax.text(x, y0 - 0.06, lab, ha='center', va='center', fontsize=8)
        ax.text(0.05, 0.92, 'books read', fontsize=7, va='center')
    return draw


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


def hm(minutes):
    h, m = divmod(minutes, 60)
    return f'{(h - 1) % 12 + 1}:{m:02d}'


# ============================================================ 第一部分：辨識句意
# Q1  L5  "ten to nine" on the watch (8:50), the watch is five minutes FAST -> the right time (wall clock) is 8:45
watch = 8 * 60 + 50
real = watch - 5
picture("My watch says it's ten to nine, but it's five minutes fast. The clock on the wall shows the right time.",
        wall_and_watch(divmod(real, 60), divmod(watch, 60)),
        [wall_and_watch(divmod(watch + 5, 60), divmod(watch, 60)), wall_and_watch((9, 5), (9, 10))], 'q01.png',
        '我的手錶顯示九點差十分，但它快了五分鐘。牆上的時鐘顯示的是正確時間。',
        f'ten to nine 是「差十分九點」＝8:50，這是「手錶」上的時間；手錶「快了五分鐘（five minutes fast）」，'
        f'正確時間要往回減五分鐘＝{hm(real)}，牆上時鐘顯示正確時間，所以要指 {hm(real)}（長針指 9、短針快到 9）。'
        f'({{c}}) 手錶 8:50、時鐘 {hm(real)}，完全符合；({{d0}}) 時鐘 {hm(watch + 5)}，是把 fast 當成「慢了」而往後加了五分鐘；'
        f'({{d1}}) 手錶 9:10，是把 ten to nine 誤聽成「九點十分」。')
assert real == 8 * 60 + 45

# Q2  L4  top shelf + dictionary LEFT of the clock + exactly two books between them
picture('The dictionary is on the top shelf, to the left of the clock, with two other books between them.',
        shelf(['b', 'D', 'b', 'b', 'C', 'b']),
        [shelf(['b', 'C', 'b', 'b', 'D', 'b']), shelf(['D', 'b', 'C', 'b', 'b', 'b'])], 'q02.png',
        '字典在上層，在時鐘的左邊，它們中間隔著另外兩本書。',
        '三個條件：字典在「上層」、在時鐘的「左邊」、兩者中間「隔著兩本書」。'
        '({c}) 字典在時鐘左邊，中間正好兩本書；({d0}) 中間雖然有兩本書，但字典在時鐘的「右邊」；'
        '({d1}) 字典在時鐘左邊，但中間只隔了一本書。')

# Q3  L4  March = twice January, and February is the lowest ("my worst month")
jan, feb, mar = 4, 2, 8
picture('In March, I read twice as many books as in January, but February was my worst month.',
        bars(jan, feb, mar), [bars(mar, feb, jan), bars(3, 5, 6)], 'q03.png',
        '我三月讀的書是一月的兩倍，但二月是我（讀最少的）最差的一個月。',
        '兩個條件：三月的本數是一月的「兩倍」；二月是「最差的月份」，也就是三個月中讀最少的。'
        f'({{c}}) 一月 {jan} 本、三月 {mar} 本（兩倍），二月 {feb} 本最少；'
        f'({{d0}}) 二月雖然最少，但變成一月 {mar} 本是三月 {jan} 本的兩倍，弄反了；'
        '({d1}) 三月 6 本是一月 3 本的兩倍，但二月 5 本不是最少的，最少的是一月。')
assert mar == 2 * jan and feb < min(jan, mar)

# ============================================================ 第二部分：基本問答
# Q4  L4  the later detail overrides the earlier one: he is NOT taking the train any more
text([['N', 'I was going to take the train to Taichung on Saturday, but my uncle offered to drive me, so I gave my ticket to my sister.']],
     'That was nice of you. A car ride will be more comfortable anyway.',
     ["Don't forget to bring your ticket on Saturday.", 'Have a good trip. Call me when your train gets in.'],
     '我本來星期六要搭火車去臺中，但我叔叔（舅舅）說要開車載我，所以我把車票給了我姊姊（妹妹）。',
     '前半句說「本來要搭火車」，後半句卻改了：叔叔開車載他，車票也送給了姊姊（妹妹）。'
     '({c})「你人真好，反正坐車也比較舒服」同時回應了這兩件事。'
     '({d0}) 車票已經給了姊姊（妹妹），不必提醒他帶；({d1}) 他不搭火車了，不會有「你的火車到站」。')

# Q5  L5  past unreal conditional: you did NOT tell me, so I did NOT make more food
text([['N', "If you'd told me you were bringing friends, I would have made more food."]],
     'Sorry. They decided to come at the last minute.',
     ['Thanks for making so much food for us.', "It's OK. I told them you were coming."],
     '如果你早告訴我你要帶朋友來，我就會多煮一點了。',
     '「If you\'d told me…, I would have made…」是與過去事實相反的假設：真正的意思是「你沒有先告訴我，所以我沒有多煮」，帶有一點抱怨。'
     '({c})「抱歉，他們是最後一刻才決定要來的」解釋了為什麼沒先說，回應得當。'
     '({d0}) 對方其實「沒有」多煮，謝他「煮這麼多」是聽錯了意思；'
     '({d1}) 對方在意的是「你沒告訴他」要帶朋友，你「告訴朋友們他會在」與此無關，答非所問。')

# Q6  L4  current event: 2026 WBC (final already played); "So was I" agrees with "He was sure ..."
text([['N', 'Venezuela won the World Baseball Classic in March, and my dad still can\'t believe it. He was sure the U.S. would win the final.']],
     'So was I. But Venezuela just played better that night.',
     ['Me too. I hope the U.S. wins the final.', "Really? I didn't know your dad played for Venezuela."],
     '委內瑞拉三月贏得了世界棒球經典賽冠軍，我爸到現在還不敢相信。他原本很確定美國會贏得冠軍戰。'
     '（2026 年 3 月 17 日，委內瑞拉在冠軍戰以 3:2 擊敗美國，首度奪冠）',
     '冠軍戰已經在三月打完，委內瑞拉贏了。So was I 是「我也是（原本很確定美國會贏）」，'
     '({c})「我也是，但委內瑞拉那天晚上就是打得比較好」回應得當。'
     '({d0}) 冠軍戰已經打完了，不能再說「希望美國贏得冠軍戰」；({d1}) 對方的爸爸只是看比賽、猜錯了，並沒有替委內瑞拉打球。')

# Q7  L4  understatement: "wasn't exactly easy" = it was hard
text([['N', "That test wasn't exactly easy, was it?"]],
     "That's for sure. I couldn't even finish half of it.",
     ['No, it was so easy that I finished early.', "Yes, I'll study for it this weekend."],
     '那次考試不怎麼簡單，對吧？',
     'wasn\'t exactly easy 是委婉的說法，意思是「很難」，而且 was 表示考試已經考完。'
     '({c})「那還用說，我連一半都寫不完」同意考試很難。'
     '({d0}) No 表示同意「不簡單」，後面卻說「簡單到提早寫完」，前後矛盾；({d1}) 考試已經考完了，不能說「這週末要準備」。')

# Q8  L4  current event: Artemis II flew around the moon but never landed; it already happened
text([['N', 'The Artemis Two astronauts went farther from Earth than anyone ever had, but they never actually landed on the moon.']],
     'Right. That trip was only a test, wasn\'t it?',
     ['Wow. How long did they stay on the moon?', 'I know. I watched them walk on the moon on TV.'],
     'Artemis II（阿提米絲二號）的太空人飛得比以往任何人都離地球更遠，但他們其實並沒有登陸月球。'
     '（Artemis II 是 2026 年 4 月的繞月試飛任務，未登月）',
     '關鍵在後半句：they never actually landed（其實沒有登陸月球）。'
     '({c})「對，那趟只是試飛，不是嗎？」與「沒有登陸」相符。'
     '({d0}) 問他們「在月球上待了多久」，忽略了他們沒有登陸；({d1}) 沒有登陸，就不可能看到他們在月球上漫步（那是阿波羅計畫）。')

# Q9  L4  "You wouldn't mind if I ..., would you?" -- who brings whom, and tense
text([['N', "You wouldn't mind if I brought my little sister along to the zoo tomorrow, would you?"]],
     "Not at all, as long as she doesn't mind walking a lot.",
     ["Yes, I'd love to bring her.", "No, I didn't mind it at all yesterday."],
     '你應該不會介意我明天帶我妹妹一起去動物園吧？',
     '對方問「你不介意我帶妹妹去吧？」答應時要說「不介意」（Not at all）。'
     '({c})「一點也不，只要她不介意走很多路就好」答應了並提醒。'
     '({d0}) 要帶妹妹的是對方，不是你，而且 Yes 會被理解成「我介意」；({d1}) 對方問的是「明天」，用過去式 yesterday 回答，時間不對。')

# Q10  L4  reproach "You could have told me ..." -> apologize and explain
text([['N', 'You could have told me the meeting was canceled. I waited at the café for an hour.']],
     'I\'m so sorry. I thought Amy had already told you.',
     ['Thanks for letting me know it was canceled.', 'Only an hour? The meeting was much longer than that.'],
     '你大可以告訴我會議取消了。我在咖啡廳等了一個小時。',
     '「You could have told me…」是責備：「你明明可以告訴我，卻沒說」。({c})「真抱歉，我以為 Amy 已經告訴你了」道歉並解釋，回應得當。'
     '({d0}) 沒有人通知他，反而謝他「告訴我取消了」，方向弄反；({d1}) 會議已經取消，根本沒有開，不會「開得比一小時還久」。')

# Q11  L5  indirect request: "If you're going past the post office, I've got a letter ..." = please mail it
text([['N', "If you're going past the post office, I've got a letter that needs to go out today."]],
     "Sure, give it to me. I'll drop it off on my way.",
     ['Really? Who sent you the letter?', 'Yes, the post office is just past the bank.'],
     '如果你會經過郵局的話，我有一封信今天得寄出去。',
     '這句話表面上只是說「有一封信要寄」，其實是委婉地請你「順路幫他寄信」。({c})「好啊，給我吧，我順路幫你寄」聽懂了請託。'
     '({d0}) 信是對方「要寄出去」的，不是別人寄給他的；({d1}) 把 going past 當成問郵局在哪裡，回答了位置，沒有回應請託。')

# ============================================================ 第三部分：言談理解
# Q12  L5  current event: 2026 World Cup final; whose team won -- feelings must be inferred
t = [['M', 'Did you stay up for the World Cup final?'],
     ['W', 'I set my alarm, but I slept right through the first half. When I woke up, it was still zero to zero.'],
     ['M', "You didn't miss much, then. Nobody scored in the whole ninety minutes."],
     ['W', 'I know. And when Spain finally scored in extra time, my brother screamed so loudly that he woke up our neighbors.'],
     ['M', 'So you were both cheering for Spain?'],
     ['W', 'He was. I wanted Argentina to win two in a row. I went back to bed before they even gave out the trophy.'],
     ['M', 'Oh. Well, at least your brother had a good night.'],
     ['W', "Too good. He's still talking about it."],
     ['Q', 'How did the woman most likely feel at the end of the game?']]
text(t, 'Disappointed, because the team she liked lost.',
     ['Excited, because Spain finally scored.', 'Upset, because she slept through the whole game.'],
     '男：妳有熬夜看世界盃冠軍戰嗎？女：我設了鬧鐘，但整個上半場都睡過頭了。我醒來的時候還是零比零。'
     '男：那妳沒錯過什麼，整整九十分鐘都沒人進球。女：我知道。西班牙終於在延長賽進球的時候，我弟弟（哥哥）叫得好大聲，把鄰居都吵醒了。'
     '男：所以你們兩個都替西班牙加油？女：他是。我希望阿根廷連續兩屆奪冠。他們連頒獎都還沒開始，我就回去睡了。'
     '男：喔，好吧，至少妳弟弟（哥哥）度過了美好的一晚。女：太美好了，他到現在還在講。問題：比賽結束時，女子最可能有什麼感覺？',
     '女子說替西班牙加油的是她弟弟（哥哥），「她」希望阿根廷連霸；西班牙進球獲勝，她連頒獎都沒看就回去睡，'
     '最後還抱怨弟弟「太開心」，可見她支持的球隊輸了，她很失望。'
     '({d0}) 為西班牙進球興奮的是她弟弟（哥哥），不是她；({d1}) 她只睡過了上半場，醒來後有看到延長賽，不是整場都睡過頭。'
     '（2026 世界盃冠軍戰：西班牙在延長賽以 1:0 擊敗衛冕軍阿根廷。）')

# Q13  L5  current event: Artemis II; who did what (grandpa / class / cousin) + the distance record
t = [['M', 'My grandpa says he watched astronauts walk on the moon on a black-and-white TV when he was a kid.'],
     ['W', 'That was the Apollo program, more than fifty years ago. Did you follow Artemis Two this spring?'],
     ['M', 'A little. Our teacher showed the launch on the big screen in class.'],
     ['W', 'My cousin watched it in person in Florida. She said she could feel the ground shake.'],
     ['M', 'Lucky her! Did the astronauts land on the moon this time?'],
     ['W', 'No, they only flew around it. It was a test for a landing in the future. But they still went farther from Earth than any people before them, even the Apollo astronauts.'],
     ['M', "So my grandpa's astronauts don't hold that record anymore."],
     ['W', "Not that one. But they're still the only people who have ever walked on the moon."],
     ['Q', 'Which of the following is true?']]
text(t, 'The Artemis Two astronauts traveled farther from Earth than the Apollo astronauts.',
     ["The man's grandpa watched the Artemis Two launch on TV.", "The woman's cousin watched the launch with the man's class."],
     '男：我爺爺說他小時候在黑白電視上看過太空人在月球上漫步。女：那是阿波羅計畫，已經是五十多年前的事了。你今年春天有關注 Artemis II 嗎？'
     '男：有一點。我們老師在課堂上用大螢幕播了發射的畫面。女：我表姊（堂姊）在佛羅里達現場看，她說她感覺得到地面在震動。'
     '男：她真幸運！這次太空人有登陸月球嗎？女：沒有，他們只繞著月球飛，是為了將來登陸做的測試。不過他們還是飛得比以前任何人都離地球更遠，連阿波羅太空人都比不上。'
     '男：所以我爺爺那時候的太空人不再保有那項紀錄了。女：那一項沒有了。但他們仍然是唯一在月球上走過的人。問題：下列何者正確？',
     '女子說 Artemis II 的太空人「飛得比以前任何人都遠，連阿波羅太空人都比不上」，男子也說阿波羅太空人「不再保有那項紀錄」，所以 ({c}) 正確。'
     '({d0}) 爺爺在黑白電視上看的是五十多年前阿波羅太空人登月，不是 Artemis II 發射；'
     '({d1}) 在佛羅里達現場看發射的是女子的表姊（堂姊），在教室看大螢幕的才是男子的班級。'
     '（Artemis II 於 2026 年 4 月 1 日發射，繞月未登月，創下人類離地球最遠的紀錄。）')

# Q14  L5  current event: 12 Aug 2026 eclipse in Spain; the reason behind the change of plan
t = [['W', 'How was your eclipse trip to Spain?'],
     ['M', 'It almost went wrong. We booked a hotel in Barcelona months ago. Then, a week before the trip, my dad read that Barcelona was just outside the area where the sun would be completely covered.'],
     ['W', 'Oh no. So you only saw part of it?'],
     ['M', 'No. The day before, we took a train to Zaragoza. It was right in the path.'],
     ['W', 'Smart. Was it in the afternoon?'],
     ['M', 'In the evening, less than an hour before sunset, so the sun was really low. We had to climb a hill to make sure no buildings were in the way.'],
     ['W', 'And how long did it stay dark?'],
     ['M', 'Less than two minutes. My little sister blinked and said she missed it.'],
     ['W', 'Ha! Would you go again?'],
     ['M', "Of course. But next time I'll check the map before we book a hotel."],
     ['Q', "Why did the man's family go to Zaragoza?"]]
text(t, 'From Barcelona, they could not have seen the sun completely covered.',
     ['Their hotel in Barcelona was fully booked.', 'They wanted to watch the sunset from a hill.'],
     '女：你們去西班牙看日食的旅行怎麼樣？男：差點就搞砸了。我們幾個月前就訂了巴塞隆納的飯店，結果出發前一個星期，我爸看到巴塞隆納剛好在太陽會被完全遮住的範圍外面。'
     '女：喔不，所以你們只看到一部分？男：不是。前一天我們搭火車到了薩拉戈薩（Zaragoza），那裡就在全食帶上。'
     '女：真聰明。是在下午嗎？男：是在傍晚，日落前不到一小時，所以太陽非常低。我們得爬到一座山丘上，確定沒有建築物擋住。'
     '女：天黑了多久？男：不到兩分鐘。我妹妹眨了一下眼，就說她錯過了。女：哈！你還會再去嗎？男：當然。但下次訂飯店前我會先看地圖。'
     '問題：男子一家人為什麼去薩拉戈薩？',
     '男子說巴塞隆納「剛好在太陽會被完全遮住的範圍外」，留在那裡只能看到日偏食，所以前一天改搭火車到「就在全食帶上」的薩拉戈薩。'
     '({d0}) 他們幾個月前就「訂好了」巴塞隆納的飯店，沒有說客滿；'
     '({d1}) 爬山丘是到了薩拉戈薩之後，為了不讓建築物擋住低空的太陽，不是去薩拉戈薩的原因，他們也不是去看日落。'
     '（2026 年 8 月 12 日日全食的全食帶經過西班牙北部，巴塞隆納剛好在全食帶外，全食發生在日落前不到一小時。旅行經過為虛構情境。）')

# Q15  L5  attitude never stated: she politely thinks the plan is too much for now
t = [['M', "I've decided to ride my bike around Taiwan this summer. In five days!"],
     ['W', "Five days? Well, that's certainly... brave. How far have you ridden in one day before?"],
     ['M', "About thirty kilometers. To my grandma's house and back."],
     ['W', "And the whole trip is almost a thousand kilometers, isn't it? That's about two hundred a day."],
     ['M', "I'll train hard. And my cousin's going with me."],
     ['W', 'Hmm. Maybe the two of you could start with something shorter first, like a weekend ride around Sun Moon Lake.'],
     ['M', "You don't think I can do it?"],
     ['W', "I didn't say that. I'm just saying there's no hurry."],
     ['Q', "What does the woman really think of the man's plan?"]]
text(t, "It's too much for him to try right now.",
     ['He should find someone to ride with him.', 'Five days is too long for the trip.'],
     '男：我決定今年暑假騎腳踏車環島，五天騎完！女：五天？嗯，這真是……很勇敢。你以前一天最遠騎過多遠？'
     '男：大概三十公里，到我奶奶家來回。女：整趟差不多一千公里，對吧？那一天大約要騎兩百公里。男：我會努力練習，而且我表哥會跟我一起去。'
     '女：嗯……也許你們兩個可以先從短一點的開始，像是週末騎日月潭一圈。男：妳覺得我做不到？女：我可沒這麼說，我只是說不用急。'
     '問題：女子對男子的計畫真正的看法是什麼？',
     '女子沒有直說「你做不到」，但她用「很勇敢」委婉帶過，又算出一天要騎兩百公里（男子最多只騎過三十公里），還建議先從短程開始、「不用急」，'
     '可見她認為這個計畫目前對他來說太勉強。'
     '({d0}) 男子已經說表哥會一起去，女子並沒有建議要找人同行；({d1}) 女子的意思正好相反：一千公里五天騎完是「太趕」，不是天數太多。')

# Q16  L5  current event: 2026 Asian Games; announcement with several changes -- where at 8:15?
t = [['N', "Good morning, everyone. As you know, the Asian Games in Aichi and Nagoya, Japan, ended on October fourth. "
           "Mr. Lee, our P.E. teacher, worked there as a volunteer on one of the cruise ships where some of the athletes stayed, "
           "and he'll tell us about it at next Monday's assembly. "
           "Usually, our assembly is on the playground at seven fifty, but the playground is being repaired, so this time it will be in the auditorium. "
           "The auditorium can't hold all of us at once, so seventh and eighth graders will go first, at eight. "
           "Ninth graders will have their turn at eight forty, after the younger students leave. "
           "Until then, ninth graders should stay in their classrooms and read quietly."],
     ['Q', 'It is eight fifteen next Monday. Where should a ninth grader be?']]
text(t, 'In her classroom.', ['In the auditorium.', 'On the playground.'],
     '大家早安。如大家所知，在日本愛知和名古屋舉行的亞運已在十月四日閉幕。我們的體育老師李老師（虛構人物）在那裡擔任志工，'
     '服務的地方是一艘讓部分選手住宿的郵輪，他會在下星期一的朝會上跟大家分享。平常朝會在操場、七點五十分開始，但操場正在整修，所以這次改在禮堂。'
     '禮堂沒辦法一次容納全校，所以七、八年級先在八點進場；九年級等學弟妹離開後，八點四十分再進場。在那之前，九年級同學請留在教室安靜閱讀。'
     '問題：下星期一八點十五分，九年級學生應該在哪裡？',
     '這次朝會改在禮堂，而且分兩梯：七、八年級八點進場，九年級要到八點四十分才進場，在那之前「留在教室」。8:15 時九年級還沒輪到，所以應該在教室。'
     '({d0}) 8:15 在禮堂的是七、八年級，九年級要 8:40 才去；({d1}) 平常朝會在操場，但操場整修中，這次不在操場。'
     '（2026 愛知–名古屋亞運於 9 月 19 日至 10 月 4 日舉行，部分選手住在郵輪上。）')

# Q17  L5  price: 4 tickets -> 3 (sister drops out) -> only 1 student ticket (card left at home); popcorn refused
adult, student, popcorn = 280, 220, 100
pay = 2 * adult + student
t = [['M', "Four tickets for the seven o'clock show, please."],
     ['W', 'Sure. Tickets are two hundred and eighty dollars each, but students pay two twenty. Are any of you students?'],
     ['M', 'Two of us are. Oh, wait. My sister just texted me. She can\'t come. So it\'s three tickets: me, and two students.'],
     ['W', 'OK. Just so you know, students have to show their student cards at the door.'],
     ['M', 'Really? Hmm, my friend left his at home. Then only one student ticket, I guess.'],
     ['W', 'All right. Would you like to add popcorn? It\'s only a hundred dollars with a ticket.'],
     ['M', "No, thanks. We just had dinner."],
     ['Q', 'How much will the man pay?']]
text(t, f'{pay} dollars.', [f'{adult + 2 * student} dollars.', f'{pay + popcorn} dollars.'],
     '男：請給我四張七點那場的票。女：好的，每張兩百八十元，學生是兩百二十元。你們有人是學生嗎？'
     '男：我們有兩個是。喔，等一下，我姊姊（妹妹）剛傳訊息說她不能來了。所以是三張：我，還有兩個學生。'
     '女：好的。先跟你說，學生要在入口出示學生證。男：真的嗎？嗯……我朋友把學生證忘在家裡了。那我想就只買一張學生票吧。'
     '女：好的。要不要加購爆米花？買票加購只要一百元。男：不用了，謝謝，我們剛吃過晚餐。問題：男子要付多少錢？',
     f'人數和票種改了兩次：四張 → 姊姊（妹妹）不來，剩三張（男子＋兩個學生）→ 朋友沒帶學生證，只能買一張學生票，另一人改買全票。'
     f'所以是兩張全票、一張學生票：{adult}×2＋{student}＝{pay} 元；爆米花他拒絕了。'
     f'({{d0}}) {adult + 2 * student} 元是還用兩張學生票計算，忘了朋友沒帶學生證；({{d1}}) {pay + popcorn} 元是加了一百元爆米花，但他說不用。',
     check=(pay == 780, [adult + 2 * student == pay, pay + popcorn == pay]))

# Q18  L5  voicemail with two self-corrections (station; who brings what)
t = [['W', "Hi, Jack, it's Lisa. It's about tomorrow's study group. We were going to meet at the library at two, but it's closed for the holiday, "
           "so we'll use Kevin's living room instead. His house is near Ming Shan Station. Wait, no, sorry. It's near Ming De Station, the one after Ming Shan. "
           "His mom has guests until three, so let's meet at the station at three and walk over together. "
           "Oh, and Kevin will bring drinks. No, actually, I'll bring the drinks, and Kevin's mom is making sandwiches. So could you bring some cookies? "
           "Call me if there's a problem. Bye."],
     ['Q', 'What does Lisa want Jack to do tomorrow?']]
text(t, 'Meet her at Ming De Station at three and bring cookies.',
     ['Meet her at Ming Shan Station at three and bring cookies.', 'Meet her at Ming De Station at three and bring drinks.'],
     '嗨，Jack，我是 Lisa。關於明天的讀書會：我們本來要兩點在圖書館碰面，但圖書館放假不開，所以改用 Kevin 家的客廳。'
     '他家在明山站附近。等等，不對，抱歉，是在明德站附近，明山的下一站。他媽媽家裡有客人到三點，所以我們三點在車站碰面，再一起走過去。'
     '喔，還有，Kevin 會帶飲料。不對，其實是我帶飲料，Kevin 的媽媽會做三明治。所以你可以帶些餅乾嗎？有問題再打給我。拜。'
     '問題：Lisa 希望 Jack 明天做什麼？',
     'Lisa 說話時更正了兩次：車站從「明山站」改成「明德站」；帶飲料的人從 Kevin 改成「她自己」。她請 Jack「三點在明德站碰面」並「帶餅乾」。'
     '({d0}) 明山站是她說錯、隨即更正的站名；({d1}) 地點和時間對了，但飲料是 Lisa 自己要帶的，Jack 要帶的是餅乾。')

# Q19  L5  zoo schedule: canceled show + 20-minute walk + no late entry -> only one plan works
bird = [10 * 60 + 30, 14 * 60]
canceled = 14 * 60
sea = [11 * 60 + 15, 15 * 60 + 30]
show, walk = 30, 20
plans = [(bi, s) for bi in bird for s in sea if bi != canceled and (bi + show + walk <= s or s + show + walk <= bi)]
assert plans == [(10 * 60 + 30, 15 * 60 + 30)]
t = [['N', "Welcome to Green Hill Zoo. Here is today's show information. The bird show is at ten thirty and at two. "
           "The sea lion show is at eleven fifteen and at three thirty. Each show lasts thirty minutes, "
           "and no one can enter after a show has started. Because of the strong wind, the two o'clock bird show has been canceled. "
           "Also, please note that it takes about twenty minutes to walk from the bird garden to the sea lion pool. "
           "The zoo closes at five. Enjoy your day."],
     ['Q', 'A family wants to see both shows today. Which plan will work?']]
text(t, 'The bird show at 10:30, and then the sea lion show at 3:30.',
     ['The bird show at 10:30, and then the sea lion show at 11:15.', 'The sea lion show at 11:15, and then the bird show at 2:00.'],
     '歡迎來到綠丘動物園，以下是今天的表演資訊。鳥類表演在十點半和兩點；海獅表演在十一點十五分和三點半。每場表演三十分鐘，表演開始後就不能進場。'
     '因為風很強，兩點的鳥類表演取消了。另外請注意，從鳥園走到海獅池大約要二十分鐘。動物園五點關門。祝您有愉快的一天。'
     '問題：一家人今天想要兩種表演都看到，哪一個安排可行？',
     '要同時套用三條規定：兩點的鳥類表演取消，鳥類只剩 10:30 那場；鳥類表演 11:00 結束，走到海獅池要二十分鐘，11:20 才到，'
     '已經趕不上 11:15 那場（開演後不能進場）；所以只能看 10:30 的鳥類表演，再看 3:30 的海獅表演。'
     '({d0}) 11:00 看完鳥類表演再走二十分鐘，11:20 才到，11:15 那場已經開始、不能進場；({d1}) 兩點的鳥類表演因為強風取消了。')

# Q20  L5  a choice where the obstacles are removed one by one; the real reason comes last
t = [['W', 'Have you decided which English class to take this fall?'],
     ['M', 'Not yet. There\'s one on Tuesday and Thursday evenings, and one on Saturday mornings.'],
     ['W', "Don't you have basketball practice on Tuesdays?"],
     ['M', 'Only until the end of September. After that, the team takes a break until spring.'],
     ['W', 'So Tuesday works. What about Saturday?'],
     ['M', 'We usually visit my grandma on Saturday mornings. But she\'s moving in with us next month.'],
     ['W', "Then you'll be free on Saturdays, too."],
     ['M', "Right. But the Saturday class is three hours long, and you know I can't sit still that long."],
     ['W', 'Ha! I know you. Two shorter classes, then?'],
     ['M', 'Exactly.'],
     ['Q', 'Which class will the man most likely take, and why?']]
text(t, 'The Tuesday and Thursday class, because shorter classes suit him better.',
     ['The Saturday class, because his grandma is moving in with his family.',
      'The Tuesday and Thursday class, because he has basketball practice on Saturdays.'],
     '女：你決定今年秋天要上哪一班英文課了嗎？男：還沒。有一班在星期二和星期四晚上，一班在星期六早上。女：你星期二不是有籃球練習嗎？'
     '男：只到九月底。之後球隊休息到春天。女：所以星期二可以。那星期六呢？男：我們星期六早上通常會去看奶奶，但她下個月要搬來跟我們住。'
     '女：那你星期六也有空了。男：對。但星期六那班一次三個小時，妳知道我沒辦法坐那麼久。女：哈！我了解你。那就選兩堂短一點的課？男：沒錯。'
     '問題：男子最可能上哪一班？為什麼？',
     '兩班原本各有阻礙，但都被排除了：籃球練習九月底就結束，奶奶搬來後星期六也有空；真正的決定理由在最後：星期六那班一次三小時，他坐不住，所以選「兩堂短一點的課」，也就是星期二、四那班。'
     '({d0}) 奶奶搬來只是讓星期六有空，他最後並沒有選星期六；({d1}) 班別選對了，但理由錯了：籃球練習是在星期二，而且九月底就結束了，星期六沒有籃球練習。')

# Q21  L5  plan changes three times in one call; what will happen next
t = [['W', "Hi, honey. I'm stuck in traffic, so I won't be able to pick you up from school at five."],
     ['M', "That's OK. I can take the bus home."],
     ['W', "No, it's raining too hard. Dad finishes work at five thirty. He'll come for you."],
     ['M', "But Dad's car is at the repair shop, isn't it?"],
     ['W', "Oh, right, I forgot. Then wait for me at the library. I'll be there by six, I think."],
     ['M', 'The library closes at five thirty on Fridays.'],
     ['W', "Then wait at the convenience store across from it. I'll call you when I'm close."],
     ['M', "OK. I'll get some homework done there."],
     ['Q', 'What will the boy most likely do after school?']]
text(t, 'Wait at the convenience store for his mother.',
     ['Wait at the library for his father.', 'Take the bus home by himself.'],
     '女：嗨，親愛的，我塞在車陣裡，沒辦法五點去學校接你了。男：沒關係，我可以搭公車回家。'
     '女：不行，雨下得太大了。爸爸五點半下班，他會去接你。男：可是爸爸的車在修車廠，不是嗎？'
     '女：喔，對，我忘了。那你在圖書館等我，我想我六點以前會到。男：圖書館星期五五點半就關門了。'
     '女：那你在圖書館對面的便利商店等，我快到的時候會打給你。男：好，我可以在那裡寫點功課。問題：男子放學後最可能做什麼？',
     '計畫一共改了三次：搭公車（媽媽說雨太大不行）→ 爸爸來接（爸爸的車在修，不行）→ 在圖書館等媽媽（圖書館五點半關門，不行）'
     '→ 最後決定在圖書館「對面的便利商店」等媽媽。'
     '({d0}) 爸爸的車在修車廠，不能來接，而且圖書館五點半就關門；({d1}) 搭公車是男子一開始的提議，媽媽因為雨太大而拒絕了。')

assert len(b.items) == 21
b.write()
