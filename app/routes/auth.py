from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
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
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password:
            flash('請填妥所有註冊欄位！', 'error')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('兩次輸入的密碼不一致，請再確認一次', 'error')
            return redirect(url_for('auth.register'))
            
        if User.get_by_email(email):
            flash('這個信箱似乎已經註冊過了，要不直接登入試試？', 'error')
            return redirect(url_for('auth.register'))

        # Hash 加密密碼後再寫入資料庫
        password_hash = generate_password_hash(password)
        user_id = User.create(username, email, password_hash)
        
        if user_id:
            flash('註冊成功！來登入看看吧', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('系統發生神祕錯誤，請稍後再試', 'error')
            return redirect(url_for('auth.register'))

    return render_template('login.html', is_register=True)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    [GET, POST] 使用者登入
    處理邏輯:
      GET: 顯示登入表單。
      POST: 利用 User.get_by_email() 驗證密碼，無誤則設定 session['user_id']。
    輸出: 渲染 'login.html' 或 重導向 '/'
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('電子郵件及密碼欄位都要填寫哦', 'error')
            return redirect(url_for('auth.login'))
            
        user = User.get_by_email(email)
        # 用 check_password_hash 來驗證加密密碼
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'歡迎回來神祕學境地，{user["username"]}。', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('我不認得這組帳號或密碼，請再檢查一下', 'error')
            return redirect(url_for('auth.login'))
            
    return render_template('login.html', is_register=False)

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    [GET] 使用者登出
    處理邏輯: 清空 session。
    輸出: 重導向 '/'
    """
    session.clear()
    flash('您已安穩抽離現有體驗狀態 (登出成功)', 'info')
    return redirect(url_for('main.index'))
