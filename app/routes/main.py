from flask import render_template, request, session, redirect, url_for, flash
from app.models.record import Record
from . import main_bp

@main_bp.route('/')
def index():
    """
    [GET] 首頁路由
    處理邏輯: 判定是否登入，渲染所有可選的占卜分類。
    輸出: 渲染 'index.html'
    """
    return render_template('index.html')

@main_bp.route('/history')
def history():
    """
    [GET] 個人歷史紀錄
    處理邏輯: 
      1. 檢查是否具有 session (登入層級)。未登入則重導向。
      2. 透過 Record.get_all(user_id) 取得該使用者的歷史紀錄。
    輸出: 渲染 'history.html'
    """
    user_id = session.get('user_id')
    if not user_id:
        flash('想查看歷史占卜精華？請先登入您的帳號', 'warning')
        return redirect(url_for('auth.login'))
        
    records = Record.get_all(user_id)
    return render_template('history.html', records=records)
