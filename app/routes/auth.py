from flask import render_template, request, redirect, url_for, flash, session
from . import auth_bp

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    [GET, POST] 使用者註冊
    處理邏輯:
      GET: 顯示註冊表單。
      POST: 檢查密碼一致性與信箱是否重複，寫入 User.create()，成功則導向登入。
    輸出: 渲染 'login.html' 或 重導向 '/auth/login'
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    [GET, POST] 使用者登入
    處理邏輯:
      GET: 顯示登入表單。
      POST: 利用 User.get_by_email() 驗證密碼，無誤則設定 session['user_id']。
    輸出: 渲染 'login.html' 或 重導向 '/'
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    [GET] 使用者登出
    處理邏輯: 清空 session。
    輸出: 重導向 '/'
    """
    pass
