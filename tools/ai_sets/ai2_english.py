"""AI-2 英文（閱讀，進階）: build src/data/ai/ai2_english.json.

Correct option first, distractors after; SetBuilder places the options by
TARGET and writes the letters ({c} {d0} {d1} {d2}) and 「故選」.
Each item carries its design level as a trailing comment (levels 2-5, see SPEC_AI2_AI3.md).

  PYTHONIOENCODING=utf-8 python tools/ai_sets/ai2_english.py
"""
from common import SetBuilder, spread_target

TOPICS = [
    'Alex Honnold 徒手攀登台北 101（2026-01-25，因雨延後一天、約 1.5 小時、Netflix 延遲約 10 秒直播；Alain Robert 2004 年用安全繩約 4 小時；台北 101 在 2010 年杜拜哈里發塔啟用前為世界最高）：https://en.wikipedia.org/wiki/Skyscraper_Live_(2026)',
    'Honnold 攀登時間約 1 小時 31 分：https://scmp.com/sport/outdoor/extreme-sports/article/3341157/us-climber-hopes-ascent-taipei-101-inspires-others-use-time-most-meaningful-way',
    '星際彗星 3I/ATLAS（2025-07-01 智利 ATLAS 望遠鏡發現、第三個星際天體、距地球最近約 2.7 億公里、火星軌道探測器觀測）：https://science.nasa.gov/solar-system/comets/3i-atlas/',
    '3I/ATLAS 速度約每秒 60 公里、前兩個星際天體 2017 ʻOumuamua、2019 Borisov：https://www.sci.news/astronomy/interstellar-object-3i-atlas-14041.html',
    '珍古德 2025-10-01 逝世（91 歲、美國巡迴演講中）、1960 年 26 歲赴坦尚尼亞 Gombe、無大學學位、為黑猩猩命名、工具使用發現、1991 年創 Roots & Shoots（多年來擴及一百多國）：https://en.wikipedia.org/wiki/Jane_Goodall',
    'Gombe 黑猩猩研究至 2025 年持續 65 年：https://news.janegoodall.org/2025/07/08/gombe-chimpanzee-research-65-year/',
    '珍古德逝世報導：https://www.scrippsnews.com/obituaries/primatologist-jane-goodall-has-died-at-age-91',
    '科學博物館夜間活動、農場體驗廣告與 email、學習手語、圖書館留言、營養午餐廚餘實驗、「無聊」的好處：虛構生活情境',
]

b = SetBuilder('ai2_english', '英文', year=902, set_name='AI-2',
               title='AI-2 英語（閱讀）模擬卷（進階）',
               note='由 AI 依會考英語科架構編寫（單題：需讀懂前後文的字彙語法；題組：篇章理解，含克漏字與雙文本），'
                    '難度較會考略高：推論、指涉、作者目的、整合文字與表格、把文章的規則套用到新情況，並以 2025–2026 年真實事件為素材；非會考真題。',
               target=spread_target(43, 4, 902), difficulty='進階', topics=TOPICS)

# ======================================================================
# 單題 1–15：每題都要讀懂兩句或對話的前後文；誘答單看文法都通，放進語境才錯
# ======================================================================
b.item('Ms. Lee ______ at our school for twenty years, so she knows almost every family in the neighborhood. She says she will keep teaching here until she retires.',  # L3
       'has taught', ['taught', 'will teach', 'was teaching'],
       '【中譯】李老師在我們學校教了二十年，所以她幾乎認識這一帶的每個家庭。她說她會繼續在這裡教到退休。\n'
       '【解析】她「到現在」已經教了二十年，而且還要繼續教，要用現在完成式 has taught。'
       '({d0}) taught 單看句子沒錯，但表示「過去教過、現在不教了」，與第二句「會繼續教」矛盾；({d1}) will teach 是未來，無法說明她現在認識每個家庭；({d2}) was teaching 是過去進行式，同樣表示已經不在這裡教。')

b.item('A: You must be tired after hiking for six hours.\nB: ______ I could walk another ten kilometers right now!\nA: Wow, you\'re in great shape.',  # L3
       'Not at all.', ['Yes, very.', 'So am I.', 'Neither am I.'],
       '【中譯】A：走了六小時的山路，你一定很累了吧。B：一點也不。我現在還能再走十公里！A：哇，你體能真好。\n'
       '【解析】B 接著說「還能再走十公里」，A 也稱讚他體能好，可見 B 並不累，用 Not at all.（一點也不）。'
       '({d0}) Yes, very. 表示很累，與後文矛盾；({d1}) So am I. 是附和「我也是」，但 A 並沒有說自己的狀況；({d2}) Neither am I. 用來附和否定句，A 的話是肯定句。')

b.item('My sister and I both entered the school drawing contest. ______ won a prize, but our art teacher said our pictures were the most creative ones in the whole contest.',  # L3
       'Neither of us', ['Both of us', 'Each of us', 'One of us'],
       '【中譯】我和妹妹都參加了學校的繪畫比賽。我們兩個都沒得獎，但美術老師說我們的畫是整個比賽中最有創意的。\n'
       '【解析】but 表示轉折：「沒得獎，但老師稱讚很有創意」才是合理的對比，用 Neither of us。'
       '({d0}) Both of us、({d1}) Each of us 都表示兩人都得獎，後面就不需要用 but 來安慰；({d2}) One of us 表示有一人得獎，後半句卻稱讚「我們兩人」的畫，也構不成轉折。')

b.item('I thought the test would be really difficult, so I studied until midnight. ______, it was the easiest test of the year, and I finished it in twenty minutes.',  # L3
       'However', ['As a result', 'In other words', 'For example'],
       '【中譯】我以為考試會很難，所以讀到半夜。然而，那是今年最簡單的一次考試，我二十分鐘就寫完了。\n'
       '【解析】「以為很難」和「結果是最簡單的」相反，用 However。'
       '({d0}) As a result 是常見誤選：讀到半夜不會「造成」考試變簡單；({d1}) In other words 用來換句話說，但前後意思相反；({d2}) For example 後面要接例子。')

b.item('You ______ bring your own lunch on the field trip. The museum café sells sandwiches and drinks, but you can bring food from home if you want to.',  # L3
       "don't have to", ['must not', 'have to', "can't"],
       '【中譯】校外教學你不必自己帶午餐。博物館的咖啡廳有賣三明治和飲料，不過如果你想，也可以從家裡帶食物。\n'
       '【解析】「可以買，也可以帶」——帶午餐是可做可不做的事，用 don\'t have to（不必）。'
       '({d0}) must not 和 ({d2}) can\'t 都是「不准」，與「想帶也可以帶」矛盾；({d1}) have to 是「必須」，與「咖啡廳有賣」不合。')

b.item("When the phone rang, I ______ a shower, so I couldn't answer it. I called my friend back ten minutes later.",  # L3
       'was taking', ['took', 'take', 'have taken'],
       '【中譯】電話響的時候我正在洗澡，所以沒辦法接。十分鐘後我回撥給朋友。\n'
       '【解析】電話響時「正在進行」的動作用過去進行式 was taking，也才能解釋為什麼不能接電話。'
       '({d0}) took 單看沒錯，但 When the phone rang, I took a shower 表示「電話響了以後才去洗澡」，接不上「所以沒辦法接」；({d1}) take、({d2}) have taken 時態不對。')

b.item('A: Did you lock the front door when we left?\nB: Yes, I clearly remember ______ it. I even checked it twice.',  # L3
       'locking', ['to lock', 'lock', 'locked'],
       '【中譯】A：我們出門時你有鎖前門嗎？B：有，我清楚記得鎖了門，我還檢查了兩次。\n'
       '【解析】remember V-ing 是「記得做過某事」，remember to V 是「記得要去做某事」。門已經鎖了，是回想過去的動作，用 locking。'
       '({d0}) to lock 表示還沒做、要記得去做，與「還檢查了兩次」矛盾；({d1}) lock、({d2}) locked 不能直接接在 remember 後面。')

b.item("A: Do you know ______?\nB: Not exactly, but I think it's somewhere near the train station.",  # L3
       'where the new library is', ['when the new library opens', 'who designed the new library', 'why the new library is closed'],
       '【中譯】A：你知道新圖書館在哪裡嗎？B：不太確定，不過我想大概在火車站附近。\n'
       '【解析】四個選項都是語序正確的間接問句，要看 B 的回答：「在火車站附近」是地點，所以 A 問的是 where。'
       '({d0}) 問時間、({d1}) 問人、({d2}) 問原因，都和「在火車站附近」對不上。')

b.item("A: I don't think I'll pass the math test tomorrow.\nB: ______ You've been practicing every day for a month.",  # L3
       "Don't worry. You'll do fine.", ["I don't think so, either.", "That's too bad.", 'Me too.'],
       '【中譯】A：我覺得我明天數學考試會不及格。B：別擔心，你會考得很好的。你已經每天練習一個月了。\n'
       '【解析】B 接著說「你已經每天練習一個月了」，是在鼓勵 A，所以前面應該是安慰的話。'
       '({d0}) I don\'t think so, either 是附和 A「我也認為你不會過」，與鼓勵矛盾；({d1}) That\'s too bad 是對已發生的壞事表示遺憾；({d2}) Me too 表示自己也會不及格，接不上後句。')

b.item("A: I've never been to Kinmen.\nB: ______ Let's go there together this summer!",  # L3
       'Neither have I.', ['So have I.', 'Neither do I.', 'I have, too.'],
       '【中譯】A：我從來沒去過金門。B：我也沒去過。我們今年夏天一起去吧！\n'
       '【解析】附和否定句「我也沒有」用 Neither＋助動詞＋主詞；A 用的是現在完成式 have never been，所以說 Neither have I. '
       '({d0}) So have I. 附和肯定句；({d1}) Neither do I. 助動詞錯誤；({d2}) I have, too. 表示「我也去過」，與 A 的否定句不合。')

b.item("I lost my umbrella on the bus yesterday, so I bought ______ this morning. It's red, just like the one I lost.",  # L3
       'a new one', ['it', 'the one', 'that'],
       '【中譯】我昨天把傘掉在公車上了，所以今天早上買了一把新的。它是紅色的，跟我掉的那把一樣。\n'
       '【解析】買的是「另一把同類的傘」，用不定代名詞 one：a new one。'
       '({d0}) it 和 ({d2}) that 指的是「同一把」——也就是掉在公車上的那把傘，不可能再去買它；({d1}) the one 後面需要說明是哪一把，而且同樣是指特定的那一把。')

b.item("There ______ a bookstore on this corner. Now it's a coffee shop, but I still miss the smell of the old books.",  # L3
       'used to be', ['is', 'will be', 'has been'],
       '【中譯】這個轉角以前有一家書店。現在變成咖啡店了，但我還是懷念那些舊書的味道。\n'
       '【解析】「以前是書店，現在是咖啡店」，表示過去的狀態，用 used to be。'
       '({d0}) is 表示現在還有書店；({d1}) will be 是未來；({d2}) has been 表示到現在一直都是書店。三者都與「現在是咖啡店」矛盾。')

b.item('You can borrow my notes ______ you give them back before Friday. I need them to study for the test on Saturday.',  # L4
       'as long as', ['unless', 'even though', 'because'],
       '【中譯】只要你在星期五之前還我，就可以借我的筆記。我需要用它們準備星期六的考試。\n'
       '【解析】「星期五前還」是借筆記的條件，用 as long as（只要）。'
       '({d0}) unless 是「除非」，變成「如果你星期五前『不』還才可以借」，意思相反，是最容易誤選的選項；({d1}) even though（即使）不表示條件；({d2}) because 表示原因，說不通。')

b.item('Dad turned the TV down ______ the baby could sleep. He watched the rest of the game with almost no sound.',  # L3
       'so that', ['because', 'although', 'unless'],
       '【中譯】爸爸把電視音量調小，好讓寶寶可以睡覺。他幾乎是無聲地看完剩下的比賽。\n'
       '【解析】調小音量的「目的」是讓寶寶能睡，用 so that。'
       '({d0}) because 變成「因為寶寶能睡，所以調小聲」，因果顛倒；({d1}) although 表示讓步，不合；({d2}) unless 是「除非」，說不通。')

b.item('Grandpa is not as ______ as he looks. He may be seventy-five, but he still swims a kilometer every morning.',  # L4
       'weak', ['strong', 'healthy', 'active'],
       '【中譯】爺爺不像他外表看起來那麼虛弱。他也許七十五歲了，但每天早上還是游一公里。\n'
       '【解析】not as … as he looks 是「不像看起來那麼……」；第二句說他七十五歲還天天游泳，表示他其實很強健，所以是「沒有看起來那麼虛弱」。'
       '({d0}) strong、({d1}) healthy、({d2}) active 放進去都變成「他沒有看起來那麼強壯／健康／活躍」，與每天游一公里矛盾。這題要同時處理否定和比較。')

# ======================================================================
# 16–17 博物館夜間活動公告（表格＋規則）
# ======================================================================
b.group(16, 17, """Riverside Science Museum
Night at the Museum — every Friday in July and August, 6:00–10:00 p.m.
Ever wondered what a science museum is like after dark? Grab a flashlight, follow the clues on our Mystery Trail, and meet our scientists at the Ask-Me tables, where you can ask them any science question you like. At 8:00, join us on the roof to look at the stars and planets through our big telescope. Hungry? Light meals and drinks are sold in the first-floor café until 9:30 p.m., but no food is allowed in the exhibition rooms.
| Ticket | Price |
| Adult (18 and over) | NT$300 |
| Student (12–17, student card needed) | NT$200 |
| Child (6–11) | NT$150 |
| Child under 6 | Free |
• Family Ticket (2 adults + up to 2 children aged 6–11): NT$750
• Museum members get 20% off every ticket they buy (up to 4 tickets). This discount cannot be used with the Family Ticket.
• Stargazing on the roof happens only when the sky is clear. On cloudy or rainy nights, we will show a film about the night sky in our Space Theater instead.
• The Mystery Trail goes through dark rooms and up many stairs, so it is not suitable for children under 8.
• Tickets can be bought online or at the front desk. Online tickets must be bought by 3:00 p.m. on the day of the event.""",
        translation="""河濱科學博物館
博物館之夜——七、八月每個星期五，晚上 6:00–10:00
想知道科學博物館天黑以後是什麼樣子嗎？拿起手電筒，跟著「神祕小徑」的線索走，並到「問我吧」桌和我們的科學家見面，你想問什麼科學問題都可以問他們。8:00 請到屋頂，用我們的大型望遠鏡觀賞星星和行星。肚子餓了嗎？一樓咖啡廳供應輕食和飲料到晚上 9:30，但展覽室內禁止飲食。
票種｜票價
成人（18 歲以上）｜新臺幣 300 元
學生（12–17 歲，須出示學生證）｜新臺幣 200 元
兒童（6–11 歲）｜新臺幣 150 元
未滿 6 歲兒童｜免費
• 家庭票（2 位成人＋最多 2 位 6–11 歲兒童）：新臺幣 750 元
• 博物館會員購買的每張票都打八折（最多 4 張）。此折扣不能與家庭票合併使用。
• 屋頂觀星只在天氣晴朗時舉行；陰天或雨天時，改在太空劇場播放一部關於夜空的影片。
• 神祕小徑會經過黑暗的展間並要爬很多樓梯，因此不適合未滿 8 歲的兒童。
• 門票可在網路或服務臺購買。網路購票須在活動當天下午 3:00 前完成。""")

b.item('Which of the following plans would NOT work?',  # L4
       'Buying tickets online at 5 p.m. on the day of the event.',
       ['Buying tickets at the front desk at 7 p.m. on the day of the event.',
        'Watching a film about the night sky on a rainy Friday night.',
        'Bringing a four-year-old child without paying for a ticket.'],
       '【中譯】下列哪一個計畫「行不通」？\n'
       '【解析】網路購票必須在活動當天下午 3:00 前完成，下午 5 點上網買票已經來不及。'
       '({d0}) 3:00 的限制只適用於「網路」購票，服務臺沒有這個限制，晚上 7 點活動還在進行；({d1}) 雨天會改在太空劇場播放夜空影片；({d2}) 未滿 6 歲兒童免費。')

adult, child = 300, 150
member = round((2 * adult + 2 * child) * 0.8)      # 4 tickets, 20% off each
family = 750
b.item('Mr. Lin is a museum member. He wants to bring his wife (not a member) and their two children, aged 8 and 10. What is the lowest total price he can pay for the four tickets?',  # L5
       f'NT${member:,}', [f'NT${family:,}', f'NT${2 * adult + 2 * child:,}', f'NT${round(family * 0.8):,}'],
       '【中譯】林先生是博物館會員，他想帶太太（不是會員）和 8 歲、10 歲的兩個孩子去。四張票最少要付多少錢？\n'
       '【解析】有兩種買法：(1) 家庭票 750 元；(2) 由會員林先生購買四張單人票，每張都打八折：(300＋300＋150＋150)×0.8＝720 元。720 元比較便宜。'
       '注意折扣是「會員購買的每張票」（最多 4 張），不是只有會員自己那張。'
       '({d0}) 750 元是家庭票，看起來最划算，但沒有算會員折扣；({d1}) 900 元是全部原價；({d2}) 600 元是把家庭票再打八折，但公告說折扣不能與家庭票合併使用。',
       check=(member == 720, [family == 720, 2 * adult + 2 * child == 720, round(family * 0.8) == 720]))

# ======================================================================
# 18–20 Alex Honnold 徒手攀登台北 101（時事）
# ======================================================================
b.group(18, 20, """On the morning of January 25, 2026, people around the world held their breath as American climber Alex Honnold began to climb the outside of Taipei 101—without a rope. The 508-meter building was the tallest in the world until the Burj Khalifa opened in Dubai in 2010, and in 2026 it was still the tallest in Taiwan.
Honnold, then 40, is famous for "free soloing": climbing with only his hands and feet and no safety equipment at all. In 2017, he became the first person to free solo El Capitan, a huge rock wall in the United States. Before Taipei 101, almost all of his famous climbs had been on natural rock, so a skyscraper of glass and metal was a very different kind of challenge. The climb was planned for January 24, but it was put off for a day because of rain.
The climb was shown live on Netflix. However, the broadcast was not completely "live." It ran about ten seconds behind real time. That way, the people running the show could stop the pictures if anything terrible happened.
Honnold reached the top in about an hour and a half. He was not the first person to climb the building, though. In 2004, French climber Alain Robert had done it too, but he used a safety rope, and it took him about four hours in heavy rain.
Not everyone enjoyed the show. Some viewers said that watching one man climb for ninety minutes became boring after a while, and others complained that the hosts talked too much. Still, for many people in Taiwan, it was a proud moment to see a building they knew so well become the stage for one of the world's most famous climbers.
* skyscraper 摩天大樓；broadcast 播出的節目""",
        translation="""2026 年 1 月 25 日早上，美國攀岩家艾力克斯．霍諾德開始在不用繩索的情況下攀爬台北 101 的外牆，全世界的人都屏住了呼吸。這棟 508 公尺高的大樓在 2010 年杜拜的哈里發塔啟用之前是世界最高的建築，2026 年時仍是臺灣最高的大樓。
當時 40 歲的霍諾德以「徒手獨攀」聞名：只用手和腳攀爬，完全不用任何安全裝備。2017 年，他成為第一個徒手獨攀美國巨大岩壁「酋長岩」的人。在台北 101 之前，他著名的攀登幾乎都是在天然岩壁上，所以一棟由玻璃和金屬構成的摩天大樓是完全不同的挑戰。這次攀登原訂在 1 月 24 日，但因為下雨延後了一天。
這次攀登在 Netflix 上直播。不過，這個節目並不是完全「即時」的，它比實際時間晚大約十秒播出。這樣一來，萬一發生可怕的事，製作節目的人就能把畫面切掉。
霍諾德大約花了一個半小時登頂。不過，他並不是第一個爬上這棟大樓的人。2004 年，法國攀岩家亞倫．羅伯特也爬過，但他用了安全繩，而且在大雨中花了大約四個小時。
並不是每個人都喜歡這個節目。有些觀眾說，看一個人爬九十分鐘，看久了會覺得無聊；也有人抱怨主持人話太多。儘管如此，對許多臺灣人來說，看到一棟自己這麼熟悉的大樓成為世界知名攀岩家的舞臺，是令人驕傲的一刻。""")

b.item('In the third paragraph, what does "That way" refer to?',  # L3
       'Showing the climb about ten seconds after it really happened.',
       ['Showing the climb live on Netflix to people around the world.',
        'Putting off the climb for one day because of the rain.',
        'Climbing without a rope or any other safety equipment.'],
       '【中譯】第三段的 That way（這樣一來）指的是什麼？\n'
       '【解析】That way 緊接在 It ran about ten seconds behind real time 之後，指「比實際時間晚約十秒播出」，這樣萬一出事才來得及切掉畫面。'
       '({d0}) 只說到「在 Netflix 直播」，但真正的直播無法切掉畫面，是只對了一半的選項；({d1}) 延期是第二段的事；({d2}) 不用繩索是攀登方式，不能讓製作單位切掉畫面。')

b.item('Why does the writer mention Alain Robert?',  # L4
       "To show how special Honnold's climb was by comparing the two climbs.",
       ['To prove that Taipei 101 is not very hard to climb.',
        "To explain why Honnold's climb was put off for a day.",
        'To show that Robert was a braver climber than Honnold.'],
       '【中譯】作者為什麼提到亞倫．羅伯特？\n'
       '【解析】羅伯特用了安全繩、花了約四小時；霍諾德不用繩索、約一個半小時就登頂。作者用對比凸顯霍諾德這次攀登的不凡。'
       '({d0}) 兩人都爬得上去，並不表示大樓很好爬，文中反而強調這是很不同的挑戰；({d1}) 延期是因為下雨，與羅伯特無關；({d2}) 羅伯特有用安全繩，文意並非說他比較勇敢。')

b.item('Which of the following is true according to the reading?',  # L4
       'Viewers saw each moment of the climb about ten seconds after it actually happened.',
       ['Honnold needed about four hours to reach the top in heavy rain.',
        'Honnold was the first person ever to climb the outside of Taipei 101.',
        'Before Taipei 101, most of Honnold\'s famous climbs had been on buildings.'],
       '【中譯】根據本文，下列何者正確？\n'
       '【解析】第三段說節目比實際時間晚約十秒播出，所以觀眾看到的每個畫面都是約十秒前發生的事。'
       '({d0}) 「大雨中約四小時」是 2004 年羅伯特的紀錄，霍諾德只花約一個半小時——細節正確但人物錯誤；({d1}) 文中明說他「不是第一個」爬上這棟大樓的人；({d2}) 他著名的攀登幾乎都在「天然岩壁」上。')

# ======================================================================
# 21–23 雙文本：農場體驗廣告＋email
# ======================================================================
b.group(21, 23, """[Advertisement]
Green Hill Farm Weekends — Yilan
Get out of the city and spend two days and one night on a real farm!
| Plan | What you'll do | Price per person |
| A: Rice Field | plant rice in the muddy fields, ride bikes along the river, cook dinner with the farmer | NT$2,400 |
| B: Tea Hill | pick tea leaves, make your own tea, hike to a waterfall | NT$2,800 |
| C: Animal Friends | feed the goats and rabbits, collect eggs, make cheese from goat's milk | NT$2,600 |
• All plans run on weekends from March to June. Plan B is not available in June because the tea-picking season ends in May.
• Groups of five or more get NT$200 off per person.
• Please book at least 7 days before your trip.

[Email]
From: Hannah
To: Cheng-en
Subject: Our farm trip!
Hi Cheng-en,
I found the farm my cousin was talking about—see the ad above! Since the three of us all have summer classes starting in June, our only free weekend is May 23–24. Leo says any plan is fine with him as long as he doesn't have to stand in mud. You know how much he hates getting his feet dirty! And you sneeze all day whenever you're near animals with fur, so I think there's really only one choice for us.
Oh, and could you ask Mia if she wants to come too? If she does, I think the farm will give us a group discount, so it'll be cheaper for all of us.
Hannah""",
        translation="""【廣告】
綠丘農場週末遊——宜蘭
離開城市，到真正的農場住兩天一夜！
方案｜活動內容｜每人價格
A：稻田｜在泥濘的田裡插秧、沿著河邊騎腳踏車、和農夫一起煮晚餐｜新臺幣 2,400 元
B：茶山｜採茶、自己製茶、健行到瀑布｜新臺幣 2,800 元
C：動物朋友｜餵山羊和兔子、撿雞蛋、用羊奶做起司｜新臺幣 2,600 元
• 所有方案在三月到六月的週末舉行。B 方案六月不開放，因為採茶季在五月結束。
• 五人以上的團體每人折抵 200 元。
• 請在出發前至少 7 天預訂。

【電子郵件】
寄件人：Hannah
收件人：Cheng-en
主旨：我們的農場之旅！
嗨，Cheng-en：
我找到我表姊說的那個農場了——看上面的廣告！因為我們三個六月都要開始上暑期課程，我們唯一有空的週末是 5 月 23–24 日。Leo 說只要不必站在泥巴裡，哪個方案他都可以。你知道他有多討厭把腳弄髒！而你只要靠近有毛的動物就會打噴嚏打一整天，所以我想我們其實只有一個選擇。
對了，你可以問問 Mia 要不要一起來嗎？如果她要來，我想農場會給我們團體折扣，這樣我們每個人都會比較便宜。
Hannah""")

b.item('Which plan will Hannah and her friends most likely choose?',  # L4
       'Plan B: Tea Hill', ['Plan A: Rice Field', 'Plan C: Animal Friends', 'None of them, because no plan is open in May.'],
       '【中譯】Hannah 和她的朋友最可能選哪個方案？\n'
       '【解析】要整合兩份資料：Leo 不想站在泥巴裡，排除要在泥濘田裡插秧的 A 方案；Cheng-en 靠近有毛的動物會打噴嚏，排除要餵山羊和兔子的 C 方案；他們的時間是 5 月 23–24 日，B 方案只有六月不開放，五月可以參加，所以只剩 B 方案。'
       '({d0}) A 要站在泥田裡；({d1}) C 有山羊和兔子；({d2}) 所有方案三月到六月都有，五月是開放的。')

price = 2800                                   # Plan B, 4 people: the discount starts at five
b.item('If Mia joins them, how much will each person pay?',  # L5
       f'NT${price:,}', ['NT$2,600', 'NT$2,400', 'NT$2,200'],
       '【中譯】如果 Mia 加入，每個人要付多少錢？\n'
       '【解析】Hannah 以為 Mia 加入就有團體折扣，但廣告寫的是「五人以上」才每人折 200 元。Hannah、Cheng-en、Leo 加上 Mia 只有四人，沒有折扣，所以 B 方案每人仍是 2,800 元。'
       '({d0}) 2,600 元是相信了 Hannah 的說法、扣掉 200 元，但四人不符合折扣條件，是本題的陷阱；({d1}) 2,400 元是 A 方案原價；({d2}) 2,200 元是 A 方案打折後的價格。',
       check=(price == 2800, [2600 == price, 2400 == price, 2200 == price]))

b.item('Suppose the friends could only go on the weekend of June 6–7 instead. Which statement would be true?',  # L4
       'None of the three plans would work for all of them.',
       ['Plan B would still be their best choice.',
        'Plan A would be fine, because Leo enjoys riding bikes.',
        'Plan C would be fine, because only Leo has a problem with it.'],
       '【中譯】假設他們只能在 6 月 6–7 日那個週末去，下列哪個說法會是正確的？\n'
       '【解析】六月 B 方案不開放；A 方案要站在泥田裡（Leo 不行）；C 方案有毛茸茸的動物（Cheng-en 不行）——三個方案都不適合所有人。'
       '({d0}) B 方案六月不開放；({d1}) A 方案雖然有騎腳踏車，但也要在泥田裡插秧，Leo 不願意；({d2}) 對 C 方案有問題的是 Cheng-en（對動物過敏），不是 Leo——人物錯置。')

# ======================================================================
# 24–26 星際彗星 3I/ATLAS（時事）
# ======================================================================
b.group(24, 26, """On July 1, 2025, a telescope in Chile spotted a faint object moving across the night sky. At first, it looked like an ordinary comet—a ball of ice and dust that grows a bright tail as it gets close to the Sun. But when scientists worked out its path, they realized something surprising: it did not belong to our solar system at all. It had come from the space between the stars.
The comet was named 3I/ATLAS. The "I" stands for "interstellar," which means "between the stars," and the "3" shows that it is only the third such visitor ever found. The first, 'Oumuamua, was discovered in 2017, and the second, Borisov, in 2019. ATLAS is the name of the telescope system that found it.
Why do visitors like this excite scientists so much? Every comet carries material from the place where it was formed. The comets of our own solar system tell us how our Sun and planets were born. 3I/ATLAS, however, was formed around a different star, perhaps billions of years ago. Studying it is a little like opening a letter from a faraway place that no one can travel to.
The comet was moving at about 60 kilometers per second—far too fast for the Sun's gravity to hold on to it. It will never come back. That gave scientists only a few months to study it before it disappeared into deep space, so telescopes on Earth and even spacecraft around Mars were turned toward it.
Some people online worried that it might hit Earth. It never came close: even at its nearest, it was about 270 million kilometers away.
* comet 彗星；gravity 重力；spacecraft 太空船""",
        translation="""2025 年 7 月 1 日，智利的一座望遠鏡發現一個黯淡的天體在夜空中移動。一開始，它看起來像一顆普通的彗星——一團冰和塵埃，靠近太陽時會長出明亮的尾巴。但科學家算出它的路徑後，發現了一件令人驚訝的事：它根本不屬於我們的太陽系，而是來自恆星與恆星之間的太空。
這顆彗星被命名為 3I/ATLAS。「I」代表 interstellar，意思是「星際的」；「3」表示它是有史以來發現的第三個這樣的訪客。第一個是 2017 年發現的 'Oumuamua，第二個是 2019 年發現的 Borisov。ATLAS 則是發現它的望遠鏡系統的名稱。
為什麼這樣的訪客讓科學家這麼興奮？每顆彗星都帶著它形成之處的物質。我們太陽系的彗星能告訴我們太陽和行星是怎麼誕生的；然而 3I/ATLAS 是在另一顆恆星周圍形成的，可能是在數十億年前。研究它有點像打開一封從沒有人能去的遠方寄來的信。
這顆彗星以每秒大約 60 公里的速度移動，快到太陽的重力根本抓不住它，它永遠不會再回來。這讓科學家只有幾個月的時間可以在它消失於深太空之前研究它，所以地球上的望遠鏡，甚至環繞火星的太空船都轉向了它。
網路上有些人擔心它會撞上地球。它從來沒有靠近過：即使在最近的時候，它離地球也大約有 2 億 7 千萬公里。""")

b.item('What does the writer mean by "opening a letter from a faraway place that no one can travel to"?',  # L3
       'Learning about another star system from the material the comet carries.',
       ['Reading messages sent by people who live near another star.',
        'Looking at photos sent back by spacecraft around Mars.',
        'Finding out how our own Sun and planets were born.'],
       '【中譯】作者說「打開一封從沒有人能去的遠方寄來的信」是什麼意思？\n'
       '【解析】這句話緊接在「每顆彗星都帶著形成之處的物質」「3I/ATLAS 是在另一顆恆星周圍形成的」之後，「信」比喻彗星帶來的物質，能讓我們了解另一個恆星系。'
       '({d0}) 把比喻當成真的有人寄信；({d1}) 火星附近的太空船是第四段的觀測工具；({d2}) 了解太陽和行星的誕生，是「我們太陽系的彗星」能告訴我們的，3I/ATLAS 帶來的是另一顆恆星的資訊——這是用文中句子拼成的半對選項。')

b.item('Which of the following can be inferred from the reading?',  # L4
       'No object from outside the solar system had been found before 2017.',
       ['3I/ATLAS is older than our solar system.',
        'Scientists were worried that 3I/ATLAS would hit Earth.',
        '3I/ATLAS will pass by Earth again after a few months.'],
       '【中譯】從本文可以推論出什麼？\n'
       '【解析】3I/ATLAS 是「有史以來第三個」星際訪客，而第一個 \'Oumuamua 是在 2017 年發現的，可見 2017 年以前從未發現來自太陽系外的天體。'
       '({d0}) 文中只說它「可能」在數十億年前形成，並沒有和太陽系的年齡比較，不能推知它比太陽系老（不要用課外印象作答）；({d1}) 擔心撞地球的是「網路上的一些人」，不是科學家；({d2}) 文中說它「永遠不會再回來」，「幾個月」是科學家能研究它的時間。')

b.item('According to the reading, why would scientists be excited if a fourth interstellar comet were found one day?',  # L4
       'It might carry material from yet another star system.',
       ['It would prove that comets from other stars can hit Earth.',
        'It would show how our own Sun and planets were born.',
        'It could be studied for many years because it would stay near the Sun.'],
       '【中譯】根據本文，如果有一天發現第四顆星際彗星，科學家為什麼會很興奮？\n'
       '【解析】把文章的道理套到新情況：彗星帶著它形成之處的物質，星際彗星形成於別的恆星周圍，所以新的星際彗星可能帶來「又一個」恆星系的資訊。'
       '({d0}) 文中沒有說星際彗星會撞地球；({d1}) 這是「我們太陽系的彗星」的價值；({d2}) 星際彗星速度太快，太陽的重力抓不住它，不會留下來讓人研究很多年。')

# ======================================================================
# 27–31 克漏字：學手語（篇章連貫）
# ======================================================================
b.group(27, 31, """When Yi-ting joined our class last fall, most of us didn't know how to talk to her. She was born deaf, and she uses Taiwanese Sign Language. At first, we just smiled and waved whenever we saw her. __27__, a smile alone is not enough to build a real friendship, and after a few weeks she usually ate lunch by herself.
One day, I asked her to teach me a few signs. She looked surprised, and then she laughed. __28__ The first sign she taught me was "friend," and I practiced it all the way home.
After that, a few other classmates started joining us at lunch. Yi-ting was a patient teacher, but she was also strict. If we made a sign too quickly or carelessly, she made us do it again. Later we found out why: __29__.
By the end of the semester, ten of us could have simple conversations with her. Our homeroom teacher was so impressed that she invited a sign language teacher to give the whole class a lesson.
Now, whenever I see people signing to each other on the MRT, I no longer look away. __30__, I try to catch a word or two that I know. I used to think Yi-ting was the one who needed to learn how to fit in with us. Now I know it was the other way around: __31__.
* deaf 聽障的；sign 手語的手勢；sign language 手語""",
        translation="""去年秋天怡婷轉進我們班的時候，我們大多數人都不知道怎麼跟她說話。她天生聽障，使用臺灣手語。一開始，我們每次看到她都只是微笑、揮手。然而，光靠微笑不足以建立真正的友誼，幾個星期後，她午餐通常都是一個人吃。
有一天，我請她教我幾個手語。她看起來很驚訝，接著笑了出來。後來她告訴我，以前從來沒有同學這樣問過她。她教我的第一個手語是「朋友」，我一路練習到回家。
在那之後，又有幾個同學開始在午餐時加入我們。怡婷是個有耐心的老師，但也很嚴格。如果我們比得太快或太隨便，她就會要我們重做。後來我們才知道原因：手的形狀只要稍微改變，就可能把一個詞變成完全不同的另一個詞。
到學期結束時，我們有十個人能和她進行簡單的對話。我們的導師非常佩服，還請了一位手語老師來幫全班上一堂課。
現在，每當我在捷運上看到有人用手語交談，我不再把視線移開；相反地，我會試著看懂一兩個我認得的詞。我以前以為怡婷才是需要學習如何融入我們的人。現在我知道事實正好相反：我們才是需要學習如何走近她的人。""")

b.item('', 'However', ['As a result', 'In other words', 'For example'],  # L3
       '【解析】前句說我們「只是微笑揮手」，後句說「光靠微笑不足以建立友誼」，她還常常一個人吃飯——前後是轉折，用 However。'
       '({d0}) As a result 表示結果，但「微笑不夠」不是「微笑揮手」造成的；({d1}) In other words 是換句話說，前後意思並不相同；({d2}) For example 後面要接例子。')

b.item('', 'Later she told me that no classmate had ever asked her that before.',
       ['She said she was too busy to teach anyone.',
        'Then she asked me to stop waving at her.',
        'That was the last time we ever talked.'],  # L4
       '【解析】空格前說她「很驚訝，接著笑了」，空格要解釋她為什麼驚訝：以前從來沒有同學問過她，才接得上下一句「她教我的第一個手語」。'
       '({d0}) 說她太忙不教，與下一句「她教我的第一個手語」矛盾；({d1}) 要我別再揮手，與前後文都接不上；({d2}) 說那是最後一次交談，與後文「後來同學也加入一起吃午餐」矛盾。')

b.item('', 'a small change in the shape of a hand can turn one word into a completely different one',
       ['she did not really want to teach us at all',
        'she wanted us to finish our lunch more quickly',
        'signing quickly is the most important skill in sign language'],  # L4
       '【解析】Later we found out why 要說明她「嚴格要我們重做比得太快或隨便的手勢」的原因：手形稍有不同就會變成別的詞，所以必須比正確。'
       '({d0}) 與「她是個有耐心的老師」矛盾；({d1}) 要我們重做只會讓午餐吃得更慢，說不通；({d2}) 她正是因為我們比得「太快」才要我們重做，與此相反。')

b.item('', 'Instead', ['However', 'For example', 'Otherwise'],  # L3
       '【解析】前句說「我不再把視線移開」，後句說「我會試著看懂一兩個字」，是用後面的做法「取代」以前移開視線的做法，用 Instead（反而、取而代之）。'
       '({d0}) However 表示語意相反，但這兩句不是相反關係；({d1}) 試著看懂手語不是「不移開視線」的例子；({d2}) Otherwise 是「否則」，語意不通。')

b.item('', 'we were the ones who needed to learn how to reach her',
       ['she was the one who needed to learn how to fit in with us',
        'she should have learned to speak like everyone else',
        'nobody in our class needed to learn anything'],  # L4
       '【解析】the other way around 是「正好相反」，與作者「以前」的想法（怡婷需要學習融入我們）相反，就是「我們才是需要學習走近她的人」，也呼應全文同學們學手語的經過。'
       '({d0}) 是作者「以前」的想法，不是相反的情況；({d1}) 要聽障的怡婷改變，與全文主旨相反；({d2}) 全班都學了手語，與文意矛盾。')

# ======================================================================
# 32–34 珍古德（時事：2025-10-01 逝世）
# ======================================================================
b.group(32, 34, """When Jane Goodall arrived at Gombe in Tanzania in July 1960, she was 26 years old and had no university degree. Many scientists did not take her seriously. They believed that only well-trained researchers could do real science.
Goodall, however, had something else: patience. Day after day, she sat quietly in the forest, waiting for the shy chimpanzees to get used to her. It took months before they let her come close. Then one day, she saw a chimpanzee push a long piece of grass into a termite hill and pull it out, covered with termites to eat. Later, she saw chimpanzees take the leaves off small branches to make the same kind of tool. At that time, most scientists believed that only humans made and used tools. Her discovery changed that belief.
Goodall also did something that other scientists didn't like. Instead of giving the chimpanzees numbers, she gave them names, such as David Greybeard, and wrote about their personalities and feelings. Some experts said this was not scientific. Today, however, many researchers agree that animals do have personalities.
In her later years, Goodall spent less time in the forest and more time traveling—sometimes nearly 300 days a year—to speak about protecting animals and the environment. In 1991, she started Roots & Shoots, a program for young people that began with just 12 teenagers in Tanzania and, over the years, spread to more than 100 countries.
She was on a speaking tour in the United States when she died on October 1, 2025, at the age of 91. The research she started at Gombe was still going on in 2025, 65 years after it began.
* chimpanzee 黑猩猩；termite 白蟻；personality 個性""",
        translation="""1960 年 7 月，珍．古德抵達坦尚尼亞的 Gombe 時，她 26 歲，沒有大學學位。許多科學家並不把她當一回事，他們認為只有受過良好訓練的研究人員才能做真正的科學研究。
然而，古德擁有別的東西：耐心。她日復一日安靜地坐在森林裡，等待害羞的黑猩猩習慣她的存在。過了好幾個月，牠們才讓她靠近。後來有一天，她看到一隻黑猩猩把一根長草伸進白蟻丘，再拉出來，上面沾滿了可以吃的白蟻。之後她又看到黑猩猩把小樹枝上的葉子拔掉，做成同樣的工具。在那個年代，大多數科學家認為只有人類會製造和使用工具，她的發現改變了這個看法。
古德還做了一件其他科學家不喜歡的事。她沒有給黑猩猩編號，而是幫牠們取名字，例如「灰鬍子大衛」，並描寫牠們的個性和情感。有些專家說這樣不科學。然而今天，許多研究者都同意動物確實有個性。
晚年的古德待在森林的時間變少，花更多時間到各地旅行——有時一年將近 300 天——宣講保護動物與環境。1991 年，她創立了「根與芽」，一個為年輕人設立的計畫，一開始只有坦尚尼亞的 12 個青少年，多年來擴展到一百多個國家。
2025 年 10 月 1 日她過世時，正在美國進行巡迴演講，享壽 91 歲。她在 Gombe 開始的研究到 2025 年仍在進行，已經持續了 65 年。""")

age_1991 = 26 + (1991 - 1960)
b.item('About how old was Goodall when she started Roots & Shoots?',  # L4
       str(age_1991), ['31', '26', '65'],
       '【中譯】古德創立「根與芽」時大約幾歲？\n'
       '【解析】要整合兩處資訊：1960 年她 26 歲，「根與芽」創立於 1991 年，相隔 31 年，所以約 57 歲（她 1934 年 4 月出生，「根與芽」在 1991 年初創立時其實是 56 歲，最接近的選項是 57）。'
       '({d0}) 31 只是兩個年份相差的年數；({d1}) 26 是她抵達 Gombe 時的年齡；({d2}) 65 是把過世時的 91 歲減去到 Gombe 時的 26 歲，算出的是兩件事相隔的年數，不是年齡。',
       check=(age_1991 == 57 and 91 - (2025 - 1991) == 57, [31 == age_1991, 26 == age_1991, 65 == age_1991]))

b.item('Which of the following is NOT true according to the reading?',  # L4
       'Roots & Shoots was started by a group of teenagers before Goodall joined it.',
       ['Goodall had to wait for months before the chimpanzees let her come close.',
        'Some experts once thought that naming the animals was not scientific.',
        'Goodall was still giving talks to the public shortly before she died.'],
       '【中譯】根據本文，下列何者「不」正確？\n'
       '【解析】第四段說「根與芽」是古德在 1991 年「創立」的，一開始有 12 個青少年參加，並不是青少年先成立、她後來才加入。'
       '({d0}) 第二段 It took months before they let her come close，正確；({d1}) 第三段專家說為黑猩猩取名「不科學」，正確；({d2}) 她過世時正在美國巡迴演講，正確。')

b.item('Which of the following would the experts in the third paragraph most likely have criticized?',  # L4
       'A researcher who calls a gorilla "Bella" and describes her as shy and gentle.',
       ['A researcher who sits quietly for months to watch wild animals.',
        'A researcher who gives each bird in a study a number instead of a name.',
        'A researcher who travels around the world to talk about the environment.'],
       '【中譯】第三段的專家最可能批評下列哪一位研究者？\n'
       '【解析】第三段的專家批評的是「為動物取名字、描寫牠們的個性和情感」。替大猩猩取名 Bella 並形容牠害羞溫和，正是同一種做法。'
       '({d0}) 耐心觀察是第二段古德的優點，專家並沒有批評；({d1}) 給動物編號正是當時專家認為「科學」的做法；({d2}) 到處演講是古德晚年的事，與第三段的批評無關。')

# ======================================================================
# 35–37 故事：圖書館裡的紙條
# ======================================================================
b.group(35, 37, """Every Tuesday after school, Wei-lun went to the city library to study. One afternoon, he took an old book about birds off the shelf, and a small piece of paper fell out. On it, someone had written: "If you found this, you must love birds too. Page 87 has the best picture in the book."
Wei-lun turned to page 87. It showed a small bird with a bright yellow chest, sitting on a branch in the rain. Under the message, he wrote his own: "Agreed! But page 112 is even better." He put the note back and returned the book to the shelf.
The next Tuesday, he couldn't wait to check. The note was still there, and a new line had been added: "You're right. Have you ever seen one in real life? I saw one at the river park last spring."
For two months, Wei-lun and the stranger wrote to each other in the book. They talked about birds, school, and their favorite places in the city. Wei-lun never tried to find out who the writer was. He was afraid that if he did, the magic would disappear.
Then one Tuesday, the book was gone. Someone had borrowed it. Wei-lun felt surprisingly sad. When it came back two weeks later, he opened it with shaking hands. The note was still there, with one last line: "My family and I are moving to Tainan. Thank you for being my friend this year. —Grandpa Lin, the man who reads by the window"
Wei-lun looked up. The chair by the window, where an old man had sat every Tuesday, was empty.""",
        translation="""每個星期二放學後，偉倫都會到市立圖書館讀書。有一天下午，他從書架上拿下一本關於鳥類的舊書，一張小紙條掉了出來。上面有人寫著：「如果你找到這張紙條，你一定也喜歡鳥。第 87 頁有這本書裡最棒的圖。」
偉倫翻到第 87 頁，上面是一隻胸前亮黃色的小鳥，在雨中停在樹枝上。他在那段話下面寫了自己的留言：「同意！不過第 112 頁更棒。」他把紙條放回去，把書放回書架。
下個星期二，他迫不及待地去看。紙條還在，而且多了一行字：「你說得對。你在現實中看過這種鳥嗎？我去年春天在河濱公園看過一隻。」
兩個月來，偉倫和這位陌生人在書裡互相寫信。他們聊鳥、聊學校，也聊他們在城市裡最喜歡的地方。偉倫從來沒有試著查出寫字的人是誰，他怕一旦知道了，那種魔力就會消失。
後來有一個星期二，那本書不見了，有人把它借走了。偉倫感到出乎意料地難過。兩個星期後書回來了，他用顫抖的手打開。紙條還在，上面多了最後一行：「我要和家人搬到臺南了。謝謝你這一年當我的朋友。——林爺爺，那個在窗邊看書的人」
偉倫抬起頭。窗邊那張每個星期二都坐著一位老先生的椅子，空著。""")

b.item('Why does the writer say Wei-lun felt "surprisingly" sad when the book was gone?',  # L4
       'He had not realized how much the notes meant to him until he might lose them.',
       ['He needed the book to finish a school report about birds.',
        'He already knew that the stranger was moving to Tainan.',
        'He was angry that someone had borrowed his favorite book.'],
       '【中譯】作者為什麼說書不見時偉倫感到「出乎意料地」難過？\n'
       '【解析】surprisingly 表示連他自己都沒想到會這麼難過——直到可能失去這些紙條，他才發現它們對他有多重要。'
       '({d0}) 文中沒有提到學校報告；({d1}) 搬家的消息是書「回來以後」才在紙條上看到的，書不見時他還不知道——時間順序錯誤；({d2}) 他的反應是難過，不是生氣，書也不是他的。')

b.item('What can we infer about Grandpa Lin?',  # L5
       'Wei-lun had probably seen him at the library many times.',
       ['He took the book with him when he moved to Tainan.',
        "He was the grandfather of one of Wei-lun's classmates.",
        'He wanted Wei-lun to meet him at the river park.'],
       '【中譯】關於林爺爺，我們可以推論出什麼？\n'
       '【解析】林爺爺署名「在窗邊看書的人」，而最後一句說窗邊的椅子「每個星期二」都坐著一位老先生；偉倫也每個星期二都去圖書館，可見他很可能已經看過林爺爺很多次，只是不知道他就是寫字的人。'
       '({d0}) 書兩週後「回來了」，紙條還在書裡，所以他沒有把書帶走；({d1})、({d2}) 文中都沒有任何根據。')

b.item('Which detail from the beginning of the story best helps to explain the ending?',  # L4
       'Wei-lun went to the library every Tuesday after school.',
       ['The bird on page 87 had a bright yellow chest.',
        'The first note said that page 87 had the best picture.',
        'Wei-lun wrote that page 112 was even better.'],
       '【中譯】故事開頭的哪一個細節最能幫助解釋結局？\n'
       '【解析】結局揭曉林爺爺就是每個星期二坐在窗邊的老先生；開頭交代偉倫「每個星期二」放學都去圖書館，說明了兩人為什麼每週都在同一個地方，卻一直沒有相認。'
       '({d0})、({d1})、({d2}) 都是兩人通信的內容，與結局的揭曉沒有關係。')

# ======================================================================
# 38–40 營養午餐廚餘實驗（表格）
# ======================================================================
b.group(38, 40, """Last semester, the student council at Hsin-yi Junior High noticed that a lot of school lunch was ending up in the trash. To find out why, they first asked 600 students to fill out a survey. Only 15% said the food did not taste good. The most common answers were "I don't have enough time to finish" and "They give me too much rice."
Next, the council tested three changes, each for three weeks. Each change was tested on its own: when a new change started, the one before it stopped. Every day, they weighed the food that was thrown away after lunch. To keep the test fair, the school served the same weekly menu for all twelve weeks.
| Weeks | What was different | Food waste (kg per day) |
| 1–3 | Nothing (normal lunch) | 48 |
| 4–6 | Students chose a small, medium, or large serving of rice | 39 |
| 7–9 | Lunch time was 10 minutes longer | 41 |
| 10–12 | Vegetables were served before the meat | 46 |
In their report, the council suggested keeping the two changes that had worked best. The principal agreed to one of them right away. The other, she said, would be harder, because all the afternoon classes would have to start later, and the school buses would have to leave later, too.""",
        translation="""上學期，信義國中的學生會注意到很多營養午餐最後都進了垃圾桶。為了找出原因，他們先請 600 名學生填寫問卷，只有 15% 說飯菜不好吃，最常見的回答是「我沒有足夠的時間吃完」和「他們給我太多飯了」。
接著，學生會測試了三種改變，每種為期三週。每種改變都單獨測試：新的改變開始時，前一個就停止。每天午餐後，他們都秤量被倒掉的食物。為了讓測試公平，學校這十二週都供應同一套每週菜單。
週次｜不同之處｜廚餘量（每天公斤數）
1–3｜沒有改變（一般午餐）｜48
4–6｜學生可以選擇小、中、大份的飯｜39
7–9｜午餐時間延長 10 分鐘｜41
10–12｜先供應蔬菜，再供應肉類｜46
在報告中，學生會建議保留效果最好的兩項改變。校長立刻同意了其中一項；至於另一項，她說比較困難，因為下午所有的課都必須延後開始，校車也得延後發車。""")

b.item('If the school keeps only the change that the principal agreed to right away, about how much food waste per day can it expect, based on the tests?',  # L5
       '39 kg', ['41 kg', '32 kg', '46 kg'],
       '【中譯】如果學校只保留校長立刻同意的那項改變，根據測試結果，每天大約會有多少廚餘？\n'
       '【解析】效果最好的兩項是「選飯量」（39 公斤）和「延長午餐時間」（41 公斤）。校長說比較難的那一項會讓下午的課和校車延後，指的是延長午餐時間；所以立刻同意的是「選飯量」，預期每天約 39 公斤。'
       '({d0}) 41 公斤是延長午餐時間的結果，正是校長說困難的那項；({d1}) 32 公斤是把兩項的減少量（9＋7）一起從 48 扣掉，但只保留一項，而且測試時兩項也沒有同時實施；({d2}) 46 公斤是先供應蔬菜的結果，不在建議保留的兩項中。')

b.item('Which of the following is true according to the reading?',  # L4
       'The test results matched the reasons most often given in the survey.',
       ['Most students said that the food tasted great.',
        'All three changes were used together in weeks 10–12.',
        'Serving vegetables first did not reduce food waste at all.'],
       '【中譯】根據本文，下列何者正確？\n'
       '【解析】問卷最常見的原因是「時間不夠」和「飯太多」，而實驗中減少最多廚餘的正是「選飯量」和「延長午餐時間」，兩者相符。'
       '({d0}) 只知道 15% 說不好吃，不能推出大多數人覺得「很好吃」，是過度推論；({d1}) 每項改變單獨測試，新的開始時前一個就停止；({d2}) 從 48 降到 46 公斤，還是有減少，只是減得少。')

b.item('Why did the school serve the same weekly menu for all twelve weeks?',  # L4
       'So that changes in food waste could not be caused by different food.',
       ['So that students would get used to the food and eat more of it.',
        'Because most students said that they liked the menu.',
        'Because the council wanted to save money on food.'],
       '【中譯】為什麼學校這十二週都供應同一套每週菜單？\n'
       '【解析】文中說是 To keep the test fair（為了讓測試公平）：菜單不變，廚餘量的差異才能歸因於測試的改變，而不是因為菜色不同——這是控制變因的概念。'
       '({d0}) 文中沒有提到要讓學生習慣菜色；({d1}) 問卷只說 15% 覺得不好吃，沒有說大多數人喜歡菜單；({d2}) 文中沒有提到省錢。')

# ======================================================================
# 41–43 短文：學會「無聊」
# ======================================================================
b.group(41, 43, """Last summer, my parents made a strange rule: for one hour every afternoon, I could not use any screens, and they would not give me anything to do. "Just be bored," my mom said. I thought it was the worst idea I had ever heard.
For the first few days, I lay on the sofa and complained. The clock seemed to stop. But near the end of the first week, something changed. Because there was nothing to fill the time, my mind started to fill it by itself. I began to notice things: the sound of the neighbor's radio, the way the light moved slowly across the wall. One afternoon, I picked up a pencil and started drawing the old tree outside our window. I didn't stop for two hours.
Some scientists say this is no accident. When we are bored, our brains do not simply switch off. Instead, they begin to wander, and this "wandering" can lead to new ideas. If we reach for our phones the moment we feel bored, we may never give our minds the chance to wander far enough.
I'm not saying screens are bad. I still watch videos and play games online with my friends. But I've learned that boredom is not an enemy to run away from. It is more like an empty room: at first it feels uncomfortable, but it is also the only place where something new can be built.
By the way, I'm still drawing. My sketchbook is almost full.
* wander（思緒）漫遊；sketchbook 素描本""",
        translation="""去年夏天，我爸媽訂了一條奇怪的規定：每天下午有一個小時，我不能使用任何螢幕，他們也不會給我任何事情做。「就無聊一下吧。」我媽說。我覺得那是我聽過最糟的主意。
頭幾天，我躺在沙發上抱怨，時鐘好像停住了。但第一週快結束時，事情起了變化。因為沒有東西填滿時間，我的腦袋開始自己去填滿它。我開始注意到一些事：鄰居收音機的聲音、光線慢慢移過牆面的樣子。有一天下午，我拿起鉛筆，開始畫窗外那棵老樹，一畫就是兩個小時。
有些科學家說這不是偶然。我們感到無聊時，大腦並不是單純關機，而是開始漫遊，而這種「漫遊」可能帶來新的想法。如果我們一覺得無聊就伸手拿手機，可能永遠不會給腦袋機會漫遊得夠遠。
我不是說螢幕不好。我還是會看影片，也會和朋友在網路上玩遊戲。但我學到，無聊不是一個要逃避的敵人。它比較像一個空房間：一開始讓人不自在，但它也是唯一能建造出新東西的地方。
對了，我現在還在畫畫，我的素描本快要畫滿了。""")

b.item('What does the writer mean by "my mind started to fill it by itself"?',  # L3
       'The writer began to notice things and find things to do without being told.',
       ['The writer started using screens again when the parents were not looking.',
        'The writer fell asleep on the sofa because there was nothing to do.',
        'The writer\'s parents finally gave the writer something to do.'],
       '【中譯】作者說「我的腦袋開始自己去填滿它」是什麼意思？\n'
       '【解析】這句後面接著舉例：開始注意到收音機的聲音、牆上的光線，還拿起鉛筆畫畫——腦袋自己找到事情做，沒有人告訴作者該做什麼。'
       '({d0}) 文中沒有偷用螢幕；({d1}) 文中沒有說睡著，反而是開始注意身邊的事；({d2}) 父母的規定正是「不給任何事情做」。')

b.item('Why does the writer say that boredom is "like an empty room"?',  # L4
       'It feels uncomfortable at first, but it leaves space for something new.',
       ['It is a place where nothing ever happens.',
        'It is something that we should run away from.',
        'It is a good place to keep our phones.'],
       '【中譯】作者為什麼說無聊「像一個空房間」？\n'
       '【解析】作者說空房間「一開始讓人不自在，但也是唯一能建造新東西的地方」，對應自己從抱怨到開始畫畫的經驗。'
       '({d0}) 只取「空」的字面意思，忽略後半句「能建造新東西」；({d1}) 作者正好說無聊「不是」要逃避的敵人；({d2}) 文中沒有這個意思。')

b.item('A friend tells the writer, "I\'m so bored. There\'s nothing to do." What advice would the writer most likely give?',  # L4
       "Don't pick up your phone right away—see where your thoughts take you.",
       ['Stop using screens forever, because they are bad for you.',
        'Ask your parents to give you something to do.',
        'Go to sleep until the boredom goes away.'],
       '【中譯】朋友對作者說：「我好無聊，沒事可做。」作者最可能給什麼建議？\n'
       '【解析】把文章的觀點套用到新情況：作者認為無聊時不要馬上伸手拿手機，讓思緒漫遊，才可能產生新想法。'
       '({d0}) 作者明白說「我不是說螢幕不好」，自己也還在看影片、玩遊戲，「永遠不用」太極端；({d1}) 作者的經驗正是父母「不給事情做」才有收穫；({d2}) 睡覺就是逃避無聊，與作者的看法相反。')

b.write()
