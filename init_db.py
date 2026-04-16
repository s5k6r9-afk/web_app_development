import sqlite3
import os

def init_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    instance_dir = os.path.join(base_dir, 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    
    db_path = os.path.join(instance_dir, 'database.db')
    conn = sqlite3.connect(db_path)
    
    # 讀取並執行 schema
    schema_path = os.path.join(base_dir, 'database', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
        
    # 寫入初始牌卡題庫，以免抽卡報錯 (因為目前還沒有管理者新增介面)
    cursor = conn.cursor()
    # 簡單確認是否已有資料
    cursor.execute('SELECT COUNT(*) FROM cards')
    if cursor.fetchone()[0] == 0:
        cards_data = [
            ('love', '戀人 (The Lovers)', '象徵愛情的美好，或是面臨重要的選擇與契合的關係。', None),
            ('love', '聖杯二 (Two of Cups)', '代表互補、平等的愛與深刻的連結。兩人頻率一致。', None),
            ('career', '皇帝 (The Emperor)', '穩定、權力與組織結構。你將獲得明確的主導權。', None),
            ('career', '權杖八 (Eight of Wands)', '代表事業將有快速的發展與大量的資訊交流，順勢而為吧！', None),
            ('comprehensive', '世界 (The World)', '代表一個循環的圓滿結束，成功與達成最終目標，獲得完美體驗。', None),
            ('comprehensive', '愚者 (The Fool)', '象徵新的開始、不受世俗拘束。順從你的直覺大膽前進吧！', None)
        ]
        cursor.executemany(
            'INSERT INTO cards (theme, name, description, image_url) VALUES (?, ?, ?, ?)',
            cards_data
        )
        print("已成功建立基本占卜卡牌題庫！")
        
    conn.commit()
    conn.close()
    print("資料庫初始化完成。")

if __name__ == '__main__':
    init_db()
