from flask import render_template, request, redirect, url_for, flash, session
from . import draw_bp

@draw_bp.route('/draw/<theme>', methods=['GET'])
def draw_page(theme):
    """
    [GET] 抽卡互動頁面
    處理邏輯: 處理動畫與抽卡的準備階段，主要承載前端互動邏輯。
    輸出: 渲染 'draw.html' (帶入 theme 資訊)
    """
    pass

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
    pass

@draw_bp.route('/result/<int:record_id>', methods=['GET'])
def result(record_id):
    """
    [GET] 占卜結果展示
    處理邏輯: 根據傳入的 record_id 單號，以 Record.get_by_id 獲取完整卡片與紀錄資料。
    輸出: 渲染 'result.html'
    """
    pass
