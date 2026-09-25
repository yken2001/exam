# tools

題庫全部只由「xxx會考xx解析.pdf」產生(題目、正解、每題解析),流程:

```
python build_bank.py            # 重組 + 切割 + 驗證 + 輸出圖片
python build_bank.py --dry      # 只解析、只出驗證報告
python build_bank.py 110 自然    # 只跑一份
python gen_ts.py                # 由 bank/*.json 產生 src/data/real/*.ts
```

1. **重組**(`bank_lib.reflow`):第 1 頁去掉標頭,每頁的頁碼 /「請翻面繼續作答」/ 廣告 / QR code 塗白,
   再把每頁從中間切成左右兩欄,依「第1頁左、第1頁右、第2頁左…」接成一條連續內容。
   各檔案特別處理寫在 `build_bank.py` 的 `RULES`(例如 111 國文、111 數學刪最後一頁)。
2. **切割**:依題號(嚴格連號)與題組標題找出每題範圍;題目 = 題號到第一行紅字(解析)之前,
   解析 = 紅字開始到下一題。題目圖上印的答案字母會塗白。
3. **驗證**:題數須與預期相符、每題都要有答案、題號旁的答案字母與解析中的「故選」須一致,
   結果寫在 `build_report.txt`。

輸出:
- `../public/questions/<科目>/<年>/qNN.png`、`../public/explanations/<科目>/<年>/eNN.png`
- `bank/<年>_<科目>.json`:題數、正解、題組、共用圖檔對應
- `answer_keys/`:正解一覽(人工備查用)
- `reflowed/`:重組後的解析 PDF(備查用,不進 git,可隨時重新產生)

來源 PDF 放在 `source_pdfs/`(只需 15 份「xxx會考xx解析.pdf」,不進 git)。
