# 路由設計文件 (ROUTES) - 主題占卜系統

本文件根據 PRD、架構設計與 DB Schema，規劃了系統中所有的 Flask 路由、接受的方法以及對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 / 回應 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (主題選擇) | GET | `/` | `index.html` | 顯示所有可選的占卜分類與網站介紹 |
| 個人歷史紀錄 | GET | `/history` | `history.html` | 僅限會員訪問，顯示先前的占卜歷程 |
| 使用者註冊頁面 | GET | `/auth/register` | `login.html` | 顯示註冊表單 (可與登入共用頁面) |
| 處理註冊 | POST | `/auth/register`| `redirect(/auth/login)` | 接收註冊表單，寫入 DB，成功後重導向 |
| 使用者登入頁面 | GET | `/auth/login` | `login.html` | 顯示登入表單 |
| 處理登入 | POST | `/auth/login` | `redirect(/)` | 驗證帳密並發放 Session，登入後重導向 |
| 使用者登出 | GET | `/auth/logout` | `redirect(/)` | 清除 Session 並重導向至首頁 |
| 抽卡互動頁面 | GET | `/draw/<theme>` | `draw.html` | 進入特定分類之前的互動過場、準備畫面 |
| 執行抽卡邏輯 | POST | `/draw/execute` | `redirect(/result/<id>)`| 後端執行隨機抽卡並儲存紀錄，重導向至結果 |
| 占卜結果展示 | GET | `/result/<record_id>`| `result.html`| 呈現剛抽中之紀錄與牌義詳細內容 |

---

## 2. 每個路由的詳細說明

### 2.1 Main 模組 (`main.py`)

#### 首頁 (`GET /`)
- **輸入**: 無
- **處理邏輯**: 確認 Session 狀態，取得可選的主題清單。
- **輸出**: 渲染 `index.html`。
- **錯誤處理**: 無特殊錯誤。

#### 個人歷史紀錄 (`GET /history`)
- **輸入**: Session (需要 `user_id`)
- **處理邏輯**: 
  - 檢查是否登入，若未登入導回登入頁。
  - 呼叫 `Record.get_all(user_id)` 取得歷史紀錄清單。
- **輸出**: 渲染 `history.html` 並傳入 `records` 資料。
- **錯誤處理**: 403 / 未登入導向首頁或登入頁。

### 2.2 Auth 模組 (`auth.py`)

#### 註冊 (`GET, POST /auth/register`)
- **輸入**: 表單傳入 `username`, `email`, `password`, `confirm_password`。
- **處理邏輯**: 
  - GET: 顯示註冊表單。
  - POST: 檢查密碼是否一致、信箱/帳號是否被註冊過。Hash 密碼並呼叫 `User.create()`。
- **輸出**: 成功則重導向 `/auth/login` 並 flash 訊息；失敗則重新渲染 `login.html` 附帶錯誤訊息。

#### 登入 (`GET, POST /auth/login`)
- **輸入**: 表單傳入 `email`, `password`。
- **處理邏輯**: 
  - GET: 顯示登入表單。
  - POST: 呼叫 `User.get_by_email()`，比對 Hash 是否正確。正確則寫入 Session。
- **輸出**: 成功則重導向 `/`；失敗則重新渲染 `login.html`。

#### 登出 (`GET /auth/logout`)
- **輸入**: 無
- **處理邏輯**: 清除 Session (`session.clear()`)。
- **輸出**: 重導向 `/`。

### 2.3 Draw 模組 (`draw.py`)

#### 抽卡互動頁面 (`GET /draw/<theme>`)
- **輸入**: URL 參數 `theme` (如 'love', 'career')
- **處理邏輯**: 檢查該主題是否存在。此頁面主要用於播放動畫。
- **輸出**: 渲染 `draw.html` 並傳遞 `theme` 變數。

#### 執行抽卡邏輯 (`POST /draw/execute`)
- **輸入**: 表單或隱藏欄位傳入 `theme`。需檢查 Session 獲取 `user_id`。
- **處理邏輯**: 
  - 檢查 `Record.has_drawn_today(user_id)`，如果今日已抽過，則阻擋並提示。
  - 否則呼叫 `DivCard.get_random_by_theme(theme)` 抽卡。
  - 呼叫 `Record.create()` 儲存紀錄。
- **輸出**: 重導向至 `/result/<record_id>`。(若未登入可能採 Session 暫存結果再導向)
- **錯誤處理**: 若當日已滿額，Flash 提示並重導向首頁。

#### 結果展示 (`GET /result/<record_id>`)
- **輸入**: URL 參數 `record_id`
- **處理邏輯**: 呼叫 `Record.get_by_id(record_id)`，可能需驗證是否為該使用者的紀錄 (或開放分享)。
- **輸出**: 渲染 `result.html`。
- **錯誤處理**: 若查無紀錄回傳 404。

---

## 3. Jinja2 模板清單

所有模板皆存放在 `app/templates/` 內。

1. **`base.html`**
   - 網站共用骨架，包含 HTML 標頭、引入 CSS/JS、共用的 Navbar (登入/登出狀態切換) 與 Footer。
2. **`index.html`** (繼承 `base.html`)
   - 網站首頁，顯示系統簡介與主題選項大按鈕。
3. **`login.html`** (繼承 `base.html`)
   - 包含登入與註冊的表單 (可用切換式設計或分上下區塊)。
4. **`draw.html`** (繼承 `base.html`)
   - 抽卡之前的沉浸式準備頁面，帶有發牌/抽籤的動畫表現，其中包含一個隱藏表單用於 POST 到 `/draw/execute`。
5. **`result.html`** (繼承 `base.html`)
   - 顯示這次抽得牌卡的圖案、名稱、牌義解析。
6. **`history.html`** (繼承 `base.html`)
   - 呈現列表的個人歷史占卜紀錄。

