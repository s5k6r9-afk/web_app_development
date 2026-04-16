from flask import Flask
import os

def create_app():
    # 初始化 Flask 應用，預設會自動抓取 app/templates 與 app/static 目錄
    app = Flask(__name__)
    
    # 應用程式安全設置
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-secret-key')
    
    # 建立 /instance 資料夾供 SQLite 資料庫存放
    instance_path = os.path.join(app.root_path, '..', 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    # 延遲引入並註冊 Blueprint 路由
    from .routes import main_bp, auth_bp, draw_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(draw_bp)
    
    return app
