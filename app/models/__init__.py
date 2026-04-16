import sqlite3
import os

def get_db_connection():
    """
    建立並回傳一個與 SQLite 資料庫的連線。
    資料庫檔案預計放在專案根目錄的 instance/database.db 中。
    """
    # 這裡的 __file__ 是在 app/models/__init__.py
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    instance_dir = os.path.join(base_dir, 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    
    db_path = os.path.join(instance_dir, 'database.db')
    conn = sqlite3.connect(db_path)
    
    # 讓回傳的資料列可以透過字典鍵值來存取欄位
    conn.row_factory = sqlite3.Row
    return conn
