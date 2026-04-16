from flask import Blueprint

# 在這裡實體化各個模組的 Blueprint，準備在 app.py 註冊給 Flask App
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
draw_bp = Blueprint('draw', __name__)

from . import main, auth, draw
