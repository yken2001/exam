"""AI-1 英聽: build src/data/ai/ai1_listening.json and the pictures of part 1.

Parts as in the real test: 辨識句意 1-3 (three pictures, drawn here), 基本問答
4-11, 言談理解 12-21. The correct option comes first in each item and is
placed by TARGET; a picture item's panels are drawn in that same order, so
the picture marked with the answer letter is the one matching the sentence.
The audio is made afterwards from the transcripts:
  python tools/ai_sets/ai1_listening.py
  python tools/gen_audio.py ai1
"""
import json
import os

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle, Wedge

plt.rcParams['font.family'] = 'Microsoft JhengHei'

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(os.path.dirname(HERE))
FIG_DIR = os.path.join(APP, 'public', 'ai', '901', 'listening')
OUT = os.path.join(APP, 'src', 'data', 'ai', 'ai1_listening.json')
os.makedirs(FIG_DIR, exist_ok=True)
TARGET = 'CACABCABCABABCBACBCAB'          # A 7, B 7, C 7


# ------------------------------------------------------------ drawing helpers
def table(ax, x=0.5, w=0.7):
    ax.add_patch(Rectangle((x - w / 2, 0.42), w, 0.05, color='#8a5a2b'))
    ax.add_patch(Rectangle((x - w / 2 + 0.03, 0.12), 0.04, 0.3, color='#8a5a2b'))
    ax.add_patch(Rectangle((x + w / 2 - 0.07, 0.12), 0.04, 0.3, color='#8a5a2b'))


def cat(ax, cx, cy, s=1.0):
    ax.add_patch(Ellipse((cx, cy), 0.26 * s, 0.13 * s, color='#555555'))
    ax.add_patch(Circle((cx + 0.14 * s, cy + 0.06 * s), 0.06 * s, color='#555555'))
    ax.add_patch(Polygon([(cx + 0.10 * s, cy + 0.10 * s), (cx + 0.12 * s, cy + 0.16 * s), (cx + 0.15 * s, cy + 0.11 * s)], color='#555555'))
    ax.add_patch(Polygon([(cx + 0.15 * s, cy + 0.11 * s), (cx + 0.19 * s, cy + 0.16 * s), (cx + 0.20 * s, cy + 0.09 * s)], color='#555555'))
    ax.plot([cx - 0.13 * s, cx - 0.22 * s], [cy, cy + 0.08 * s], color='#555555', linewidth=3)   # tail
    ax.text(cx + 0.02, cy + 0.14 * s, 'z z', fontsize=9, color='#333333')                          # sleeping


def boy(ax, cap, umbrella):
    x = 0.45
    ax.add_patch(Circle((x, 0.72), 0.07, fill=False, linewidth=1.8))                   # head
    ax.plot([x, x], [0.65, 0.40], color='black', linewidth=1.8)                          # body
    ax.plot([x, x - 0.08], [0.40, 0.18], color='black', linewidth=1.8)                   # legs
    ax.plot([x, x + 0.08], [0.40, 0.18], color='black', linewidth=1.8)
    ax.plot([x, x - 0.12], [0.58, 0.46], color='black', linewidth=1.8)                   # left arm
    if cap:
        ax.add_patch(Wedge((x, 0.765), 0.075, 0, 180, color='#1f5fb4'))
        ax.add_patch(Rectangle((x, 0.755), 0.12, 0.02, color='#1f5fb4'))
    if umbrella:
        ax.plot([x, x + 0.16], [0.58, 0.50], color='black', linewidth=1.8)               # right arm to handle
        ax.plot([x + 0.16, x + 0.16], [0.50, 0.86], color='black', linewidth=1.5)       # stick
        ax.add_patch(Wedge((x + 0.16, 0.86), 0.17, 0, 180, color='#c0392b'))
    else:
        ax.plot([x, x + 0.12], [0.58, 0.46], color='black', linewidth=1.8)


def plate(ax, apples, bananas):
    ax.add_patch(Ellipse((0.5, 0.35), 0.9, 0.34, fill=False, linewidth=1.8))
    xs = [0.2 + 0.13 * i for i in range(apples)]
    for x in xs:
        ax.add_patch(Circle((x, 0.40), 0.055, color='#d62728'))
        ax.plot([x, x + 0.01], [0.455, 0.49], color='#5a3d1e', linewidth=1.5)
    for j in range(bananas):
        ax.add_patch(Wedge((0.60 + 0.14 * j, 0.42), 0.06, 200, 340, width=0.03, color='#e6b800'))


def panels(draws, name):
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6))
    for ax, (label, draw) in zip(axes, zip('ABC', draws)):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.add_patch(Rectangle((0.01, 0.01), 0.98, 0.98, fill=False, linewidth=1, edgecolor='#999999'))
        draw(ax)
        ax.text(0.5, -0.1, f'({label})', ha='center', fontsize=12)
    fig.savefig(os.path.join(FIG_DIR, name), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return f'ai/901/listening/{name}'


def order(correct, distractors, letter):
    opts = list(distractors)
    opts.insert('ABC'.index(letter), correct)
    return opts


# ------------------------------------------------------------ items
items = []


def picture_item(n, sentence, correct, distractors, zh, why):
    letter = TARGET[n - 1]
    fig = panels(order(correct, distractors, letter), f'q{n:02d}.png')
    items.append(dict(qNo=n, stem='', options=['', '', ''], answer=letter, figure=fig,
                      transcript=[['N', sentence]],
                      explanation=f'【聽力稿】{sentence}\n【中譯】{zh}\n【解析】{why}故選 ({letter})。'))


def text_item(n, transcript, correct, distractors, zh, why):
    letter = TARGET[n - 1]
    heard = '\n'.join(f"{'Question' if w == 'Q' else w}: {t}" if w != 'N' else t for w, t in transcript)
    items.append(dict(qNo=n, stem='', options=order(correct, distractors, letter), answer=letter,
                      transcript=[list(x) for x in transcript],
                      explanation=f'【聽力稿】{heard}\n【中譯】{zh}\n【解析】{why}故選 ({letter})。'))


# 第一部分：辨識句意
picture_item(1, 'The cat is sleeping under the table.',
             lambda ax: (table(ax), cat(ax, 0.47, 0.19)),
             [lambda ax: (table(ax), cat(ax, 0.47, 0.54)),
              lambda ax: (table(ax, 0.33, 0.56), cat(ax, 0.80, 0.19, 0.7))],
             '貓正在桌子底下睡覺。', '句子說貓在桌子「底下」（under the table）睡覺，要選貓在桌子下方的圖；貓在桌上或桌子旁邊都不對。')
picture_item(2, 'The boy is wearing a cap, and he is holding an umbrella.',
             lambda ax: boy(ax, True, True),
             [lambda ax: boy(ax, False, True), lambda ax: boy(ax, True, False)],
             '這個男孩戴著一頂帽子，手上拿著一把傘。', '男孩要同時「戴帽子」和「拿著傘」。只拿傘沒戴帽子、或只戴帽子沒拿傘的圖都不符合。')
picture_item(3, 'There are three apples and two bananas on the plate.',
             lambda ax: plate(ax, 3, 2),
             [lambda ax: plate(ax, 2, 3), lambda ax: plate(ax, 3, 1)],
             '盤子上有三顆蘋果和兩根香蕉。', '要選「三顆蘋果、兩根香蕉」的圖。兩顆蘋果三根香蕉、或三顆蘋果一根香蕉的數量都不對。')

# 第二部分：基本問答
text_item(4, [('N', 'What time does the movie start?')], 'At seven thirty.', ["It's about a dog.", 'With my sister.'],
          '電影幾點開始？(A)(B)(C) 七點半／它是關於一隻狗的／和我姊姊（妹妹）一起。', '問「幾點」開始，要回答時間。')
text_item(5, [('N', 'Can I borrow your eraser?')], 'Sure, here you are.', ["I'm fine, thanks.", "It's on Monday."],
          '我可以跟你借橡皮擦嗎？', '別人向你借東西時，答應並遞給對方，說 Sure, here you are.（當然，給你）。')
text_item(6, [('N', 'How often do you go swimming?')], 'Twice a week.', ['For two hours.', 'At the pool.'],
          '你多久去游泳一次？', 'How often 問「頻率」，要回答多久一次，例如 twice a week（一星期兩次）。For two hours 回答的是「多久時間」。')
text_item(7, [('N', "You look tired. What's wrong?")], 'I stayed up late to study for the test.', ['Yes, I like it.', "It's not far from here."],
          '你看起來很累，怎麼了？', '對方關心你為什麼累，要說明原因：為了準備考試熬夜。')
text_item(8, [('N', 'Would you like some more cake?')], "No, thanks. I'm full.", ['Yes, I did.', 'I made it yesterday.'],
          '你還想再吃一些蛋糕嗎？', 'Would you like…? 是詢問要不要，可以回答 Yes, please. 或 No, thanks.，並說明原因「我吃飽了」。Yes, I did. 的時態不對。')
text_item(9, [('N', 'Which bus goes to the train station?')], 'Take Bus 12.', ['It takes ten minutes.', 'I usually walk.'],
          '哪一班公車會到火車站？', '問「哪一班」公車，要回答公車的號碼：搭 12 號公車。')
text_item(10, [('N', 'Congratulations on winning the contest!')], 'Thank you. I practiced a lot.', ["Don't worry about it.", 'Nice to meet you.'],
          '恭喜你贏得比賽！', '別人恭喜你時，要向對方道謝。')
text_item(11, [('N', 'Excuse me, is anyone sitting here?')], "No, it's free. Go ahead.", ["I'm sorry to hear that.", "Yes, I'll have one."],
          '不好意思，這裡有人坐嗎？', '對方問這個座位有沒有人坐，回答「沒有，是空位，請坐」最適當。')

# 第三部分：言談理解
text_item(12, [('W', 'Tom, can you help me carry these boxes to the car?'),
               ('M', 'Sure, Mom. But can I finish this game first? It will only take five minutes.'),
               ('W', 'OK, but only five minutes. We have to leave at four.'),
               ('Q', 'What will Tom do first?')],
          'Finish his game.', ['Carry the boxes.', 'Leave the house.'],
          '女：Tom，你可以幫我把這些箱子搬到車上嗎？男：好啊，媽。但我可以先把這場遊戲玩完嗎？只要五分鐘。女：好，但只能五分鐘，我們四點要出門。問題：Tom 會先做什麼？',
          'Tom 請媽媽讓他先把遊戲玩完（finish this game first），媽媽答應了，所以他會先玩完遊戲，再搬箱子。')
price, second = 300, 300 // 2
text_item(13, [('M', 'Excuse me, how much is this T-shirt?'),
               ('W', "It's three hundred dollars. But if you buy two, you get the second one for half price."),
               ('M', "Great. I'll take two, then."),
               ('Q', 'How much will the man pay?')],
          f'{price + second} dollars.', ['300 dollars.', '600 dollars.'],
          '男：不好意思，這件 T 恤多少錢？女：300 元。但如果買兩件，第二件半價。男：太好了，那我買兩件。問題：這位男子要付多少錢？',
          f'第一件 300 元，第二件半價 150 元，共 300＋150＝{price + second} 元。')
text_item(14, [('W', 'Did you watch the baseball game last night?'),
               ('M', "No, I didn't. My little brother was sick, so I took care of him."),
               ('W', 'Oh, is he better now?'),
               ('M', 'Yes, he went back to school today.'),
               ('Q', "Why didn't the man watch the game?")],
          'He was taking care of his brother.', ['He was sick.', 'He had to go to school.'],
          '女：你昨晚有看棒球比賽嗎？男：沒有。我弟弟生病了，所以我在照顧他。女：喔，他好一點了嗎？男：好了，他今天回學校上課了。問題：男子為什麼沒有看比賽？',
          '男子說弟弟生病，他在照顧弟弟（took care of him），所以沒看比賽。生病的是弟弟，不是他自己。')
text_item(15, [('W', "Attention, please. Because of the heavy rain, today's outdoor sports day will be moved to next Friday. All classes will be held as usual this afternoon. Please remember to bring your sports clothes next Friday."),
               ('Q', 'What will the students do this afternoon?')],
          'Have their usual classes.', ['Have their sports day.', 'Go home early.'],
          '女：請注意。因為下大雨，今天的戶外運動會將延到下星期五舉行。今天下午所有的課程照常上課。請記得下星期五帶運動服。問題：學生今天下午要做什麼？',
          '廣播說運動會延到下星期五，今天下午照常上課（classes will be held as usual）。')
text_item(16, [('M', "I'm thinking of getting a dog."),
               ('W', 'That sounds great, but dogs need a lot of time. You have to walk them every day.'),
               ('M', "I know. That's why I'm waiting until summer vacation. I'll have more free time then."),
               ('Q', 'When will the man most likely get a dog?')],
          'During summer vacation.', ['Today.', 'Next weekend.'],
          '男：我在考慮養一隻狗。女：聽起來很棒，但狗需要很多時間，你每天都要遛牠。男：我知道，所以我要等到暑假，那時我會有比較多空閒時間。問題：男子最可能什麼時候養狗？',
          '男子說要等到暑假（waiting until summer vacation），那時比較有空。')
text_item(17, [('W', 'Excuse me, where is the library?'),
               ('M', "Go straight down this street and turn left at the second corner. It's next to the post office."),
               ('W', 'Next to the post office. Thank you.'),
               ('Q', 'Where is the library?')],
          'Next to the post office.', ['At the first corner.', 'Across from the school.'],
          '女：不好意思，圖書館在哪裡？男：沿著這條街直走，在第二個轉角左轉，它就在郵局旁邊。女：在郵局旁邊，謝謝。問題：圖書館在哪裡？',
          '男子說圖書館在郵局旁邊（next to the post office），要在第二個轉角左轉，不是第一個。')
text_item(18, [('M', 'Mia, you look happy today.'),
               ('W', 'I am! I just got the results of the English speech contest. I got second place.'),
               ('M', 'Wow, congratulations! Who got first place?'),
               ('W', 'My best friend, Amy. We practiced together every day.'),
               ('Q', 'What do we know about Mia?')],
          'Her friend did better than she did.', ['She got first place.', 'She practiced alone.'],
          '男：Mia，妳今天看起來很開心。女：對啊！我剛拿到英語演講比賽的結果，我得到第二名。男：哇，恭喜！第一名是誰？女：我最好的朋友 Amy，我們每天一起練習。問題：關於 Mia，我們知道什麼？',
          'Mia 得到第二名，第一名是她的好朋友 Amy，所以她的朋友表現得比她好。她們是一起練習的。')
text_item(19, [('W', "Good morning! Here's today's weather. It will be sunny in the morning, but it will get cloudy in the afternoon, and there may be thunderstorms in the evening. If you go out tonight, don't forget your umbrella."),
               ('Q', 'What will the weather be like in the evening?')],
          'There may be thunderstorms.', ['It will be sunny.', 'It will be cloudy but dry.'],
          '女：早安！以下是今天的天氣。上午是晴天，下午會轉為多雲，晚上可能有雷雨。如果你今晚要出門，別忘了帶傘。問題：晚上的天氣會是什麼樣子？',
          '氣象報告說晚上可能有雷雨（thunderstorms in the evening），所以提醒出門帶傘。晴天是上午的天氣。')
text_item(20, [('M', 'Grandma, I want to try your recipe for beef noodles.'),
               ('W', "It's easy, but the most important thing is time. You have to cook the beef slowly for at least two hours."),
               ('M', 'Two hours? I thought thirty minutes was enough.'),
               ('W', "No. The beef won't be soft if you hurry."),
               ('Q', 'What does Grandma say is the most important thing?')],
          'Cooking the beef slowly for a long time.', ['Buying expensive beef.', 'Cooking the beef for thirty minutes.'],
          '男：奶奶，我想試試您的牛肉麵食譜。女：很簡單，但最重要的是時間，牛肉要用小火慢慢煮至少兩個小時。男：兩個小時？我以為三十分鐘就夠了。女：不行，太急的話牛肉不會軟。問題：奶奶說最重要的是什麼？',
          '奶奶說最重要的是時間，牛肉要慢慢煮至少兩小時。三十分鐘是孫子原本以為的時間。')
text_item(21, [('M', 'Have you finished your science report?'),
               ('W', 'Not yet. I used an AI chatbot to find information, but some of it was wrong, so I had to check everything in books.'),
               ('M', 'That sounds like a lot of work.'),
               ('W', 'It is, but now I understand the topic much better.'),
               ('Q', 'What did the woman learn from writing her report?')],
          'She should check the information from AI.', ['AI chatbots are always right.', 'Books are not useful.'],
          '男：妳的自然科報告寫完了嗎？女：還沒。我用 AI 聊天機器人找資料，但有些資料是錯的，所以我必須用書本把所有內容查證一遍。男：聽起來很費工夫。女：是啊，但現在我對這個主題了解得更多了。問題：這位女子從寫報告中學到了什麼？',
          '女子發現 AI 給的資料有些是錯的，所以要用書本查證，也就是 AI 的資訊需要查證。她是用書本查證，所以書本是有用的。')

assert [i['qNo'] for i in items] == list(range(1, 22))
assert len(TARGET) == 21 and all(TARGET.count(L) == 7 for L in 'ABC')
data = {
    'set': 'AI-1', 'year': 901, 'subject': '英聽', 'title': 'AI-1 英語（聽力）模擬卷',
    'note': '由 AI 依心測中心英語聽力架構（辨識句意 3 題、基本問答 8 題、言談理解 10 題，三選一）編寫，非會考真題；第一部分的圖片由程式繪製（tools/ai_sets/ai1_listening.py），語音以錄音稿合成（非會考原音）。',
    'groups': [],
    'items': items,
}
if os.path.exists(OUT):
    data['verification'] = json.load(open(OUT, encoding='utf-8')).get('verification', [])
json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', OUT, 'answers', ''.join(i['answer'] for i in items))
