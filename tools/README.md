# tools

一次性內容產生腳本,用來把 PDF 題本/解析裁切成 `public/questions` 與 `public/explanations` 底下的圖片,並印出各題正解供 `src/data/real/*.ts` 使用。

- `crop_lib.py` — 共用裁切函式庫,涵蓋 110/111 年翰林單欄格式與 112 年官方雙欄格式,各科各年細節差異都靠不同 regex/裁切函式處理。
- `regenerate_all.py` — 一次重新產生全部 15 組(5科 x 3年)的主控腳本。PDF 來源路徑寫死在 `DL`,需要對應調整。

日後若要修圖或新增年度資料,從這裡改起。
