from flask import render_template, request, redirect, url_for, flash, session
from app.models.record import Record
from app.models.div_card import DivCard
from . import draw_bp

# 定義合法的主題列表，防堵惡意修改參數
VALID_THEMES = ['love', 'career', 'comprehensive']

@draw_bp.route('/draw/<theme>', methods=['GET'])
def draw_page(theme):
    """
    [GET] 抽卡互動頁面
    處理邏輯: 處理動畫與抽卡的準備階段，主要承載前端互動邏輯。
    輸出: 渲染 'draw.html' (帶入 theme 資訊)
    """
    if theme not in VALID_THEMES:
        flash('這似乎是不在選項當中的神祕主題', 'error')
        return redirect(url_for('main.index'))
        
    return render_template('draw.html', theme=theme)

@draw_bp.route('/draw/execute', methods=['POST'])
def draw_execute():
    """
    [POST] 執行抽卡邏輯
    處理邏輯:
      1. 確認是否登入(取得 user_id)
      2. 呼叫 Record.has_drawn_today 檢查是否滿抽卡額度
      3. 若皆通過，利用 DivCard.get_random_by_theme 抽卡
      4. 呼叫 Record.create() 將結果寫入紀錄表
    輸出: 重導向至 '/result/<record_id>'
    """
    # 從表單接收隱藏的主題參數
    theme = request.form.get('theme')
    user_id = session.get('user_id')
    
    # 權限卡控
    if not user_id:
        flash('請先登入後才能尋求占卜的指引', 'warning')
        return redirect(url_for('auth.login'))
        
    if not theme or theme not in VALID_THEMES:
        flash('無法識別的占卜選項', 'error')
        return redirect(url_for('main.index'))
        
    # 限制每日一抽次數
    if Record.has_drawn_today(user_id):
        flash('今日的魔法能量已經完全釋放過了，請明天再來體驗每日運勢吧！', 'info')
        return redirect(url_for('main.index'))
        
    # 從題庫抽取該類別隨機卡片
    card = DivCard.get_random_by_theme(theme)
    if not card:
        flash('命運的齒輪卡住了 (無題庫資料)', 'error')
        return redirect(url_for('main.index'))
        
    # 儲存此抽卡歷史
    record_id = Record.create(user_id, card['id'])
    if not record_id:
        flash('儲存命運的解語時發生異常，請重試！', 'error')
        return redirect(url_for('main.index'))
        
    return redirect(url_for('draw.result', record_id=record_id))

@draw_bp.route('/result/<int:record_id>', methods=['GET'])
def result(record_id):
    """
    [GET] 占卜結果展示
    處理邏輯: 根據傳入的 record_id 單號，以 Record.get_by_id 獲取完整卡片與紀錄資料。
    輸出: 渲染 'result.html'
    """
    user_id = session.get('user_id')
    
    if not user_id:
        flash('要查看歷史軌跡，請先登入帳號', 'warning')
        return redirect(url_for('auth.login'))
        
    record = Record.get_by_id(record_id)
    if not record:
        flash('查無這段屬於命運的記憶 (找不到紀錄)', 'error')
        return redirect(url_for('main.index'))
        
    # 防堵他人窺探特定帳號紀錄
    if record['user_id'] != user_id:
        flash('這是別人的指引，你不應該擅自翻閱喔', 'error')
        return redirect(url_for('main.index'))
        
    return render_template('result.html', record=record)
