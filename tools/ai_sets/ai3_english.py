"""AI-3 英文（閱讀，挑戰）: build src/data/ai/ai3_english.json.

Correct option first, distractors after; SetBuilder places the options by
TARGET and writes the letters ({c} {d0} {d1} {d2}) and 「故選」.
Each item carries its design level as a trailing comment (levels 3-5, see SPEC_AI2_AI3.md).

  PYTHONIOENCODING=utf-8 python tools/ai_sets/ai3_english.py
"""
from common import SetBuilder, spread_target

TOPICS = [
    '溫布頓 2025 全面改用電子司線 Hawk-Eye Live（18 面球場、取消挑戰制度、約 147 年來首次沒有司線員）：https://africa.espn.com/tennis/story/_/id/41695328/wimbledon-replace-line-judges-ai-technology-2025',
    '溫布頓 Kartal 對 Pavlyuchenkova 第四輪中央球場系統被誤關一局、重打該分、道歉、歸咎人為疏失並取消手動關閉功能：https://www.skysports.com/tennis/news/32498/13393402/wimbledon-officials-apologise-to-players-after-line-calling-technology-turned-off-in-malfunction-on-centre-court',
    'Colossal Biosciences 2025 年 4 月宣布「恐狼」幼崽 Romulus、Remus、Khaleesi（13,000 年牙齒、72,000 年耳骨、14 個基因 20 處編輯、狗代孕、複製紅狼；灰狼為最近親屬是公司說法）：https://colossal.com/the-return-of-the-dire-wolf/',
    '恐狼爭議（科學家批評仍是灰狼、無法向親代學習；公司稱目標是填補生態角色；滅絕逾一萬年）：https://www.npr.org/2025/04/08/nx-s1-5355686/dire-wolf-extinct-colossal-biosciences',
    '澳洲 16 歲以下社群媒體禁令 2025-12-10 生效（罰款上限 4,950 萬澳幣、WhatsApp 與 Roblox 不在名單、AI 臉部年齡估計或上傳證件）：https://www.khaleejtimes.com/world/australia-bans-under-16s-from-social-media',
    '澳洲禁令後續：2026 年 3 月（約三個月後）eSafety 檢查約 70% 原有帳號兒童仍活躍、2026 年 6 月政府擬將罰款上限加倍、部長稱 "not seeing improvements"：https://www.euronews.com/next/2026/06/29/fines-doubled-as-teens-outsmart-australias-world-first-social-media-ban',
    '修理咖啡館（第一家 2009 年阿姆斯特丹，全球逾千家）：https://en.wikipedia.org/wiki/Repair_Caf%C3%A9',
    '保溫瓶裡的湯、植物聽音樂的科展報告與老師評語、「天分」一詞的迷思：虛構情境',
]

b = SetBuilder('ai3_english', '英文', year=903, set_name='AI-3',
               title='AI-3 英語（閱讀）模擬卷（挑戰）',
               note='由 AI 依會考英語科架構編寫，難度高於會考：長篇（300–500 字）跨段推論、作者觀點與語氣、'
                    '段落功能、指涉、「何者不正確／無法推知」、雙文本與表格整合、把文章的規則套用到新情況；'
                    '誘答多為「細節對但人物或時間錯」「只對一半」「推論過頭」。以 2025–2026 年真實事件為素材；非會考真題。',
               target=spread_target(43, 4, 903), difficulty='挑戰', topics=TOPICS)

# ======================================================================
# 單題 1–15：每題都要讀懂前後文；誘答單看文法都通，放進語境才錯
# ======================================================================
b.item("Kevin was disappointed with his test score, but he didn't make any excuses. ______, he asked his teacher which kinds of mistakes he should watch out for next time.",  # L4
       'Instead', ['Besides', 'Otherwise', 'Even so'],
       '【中譯】Kevin 對自己的考試成績很失望，但他沒有找任何藉口，反而去問老師下次應該注意哪些錯誤。\n'
       '【解析】「不找藉口」和「去問老師」是以後者取代前者的做法，用 Instead（反而、取而代之）。'
       '({d0}) Besides 表示「此外」，前句是「沒有做某事」，無法再「此外」；({d1}) Otherwise（否則）語意不通；({d2}) Even so（即使如此）表示讓步，但「不找藉口」和「去問老師」並不衝突。')

b.item("A: Is your new manager easy to work with?\nB: Let's just say I've started reading job ads again.\nA: ______",  # L4
       'Oh no. Is it really that bad?', ["Great! I'm happy for you.", "So you'll get a promotion soon?", 'Then you must really love your job.'],
       '【中譯】A：你的新主管好相處嗎？B：這麼說吧，我又開始看徵才廣告了。A：喔不，真的有那麼糟嗎？\n'
       '【解析】B 沒有直接回答，而是說「又開始看徵才廣告」，暗示想換工作，也就是新主管很難相處。A 聽懂了弦外之音，才會說「真的那麼糟嗎」。'
       '({d0}) 表示替 B 高興，誤解了 B 的意思；({d1}) 升遷和想換工作無關；({d2}) 想換工作不可能是很愛這份工作。')

b.item("A: Could you lend me NT$500? I promise I'll pay you back tomorrow.\nB: ______ You still owe me the NT$300 you borrowed last month.",  # L4
       "That's what you said last time.", ['Of course. Here you go.', "Don't worry about paying me back.", "I'm sorry to hear that."],
       '【中譯】A：可以借我 500 元嗎？我保證明天就還你。B：你上次也是這麼說的。你上個月借的 300 元都還沒還我。\n'
       '【解析】B 接著提到 A 上個月借的錢還沒還，可見 B 不相信 A「明天就還」的保證，用 That\'s what you said last time.（你上次也是這麼說）表示懷疑。'
       '({d0}) 爽快借錢，與後句的抱怨矛盾；({d1}) 「不用還」更與「你還欠我錢」矛盾；({d2}) 是對壞消息表示同情，接不上借錢的請求。')

b.item('The red backpack costs NT$900, and the blue one costs NT$1,200. The green one costs less than the blue one but more than the red one, so the green one is ______.',  # L4
       'neither the cheapest nor the most expensive', ['the cheapest of the three', 'the most expensive of the three', 'as expensive as the blue one'],
       '【中譯】紅色背包 900 元，藍色背包 1,200 元。綠色背包比藍色便宜、但比紅色貴，所以綠色背包既不是最便宜也不是最貴的。\n'
       '【解析】綠色介於紅色（900）與藍色（1,200）之間，三者中排第二，所以「既不是最便宜，也不是最貴」。'
       '({d0}) 最便宜的是紅色；({d1}) 最貴的是藍色；({d2}) 綠色比藍色便宜，不可能一樣貴。')

b.item("It's starting to rain hard. We ______ take a taxi home, or we'll be completely wet by the time we get there.",  # L3
       'had better', ['would rather not', "don't have to", 'used to'],
       '【中譯】雨開始下大了，我們最好搭計程車回家，否則到家時會全身濕透。\n'
       '【解析】「, or（否則）會濕透」表示搭計程車是該做的事，用 had better（最好）。'
       '({d0}) would rather not 是「寧可不要」，那就會淋濕，與 or 後面的警告矛盾；({d1}) don\'t have to 是「不必」，同樣說不通；({d2}) used to 是「過去常常」，不是對現在的建議。')

b.item('At first, the scientist was very ______ about her results. She repeated the experiment three times before she told anyone about her discovery.',  # L3
       'cautious', ['careless', 'proud', 'excited'],
       '【中譯】一開始，這位科學家對她的結果非常謹慎。她把實驗重做了三次，才告訴別人她的發現。\n'
       '【解析】「重做三次才告訴別人」表示她非常小心、不急著下結論，用 cautious（謹慎的）。'
       '({d0}) careless（粗心的）正好相反；({d1}) proud、({d2}) excited 的人通常會急著告訴別人，與「重做三次才說」不合。')

b.item('The road up to the mountain village is narrow and full of sharp turns. ______, buses run there every hour, and the drivers seem to know every curve by heart.',  # L4
       'Even so', ['As a result', 'That is', 'Instead'],
       '【中譯】通往山上村莊的路又窄又多急轉彎。即使如此，那裡每小時都有公車，司機們似乎熟記每一個彎道。\n'
       '【解析】路況很差，「卻」每小時都有公車——前後是讓步關係，用 Even so（即使如此）。'
       '({d0}) As a result：路窄多彎不會「造成」公車很多；({d1}) That is（也就是說）用於解釋前句，但後句不是在解釋路況；({d2}) Instead 表示取代，但公車並沒有取代道路。')

b.item('When our class first heard that every student had to take turns working in the school garden, almost everyone complained. ______ By the end of the semester, even the loudest complainers were proud of the vegetables our class grew.',  # L4
       'Within a few weeks, though, many of us began to look forward to our turn.',
       ['So the school decided to cancel the plan after just one day.',
        'Besides, the garden was too far away from our classroom.',
        'As a result, fewer and fewer students were willing to help.'],
       '【中譯】我們班剛聽說每個學生都要輪流到學校菜園工作時，幾乎每個人都在抱怨。不過，幾個星期之內，很多人開始期待輪到自己。到學期末，連抱怨最大聲的人都對我們班種出的蔬菜感到驕傲。\n'
       '【解析】空格前是「大家抱怨」，空格後是「學期末連最會抱怨的人都很驕傲」，中間需要一個「態度轉變」的句子，只有第一個選項（though 表轉折）接得上兩邊。'
       '({d0}) 計畫若第一天就取消，後面就不會有種出來的蔬菜；({d1}) 只是補充抱怨的理由，接不上後面的轉變；({d2}) 願意幫忙的人越來越少，與「連最會抱怨的人都很驕傲」矛盾。')

b.item('I have two brothers. ______ of them is good at cooking: Leo makes great beef noodles, and Sam bakes the best bread in town.',  # L4
       'Each', ['Neither', 'None', 'Both'],
       '【中譯】我有兩個哥哥。他們每個都很會做菜：Leo 的牛肉麵很棒，Sam 烤的麵包是鎮上最好吃的。\n'
       '【解析】冒號後說明兩人「各自」擅長的料理，表示兩個都很會做菜，用 Each of them is。'
       '({d0}) Neither 表示兩個都不會，與冒號後的說明矛盾；({d1}) None 用於三者以上，且同樣是否定；({d2}) Both 的意思雖然對，但 Both of them 是複數，動詞要用 are，與空格後的 is 不合——這題要同時看語意和主詞動詞一致。')

b.item('A sign at a swimming pool says: "Children under 12 must be with an adult at all times. Children under 6 may only use the small pool." Which of the following follows the rules?',  # L5
       'A 10-year-old girl swimming in the big pool with her father.',
       ['An 11-year-old boy swimming by himself in the big pool.',
        'A 5-year-old boy swimming in the big pool with his mother.',
        'A 9-year-old girl playing by herself in the small pool.'],
       '【中譯】游泳池的告示寫著：「未滿 12 歲的兒童必須隨時由成人陪同。未滿 6 歲的兒童只能使用小池。」下列哪一個情況符合規定？\n'
       '【解析】兩條規定要同時檢查：10 歲有爸爸陪同（符合第一條），10 歲不受「只能用小池」限制（符合第二條）。'
       '({d0}) 11 歲未滿 12 歲，不能自己游；({d1}) 5 歲未滿 6 歲，即使有媽媽陪也只能用小池；({d2}) 9 歲雖然在小池，但沒有成人陪同。')

b.item('______ you leave right now, you will still miss the last bus. It leaves in five minutes, and the bus stop is a fifteen-minute walk from here.',  # L5
       'Even if', ['Unless', 'As long as', 'Because'],
       '【中譯】就算你現在馬上離開，還是會錯過末班公車。公車五分鐘後開，而公車站離這裡要走十五分鐘。\n'
       '【解析】公車五分鐘後開，走到站要十五分鐘，所以「現在出發也趕不上」，要用讓步的 Even if（即使），句中的 still 也是線索。'
       '({d0}) Unless you leave now, you\'ll miss…表示「現在走就趕得上」，與第二句的時間計算矛盾，是最容易誤選的選項；({d1}) As long as（只要）表示「只要現在走就會錯過」，不合邏輯；({d2}) Because 表示「因為你現在走所以錯過」，因果不通。')

b.item('A sign at a café says: "Free Wi-Fi for customers—please ask for the password at the counter. When the café is busy, we kindly ask customers using laptops to stay no longer than two hours." What does the sign suggest?',  # L5
       'On a quiet afternoon, a customer may work on a laptop there for more than two hours.',
       ['Anyone walking past the café can use the Wi-Fi without buying anything.',
        'Laptops cannot be used in the café when it is busy.',
        'The Wi-Fi password is printed on the sign.'],
       '【中譯】咖啡廳的告示寫著：「顧客可免費使用 Wi-Fi，請向櫃檯索取密碼。店內客滿時，敬請使用筆電的顧客停留不超過兩小時。」這個告示暗示什麼？\n'
       '【解析】兩小時的限制只在「店內忙碌時」才適用，所以人少的時候，用筆電的顧客可以待超過兩小時。'
       '({d0}) Wi-Fi 是給「顧客」用的，路過的人不算；({d1}) 忙碌時是限制停留「兩小時」，不是不能用筆電，屬於過度推論；({d2}) 密碼要向櫃檯索取，並沒有寫在告示上。')

b.item('One of the most important skills that students need in the age of AI ______ the ability to check whether the information they find is true.',  # L4
       'is', ['are', 'be', 'being'],
       '【中譯】在 AI 時代，學生最需要的重要技能之一，是查核所找到的資訊是否正確的能力。\n'
       '【解析】主詞是 One（of the most important skills…），是單數，動詞用 is。中間的 skills、students 都是修飾語，不是主詞，這是最容易誤選 are 的陷阱。'
       '({d0}) are 誤把 skills 當主詞；({d1}) be、({d2}) being 都不能當句子的主要動詞。')

b.item('The movie started at 7:00 and lasted exactly two hours. Because my little brother felt sick, we left the theater twenty minutes ______ it ended, and we got home before nine.',  # L4
       'before', ['after', 'until', 'since'],
       '【中譯】電影七點開始，正好演兩個小時。因為我弟弟不舒服，我們在電影結束前二十分鐘就離開戲院，九點前就到家了。\n'
       '【解析】電影 9:00 結束；「九點前到家」表示一定是在結束「之前」離開（8:40 離開）。'
       '({d0}) after 是 9:20 才離開，不可能九點前到家，而且弟弟不舒服也不會多留；({d1}) until、({d2}) since 放在 twenty minutes ___ it ended 中語意不通。')

b.item("A: Why didn't you tell me the party was canceled?\nB: I ______, but your phone was off all afternoon.",  # L4
       'tried to', ['forgot to', "didn't want to", 'promised not to'],
       '【中譯】A：你為什麼沒告訴我派對取消了？B：我有試著告訴你，但你的手機整個下午都關機。\n'
       '【解析】but 後面說「你的手機關機」，是在解釋「想聯絡卻聯絡不上」，所以前面是 tried to（試著要告訴你）。'
       '({d0}) forgot to、({d1}) didn\'t want to、({d2}) promised not to 都表示 B 本來就沒打算或忘了聯絡，後面再說「但你的手機關機」就不合邏輯。')

# ======================================================================
# 16–19 雙文本：溫布頓電子司線（新聞＋讀者留言）（時事）
# ======================================================================
b.group(16, 19, """[Text A] Wimbledon Says Goodbye to Line Judges
For almost 150 years, line judges were as much a part of Wimbledon as its grass courts and its rule that players must wear white. Dressed in smart uniforms, they stood around the court and shouted "Out!" or "Fault!" whenever a ball landed outside the lines. In 2025, their voices fell silent. For the first time, line calls on all 18 courts were made by a computer system called Hawk-Eye Live, which follows the ball with cameras and then plays a recorded voice to announce the call.
Supporters of the change say machines are simply more accurate. A serve can travel at more than 200 kilometers an hour, and even the sharpest human eye can miss by a few millimeters. With the new system, players no longer need to "challenge" a call and wait for a replay.
The system, however, did not have a perfect first year. During a fourth-round match on Centre Court between Britain's Sonay Kartal and Russia's Anastasia Pavlyuchenkova, a ball that was clearly out went uncalled, and the umpire ordered the point to be played again. It later turned out that the system had been switched off by mistake on part of the court for a whole game, and nobody had told the umpire. The club apologized to both players. It blamed "human error," not the technology, and changed its rules so that operators could no longer turn the system off by hand.
The incident left an uncomfortable question. If the people running the machine can make mistakes, has human error really been removed—or has it just been moved somewhere the players can't see it?

[Text B] Readers' Comments
TennisDad_88: My daughter plays in a junior league, and the arguments over line calls never end. Kids cry, parents shout. If a machine made the calls, half of those fights would never start. Well done, Wimbledon.
Grace L.: I've been going to Wimbledon every summer since 1990. The courts felt strangely empty this year. Those men and women in uniform were part of the show—part of the history. Accuracy matters, but tennis is not just a math problem.
Ryo_K: Everyone is missing the point. The machine didn't fail; the people did. That's actually an argument for MORE technology, not less. Take away the off switch completely and let the system do its job.
* umpire 主審；serve 發球；accurate 準確的""",
        translation="""【文本 A】溫布頓向司線員說再見
將近 150 年來，司線員和草地球場、選手必須穿白色服裝的規定一樣，都是溫布頓的一部分。他們穿著體面的制服站在球場四周，只要球落在線外，就大喊「出界！」或「發球失誤！」。2025 年，他們的聲音消失了。所有 18 面球場的判線第一次全部由一套叫做 Hawk-Eye Live（鷹眼即時系統）的電腦系統負責：它用攝影機追蹤球，再播放預先錄好的聲音宣布判決。
支持這項改變的人說，機器就是比較準確。發球的球速可以超過每小時 200 公里，即使是最敏銳的人眼也可能誤差幾公釐。有了新系統，選手不再需要「挑戰」判決並等待重播。
然而，這套系統的第一年並不完美。在中央球場一場英國選手 Sonay Kartal 對俄羅斯選手 Anastasia Pavlyuchenkova 的第四輪比賽中，一顆明顯出界的球沒有被判出界，主審下令這一分重打。後來才發現，系統在球場的一部分被誤關了一整局，而且沒有人告訴主審。主辦的俱樂部向兩位選手道歉，把原因歸咎於「人為疏失」而不是科技，並修改規定，讓操作人員再也不能手動關閉系統。
這起事件留下了一個令人不安的問題：如果操作機器的人會犯錯，人為的錯誤真的被消除了嗎？還是只是被移到了選手看不到的地方？

【文本 B】讀者留言
TennisDad_88：我女兒參加青少年聯賽，關於判線的爭吵永遠吵不完，小孩哭、家長吼。如果由機器判，這些爭吵有一半根本不會發生。溫布頓做得好。
Grace L.：從 1990 年起我每年夏天都去溫布頓。今年的球場感覺空蕩蕩的，那些穿制服的男男女女是表演的一部分，也是歷史的一部分。準確很重要，但網球不只是一道數學題。
Ryo_K：大家都沒抓到重點。失敗的不是機器，是人。這其實是支持「更多」科技、而不是更少的理由。把關閉開關整個拿掉，讓系統好好做它的工作。""")

b.item('What can be inferred about the umpire in the Kartal–Pavlyuchenkova match?',  # L5
       'The umpire was depending on the system to call balls that were out.',
       ['The umpire knew that the system had been switched off.',
        'The umpire turned off the system in order to make the calls himself.',
        'The umpire was punished by the club for the mistake.'],
       '【中譯】關於 Kartal 對 Pavlyuchenkova 那場比賽的主審，可以推論出什麼？\n'
       '【解析】一顆「明顯出界」的球主審卻沒有判，而文中說系統被誤關「而且沒有人告訴主審」——可見主審以為系統仍在運作，依賴它來判出界。'
       '({d0}) 文中明說沒有人告訴主審，他並不知道；({d1}) 系統是被「誤關」的，俱樂部歸咎於操作人員，不是主審自己關的；({d2}) 文中只說俱樂部道歉並修改規定，沒有提到處罰主審。')

b.item('What does the writer of Text A suggest with the question at the end?',  # L5
       'Replacing line judges with machines has not completely removed the chance of human mistakes.',
       ['Line judges should be brought back to Wimbledon right away.',
        "Players should be allowed to challenge the machine's calls again.",
        'The technology itself was the real cause of the mistake.'],
       '【中譯】文本 A 的作者用最後的問句想表達什麼？\n'
       '【解析】作者問「人為錯誤是真的被消除了，還是只是被移到選手看不到的地方？」——意思是機器仍由人操作，人為疏失並沒有因為換成機器而完全消失。'
       '({d0}) 作者只是提出疑問，並沒有主張立刻恢復司線員，屬於過度推論；({d1}) 文中沒有提到恢復挑戰制度；({d2}) 作者的問句是順著俱樂部「人為疏失」的說法提出的，並沒有說錯在科技本身。')

b.item('What does Grace L. mean by "tennis is not just a math problem"?',  # L4
       'Getting every call exactly right is not the only thing that gives the sport its value.',
       ['Machines are not good at measuring where a ball lands.',
        'Tennis players do not need to be good at math.',
        'Line judges made fewer mistakes than the new system.'],
       '【中譯】Grace L. 說「網球不只是一道數學題」是什麼意思？\n'
       '【解析】她先說「準確很重要」，再說「但網球不只是數學題」，並提到穿制服的司線員是表演和歷史的一部分——意思是判得準確並不是這項運動唯一的價值。'
       '({d0}) 她承認準確很重要，並沒有說機器量不準；({d1}) 只取字面意思；({d2}) 她沒有比較司線員和機器誰比較準。')

b.item("Which piece of information in Text A is most closely related to Ryo_K's suggestion?",  # L5
       'The club changed its rules so that operators could no longer turn the system off by hand.',
       ['A serve can travel at more than 200 kilometers an hour.',
        'Players no longer need to "challenge" a call and wait for a replay.',
        'The system plays a recorded voice to announce each call.'],
       '【中譯】文本 A 中的哪一項資訊與 Ryo_K 的建議最相關？\n'
       '【解析】Ryo_K 建議「把關閉開關整個拿掉」；文本 A 最後提到俱樂部已經修改規定，讓操作人員不能再「手動」關閉系統——等於已經做了他建議的一部分。這題要把留言和新聞的細節對起來。'
       '({d0}) 球速是支持機器判線的理由，與關閉開關無關；({d1}) 取消挑戰制度是新系統的好處，不是針對這次事件的改變；({d2}) 錄音宣判只是系統的運作方式。')

# ======================================================================
# 20–23 「恐狼復活」的爭議（時事）
# ======================================================================
b.group(20, 23, """In April 2025, an American company called Colossal Biosciences made an announcement that sounded like something out of a movie: it had brought back the dire wolf, a large wolf that died out more than 10,000 years ago. Photos of three fluffy white pups—two males named Romulus and Remus, and a female named Khaleesi—quickly spread around the world.
How was it done? The company's scientists studied ancient DNA from two fossils: a tooth about 13,000 years old and a piece of ear bone about 72,000 years old. They compared it with the DNA of the gray wolf, which the company calls the dire wolf's closest living relative. Then, instead of putting ancient DNA into the animals, they made 20 changes to 14 genes in gray wolf cells, so that the pups would have some dire wolf features, such as a white coat, a larger head, and stronger shoulders. Dogs acted as mothers and carried the pups until they were born.
Not everyone was impressed. Many scientists pointed out that the pups are still gray wolves, just with a few changes. You cannot bring back a species, they argued, simply by making one animal look like another. Others noted that even if the pups look like dire wolves, there are no dire wolf parents to teach them how to live like one.
Colossal answered that it had never tried to make an exact copy. Its goal, the company said, was to create animals that could play the role dire wolves once played in nature.
So, are they dire wolves or not? The answer may depend on what we mean by "species." If a species is defined by how an animal looks, perhaps the answer is yes. If it is defined by its full set of genes, or by the way it lives and the knowledge that passes from parents to young, the answer is clearly no.
Perhaps the more important question is not whether we can bring extinct animals back, but whether we should spend so much money and attention doing so while many living species are disappearing today. The company says it has already used similar tools to make copies of the red wolf, a wolf so rare that it is in serious danger of dying out. Whether this kind of work can really help animals like that will tell us more about the value of the project than any photo of a cute white pup.
* dire wolf 恐狼；fossil 化石；species 物種；extinct 絕種的；gene 基因""",
        translation="""2025 年 4 月，美國一家叫 Colossal Biosciences 的公司發布了一則像是電影情節的消息：它讓恐狼復活了。恐狼是一種在一萬多年前就滅絕的大型狼。三隻毛茸茸的白色幼崽——兩隻雄的叫 Romulus 和 Remus，一隻雌的叫 Khaleesi——的照片很快傳遍全世界。
這是怎麼做到的？公司的科學家研究了兩件化石中的古代 DNA：一顆約 13,000 年前的牙齒和一塊約 72,000 年前的耳骨。他們把它和灰狼的 DNA 做比較——這家公司稱灰狼是恐狼現存最近的親戚。接著，他們沒有把古代 DNA 放進動物體內，而是在灰狼細胞的 14 個基因上做了 20 處修改，讓幼崽具有一些恐狼的特徵，例如白色的毛、較大的頭和較強壯的肩膀。由狗擔任代理孕母，懷著幼崽直到牠們出生。
並不是每個人都買帳。許多科學家指出，這些幼崽仍然是灰狼，只是做了一些修改。他們認為，光是讓一種動物長得像另一種動物，並不能讓一個物種復活。另有人指出，即使幼崽長得像恐狼，也沒有恐狼父母可以教牠們如何像恐狼一樣生活。
Colossal 回應說，它從來沒有打算做出一模一樣的複製品。公司表示，它的目標是創造出能在自然界中扮演恐狼過去角色的動物。
那麼，牠們到底是不是恐狼？答案可能取決於我們所說的「物種」是什麼意思。如果物種是由動物的外表來定義，答案或許是肯定的；如果是由全部的基因，或由牠的生活方式以及親代傳給下一代的知識來定義，答案顯然是否定的。
或許更重要的問題不是我們「能不能」讓絕種動物復活，而是在許多現存物種正在消失的今天，我們「該不該」花這麼多金錢和注意力去做這件事。這家公司說，它已經用類似的技術複製出紅狼——一種稀少到面臨嚴重滅絕危機的狼。這類工作是否真的能幫助這樣的動物，比任何一張可愛白色幼崽的照片，更能告訴我們這個計畫的價值。""")

b.item('Which of the following is true according to the passage?',  # L5
       "The scientists changed some of the gray wolf's own genes instead of adding ancient DNA.",
       ['The tooth that the scientists studied was about 72,000 years old.',
        "Scientists agree that the gray wolf is the dire wolf's closest living relative.",
        'The scientists made 14 changes to 20 different genes.'],
       '【中譯】根據本文，下列何者正確？\n'
       '【解析】第二段說他們「沒有把古代 DNA 放進動物體內」，而是修改灰狼細胞的基因。'
       '({d0}) 牙齒約 13,000 年，72,000 年的是耳骨——數字對但東西錯；({d1}) 文中說灰狼是恐狼最近親屬是「公司的說法」(which the company calls)，並沒有說科學家都同意；({d2}) 是 14 個基因上的 20 處修改，數字前後顛倒。')

b.item('According to the fifth paragraph, who would be the most likely to call Romulus a real dire wolf?',  # L4
       'Someone who thinks a species is defined by how an animal looks.',
       ['Someone who thinks a species is defined by its full set of genes.',
        'Someone who thinks young animals must learn how to live from their own parents.',
        'Someone who agrees with the scientists in the third paragraph.'],
       '【中譯】根據第五段，誰最可能把 Romulus 稱為真正的恐狼？\n'
       '【解析】第五段說：如果物種是以「外表」定義，答案「或許是肯定的」；以全部基因或生活方式定義，答案「顯然是否定的」。'
       '({d0}) 以基因定義，答案是否定的；({d1}) 以親代傳授的生活方式定義，答案也是否定的；({d2}) 第三段的科學家認為幼崽仍是灰狼。')

b.item('What is the main purpose of the fifth paragraph ("So, are they dire wolves or not?")?',  # L5
       'To show that whether the pups are dire wolves depends on how "species" is defined.',
       ['To prove that the pups are real dire wolves.',
        'To explain how the scientists chose which genes to change.',
        "To give Colossal's answer to its critics."],
       '【中譯】第五段（So, are they dire wolves or not?）主要的作用是什麼？\n'
       '【解析】第五段提出「答案取決於物種的定義」：以外表定義也許是，以基因或生活方式定義則不是，作用是說明爭議的關鍵在定義。'
       '({d0}) 作者說以基因或生活方式定義時「顯然不是」，並沒有證明牠們是真的恐狼；({d1}) 選擇基因的過程在第二段，第五段沒有談；({d2}) 公司的回應在第四段。')

b.item("Which best describes the writer's attitude toward the project?",  # L5
       'Doubtful that the pups are true dire wolves, but willing to judge the project by whether it helps endangered animals.',
       ['Excited, because the pups prove that extinct animals can now return.',
        'Angry, because the company lied to the public on purpose.',
        'Uninterested, because the writer thinks the topic is not worth discussing.'],
       '【中譯】下列何者最能描述作者對這個計畫的態度？\n'
       '【解析】作者在第五段指出以基因和生活方式來看「顯然不是」恐狼，表示懷疑；但最後一段說這類技術能否真正幫助紅狼等瀕危動物，才更能顯示計畫的價值——作者保留了以成果來評價的空間。'
       '({d0}) 作者並不認為幼崽證明絕種動物能回來；({d1}) 作者沒有指控公司故意說謊，而且有寫出公司的回應；({d2}) 作者花了整篇討論，還提出「更重要的問題」，並非不感興趣。')

# ======================================================================
# 24–28 克漏字：修理咖啡館（篇章連貫）
# ======================================================================
b.group(24, 28, """The first time I walked into the repair café near my school, I was carrying a broken desk lamp and very low expectations. I was sure someone would tell me to throw it away and buy a new one. __24__, a white-haired man named Mr. Ho took it from me, turned it over, and smiled. "Let's see what's wrong with it," he said. "But you're going to do the work. I'll just tell you what to do."
He meant it. For the next forty minutes, Mr. Ho never once touched the lamp himself. __25__, he kept asking me questions: "What do you think this part does? What happens if you take this off?" Slowly, I opened, checked, and cleaned parts I never knew the lamp had. The problem turned out to be a tiny wire that was loose. When I finally switched the lamp on and it lit up, a few people at the next table actually clapped.
Repair cafés like this one are not really cafés. They are free events where volunteers help people fix their own things—clothes, toys, bikes, and small machines. The first one was held in Amsterdam in 2009, and today there are more than a thousand around the world. The idea behind them is simple: many things we throw away are not truly broken; __26__ just need a little care and someone who knows how to help.
Since that day, I've gone back almost every month. I've fixed a fan, a pair of headphones, and my little sister's favorite toy car, and I've even started helping first-time visitors find the right tools. __27__, Mr. Ho says I'm almost ready to become a volunteer myself.
What I've learned, though, is bigger than how to use a screwdriver. Every time we fix something instead of replacing it, we save money and reduce waste. __28__, we change the way we look at the things around us: not as objects to use and throw away, but as things worth keeping.
* repair café 修理咖啡館；volunteer 志工；screwdriver 螺絲起子""",
        translation="""我第一次走進學校附近的修理咖啡館時，手裡拿著一盞壞掉的檯燈，心裡也不抱什麼期望。我確信會有人叫我把它丟掉、買一盞新的。出乎我意料的是，一位白髮的何先生從我手中接過檯燈，把它翻過來看了看，笑了。「我們來看看它哪裡壞了，」他說，「不過要動手的是你，我只負責告訴你怎麼做。」
他是說真的。接下來的四十分鐘，何先生一次都沒有自己碰檯燈，反而一直問我問題：「你覺得這個零件是做什麼的？把這個拆下來會怎樣？」我慢慢地把一些我從來不知道檯燈裡有的零件打開、檢查、清乾淨。問題原來是一條鬆掉的細電線。當我終於打開開關、檯燈亮起來時，隔壁桌有幾個人還真的鼓起掌來。
像這樣的修理咖啡館其實不是咖啡館，而是免費的活動，由志工幫助大家修理自己的東西——衣服、玩具、腳踏車和小型機器。第一場在 2009 年於阿姆斯特丹舉辦，如今全世界已經有一千多個。背後的理念很簡單：許多我們丟掉的東西其實並沒有真的壞掉，其中很多只需要一點照顧，以及一個懂得怎麼幫忙的人。
從那天起，我幾乎每個月都會回去。我修好了一台電扇、一副耳機，還有我妹妹最喜歡的玩具車，甚至開始幫第一次來的人找合適的工具。因此，何先生說我差不多可以自己當志工了。
不過，我學到的東西比怎麼用螺絲起子更重要。每當我們修理東西而不是換新的，我們就省了錢、減少了垃圾。更重要的是，我們改變了看待身邊事物的方式：它們不是用完就丟的物品，而是值得保留的東西。""")

b.item('', 'To my surprise', ['As I expected', 'In other words', 'As a result'],  # L4
       '【解析】前句說「我確信有人會叫我把它丟掉」，結果何先生卻接過檯燈要幫我修——實際發生的事和預期相反，用 To my surprise（出乎我意料）。'
       '({d0}) As I expected（如我所料）與前句的預期正好相反；({d1}) In other words 是換句話說，但前後並不是同一件事；({d2}) As a result 表示因果，但我的預期不會「造成」何先生接手。')

b.item('', 'Instead', ['Besides', 'Otherwise', 'For example'],  # L4
       '【解析】前句說何先生「一次都沒有自己碰檯燈」，後句說他「一直問我問題」，是用問問題「取代」親手修理，用 Instead。這也呼應第一段他說的「動手的是你，我只告訴你怎麼做」。'
       '({d0}) Besides（此外）要接同方向的補充，但前句是「沒有做」某事；({d1}) Otherwise（否則）語意不通；({d2}) 問問題不是「沒碰檯燈」的例子。')

b.item('', 'many of them', ['none of them', 'most of us', 'every one of them'],  # L4
       '【解析】空格指的是前面的 many things we throw away（許多被丟掉的東西），「其中很多只需要一點照顧」，用 many of them，動詞 need 也和複數主詞一致。'
       '({d0}) none of them 表示「沒有一個只需要照顧」，與「並沒有真的壞掉」矛盾；({d1}) most of us 指人，但需要照顧的是東西；({d2}) every one of them 是單數，動詞要用 needs，而且說「每一件」都只需要照顧也太絕對。')

b.item('', 'As a result', ['Even so', 'On the other hand', 'For example'],  # L4
       '【解析】空格前說作者已經修好很多東西，甚至開始幫第一次來的人找工具；空格後說何先生認為作者「差不多可以當志工了」——前面是原因，後面是結果，用 As a result（因此）。'
       '({d0}) Even so（即使如此）用於讓步，前句必須是不利的情況，但前句全是作者的進步；({d1}) On the other hand 用來提出相對的另一面，但前後方向一致，沒有對比；({d2}) 何先生的評語不是「修好很多東西」的例子，而是它帶來的結果。')

b.item('', 'More importantly', ['In other words', 'Otherwise', 'For example'],  # L5
       '【解析】段落開頭說「我學到的東西比怎麼用螺絲起子『更重要』」，接著先講省錢、減少垃圾，再帶出「改變我們看待事物的方式」這個更深一層的收穫，用 More importantly（更重要的是）。'
       '({d0}) In other words 用來換句話說，但「改變看法」和「省錢減廢」不是同一件事；({d1}) Otherwise（否則）語意不通；({d2}) 改變看法不是省錢減廢的例子。')

# ======================================================================
# 29–32 澳洲 16 歲以下社群媒體禁令（時事）
# ======================================================================
b.group(29, 32, """On December 10, 2025, Australia became the first country in the world to ban children under 16 from having social media accounts. From that day on, platforms such as TikTok, Instagram, Facebook, Snapchat, and YouTube had to take "reasonable steps" to keep under-16s off their services—or face fines of up to 49.5 million Australian dollars. Messaging apps like WhatsApp and the game platform Roblox were not included, at least at first.
Supporters of the law argued that social media is designed to keep young people scrolling for as long as possible, and that parents alone cannot win a fight against some of the world's richest companies. Under the new law, it is the companies, not the children or their parents, that are punished if the rules are broken.
Critics, however, raised several concerns. Checking a user's age is not simple. Some platforms chose to estimate ages with AI tools that study a person's face in a photo; others asked users to upload an ID. Neither method is perfect, and some people worried about handing so much personal information to tech companies. Others feared that teenagers would simply move to corners of the internet that are even less safe.
The early results were mixed. The government said that millions of accounts belonging to children had been removed, turned off, or limited. Yet in March 2026, a check by the country's online safety office found that about 70 percent of children who had accounts on the day the ban began were still active on major platforms such as Facebook, Instagram, Snapchat, and TikTok. In June 2026, about six months after the ban started, the government announced plans to double the largest possible fine, saying it was "not seeing improvements."
What should we make of this? It would be easy to say the ban has failed. But laws often work slowly. Seat belt laws did not make every driver buckle up overnight; it took years of rules, checks, and changing habits. On the other hand, a law that many people ignore can teach the wrong lesson: that rules are only words on paper.
Other countries are watching closely. Whatever happens next in Australia, one thing is already clear: the question is no longer whether governments should do anything about young people and social media, but what—and how much—they should do.
* platform 平臺；fine 罰款；scroll 滑（螢幕）；buckle up 繫上安全帶""",
        translation="""2025 年 12 月 10 日，澳洲成為全世界第一個禁止 16 歲以下兒童擁有社群媒體帳號的國家。從那天起，TikTok、Instagram、Facebook、Snapchat 和 YouTube 等平臺必須採取「合理的措施」，不讓 16 歲以下的人使用服務，否則最高可罰 4,950 萬澳幣。WhatsApp 等通訊軟體和遊戲平臺 Roblox 不在名單內，至少一開始是如此。
支持這項法律的人認為，社群媒體的設計就是要讓年輕人盡可能一直滑下去，而光靠父母，是打不贏世界上一些最有錢的公司的。在新法之下，違反規定時受罰的是公司，而不是孩子或他們的父母。
然而，批評者提出了幾項疑慮。確認使用者的年齡並不簡單。有些平臺選擇用 AI 工具分析照片中的臉來估計年齡，有些則要求使用者上傳證件。兩種方法都不完美，也有人擔心要把這麼多個人資料交給科技公司。另外有人擔心，青少年只會轉移到網路上更不安全的角落。
初期的成效好壞參半。政府表示，已有數百萬個屬於兒童的帳號被刪除、停用或限制。然而，2026 年 3 月，該國網路安全主管機關的檢查發現，在禁令開始當天擁有帳號的兒童中，約有 70% 仍活躍於 Facebook、Instagram、Snapchat 和 TikTok 等主要平臺。2026 年 6 月，也就是禁令開始約六個月後，政府宣布計畫把罰款上限加倍，表示「沒有看到改善」。
我們該怎麼看待這種情況？說這項禁令失敗了很容易。但法律常常是慢慢發揮作用的。安全帶法規並沒有讓每個駕駛一夜之間就繫上安全帶，而是花了好幾年的規定、稽查和習慣的改變。另一方面，一條很多人都不遵守的法律，也可能教給人錯誤的一課：規定只是紙上的文字。
其他國家正密切關注。不論澳洲接下來如何發展，有一件事已經很清楚：問題不再是政府「該不該」對年輕人與社群媒體做些什麼，而是該做「什麼」、做到「多少」。""")

b.item('Which of the following is NOT mentioned as a concern about the ban?',  # L4
       'Teachers would no longer be able to use online videos in class.',
       ["Age checks may sometimes get a user's age wrong.",
        'Users may have to share personal information with companies.',
        'Teenagers may move to less safe places online.'],
       '【中譯】下列何者「不是」文中提到的對禁令的疑慮？\n'
       '【解析】第三段批評者的疑慮有：年齡檢查方法不完美、要把個人資料交給科技公司、青少年轉移到更不安全的網路角落。文中完全沒有提到老師上課不能用影片。'
       '({d0}) 對應 Neither method is perfect；({d1}) 對應 handing so much personal information to tech companies；({d2}) 對應 move to corners of the internet that are even less safe。')

b.item("About how long after the ban began did the online safety office's check take place?",  # L5
       'About three months.', ['About six months.', 'About one year.', 'About two weeks.'],
       '【中譯】網路安全主管機關的檢查大約是在禁令開始多久之後進行的？\n'
       '【解析】禁令在 2025 年 12 月 10 日開始，檢查在 2026 年 3 月，相隔約三個月。'
       '({d0}) 「約六個月」是文中描述 2026 年 6 月政府宣布加重罰款的時間，不是檢查的時間——數字出現在文中，但對應的是另一件事；({d1})、({d2}) 與日期不合。')

b.item('Why does the writer mention seat belt laws?',  # L5
       "To suggest that a law may need time before it changes people's behavior.",
       ['To show that people always obey a law once it is checked strictly.',
        'To argue that social media is as dangerous as driving without a seat belt.',
        'To suggest that the ban should become a rule for parents instead.'],
       '【中譯】作者為什麼提到安全帶法規？\n'
       '【解析】作者先說「法律常常是慢慢發揮作用的」，再舉安全帶法規花了好幾年才改變駕駛習慣為例，意思是不能因為成效還不好就斷定禁令失敗。'
       '({d0}) 作者說花了「好幾年」，而且下一句還提醒很多人不遵守的法律有害，「一定會遵守」是過度推論；({d1}) 作者比較的是「法律需要時間」，不是比較兩者的危險，這是只看字面的誤解；({d2}) 文中支持者強調受罰的是公司而非父母，作者也沒有提議改成管父母。')

b.item("Which best describes the writer's position?",  # L5
       'It is too early to call the ban a failure, but a law that many people ignore also has a cost.',
       ['The ban has not worked so far, so governments should give up on it and try something else.',
        'Laws always take years to work, so the poor early results do not matter at all.',
        'The ban will succeed only if the largest fine is doubled.'],
       '【中譯】下列何者最能描述作者的立場？\n'
       '【解析】第五段作者一方面說「說它失敗很容易，但法律常常慢慢發揮作用」，另一方面又說「很多人不遵守的法律可能教給人錯誤的一課」，兩面都顧及。'
       '({d0}) 只對一半：作者承認成效不佳，但正好反對急著說它失敗、放棄；({d1}) 作者說的是 often（常常），不是 always，而且他也提醒被忽視的法律有代價，並非「完全不重要」；({d2}) 加倍罰款是政府的計畫，作者沒有說只有這樣才會成功。')

# ======================================================================
# 33–36 記敘文：藍色保溫瓶
# ======================================================================
b.group(33, 36, """Every morning for three years, my father handed me the same blue thermos at the door. "Corn soup," he would say, or "Fish soup today," as if it were news. I would nod, put it in my bag, and forget about it as soon as I got to school.
The truth is, I was a little embarrassed by it. My classmates bought bubble tea and sandwiches at the convenience store. Nobody else carried soup in a dented old thermos that their father had used since before they were born. Some days I didn't even open it. I just poured the soup out in the school garden on my way home, so that the thermos would be empty when I gave it back.
One night in December, I couldn't sleep. At around five in the morning, I heard noises in the kitchen and went to look. My father was standing at the stove, still in the uniform he wore for his night job at the hospital parking lot. His eyes were red. He was cutting carrots very slowly, the way people do when they are trying not to fall asleep.
"Why are you up?" he asked, surprised.
"Why are YOU up?" I said. "You just got home."
He shrugged. "Soup takes two hours. If I go to bed first, I won't wake up in time." Then he smiled. "Your grandma made soup for me every day when I was your age. I hated carrying it, too."
I didn't know what to say. I took a spoon and tasted the soup in the pot. It was sweet and warm, and it tasted like something I had forgotten.
That day at lunch, I opened the thermos for the first time in weeks. A classmate leaned over and asked what it was. "My dad's soup," I said, and for once, I didn't feel the need to explain.
The thermos is still blue and still dented. These days, though, I'm the one who gets up early on Sundays, so that my father can sleep in—and so that I can learn how the soup is made.
* thermos 保溫瓶；dented 有凹痕的；shrug 聳肩""",
        translation="""三年來，每天早上爸爸都會在門口遞給我同一個藍色保溫瓶。「玉米濃湯。」他會這樣說，或是「今天是魚湯」，好像在報告什麼新聞似的。我會點點頭，把它放進書包，一到學校就忘了它。
老實說，我有點覺得丟臉。我的同學都在便利商店買珍珠奶茶和三明治，沒有人會帶著一個舊得凹凹凸凸、爸爸在自己出生前就在用的保溫瓶裝湯。有些日子我連打開都沒有，只是在回家的路上把湯倒在學校的花園裡，好讓還給爸爸的時候保溫瓶是空的。
十二月的某個晚上，我睡不著。大約清晨五點，我聽見廚房有聲音，就過去看看。爸爸站在爐子前，身上還穿著他在醫院停車場上夜班時的制服。他的眼睛紅紅的，正很慢很慢地切著紅蘿蔔，就像努力不讓自己睡著的人那樣。
「你怎麼起來了？」他驚訝地問。
「『你』怎麼還沒睡？」我說，「你才剛回家。」
他聳聳肩。「湯要煮兩個小時。如果我先去睡，就來不及起來了。」接著他笑了笑。「我像你這麼大的時候，你奶奶每天都煮湯給我帶。我那時候也很討厭帶湯。」
我不知道該說什麼。我拿了一支湯匙，嚐了嚐鍋裡的湯。湯甜甜的、暖暖的，嚐起來像是某種我已經遺忘的東西。
那天午餐時，我好幾個星期以來第一次打開保溫瓶。一個同學湊過來問那是什麼。「我爸煮的湯。」我說。這一次，我不覺得需要解釋什麼。
保溫瓶還是藍色的，也還是凹凹凸凸的。不過現在，星期天早起的人換成了我，好讓爸爸可以睡晚一點——也好讓我學會這湯是怎麼煮的。""")

b.item('On some days, the writer poured the soup out on the way home and gave the father an empty thermos. What did the writer want the empty thermos to make the father believe?',  # L5
       'That the soup had been eaten at school.',
       ['That the writer was embarrassed to carry soup.',
        'That the soup had gone bad by the afternoon.',
        'That the writer no longer wanted any soup.'],
       '【中譯】有些日子，作者在回家路上把湯倒掉，把空的保溫瓶還給爸爸。作者想用空保溫瓶讓爸爸相信什麼？\n'
       '【解析】第二段說倒掉湯是為了「還給爸爸時保溫瓶是空的」——空瓶子會讓爸爸以為湯在學校被喝掉了。'
       '({d0}) 覺得丟臉是作者「不喝湯」的真正原因，文中確實有寫，但這正是作者想「隱瞞」的事，不是想讓爸爸相信的事，這是本題的陷阱；({d1}) 文中沒有說湯壞了，而且空瓶子也無法讓人相信湯壞了；({d2}) 空瓶子傳達的正好相反——看起來像是全部喝光了。')

b.item('What do the father\'s words "I hated carrying it, too" suggest?',  # L5
       'He had probably guessed how the writer felt about carrying the soup.',
       ['He wanted the writer to stop taking soup to school.',
        'His own mother had never made soup for him.',
        'He was angry that the writer had poured the soup away.'],
       '【中譯】爸爸說「我那時候也很討厭帶湯」暗示了什麼？\n'
       '【解析】too（也）表示「和你一樣」：爸爸在作者什麼都沒說的情況下就這樣說，可見他大概早就猜到作者不喜歡帶湯，卻仍然每天熬夜煮。'
       '({d0}) 他說完還笑了，並沒有要作者別帶，而且他說熬夜是為了來得及煮好；({d1}) 他明明說奶奶每天都煮湯給他；({d2}) 文中沒有跡象顯示他知道湯被倒掉，他的語氣也不是生氣。')

b.item('Which of the following is NOT true according to the story?',  # L5
       "The writer's grandmother made soup for the writer every day.",
       ['The father usually started making the soup after coming home from work.',
        'The writer had not opened the thermos for weeks before that December day.',
        'The thermos had been used since before the writer was born.'],
       '【中譯】根據故事，下列何者「不」正確？\n'
       '【解析】爸爸說「我像你這麼大的時候，你奶奶每天都煮湯給『我』帶」——奶奶是煮給爸爸，不是煮給作者，細節對但人物錯。'
       '({d0}) 作者說「你才剛回家」，爸爸說「如果先去睡就來不及」，可見他下班回家後才開始煮湯，正確；({d1}) 那天作者「好幾個星期以來第一次」打開保溫瓶，正確；({d2}) 第二段說這是爸爸在作者出生前就在用的保溫瓶，正確。')

b.item('What does the last paragraph suggest?',  # L5
       'The writer has come to value the soup and wants to give something back to the father.',
       ['The writer now makes the soup every day so that the father can rest.',
        'The writer plans to buy a new thermos to replace the old one.',
        'The writer still feels embarrassed but hides it better now.'],
       '【中譯】最後一段暗示了什麼？\n'
       '【解析】作者現在週日早起，讓爸爸能睡晚一點，也學著煮這道湯——表示作者已經珍惜這份湯和其中的心意，想回報爸爸。'
       '({d0}) 作者只說「星期天」早起，「每天」是過度推論；({d1}) 保溫瓶「還是藍色的、還是凹凹的」，作者並沒有要換新的；({d2}) 午餐時作者「不覺得需要解釋」，已經不再難為情。')

# ======================================================================
# 37–40 科展報告＋老師評語（表格）
# ======================================================================
b.group(37, 40, """Science Fair Report: Does Music Help Plants Grow?
by Chen Yu-ching and Lai Po-han, Class 9-2
We had heard that playing music to plants makes them grow faster, so we decided to test it. We also wanted to find out whether the kind of music makes a difference. We planted 30 bean seeds in the same kind of pots with the same soil, divided them into three groups of 10, and gave every plant the same amount of water each day. Group A grew without music. Group B listened to classical music for three hours a day, and Group C listened to rock music for three hours a day. Because the music room was the only place where we could play music all afternoon, Groups B and C were kept there, next to a large sunny window. Group A was kept in a quiet storage room with one small lamp. Every evening, we checked the plants and wrote down anything unusual in a notebook. After three weeks, we measured the height of every plant with a ruler and worked out the average for each group.
| Group | Condition | Average height after 3 weeks |
| A | No music (storage room) | 11.2 cm |
| B | Classical music (music room) | 15.8 cm |
| C | Rock music (music room) | 15.1 cm |
Conclusion: Music helps plants grow, and classical music works a little better than rock music.

Teacher's comment:
This is an interesting question, and many people have wondered about it. You measured carefully, and your table is very clear. However, before you can say what you said in your conclusion, you need to think about one problem in the way the experiment was set up. Also, a difference of 0.7 cm between two groups of only 10 plants may not mean very much. I suggest that you repeat the experiment and see whether you get the same result.""",
        translation="""科展報告：音樂能幫助植物生長嗎？
九年二班 陳雨青、賴柏翰
我們聽說對植物播放音樂會讓它們長得比較快，所以決定來測試看看。我們也想知道音樂的種類會不會造成差別。我們把 30 顆豆子種在同款的盆子裡、用同樣的土，分成三組，每組 10 顆，每天給每株植物一樣多的水。A 組不聽音樂；B 組每天聽三小時古典音樂；C 組每天聽三小時搖滾樂。因為音樂教室是唯一能整個下午播放音樂的地方，B、C 兩組就放在那裡，靠近一扇陽光充足的大窗戶；A 組則放在一間只有一盞小燈的安靜儲藏室。每天傍晚，我們都會檢查植物，把任何不尋常的地方記在筆記本上。三週後，我們用尺量了每一株植物的高度，並算出每組的平均值。
組別｜條件｜三週後平均高度
A｜沒有音樂（儲藏室）｜11.2 公分
B｜古典音樂（音樂教室）｜15.8 公分
C｜搖滾樂（音樂教室）｜15.1 公分
結論：音樂能幫助植物生長，而且古典音樂的效果比搖滾樂稍好。

老師評語：
這是個有趣的問題，很多人都好奇過。你們測量得很仔細，表格也非常清楚。不過，在你們能下結論之前，需要想一想實驗設計上的一個問題。另外，兩組各只有 10 株植物，0.7 公分的差距可能說明不了什麼。我建議你們重做一次實驗，看看會不會得到相同的結果。""")

b.item('What does the teacher mean by saying that "a difference of 0.7 cm between two groups of only 10 plants may not mean very much"?',  # L4
       'Such a small difference could happen by chance, even if the kind of music had no effect.',
       ['The students measured the plants in the wrong unit.',
        'Rock music made the plants in Group C 0.7 cm shorter on purpose.',
        'Groups B and C should have been given 0.7 cm more water.'],
       '【中譯】老師說「兩組各只有 10 株植物，0.7 公分的差距可能說明不了什麼」是什麼意思？\n'
       '【解析】每組植物不多，差距又很小，就算音樂種類根本沒有影響，兩組也可能因為偶然（例如個別種子的差異）而相差 0.7 公分，所以不能據此說古典音樂比較好。'
       '({d0}) 老師稱讚他們「測量得很仔細」，沒有說單位錯；({d1}) 只是把數字套進去，文中沒有這樣的說法；({d2}) 水量是用「多少」計算，不是公分，而且各組水量本來就相同。')

b.item('What "problem in the way the experiment was set up" does the teacher most likely mean?',  # L5
       'Group A got much less light than Groups B and C.',
       ['The students used bean seeds instead of flowers.',
        'The rock music was played louder than the classical music.',
        'The plants were measured after only three weeks.'],
       '【中譯】老師說的「實驗設計上的一個問題」最可能是指什麼？\n'
       '【解析】B、C 組放在陽光充足的窗邊，A 組放在只有一盞小燈的儲藏室——除了音樂之外，「光線」也不同，所以 A 組長得矮可能是因為光線不足，而不是沒有音樂。'
       '({d0}) 用豆子做實驗沒有問題；({d1}) 報告中沒有提到音量，這是無中生有；({d2}) 三組都在三週後測量，時間相同，不會造成組間差異。')

b.item("Based on the report and the teacher's comment, which statement is best supported?",  # L5
       'The students cannot yet say whether classical music works better than rock music.',
       ['Music clearly makes bean plants grow faster.',
        'Plants in a quiet room always grow more slowly.',
        'Rock music is harmful to the growth of plants.'],
       '【中譯】根據報告和老師的評語，哪一個說法最有根據？\n'
       '【解析】老師指出 B、C 兩組只差 0.7 公分，每組又只有 10 株，「可能說明不了什麼」，建議重做；所以目前還不能說古典音樂比搖滾樂有效。'
       '({d0}) 因為光線條件不同，還不能確定是音樂造成的，用 clearly 太武斷；({d1}) A 組矮可能是光線不足，而且 always 是過度推論；({d2}) C 組（搖滾樂）長得比 A 組高，資料並不支持「有害」。')

b.item('Which change would best solve the problem in the way the experiment was set up?',  # L4
       'Keeping all three groups in places with the same amount of light.',
       ['Giving Group A more water so that it can catch up.',
        'Playing music to Group A as well.',
        'Adding a fourth group that listens to pop music.'],
       '【中譯】哪一種改變最能解決實驗設計上的問題？\n'
       '【解析】問題在於 A 組的光線比 B、C 組少，只要讓三組的光線相同，除了音樂之外其他條件都一樣，才能看出音樂的影響。'
       '({d0}) 改變水量會多出另一個不同的條件，讓問題更嚴重；({d1}) A 組也聽音樂，就沒有「不聽音樂」的對照組了；({d2}) 多加一組並不能解決 A 組光線不足的問題。')

# ======================================================================
# 41–43 論說文：「天分」這個詞
# ======================================================================
b.group(41, 43, """When people watch a great musician or athlete, they often say, "She's so talented." It sounds like praise, and it is usually meant as praise. But the word "talent" can hide more than it shows.
Think of a girl I'll call Mei, who won a national violin competition at fifteen. Reporters described her as "a natural." What they did not see were the eight years before that: the early mornings, the same short piece played two hundred times until her fingers stopped making mistakes, the competitions she lost, and the nights she cried after losing them. When we call Mei "talented," we turn all of that work into something that seems to have simply been given to her.
This matters for two reasons. First, it is unfair to people like Mei, because it ignores what they have done. Second, and more seriously, it can stop the rest of us from trying. If success comes from a gift that you either have or don't, then a beginner who struggles may decide, "I just don't have it," and quit—at exactly the point where people like Mei kept going. And since nobody is good at anything in the beginning, this way of thinking can stop people before they have really started.
None of this means that people are all the same. Some people really do learn certain skills faster than others, and pretending otherwise would be dishonest. But "faster" is not the same as "without effort." In most fields, the difference between those who get good and those who don't is less about where they start than about what they do next.
So the next time you are about to say that someone is talented, try asking a different question: "How did you get so good at that?" You may be surprised by the answer—and you may find that the road they walked is one you could walk, too.
* talent 天分；talented 有天分的；struggle 苦苦掙扎""",
        translation="""人們看到傑出的音樂家或運動員時，常會說：「她好有天分。」這聽起來像稱讚，通常也是出於稱讚。但「天分」這個詞所遮蓋的，可能比它說明的還多。
想想一個我稱她為小美的女孩，她十五歲時贏得全國小提琴比賽。記者形容她是「天生的」。他們沒看到的是在那之前的八年：一個個清晨、同一首短曲拉了兩百遍直到手指不再出錯、她輸掉的比賽，以及輸了之後哭泣的夜晚。當我們說小美「有天分」，就把那一切努力變成了好像只是上天直接給她的東西。
這件事之所以重要，有兩個原因。第一，這對像小美這樣的人不公平，因為它忽略了他們所付出的。第二，也是更嚴重的，它可能讓我們其他人不再嘗試。如果成功來自一種「有就有、沒有就沒有」的天賦，那麼一個學得很辛苦的初學者可能會認定「我就是沒有那個天分」而放棄——而這恰恰是像小美這樣的人堅持下去的時刻。既然沒有人一開始就擅長任何事，這種想法可能讓人在真正起步之前就停下來。
這並不表示每個人都一樣。有些人學某些技能確實比別人快，假裝不是這樣是不誠實的。但「比較快」不等於「不用努力」。在大多數領域，變得厲害的人和沒有變厲害的人之間的差別，與其說在於起點，不如說在於他們接下來怎麼做。
所以，下次你想說某人有天分時，試著換一個問題問：「你是怎麼變得這麼厲害的？」答案可能會讓你驚訝——你也可能發現，他們走過的那條路，你也走得了。""")

b.item('What is the main function of the second paragraph?',  # L4
       'To give an example of the hard work that the word "talent" can hide.',
       ['To prove that Mei was born with a special gift.',
        'To explain how violin competitions are judged.',
        'To show that losing competitions makes people quit.'],
       '【中譯】第二段的主要作用是什麼？\n'
       '【解析】第一段說「天分」這個詞會遮蓋很多東西；第二段用小美的例子說明，記者只看到「天生的」，卻沒看到她八年的苦練——是用實例支持第一段的論點。'
       '({d0}) 作者正好要說明她的成功不只是天賦；({d1}) 文中沒有談比賽怎麼評分；({d2}) 小美輸了還是繼續練習，並沒有因此放棄。')

b.item('According to the writer, what is the "more serious" problem with calling people talented?',  # L5
       'It may lead beginners to give up when they find something difficult.',
       ['It ignores the hard work that successful people have done.',
        'It makes successful people proud and lazy.',
        'It makes beginners learn new skills more slowly.'],
       '【中譯】根據作者，說別人「有天分」比較嚴重的問題是什麼？\n'
       '【解析】第三段的 Second, and more seriously 之後說：這可能讓其他人不再嘗試——學得辛苦的初學者會認為自己「沒有天分」而放棄。'
       '({d0}) 忽略成功者的努力是作者說的「第一個」原因，文中有提到，但不是「更嚴重」的那一個，這是最容易誤選的選項；({d1}) 文中沒有提到讓成功的人驕傲懶惰；({d2}) 作者說的是初學者「放棄」，不是學得比較慢。')

b.item('Which statement would the writer most likely agree with?',  # L5
       'Learning a skill faster than others does not mean learning it without effort.',
       ['Talent does not exist, so anyone can reach the top of any field.',
        'People who learn faster at the start usually become the best in the end.',
        "Praising someone's talent is always unfair and should be avoided."],
       '【中譯】作者最可能同意下列哪一個說法？\n'
       '【解析】第四段作者承認「有些人確實學得比較快」，但強調「『比較快』不等於『不用努力』」。'
       '({d0}) 作者說「這並不表示每個人都一樣」，假裝大家都一樣是不誠實的，「天分不存在」太極端；({d1}) 作者說差別「與其說在於起點，不如說在於接下來怎麼做」，正好相反；({d2}) 作者說這種稱讚「通常是出於好意」，只建議換個問法，「總是不公平、應該避免」說得太重。')

b.write()
