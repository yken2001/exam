# exam-app 專案須知

國中會考練習 App，給家長自己的小孩用。先讀 README.md（架構、重組方式、問題處理心智圖）與 tools/README.md。

## 規則
- 只做本地 commit；**push 等使用者開口**。push 到 main 會自動部署到 GitHub Pages（公開網址）。
- `src/data/real/*.ts` 是 `tools/gen_ts.py` 產生的，不要手改；要改答案或題組，改切割程式後重跑整條流程。
- 題庫正確性最重要（怕答案錯影響小孩信心）。改動切割邏輯後一定要：
  1. `python tools/build_bank.py --dry` 看 `tools/build_report.txt`，不能有 error
  2. 和改動前的 `tools/bank/*.json` 比對答案，任何差異都要回原始 PDF 查證
  3. 在瀏覽器實際跑：每份卷填正確答案 → 成績頁必須 100%、0 張破圖；再故意答錯幾題確認顯示「答錯」
- 來源 PDF 放 `tools/source_pdfs/`（110–115 各 5 份解析卷＋113–115 英聽解析卷，共 33 份，不進 git，從 README 的連結下載）。`tools/reflowed/` 是重組後的備查 PDF，也不進 git。
- 成績存在各瀏覽器的 IndexedDB，沒有後端。
- 題目版權屬原出版社，不要把 PDF 或重組 PDF 放進 repo。

## 常用指令
- `npm run dev`（Claude Code 預覽設定：`.claude/launch.json` 的 exam-app-dev，port 5183）
- `npm run build` → `dist/`（單一 index.html，可用 file:// 開）
- 題庫：`python tools/build_bank.py` → `build_listening.py <年>`（112–115）→ `gen_audio.py <年>`（需 Windows 英文語音 Zira）→ `gen_ts.py` → `check_leaks.py`（必須 0 洩漏）→ `check_official.py`（與心測中心官方答案必須 0 不一致；新年度先把官方答案表存到 `tools/official_answers/<年>.txt`）
