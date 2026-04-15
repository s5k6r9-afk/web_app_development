# 流程圖文件 (FLOWCHART) - 主題占卜系統

本文件根據 PRD 與系統架構文件所繪製，用於視覺化展現系統中「使用者操作路徑」與「資料系統流動」。

## 1. 使用者流程圖（User Flow）

以下圖表展示使用者從進入網站開始，可能經歷的所有主要操作與頁面跳轉邏輯。

```mermaid
flowchart LR
    A([使用者開啟首頁]) --> B{是否已登入?}
    
    B -->|否| C[首頁 - 瀏覽主題與未登入狀態]
    C -->|點擊登入/註冊| D[登入與註冊頁面]
    D -->|註冊成功| E[登入狀態]
    D -->|登入成功| E
    
    B -->|是| E
    
    E --> F[會員專區 / 歷史紀錄查詢]
    
    C -->|選擇任一主題| G[抽牌互動預備頁面]
    E -->|選擇任一主題| G
    
    G -->|確認進行抽牌| H{檢查是否符合抽牌條件?}
    
    H -->|未達每日一抽上限| J[播放抽卡特效動畫]
    H -->|每日一抽額度已滿| I[提示訊息：今日已抽過]
    I --> C
    
    J --> K[占卜結果展示頁面]
    K -->|若有登入則自動儲存紀錄| L((紀錄寫入資料庫))
    
    K -->|查看其他主題| C
    F -->|退出登入| C
```

## 2. 系統序列圖（Sequence Diagram）

以下圖表以核心功能「使用者進行抽牌並獲得結果」為例，展示各個系統元件間的互動順序與資料傳遞過程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器端
    participant Flask Route as 後端路由 (Controller)
    participant Model as 資料模型 (Model)
    participant DB as SQLite DB

    User->>Browser: 在首頁選擇「愛情」主題並點擊抽卡
    Browser->>Flask Route: POST /draw/execute {theme: 'love'}
    
    %% 確認是否已登入與歷史限制
    Flask Route->>Flask Route: 驗證 Session 狀態 (若有登入則取得 User ID)
    Flask Route->>Model: 查詢今日是否已有抽卡紀錄?
    Model->>DB: SELECT * FROM records WHERE user_id=? AND date=?
    DB-->>Model: 回傳查詢結果
    
    %% 開始抽卡邏輯
    Flask Route->>Model: 要求從「愛情」分類題庫中隨機抽卡
    Model->>DB: 隨機 SELECT 一筆對應的主題牌卡資料
    DB-->>Model: 回傳選中的塔羅牌或籤詩資訊 (牌義、圖片)
    
    %% 儲存結果並回傳
    opt 若使用者已登入
        Flask Route->>Model: 要求儲存此次占卜紀錄
        Model->>DB: INSERT INTO records (user_id, card_id, date)
        DB-->>Model: 寫入成功
    end
    
    Flask Route-->>Browser: HTTP 302 重導向至結果頁 (帶上紀錄 ID)
    Browser->>Flask Route: GET /result/<record_id>
    Flask Route-->>Browser: 渲染回傳 result.html
    Browser-->>User: 顯示最終占卜結果與解析內容
```

## 3. 功能清單對照表

本表列出每個功能對應的 URL 路由路徑與 HTTP 請求方法，以此作為後續 API 與路由設計的藍圖。

| 功能名稱 | URL 路徑 | HTTP 方法 | 對應控制器 (Route) | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (主題選擇) | `/` | GET | `main.py` | 顯示所有可選的占卜分類與網站介紹 |
| 使用者註冊 | `/auth/register` | GET / POST| `auth.py` | (GET) 顯示註冊表單，(POST) 接收資料寫入資料 |
| 使用者登入 | `/auth/login` | GET / POST| `auth.py` | (GET) 顯示登入表單，(POST) 驗證帳密並發放 Session |
| 使用者登出 | `/auth/logout` | GET | `auth.py` | 清除使用者 Session 並重導向至首頁 |
| 抽卡互動頁面 | `/draw/<theme>` | GET | `draw.py` | 進入特定分類之前的互動過場、準備畫面 |
| 執行抽卡邏輯 | `/draw/execute` | POST | `draw.py` | 後端執行隨機抽卡並儲存紀錄，處理完畢重導向至結果|
| 占卜結果展示 | `/result/<record_id>`| GET | `draw.py` | 呈現剛抽中之牌卡圖案及詳細解說內容 |
| 個人歷史紀錄 | `/history` | GET | `main.py` | 僅限會員訪問，透過撈取 DB 紀錄顯示先前的占卜歷程 |
